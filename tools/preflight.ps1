<#
.SYNOPSIS
  Pre-publish checks for guide articles in _guides/.

.DESCRIPTION
  Every check here exists because the failure it catches is SILENT — the site
  builds, the page renders, and the damage is only visible if you happen to look
  at the right part of the right page. Two of them have already shipped broken
  once.

  Run it before pushing:
      .\tools\preflight.ps1
      .\tools\preflight.ps1 -Path _guides\word-copilot-tab-missing.md

  Exit code 0 = no errors (warnings allowed), 1 = at least one error.

.PARAMETER Path
  A single article to check. Omit to check every file in _guides/.
#>

[CmdletBinding()]
param(
  [string]$Path
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot

if ($Path) {
  if (-not [System.IO.Path]::IsPathRooted($Path)) { $Path = Join-Path $repo $Path }
  $files = @(Get-Item $Path)
} else {
  $files = @(Get-ChildItem (Join-Path $repo '_guides') -Filter *.md -ErrorAction SilentlyContinue)
}

if ($files.Count -eq 0) { Write-Host "No articles found." -ForegroundColor Yellow; exit 0 }

$totalErr = 0
$totalWarn = 0

function Say([string]$level, [string]$msg) {
  switch ($level) {
    'ERR'  { Write-Host "  [ERROR] $msg" -ForegroundColor Red }
    'WARN' { Write-Host "  [warn ] $msg" -ForegroundColor Yellow }
    'OK'   { Write-Host "  [ ok  ] $msg" -ForegroundColor DarkGreen }
    'INFO' { Write-Host "  [ info] $msg" -ForegroundColor DarkGray }
  }
}

foreach ($file in $files) {
  Write-Host ""
  Write-Host "=== $($file.Name) ===" -ForegroundColor Cyan
  $lines = Get-Content $file.FullName -Encoding UTF8
  $err = 0; $warn = 0

  # --- locate front matter -------------------------------------------------
  $fmEnd = -1
  if ($lines[0] -eq '---') {
    for ($i = 1; $i -lt $lines.Count; $i++) { if ($lines[$i] -eq '---') { $fmEnd = $i; break } }
  }
  if ($fmEnd -lt 0) { Say ERR "No front matter found (file must start with ---)"; $totalErr++; continue }
  $fm   = $lines[1..($fmEnd-1)]
  $body = $lines[($fmEnd+1)..($lines.Count-1)]

  # --- draft state ---------------------------------------------------------
  $draft = ($fm | Where-Object { $_ -match '^\s*draft:\s*true\s*$' }).Count -gt 0
  if ($draft) { Say INFO "draft: true  -> noindex, unlisted, not in sitemap. Set false to publish." }
  else        { Say INFO "draft: false -> this WILL publish and be indexed." }

  # --- CHECK 1: figure includes must not split the ordered list ------------
  # An include at column 0 between two numbered items terminates the <ol>, so
  # the next item restarts at 1. This shipped once (steps 3 and 4 rendered as
  # 1 and 2) and is invisible in the Markdown.
  $split = 0
  for ($i = 0; $i -lt $body.Count; $i++) {
    if ($body[$i] -notmatch '^\{%\s*include\s+figure\.html') { continue }
    $before = $false; $after = $false
    for ($j = $i - 1; $j -ge 0; $j--) {
      if ($body[$j] -match '^##\s') { break }
      if ($body[$j] -match '^\d+\.\s') { $before = $true; break }
    }
    for ($j = $i + 1; $j -lt $body.Count; $j++) {
      if ($body[$j] -match '^##\s') { break }
      if ($body[$j] -match '^\d+\.\s') { $after = $true; break }
    }
    if ($before -and $after) {
      Say ERR "line $($i+$fmEnd+2): figure include sits at column 0 between two numbered steps -> the list will restart at 1. Indent it 3 spaces so it belongs to the step above."
      $split++
    }
  }
  if ($split -eq 0) { Say OK "figure includes do not split the numbered list" } else { $err += $split }

  # --- CHECK 2: body step numbers are sequential ---------------------------
  $stepsStart = -1; $stepsEnd = $body.Count
  for ($i = 0; $i -lt $body.Count; $i++) { if ($body[$i] -match '^##\s+Steps\s*$') { $stepsStart = $i; break } }
  $bodySteps = @()
  if ($stepsStart -ge 0) {
    for ($i = $stepsStart + 1; $i -lt $body.Count; $i++) {
      if ($body[$i] -match '^##\s') { $stepsEnd = $i; break }
      if ($body[$i] -match '^(\d+)\.\s') { $bodySteps += [int]$Matches[1] }
    }
    $expected = 1..$bodySteps.Count
    $mismatch = $false
    for ($i = 0; $i -lt $bodySteps.Count; $i++) { if ($bodySteps[$i] -ne ($i+1)) { $mismatch = $true } }
    if ($bodySteps.Count -eq 0) {
      Say WARN "a '## Steps' section exists but contains no numbered items"; $warn++
    } elseif ($mismatch) {
      Say ERR "step numbers are not sequential: $($bodySteps -join ', ')"; $err++
    } else {
      Say OK "$($bodySteps.Count) steps, numbered 1..$($bodySteps.Count)"
    }
  } else {
    Say INFO "no '## Steps' section (fine for a non-procedural article)"
  }

  # --- CHECK 3: front-matter steps match the visible steps -----------------
  # These are written twice on purpose (the schema must be reliably true), so
  # they can drift. A HowTo that disagrees with the page is worse than none.
  $fmSteps = ($fm | Where-Object { $_ -match '^\s+-\s+name:' }).Count
  if ($fmSteps -gt 0 -or $bodySteps.Count -gt 0) {
    if ($fmSteps -ne $bodySteps.Count) {
      Say ERR "front matter declares $fmSteps steps but the body has $($bodySteps.Count) -> schema.org HowTo will disagree with the page"
      $err++
    } else {
      Say OK "front-matter steps ($fmSteps) match the body"
    }
  }

  # --- CHECK 4: 'step N' references point at steps that exist --------------
  $maxRef = 0
  foreach ($l in $body) {
    foreach ($m in [regex]::Matches($l, '(?i)\bstep\s+(\d+)\b')) {
      $n = [int]$m.Groups[1].Value
      if ($n -gt $maxRef) { $maxRef = $n }
    }
  }
  if ($maxRef -gt 0 -and $bodySteps.Count -gt 0) {
    if ($maxRef -gt $bodySteps.Count) {
      Say ERR "prose refers to 'step $maxRef' but there are only $($bodySteps.Count) steps"; $err++
    } else {
      Say OK "cross-references to 'step N' are all within range (max $maxRef)"
    }
  }

  # --- CHECK 5: every figure has alt text, and the image exists ------------
  $raw = ($body -join "`n")
  $figs = [regex]::Matches($raw, '\{%\s*include\s+figure\.html(.*?)%\}', 'Singleline')
  if ($figs.Count -eq 0) {
    Say INFO "no figures"
  } else {
    $bad = 0
    foreach ($f in $figs) {
      $blk = $f.Groups[1].Value
      $altM = [regex]::Match($blk, 'alt="([^"]*)"')
      $srcM = [regex]::Match($blk, 'src="([^"]*)"')
      $src  = if ($srcM.Success) { $srcM.Groups[1].Value } else { '(no src)' }
      if (-not $altM.Success -or $altM.Groups[1].Value.Trim().Length -eq 0) {
        Say ERR "figure $src has no alt text"; $bad++
      }
      if ($srcM.Success) {
        $disk = Join-Path $repo ($src -replace '^/','' -replace '/','\')
        if (-not (Test-Path $disk)) { Say ERR "figure image not found on disk: $src"; $bad++ }
      }
    }
    if ($bad -eq 0) { Say OK "$($figs.Count) figure(s): alt text present, image files exist" } else { $err += $bad }
  }

  # --- CHECK 6: metadata lengths -------------------------------------------
  $titleM = ($fm | Where-Object { $_ -match '^title:\s*' }) -replace '^title:\s*','' -replace '^"','' -replace '"$',''
  $descM  = ($fm | Where-Object { $_ -match '^description:\s*' }) -replace '^description:\s*','' -replace '^"','' -replace '"$',''
  if ($titleM) {
    $tl = $titleM.Length
    if ($tl -gt 60) { Say WARN "title is $tl chars; search results truncate near 60 -> the tail is spent on text nobody sees"; $warn++ }
    else            { Say OK "title length $tl" }
  }
  if ($descM) {
    $dl = $descM.Length
    if ($dl -gt 160) { Say WARN "description is $dl chars; snippets truncate near 160"; $warn++ }
    else             { Say OK "description length $dl" }
  } else {
    Say ERR "no description in front matter -> the snippet becomes whatever the crawler picks"; $err++
  }

  # --- CHECK 7: stray hard line breaks -------------------------------------
  # Two trailing spaces in Markdown is a <br>. Almost always accidental, and
  # completely invisible in an editor.
  $trail = 0
  for ($i = 0; $i -lt $body.Count; $i++) {
    if ($body[$i] -match '\S[ ]{2,}$') { $trail++ }
  }
  if ($trail -gt 0) { Say WARN "$trail line(s) end in 2+ spaces -> Markdown renders those as forced <br>"; $warn++ }
  else              { Say OK "no accidental hard line breaks" }

  Write-Host ("  -> {0} error(s), {1} warning(s)" -f $err, $warn) -ForegroundColor $(if ($err) { 'Red' } else { 'Green' })
  $totalErr += $err; $totalWarn += $warn
}

Write-Host ""
if ($totalErr -gt 0) {
  Write-Host "FAIL - $totalErr error(s), $totalWarn warning(s). Fix errors before pushing." -ForegroundColor Red
  exit 1
} else {
  Write-Host "PASS - 0 errors, $totalWarn warning(s)." -ForegroundColor Green
  exit 0
}
