---
title: "Setup OrcaSlicer with your 3D printer over Wi-Fi"
description: "Download, install and connect, in one pass — including the field almost every guide skips, which is why the Device tab shows 404 even when printing works."
date: 2026-09-11
app: "OrcaSlicer 2.4.2"
os: "Windows 10 / 11"

# Recognised HowTo property; an answer engine reporting "about 15 minutes" is
# more useful than one reporting nothing. ISO 8601 duration.
total_time: PT15M

# Feeds the "image" of the schema.org HowTo, which is what a rich result shows.
hero_image: /images/guides/orcaslicer-connect-printer-wifi/06-device-tab-fluidd.png

# Set to false to publish. While true: noindex, hidden from /guides/, and left
# out of the sitemap, so this can be pushed and previewed at its real URL, with
# the real layout and CTA, without being discoverable.
draft: true

steps:
  - name: "Download the Windows installer"
    text: "OrcaSlicer is distributed on GitHub, not through an app store. Go to https://github.com/SoftFever/OrcaSlicer/releases and take the newest entry marked Official Release. Scroll to the Assets section at the bottom and download the file named OrcaSlicer_Windows_Installer_V<version>_x64.exe -- x64, not arm64, unless your PC has an ARM processor."
    image: /images/guides/orcaslicer-connect-printer-wifi/01-github-assets.jpg
  - name: "Pick your printer in the setup wizard"
    text: "Run the OrcaSlicer installer and work through the first-run wizard. On its Printer Selection page use the search icon in the top left rather than scrolling, tick your model, and click Next. This sets your bed size, nozzle diameter and print profiles."
    image: /images/guides/orcaslicer-connect-printer-wifi/02-printer-selection.png
  - name: "Click Next through the remaining wizard pages"
    text: "On the remaining pages of the OrcaSlicer setup wizard, tick the filament types you own, leave Stealth Mode off, and leave the Bambu Network plug-in unticked unless you have a Bambu Lab printer. Click Finish, then New Project to open the workspace."
  - name: "Open the connection settings from the Wi-Fi icon"
    text: "In OrcaSlicer's main window, look at the left rail and click the small Wi-Fi icon beside the Printer header. That opens the Physical Printer dialog. The connection settings are not on the Device tab and not in the File menu."
    image: /images/guides/orcaslicer-connect-printer-wifi/03-printer-wifi-icon.png
  - name: "Scan the network and select your printer"
    text: "In OrcaSlicer's Physical Printer dialog, set both Host Type and Printer Agent to CrealityPrint, then click Browse next to Hostname, IP or URL to scan the local network. Click the row for your printer and click Use Selected. Write down the IP address shown -- the next step needs it."
    image: /images/guides/orcaslicer-connect-printer-wifi/04-detect-creality-printer.png
  - name: "Fill in Device UI with the printer's web interface"
    text: "In OrcaSlicer's Physical Printer dialog, fill in the Device UI field with your printer's own web interface: http:// followed by the printer's IP address and port 4408, for example http://192.168.0.88:4408/. This is the field that decides whether the Device tab works; left empty it shows 404 Not Found permanently. Leave API Key / Password and HTTPS CA File empty on a standard Creality setup, then click OK."
    image: /images/guides/orcaslicer-connect-printer-wifi/05-device-ui-field.png
  - name: "Check the Device tab"
    text: "Open the Device tab along the top of OrcaSlicer. With Device UI filled in, OrcaSlicer loads the printer's own web interface inside that tab -- on a Creality K-series that is fluidd, showing live bed, nozzle and chamber temperatures, recent print jobs, and axis jog controls."
    image: /images/guides/orcaslicer-connect-printer-wifi/06-device-tab-fluidd.png
---

OrcaSlicer turns a 3D model into the G-code your printer runs. Installing it is a download and a
short wizard. The part that trips people up is the last mile — telling the slicer where the printer
lives on your network, so you can send a print without carrying a microSD card across the room.

There is also a field in that dialog that almost every guide skips. Miss it and everything appears
to work — you can slice, you can print — but the **Device** tab shows a blank **404 Not Found**
forever.

