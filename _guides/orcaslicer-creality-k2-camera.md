---
title: "Show the Creality K2 camera in OrcaSlicer, without root"
description: "On current K2 firmware the camera only shows in Creality Print. A free program, go2rtc, puts it back in OrcaSlicer's Device tab. No root, no downgrade."
date: 2026-11-23
app: "OrcaSlicer 2.4.2 · Creality K2 Plus"
os: "Windows 10 / 11"
total_time: PT20M
draft: true

steps:
  - name: "Find the printer's IP address in OrcaSlicer"
    text: "In OrcaSlicer, on the Prepare tab, click the small Wi-Fi icon beside the Printer header in the left rail. The Physical Printer dialog opens. The printer's address is in the Hostname, IP or URL field, for example 192.168.0.88. Note it and close the dialog."
  - name: "Make two folders: Documents\\go2rtc and Documents\\go2rtc\\www"
    text: "In File Explorer, open Documents and create a folder named go2rtc. Inside it, create a folder named www."
  - name: "Download go2rtc for Windows"
    text: "Open https://github.com/AlexxIT/go2rtc/releases, find the newest release, open its Assets list and download go2rtc_win64.zip."
  - name: "Put go2rtc.exe in Documents\\go2rtc"
    text: "Open the downloaded go2rtc_win64.zip and copy go2rtc.exe into the Documents\\go2rtc folder."
  - name: "Create go2rtc.yaml with your printer's address"
    text: "Open Notepad. On the guide page, click Copy go2rtc.yaml and paste it into Notepad. Replace 192.168.0.88 with your printer's address. Choose File, Save as, go to Documents\\go2rtc, set Save as type to All files, name the file go2rtc.yaml and save."
  - name: "Create k2.html"
    text: "Open a new Notepad window. On the guide page, click Copy k2.html and paste it. Save it into Documents\\go2rtc\\www with Save as type set to All files and the name k2.html. Nothing in it needs editing."
  - name: "Start go2rtc.exe"
    text: "Double-click go2rtc.exe in Documents\\go2rtc. If Windows shows Windows protected your PC, click More info, then Run anyway. A black window opens; leave it open, because closing it stops the camera."
  - name: "Check the camera in a browser"
    text: "Open http://127.0.0.1:1984/k2.html in a web browser. Fluidd appears on the left and the printer camera on the right, with Camera: live above it."
  - name: "Point OrcaSlicer's Device UI at the camera page"
    text: "In OrcaSlicer, on the Prepare tab, click the Wi-Fi icon beside the Printer header again. Set the Device UI field to http://127.0.0.1:1984/k2.html and click OK."
  - name: "Open the Device tab"
    text: "Click the Device tab at the top of OrcaSlicer. Fluidd shows on the left and the live printer camera on the right."
---

You set up a Creality K2 in OrcaSlicer, the Device tab shows Fluidd, and the camera is nowhere. The
usual advice is to add a camera in Fluidd pointing at `http://<printer-ip>:8080/?action=stream`, or
at port 8000. On current K2 firmware neither address serves any video, and Creality's own answer is
to watch the camera in Creality Print instead.

**The short answer:** the K2 camera still streams, but only over Creality's own WebRTC connection on
port 8000, which neither Fluidd nor OrcaSlicer can play. A free program, **go2rtc**, can. Run it on
your PC with a two-line setting naming the printer, then set OrcaSlicer's **Device UI** to a small
page it serves, `http://127.0.0.1:1984/k2.html`. The Device tab then shows Fluidd and the live
camera side by side. Nothing on the printer changes, so no root and no firmware downgrade.

## Before you start

- **Checked on a Creality K2 Plus** with OrcaSlicer 2.4.2 on Windows 11. The K2 and K2 Pro use the
  same camera connection, so it should work on them too, but that is not tested. On a K1C (2025) it
  is untested.
- **go2rtc has to be running on this PC** for the camera to show, and the camera page only works
  on this PC. It listens on `127.0.0.1` only, so nothing new is opened to your network.
