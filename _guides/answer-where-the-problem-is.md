---
title: "The answer, where the problem is"
description: "Books, then search, then pictures, then video, then agents that click for you. Each better than the last. Each still not quite it."
date: 2026-09-23
author: "Jin Fu"

# No `steps:` here on purpose. This is an essay, not a procedure, so the layout
# emits schema.org TechArticle rather than HowTo — and `app` / `os` are left out
# too, since the chip row under the title is for "which app is this about".
hero_image: /images/guides/orcaslicer-connect-printer-wifi/00-session-start.jpg
hero_alt: "Navisual pointing at a Chrome address bar, ringed in orange, with a caption strip along the bottom of the screen giving the instruction"

draft: true
---

You have a question. Nobody around you knows the answer. What can you do?

In the good old days you found a book and studied it. Eventually you found the answer. It could
take days.

Then came the internet. You type the question into a search box and look for the right article
with the right answer. Information at your fingertips — nice.

But you want more. You want to see what the answer looks like. So articles started carrying
pictures, and most of us are visual learners — nicer.

And you want more again. You want to see the problem actually being solved. You want someone to
talk through it, explain the reasoning, take questions. Here come YouTube and TikTok — even
nicer.

## Just tell me the answer

After the initial excitement, you notice something. Sometimes you just want to know what the fix
is. You don't want to spend ten minutes watching, never mind the sponsor read and the reminder to
subscribe.

You are not the only one. There is a thread on Blender Artists called *"Why does everything have
to be a video these days?"* The person who started it had found his answer in a manual in about
eight seconds, after ten minutes of video that covered things he already knew. Twenty people
showed up to agree.

The most-liked reply explains why it keeps happening: creators earn from you watching, not from
you finding.

## So, agents

Here comes the AI chatbot, and then the AI agent. No more gambling on which link might answer
you. And even *"nicer"* — the agent can do it for you. It sees your browser, clicks and types on
your behalf, books the whole trip, edits your document, makes the purchase.

But is it nicer?

You start to worry about what it decides on your behalf. The security firm Cyera looked at 7,246
publicly reported AI incidents and verified 344 as enterprise-relevant. **188 of those were caused
by an autonomous agent with no attacker anywhere in the chain.** Nobody attacked anything. An
agent was given a task, pursued it, and broke something on the way.

So the agents ask for your approval instead, and you get approval fatigue. You are clicking
*Allow* on a stream of decisions you do not have time to judge. And when it finishes, you have the
result but you did not learn anything. Next time, you will need it again.

## The tell

Here is the part I find most telling.

In a thread about using Claude Code to tune a PC, the AI described its own limits. For GUI-only
apps like the NVIDIA Control Panel, it said, it took a screenshot of the user's screen and told
him what to click.

The most capable agent available falls back to pointing — and it does it badly. One static
screenshot, prose instead of a pointer, no idea whether you are even looking at the right window.

## Now it is possible to do that properly

Navisual is the buddy you ask while you are working. Ask your question without leaving what you
are doing. It understands the question better because it is looking at exactly what you are
looking at. It works out a plan, then walks you through each step with a pointer on the actual
button and narration in text and speech. You can talk back to it, correct it, ask why. It gets
you straight to the point, in a way you can see.

And it never clicks for you. You do every step yourself, which is the reason you still remember
it tomorrow.

Here is what that looks like in practice.

{% include figure.html
   src="/images/guides/orcaslicer-connect-printer-wifi/00-session-start.jpg"
   alt="A Chrome new-tab page with the address bar ringed in orange and a caption strip along the bottom of the screen giving the instruction, with Navisual's panel at the right"
   caption="The pointer goes on the real control, with the instruction captioned and spoken." %}

{% include figure.html
   src="/images/guides/orcaslicer-connect-printer-wifi/01-github-assets.jpg"
   alt="The GitHub releases page for OrcaSlicer scrolled to the Assets section listing twelve downloads, with the correct Windows installer ringed in orange and the Navisual panel at the right"
   caption="Twelve downloads on the page. Navisual rings the one you need." %}

{% include figure.html
   src="/images/guides/word-copilot-tab-missing/02-privacy-settings-analyze-content.png"
   alt="Word's Privacy Settings window with the Connected experiences checkbox highlighted, and the Navisual panel on the right listing the planned route for the task"
   caption="The plan stays visible on the right, so you can see where the next few steps are going." %}

## Two real ones

Both of these started as someone stuck in front of a screen, asking Navisual. They are written up
step by step:

**[Setup OrcaSlicer with your 3D printer over Wi-Fi](/guides/orcaslicer-connect-printer-wifi/)**
— almost every guide online skips one field. Leave it blank and the Device tab shows a blank
404 even though printing works fine.

**[No Copilot tab in Word Options?](/guides/word-copilot-tab-missing/)** — most answers say
File ▸ Options ▸ Copilot. That tab is missing in many builds of Word.

Which is the whole idea. The answer, where the problem is.
