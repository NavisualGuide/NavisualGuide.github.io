---
title: "Show the Creality K2 camera in OrcaSlicer"
description: "On current K2 firmware the camera only shows in Creality Print. A free program, go2rtc, puts it back in OrcaSlicer's Device tab. No root, no downgrade."
date: 2026-11-23
app: "OrcaSlicer · Creality K2 Plus"
os: "Windows 10 / 11"
total_time: PT20M
hero_image: /images/guides/orcaslicer-creality-k2-camera/01-device-tab-camera.jpg
hero_alt: "OrcaSlicer's Device tab with Fluidd on the left and the live Creality K2 Plus camera on the right"
draft: false

steps:
  - name: "Find the printer's IP address in OrcaSlicer"
    text: "In OrcaSlicer, on the Prepare tab, click the small Wi-Fi icon beside the Printer header in the left rail. The Physical Printer dialog opens. The printer's address is in the Hostname, IP or URL field, for example 192.168.0.88. The box is narrow and usually cuts the address off, so click in it and press End to see the rest. Note it and close the dialog."
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

So you've hooked a Creality K2 up to OrcaSlicer, the Device tab shows Fluidd, and there's no camera
anywhere. Search around and you'll be told to add a camera in Fluidd at
`http://<printer-ip>:8080/?action=stream`, or to try port 8000. On current K2 firmware neither one
gives you any video, and Creality's own answer is basically "use Creality Print".

**The short answer:** the K2 camera still streams, just only over Creality's own WebRTC connection
on port 8000, and neither Fluidd nor OrcaSlicer can play that. A free little program called
**go2rtc** can. You run it on your PC with a short settings file that names the printer, then set
OrcaSlicer's **Device UI** to a page it serves, `http://127.0.0.1:1984/k2.html`. After that the
Device tab shows Fluidd and the live camera side by side. Nothing on the printer gets touched: no
root, no firmware downgrade.

{% include figure.html
   src="/images/guides/orcaslicer-creality-k2-camera/01-device-tab-camera.jpg"
   alt="OrcaSlicer's Device tab showing Fluidd on the left and the live Creality K2 Plus camera on the right, labelled Camera: live"
   caption="Where you'll end up: Fluidd and the K2 camera side by side in OrcaSlicer's Device tab."
   width="1920" height="1032" %}

## Before you start

- **I tested this on a K2 Plus**, with OrcaSlicer 2.4.2 on Windows 11. OrcaSlicer updates a lot,
  but all this needs is its Physical Printer dialog and the Device tab, so a newer version should
  be fine. The K2 and K2 Pro use the same camera connection and should work too, though I haven't
  tried them. Same for the K1C (2025).
- **go2rtc has to be running on your PC** for the camera to show up, and the camera page only
  works on that PC. It only listens on `127.0.0.1`, so nothing new gets opened up to your network.
- **Creality Print keeps working.** It happily showed the camera at the same time as OrcaSlicer.
- You'll copy two small files from this page. Each one has a **Copy** button.

## Steps

1. **Find the printer's IP address.** In OrcaSlicer, on the **Prepare** tab, click the little
   **Wi-Fi icon** next to the **Printer** header in the left rail. The address is in the
   **Hostname, IP or URL** box, something like `192.168.0.88`. The box is narrow and usually only
   shows the start, like `http://192.168`, so click in it and press **End** to see the rest. Jot it
   down and close the dialog.
2. **Make two folders.** In File Explorer, open **Documents**, make a folder called `go2rtc`, and
   inside that one a folder called `www`.