- **Creality Print keeps working.** It showed the camera at the same time as OrcaSlicer.
- You will copy two small files from this page. Each has a **Copy** button.

## Steps

1. **Find the printer's IP address.** In OrcaSlicer, on the **Prepare** tab, click the small
   **Wi-Fi icon** beside the **Printer** header in the left rail. The address is in the
   **Hostname, IP or URL** field, for example `192.168.0.88`. Note it and close the dialog.
2. **Make two folders.** In File Explorer, open **Documents**, create a folder named `go2rtc`, and
   inside it a folder named `www`.
3. **Download go2rtc.** Open
   [github.com/AlexxIT/go2rtc/releases](https://github.com/AlexxIT/go2rtc/releases), find the
   newest release, open its **Assets** list and download `go2rtc_win64.zip`.
4. **Put go2rtc.exe in Documents\go2rtc.** Open the zip and copy `go2rtc.exe` into the `go2rtc`
   folder.
5. **Create go2rtc.yaml.** Open Notepad, click **Copy go2rtc.yaml** below and paste. Replace
   `192.168.0.88` with your printer's address. Choose **File ▸ Save as**, go to
   `Documents\go2rtc`, set **Save as type** to **All files**, name it `go2rtc.yaml` and save.
   *All files* matters: without it Notepad saves `go2rtc.yaml.txt`, and go2rtc will not find it.
6. **Create k2.html.** In a new Notepad window, click **Copy k2.html** below and paste. Save it
   into `Documents\go2rtc\www` the same way, as `k2.html`. Nothing in it needs editing.
7. **Start go2rtc.exe.** Double-click it. If Windows shows *Windows protected your PC*, click
   **More info**, then **Run anyway**. A black window opens. Leave it open: closing it stops the
   camera.
8. **Check it in a browser.** Open `http://127.0.0.1:1984/k2.html`. Fluidd appears on the left
   and the camera on the right, with **Camera: live** above it.
9. **Point OrcaSlicer at the page.** Click the **Wi-Fi icon** beside **Printer** again, set
   **Device UI** to `http://127.0.0.1:1984/k2.html`, and click **OK**.
10. **Open the Device tab.** Fluidd on the left, the live camera on the right.

**To start it with Windows** (optional): press **Win+R**, type `shell:startup`, press Enter, and
put a shortcut to `go2rtc.exe` in the folder that opens.

## The two files

**go2rtc.yaml**: the only line to change is the printer's address.

```yaml
api:
  listen: "127.0.0.1:1984"
  static_dir: "www"
rtsp:
  listen: ""
webrtc:
  listen: "127.0.0.1:8555"
streams:
  k2: webrtc:http://192.168.0.88:8000/call/webrtc_local#format=creality
```
{: data-file="go2rtc.yaml"}

**k2.html**: Fluidd on the left, the camera on the right. It reads the printer's address from
go2rtc.yaml, so there is nothing to edit.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>K2 camera</title>
<style>
  html, body { margin: 0; height: 100%; background: #121212; color: #ccc; font: 13px "Segoe UI", sans-serif; }
  body { display: flex; }
  iframe { flex: 1; border: 0; min-width: 0; }
  aside { width: 36vw; max-width: 640px; padding: 0 8px; box-sizing: border-box; }
  video { width: 100%; aspect-ratio: 16/9; background: #000; }
</style>
</head>
<body>
<iframe id="fluidd" title="Fluidd"></iframe>
<aside><p id="state">Camera: connecting...</p><video id="cam" autoplay muted playsinline></video></aside>
<script>
const SRC = "k2";
const state = document.getElementById("state");

// The printer's address comes from go2rtc.yaml, so it is typed in one place only.
fetch("/api/streams").then(r => r.json()).then(s => {
  const m = JSON.stringify(s[SRC] || "").match(/\/\/([^:\/"]+):8000/);
  if (m) document.getElementById("fluidd").src = "http://" + m[1] + ":4408/";
  else state.textContent = "No printer address found in go2rtc.yaml";
});

function connect() {
  const ws = new WebSocket("ws://" + location.host + "/api/ws?src=" + SRC);
  const pc = new RTCPeerConnection();
  pc.addTransceiver("video", { direction: "recvonly" });
  pc.ontrack = e => { document.getElementById("cam").srcObject = e.streams[0] || new MediaStream([e.track]); };
  pc.onicecandidate = e => {
    if (e.candidate) ws.send(JSON.stringify({ type: "webrtc/candidate", value: e.candidate.candidate }));
  };
  pc.onconnectionstatechange = () => {
    if (pc.connectionState === "connected") state.textContent = "Camera: live";
    if (pc.connectionState === "failed" || pc.connectionState === "disconnected") {
      pc.close(); ws.close();
      state.textContent = "Camera: reconnecting...";
      setTimeout(connect, 3000);
    }
  };
  ws.onopen = async () => {
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    ws.send(JSON.stringify({ type: "webrtc/offer", value: offer.sdp }));
  };
  ws.onmessage = async e => {
    const m = JSON.parse(e.data);
    if (m.type === "webrtc/answer") await pc.setRemoteDescription({ type: "answer", sdp: m.value });
    if (m.type === "webrtc/candidate") pc.addIceCandidate({ candidate: m.value, sdpMid: "0" }).catch(() => {});
  };
  ws.onerror = () => { state.textContent = "Camera: go2rtc is not running"; };
}
connect();
</script>
</body>
</html>
```
{: data-file="k2.html"}

## Why adding a camera in Fluidd does nothing

This is the part that sends people in circles. Fluidd's **Settings ▸ Cameras** accepts the camera,
then lists it with a warning triangle and never shows it, whatever stream type and address you
give it. The Moonraker version Creality ships on the K2 is old, and it drops the camera's
**Enable** setting when it saves; Fluidd reads the missing setting as *off*. So no camera added
there ever displays on a K2, including a working one. That is why this guide shows the camera
beside Fluidd instead of inside it.

## If the camera stays black

- **The go2rtc window was closed.** The page says *Camera: go2rtc is not running*. Start
  `go2rtc.exe` again.
- **Fluidd is blank, or the page says no printer address was found.** Check the address in
  `go2rtc.yaml`, and that the file is really `go2rtc.yaml`, not `go2rtc.yaml.txt`.
- **The black window closes straight away.** go2rtc could not read its settings. Open
  `go2rtc.yaml` again and compare it with the block above; the indentation has to match.
- **Check the printer's side.** `http://<printer-ip>:8000/` should answer in a browser, even with
  a blank page. If it does not load at all, the printer is not reachable from this PC.

## How this guide was made

Draft. To be completed after the Navisual walkthrough.

## Let Navisual walk you through it

Paste this into Navisual's task box. It points at each control on your screen, one step at a time.

```text
Walk me through these steps to show my Creality K2 camera in OrcaSlicer, using the guide at navisualguide.com/guides/orcaslicer-creality-k2-camera/:
1. Find the printer's IP address in OrcaSlicer's Physical Printer dialog (Wi-Fi icon beside the Printer header on the Prepare tab).
2. Make Documents\go2rtc and Documents\go2rtc\www.
3. Download go2rtc_win64.zip from github.com/AlexxIT/go2rtc/releases (Assets of the newest release).
4. Copy go2rtc.exe from the zip into Documents\go2rtc.
5. Copy go2rtc.yaml from the guide into Notepad, change the IP, and save it in Documents\go2rtc (Save as type: All files).
6. Copy k2.html from the guide into Notepad and save it in Documents\go2rtc\www the same way.
7. Double-click go2rtc.exe and leave its window open.
8. Open http://127.0.0.1:1984/k2.html in a browser to check it.
9. In OrcaSlicer's Physical Printer dialog, set Device UI to http://127.0.0.1:1984/k2.html and click OK.
10. Open the Device tab.
```
{: data-file="steps for Navisual"}

go2rtc is an open-source project by AlexxIT on GitHub, MIT licensed; its Creality support arrived in version 1.9.10.