**The short version.** Connect the printer with **Browse…** in the *Physical Printer* dialog, then —
before clicking OK — fill the **Device UI** field with your printer's own web interface:
`http://<printer-ip>:4408/` on a Creality K-series. That single field is what the Device tab loads,
and leaving it blank is why the tab returns 404 even though printing works. The long version, with
every screen, is below.

Two parts: install, then connect. If OrcaSlicer is already set up, skip to part two.

Every screenshot below is a real frame from one session, recorded while someone actually did this
with **Navisual** — an assistant that watches the screen and marks the control you need next. The
orange marks are Navisual pointing; the strip along the bottom is the instruction it spoke.

{% include figure.html
src="/images/guides/orcaslicer-connect-printer-wifi/00-session-start.jpg"
alt="A Chrome new-tab page with the address bar ringed in orange, a caption strip along the bottom of the screen reading 'Click the address bar at the top, paste the URL, and press Enter to go to the OrcaSlicer releases page', and the Navisual panel docked down the right-hand side showing the typed question 'how to install and setup Orca slicer for my 3D printer?'."
caption="The session begins. The question is typed into the panel on the right; the ring on the address bar and the caption along the bottom are the answer, drawn straight onto the screen. The URL was already on the clipboard, so this step is paste-and-Enter."
width="1920" height="1080" %}

## Before you start

- **Windows 10 or 11**, about 400 MB free.
- **The printer must be on the same network as the PC.** Not just "on Wi-Fi". If the scan in step 5
  comes back empty, the usual cause is the printer on a 2.4 GHz guest SSID and the PC on the 5 GHz
  main one. Same router, different networks, no discovery.
- **This page was checked on a Creality K2 Plus.** Port 4408 is the Creality K-series web interface.
  On other hardware the *field* is still the answer; the port may not be. See the troubleshooting
  section.

## Part one: install

