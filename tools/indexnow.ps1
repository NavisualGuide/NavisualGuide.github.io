<#
.SYNOPSIS
  Tell Bing (and the other IndexNow engines) that pages changed, without
  waiting for a crawl.

.DESCRIPTION
  Why this exists: on 2026-09-19 Bing was found to be serving a sitemap it had
  last read on 2026-09-02 -- one day BEFORE the first guide was published. Two
  articles had been live for 17 and 8 days and Bing had never seen either one.
  Nothing was broken; Bing simply had not come back to re-read the list.

  IndexNow inverts that. Instead of waiting to be crawled, the site pushes the
  changed URLs and Bing fetches them in minutes. Google does not participate;
  Bing, Yandex, Seznam and Naver do, and Bing is what feeds Copilot.

  Run it after a push has finished deploying:
      .\tools\indexnow.ps1                       # every URL in sitemap.xml
      .\tools\indexnow.ps1 -Url /guides/my-slug/ # just these
      .\tools\indexnow.ps1 -DryRun               # show, do not send

  The GitHub workflow in .github/workflows/indexnow.yml does this automatically
  on every Pages build, so running it by hand is only for a one-off resubmit.

  Exit code 0 = accepted, 1 = rejected or unreachable.

.PARAMETER Url
  One or more URLs to submit. Absolute, or site-relative starting with "/".
  Omit to submit every URL listed in the live sitemap.

.PARAMETER DryRun
  Print what would be sent and stop.
#>

[CmdletBinding()]
param(
  [string[]]$Url,
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

# The key is PUBLIC by design -- IndexNow proves ownership by having you serve
# it at the site root, so it is committed alongside the site on purpose. It is
# not a credential and does not belong in the credential vault.
$SiteHost  = 'navisualguide.com'
$Key       = 'a51b36ed613e4e2babe7dc20900c0b08'
$KeyUrl    = "https://$SiteHost/$Key.txt"
$Endpoint  = 'https://api.indexnow.org/indexnow'

function Say([string]$level, [string]$msg) {
  switch ($level) {
    'ERR'  { Write-Host "  [ERROR] $msg" -ForegroundColor Red }
    'WARN' { Write-Host "  [warn ] $msg" -ForegroundColor Yellow }
    'OK'   { Write-Host "  [ ok  ] $msg" -ForegroundColor DarkGreen }
    'INFO' { Write-Host "  [ info] $msg" -ForegroundColor DarkGray }
  }
}

Write-Host ""
Write-Host "=== IndexNow submit: $SiteHost ===" -ForegroundColor Cyan

# --- the key file has to be readable, or every submission is rejected -------
# Checked here rather than assumed: a 404 returns 403 from the API with no
# explanation of which half is wrong.
try {
  $served = (Invoke-WebRequest -Uri $KeyUrl -UseBasicParsing -TimeoutSec 20).Content.Trim()
} catch {
  Say ERR "key file not reachable at $KeyUrl -- $($_.Exception.Message)"
  Say INFO "it must be committed at the repo root and deployed before submitting"
  exit 1
}
if ($served -ne $Key) {
  Say ERR "key file serves '$served' but this script sends '$Key'"
  exit 1
}
Say OK "key file verified at $KeyUrl"

# --- build the URL list ----------------------------------------------------
if ($Url) {
  $list = @()
  foreach ($u in $Url) {
    if ($u -like 'http*') { $list += $u }
    else                  { $list += "https://$SiteHost" + $u }
  }
} else {
  try {
    $xml = [xml](Invoke-WebRequest -Uri "https://$SiteHost/sitemap.xml" -UseBasicParsing -TimeoutSec 20).Content
  } catch {
    Say ERR "could not read the live sitemap -- $($_.Exception.Message)"
    exit 1
  }
  $list = @($xml.urlset.url | ForEach-Object { $_.loc })
  Say INFO "read $($list.Count) URL(s) from the live sitemap"
}

# Anything not on this host is refused by the API for the whole batch, so drop
# it here where the reason is visible.
$offHost = @($list | Where-Object { $_ -notlike "https://$SiteHost/*" })
if ($offHost.Count -gt 0) {
  foreach ($o in $offHost) { Say WARN "skipping (wrong host): $o" }
  $list = @($list | Where-Object { $_ -like "https://$SiteHost/*" })
}

if ($list.Count -eq 0) { Say ERR "nothing to submit"; exit 1 }

Write-Host ""
foreach ($u in $list) { Write-Host "    $u" -ForegroundColor Gray }
Write-Host ""

if ($DryRun) { Say INFO "dry run -- nothing sent"; exit 0 }

# --- submit ----------------------------------------------------------------
$payload = @{
  host        = $SiteHost
  key         = $Key
  keyLocation = $KeyUrl
  urlList     = $list
} | ConvertTo-Json -Depth 3

try {
  $resp = Invoke-WebRequest -Uri $Endpoint -Method Post -Body $payload `
            -ContentType 'application/json; charset=utf-8' `
            -UseBasicParsing -TimeoutSec 30
  $code = [int]$resp.StatusCode
} catch {
  $code = -1
  if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode }
}

# 200 = accepted. 202 = accepted, key still being verified -- also a success,
# and the usual answer on a first submission.
switch ($code) {
  200     { Say OK   "submitted $($list.Count) URL(s) -- accepted (200)"; exit 0 }
  202     { Say OK   "submitted $($list.Count) URL(s) -- accepted, key verification pending (202)"; exit 0 }
  400     { Say ERR  "400 bad request -- the payload was malformed"; exit 1 }
  403     { Say ERR  "403 forbidden -- the key file did not validate"; exit 1 }
  422     { Say ERR  "422 -- a URL does not belong to $SiteHost, or the key does not match"; exit 1 }
  429     { Say ERR  "429 too many requests -- submitting too often; wait before retrying"; exit 1 }
  default { Say ERR  "unexpected response: $code"; exit 1 }
}