3. **Download go2rtc.** Go to
   [github.com/AlexxIT/go2rtc/releases](https://github.com/AlexxIT/go2rtc/releases), find the
   newest release, open its **Assets** list and grab `go2rtc_win64.zip`.
4. **Put go2rtc.exe in Documents\go2rtc.** Open the zip and copy `go2rtc.exe` into the `go2rtc`
   folder.
5. **Create go2rtc.yaml.** Open Notepad, hit **Copy go2rtc.yaml** below and paste. Swap
   `192.168.0.88` for your printer's address. Then **File ▸ Save as**, go to `Documents\go2rtc`,
   set **Save as type** to **All files**, name it `go2rtc.yaml` and save. Don't skip the *All
   files* bit: without it Notepad quietly saves `go2rtc.yaml.txt` and go2rtc won't find it.
6. **Create k2.html.** In a new Notepad window, hit **Copy k2.html** below and paste. Save it into
   `Documents\go2rtc\www` the same way, as `k2.html`. You don't need to change anything in it.
7. **Start go2rtc.exe.** Double-click it. Windows will probably say *Windows protected your PC*,
   just because go2rtc isn't from a big publisher. Click **More info**, then **Run anyway**. A
   black window pops up listing what it's listening on. Leave it open: closing it stops the
   camera.
8. **Check it in a browser.** Open `http://127.0.0.1:1984/k2.html`. You should see Fluidd on the
   left and the camera on the right, with **Camera: live** above it. Windows Firewall might ask
   whether go2rtc can use public and private networks. For me the camera worked either way,
   since go2rtc only listens on your own PC.
9. **Point OrcaSlicer at the page.** Click the **Wi-Fi icon** next to **Printer** again, set
   **Device UI** to `http://127.0.0.1:1984/k2.html`, and click **OK**.
10. **Open the Device tab.** Fluidd on the left, live camera on the right. Done.

**Want it to start with Windows?** Press **Win+R**, type `shell:startup`, press Enter, and drop a
shortcut to `go2rtc.exe` in the folder that opens.

## The two files

**go2rtc.yaml**: the only thing you change is the printer's address.

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

**k2.html**: Fluidd on the left, camera on the right. It reads the printer's address from
go2rtc.yaml, so there's nothing to edit.

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
  pc.onicecandidate = e => {
    if (e.candidate) ws.send(JSON.stringify({ type: "webrtc/candidate", value: e.candidate.candidate }));
  };
  pc.onconnectionstatechange = () => {
    if (pc.connectionState === "connected") {
      const cam = document.getElementById("cam");
      cam.srcObject = new MediaStream(pc.getReceivers().map(r => r.track));
      cam.play().catch(() => {});
      state.textContent = "Camera: live";
    }
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

This is the bit that sends everyone in circles. Fluidd's **Settings ▸ Cameras** lets you add the
camera, then shows it with a warning triangle and never actually displays it, no matter which
stream type or address you try. The reason: the Moonraker version Creality ships on the K2 is old,
and it drops the camera's **Enable** setting when it saves. Fluidd reads the missing setting as
*off*. So no camera you add there will ever show on a K2, even one that works. That's why this
guide puts the camera next to Fluidd instead of inside it.

## If the camera stays black

- **The page says *Camera: live* but the picture is black.** Could just be the printer: with the
  chamber light off, the K2 camera sends an almost black picture. Turn the light on from the
  printer's screen or from Fluidd.
- **You closed the go2rtc window.** The page will say *Camera: go2rtc is not running*. Start
  `go2rtc.exe` again.
- **Fluidd is blank, or the page says no printer address was found.** Double-check the address in
  `go2rtc.yaml`, and make sure the file really is `go2rtc.yaml` and not `go2rtc.yaml.txt`.
- **The black window closes right away.** go2rtc couldn't read its settings. Open `go2rtc.yaml`
  and compare it with the block above; the indentation has to match exactly.
- **Check the printer end.** `http://<printer-ip>:8000/` should load in a browser, even if it's a
  blank page. If it doesn't load at all, your PC can't reach the printer.

## Let Navisual walk you through it

If you'd rather not follow along by hand, paste this into Navisual's task box. It'll point at
each control on your screen, one step at a time.

```text
Walk me through these steps to show my Creality K2 camera in OrcaSlicer, using the guide at navisualguide.com/guides/orcaslicer-creality-k2-camera/:
1. Find the printer's IP address in OrcaSlicer's Physical Printer dialog (Wi-Fi icon beside the Printer header on the Prepare tab). The Hostname box cuts the address off, so ask me to click in it and press End before reading it.
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

{% include figure.html
   src="/images/guides/orcaslicer-creality-k2-camera/02-navisual-copy-button.png"
   alt="Navisual pointing at this guide's Copy go2rtc.yaml button, with its panel on the right reading: Click the Copy go2rtc.yaml button above the code box"
   caption="Navisual pointing at this page's own Copy button."
   width="1349" height="942" %}

go2rtc is an open-source project by AlexxIT on GitHub, MIT licensed. Creality support landed in version 1.9.10.