1. **Download the Windows installer.**
   OrcaSlicer lives on GitHub, not in an app store. Open the
   [releases page](https://github.com/SoftFever/OrcaSlicer/releases) and take the newest entry
   marked **Official Release** — skip anything labelled *Nightly*, *Beta* or *Alpha*.

   Release notes come first; the downloads are at the bottom under **Assets**. There are a dozen
   files and most are not for you — Linux flatpaks, an AppImage, a macOS `.dmg`, portable zips, a
   debug build. You want `OrcaSlicer_Windows_Installer_..._x64.exe`, about 131 MB. Note **x64**, not
   **arm64**, unless you are on an ARM machine.

   {% include figure.html
   src="/images/guides/orcaslicer-connect-printer-wifi/01-github-assets.jpg"
   alt="The GitHub releases page for OrcaSlicer v2.4.2, scrolled to the Assets section listing twelve downloads. OrcaSlicer_Windows_Installer_V2.4.2_x64.exe is ringed in orange. The Navisual panel is docked down the right-hand side of the screen, showing the typed question and the steps completed so far."
   caption="Twelve near-identical filenames, one right answer. The panel on the right is Navisual, keeping the conversation and the plan; the orange mark is it pointing at the x64 installer."
   width="1920" height="1080" %}

2. **Pick your printer in the setup wizard.**
   Run the installer, click through the licence and install location, then work through the
   first-run wizard. Only one page changes an outcome: **Printer Selection**.

   The list is long, grouped by vendor, and opens on whoever is first alphabetically — nowhere near
   you. Use the **search icon in the top left** rather than scrolling, tick the box on your
   printer's card, and click **Next**.

   This is what fills in your bed size, nozzle diameter and print profiles. Get it wrong here and
   every print afterwards is wrong.

   {% include figure.html
   src="/images/guides/orcaslicer-connect-printer-wifi/02-printer-selection.png"
   alt="The OrcaSlicer Setup Wizard on the Printer Selection page, showing a grid of printer cards grouped by vendor with CoLiDo at the top. The search icon sits at the top left of the dialog. The Next button at the bottom right is ringed in orange by Navisual."
   caption="Printer Selection opens on whichever vendor is first alphabetically. Use the search icon at the top left rather than scrolling. The orange mark is Navisual pointing at Next."
   width="1188" height="795" %}

3. **Click Next through the rest.**
   Nothing else needs a decision on a first install. Tick the filament types you actually own — PLA
   is enough to start, and you can add more later from the Filament dropdown. Leave **Stealth Mode**
   off; it only stops OrcaSlicer's own network calls and does not affect talking to your printer.
   Leave **Install Bambu Network plug-in** unticked unless you have a Bambu Lab machine.

   Click **Finish**, then **New Project** to land in the workspace, with your printer, nozzle and
   filament down the left and a build plate sized to your machine.

## The question changed here

Worth noting, because it is what the rest of this page came out of. At this point the session
stopped being about installing anything. Instead of moving to the next step, the user typed a new
question into the panel:

> how to connect to my 3D printer using wifi? It is a Creality K2+ and it is turned on.

Navisual kept the screen it was already looking at, rewrote its plan from *Install and setup Orca
Slicer* to *Connect Creality K2+ 3D printer to OrcaSlicer over Wi-Fi*, and carried on from the same
window. Everything below came out of that one sentence.

## Part two: connect over Wi-Fi

{: start="4"}
4. **Open the connection settings from the Wi-Fi icon.**
   In the left rail, the **Printer** header has a small **Wi-Fi icon** beside it. That is the entry
   point, and the first place people get stuck: it is not on the **Device** tab, which is what the
   name suggests, and it is not in the **File** menu. It is a glyph a few pixels wide next to a
   heading.

   {% include figure.html
   src="/images/guides/orcaslicer-connect-printer-wifi/03-printer-wifi-icon.png"
   alt="The OrcaSlicer main window with the left rail showing a Creality K2 Plus printer profile. A small Wi-Fi icon sits to the right of the Printer heading, ringed in orange by Navisual."
   caption="The Wi-Fi glyph beside the Printer header. Easy to miss at this size, and the only route into the Physical Printer dialog."
   width="1188" height="795" %}

5. **Scan the network and select your printer.**
   The **Physical Printer** dialog opens. For a Creality K-series, set both **Host Type** and
   **Printer Agent** to `CrealityPrint`.

   You can type the IP by hand if you know it, but **Browse…** next to *Hostname, IP or URL* scans
   the local network and finds it — no trip to the printer's touchscreen. Click the row for your
   printer, then the green **Use Selected** button below the list.

   **Write the IP down.** Step 6 needs it, and this dialog is the easiest place to read it.

   {% include figure.html
   src="/images/guides/orcaslicer-connect-printer-wifi/04-detect-creality-printer.png"
   alt="The Detect Creality K-series printer dialog listing one result: model K2 Plus, hostname K2-2E8A, IP 192.168.0.88. The row is ringed in orange by Navisual, with the green Use Selected button below the list."
   caption="One printer found, with its model, hostname and IP. Selecting the row fills the address into the dialog behind it."
   width="1188" height="795" %}

6. **Fill in Device UI — the step that prevents the 404.**
   Back in the Physical Printer dialog, *Hostname, IP or URL* is now filled in and it is tempting to
   press **OK**. Do one more thing first.

   The **Device UI** field is what the **Device** tab loads. Leave it empty and that tab shows a
   bare 404 forever. Fill it with your printer's own web interface — the same IP, on port **4408**:

   ```
   http://192.168.0.88:4408/
   ```

   Substitute your own address. *API Key / Password* and *HTTPS CA File* stay empty on a standard
   Creality setup. **Save Machine as** at the top names this connection in your printer list — worth
   editing if you run more than one machine. Then click **OK**.

   {% include figure.html
   src="/images/guides/orcaslicer-connect-printer-wifi/05-device-ui-field.png"
   alt="The Physical Printer dialog with Host Type and Printer Agent both set to CrealityPrint, the Hostname field showing http://192.168, and the Device UI field filled in with 192.168.0.88:4408."
   caption="Device UI, filled in with the printer's own web interface on port 4408. This one field is the difference between a working Device tab and a permanent 404."
   width="683" height="474" %}

7. **Check the Device tab.**
   Open **Device** along the top. OrcaSlicer loads the printer's own interface inside the tab — on a
   Creality K-series that is **fluidd**: live bed, nozzle and chamber temperatures, recent jobs with
   their durations, axis jog controls and a console, without leaving the slicer.

   Slicing a model now gives you a **Print** button that sends the job over the network instead of
   writing G-code to a card.

   {% include figure.html
   src="/images/guides/orcaslicer-connect-printer-wifi/06-device-tab-fluidd.png"
   alt="The OrcaSlicer Device tab showing the fluidd web interface: a Thermals panel with live chamber heater, extruder and heater bed temperatures, a temperature graph, a list of three recent gcode jobs with print durations, and tool jog controls."
   caption="The Device tab doing its job: thermals updating live, recent prints listed, jog controls ready."
   width="1188" height="794" %}

## If the Device tab still shows 404

{% include figure.html
src="/images/guides/orcaslicer-connect-printer-wifi/07-device-tab-404.png"
alt="The OrcaSlicer Device tab showing a blank white page with the heading 404 Not Found."
caption="What an empty Device UI field looks like. The connection is fine; the tab is loading a URL that was never supplied."
width="1188" height="795" %}

In order:

- **Check the port.** `4408` is the Creality K-series web interface. Other hardware differs — a
  Klipper machine running Mainsail or fluidd directly is usually `80` or `81`, and some builds use
  `7125` for the Moonraker API rather than the UI. The quickest test is to open the same URL in a
  browser on the same PC: if the browser shows the interface, that exact URL belongs in **Device
  UI**; if the browser 404s too, the port is wrong and OrcaSlicer is only relaying the printer's
  answer.
- **Include the scheme.** `http://` at the front. A bare `192.168.0.88:4408` is not a URL and the
  embedded browser will not guess.
- **Do not put the Device UI address in the Hostname field.** Different fields, different jobs:
  *Hostname, IP or URL* is where prints are sent, *Device UI* is what the tab displays.
- **Confirm it saved.** Closing the dialog with the red X rather than **OK** discards the edit, and
  the tab keeps showing 404 with no sign the field was ever touched.

## Why this is hard to find

1. **The connection works without it.** Fill in the IP and you can slice and send a print. Nothing
   warns you a second field exists, so guides that end at "Use Selected, OK, done" are not wrong —
   they are answering a different question.
2. **The failure is silent and in the wrong place.** The field you skipped is in the *Physical
   Printer* dialog; the symptom appears on a *Device* tab that looks like a separate feature.
   Nothing on screen links the two.
3. **The port is hardware-specific and undocumented in the app.** OrcaSlicer asks for a URL and
   offers no hint what yours is. 4408 comes from Creality's firmware, not from anything in the
   dialog.

The field also reads as optional. It sits between *Hostname, IP or URL* and *API Key / Password*,
both of which genuinely are optional on a local network, and it has no asterisk, no placeholder and
no tooltip.

## How this guide was made

Nothing here was written from memory or rebuilt from a manual. Somebody sat down at a Windows
machine and asked one question — *"how to install and setup Orca slicer for my 3D printer?"* — and
Navisual guided them through it one control at a time, drawing a mark on screen and speaking each
instruction. The screenshots above are the frames it captured.

- **The session** ran 20 steps across 18 exchanges, in one sitting, from an empty browser tab to a
  live printer dashboard.
- **16 of 20 controls** were pinpointed on screen. Two steps were scrolling or summaries with
  nothing to point at; one fell back to the model's own visual estimate, which was correct.
- **It changed course twice** — once when the question changed mid-task, once when a step led to a
  404 and had to be worked back from. Both are in this guide rather than tidied out of it.
- **Edited:** screenshots are cropped to the application window except the two that show the
  Navisual panel; the desktop behind it is the author's and is nobody else's business. Repeated
  clicks were merged and the no-decision wizard pages compressed into one step.
- **Not edited:** every orange mark is where Navisual actually drew it, including the one on a
  button it could not name.

---

*Checked on OrcaSlicer 2.4.2 with a Creality K2 Plus on Windows 11 in September 2026. Every
screenshot is a real frame from one session, and the orange marks are Navisual pointing at the
control named in the step beside them.*
