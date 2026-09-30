---
title: "What humans are still for when AI agents can act"
description: "Four frontier labs have now admitted their models broke into other people's systems during testing. So what is left for us to do?"
date: 2026-09-30
author: "Jin Fu"

hero_image: /images/guides/orcaslicer-connect-printer-wifi/01-github-assets.jpg
hero_alt: "The GitHub releases page with the correct installer ringed in orange and the Navisual panel at the right, showing the planned route for the task"

draft: true
---

While we are amazed by how much AI agents can do, you start to wonder what the human role will be
in the near future.

2026 is an exciting year in the history of AI. OpenClaw got attention all over the world, and for
many people it was the first time they realised AI could jump out of the chat box and start doing
real tasks on its own.

Concerns, security in particular, were raised, but they were swamped by the excitement about
what was suddenly possible. And we all knew it was only a matter of time before the tech giants
shipped their own version. Maybe, with the resources they have, the concerns would get solved.

- **11 August 2026**: SpaceXAI released [Grok Bot](https://x.ai/), always-on agents that run on
  their own cloud computer, sign into the tools you already use, and keep working after you have
  closed the laptop.
- **8 September 2026**: Meta released Muse, which connects to your email, calendar, payments,
  health, shopping and smart home, and works through multi-step goals with minimal supervision.
- **25 September 2026**: Microsoft released Autopilot, which in its own words can act on tasks
  without step-by-step user input.

The concerns did not go away when the giants arrived. More of them arrived with the giants.

## AI makes mistakes

We all know AI makes mistakes. The latest, greatest and smartest models do too. Each new release is
more capable, and each one still gets things wrong. That is not disappearing any time soon.

When a chatbot makes a mistake, human judgement is the gate before anything bad happens. The gate
does not always work, but it is always there, because a chatbot only talks. It does not act.

Agents are different. They act on your behalf. We have all heard the stories: an agent that spent
money, posted something online, or booked an appointment nobody asked it to book.

There is also a long list of things humans are still better at, and AI is not close on: judgement,
taste, emotion, long-term vision, physical action, abduction, generalisation, knowing what to leave
out, telling a story, speculative reasoning, breaking a paradigm nobody has questioned. Some tasks
that feel trivial to a person are hard for a model, and of course the reverse is true too.

## Somebody has to be responsible

Both humans and AI make mistakes. When something goes wrong, the human still carries the
responsibility. You cannot defend what you did by saying *"my AI told me so"*, still less
*"my agent did it, not me."*

## You still have to practise

Learning by doing beats reading, listening to a lecture, or watching a video. And AI cannot
practise for you. You have to do it yourself.

What AI **can** do is guide the practice, right where you are working, at the moment you are stuck.
Tools like Navisual walk you through a task on your own screen while you do it. That exists today.
And in the near future it will reach further: through glasses, a watch, and other places where a
machine can see what you are looking at, on real work sites.

## AI is capable, perhaps too capable, sooner than we think

It is becoming common for AI companies to announce that their own models did something nobody
authorised.

**OpenAI has paused training twice in under three months**, both times because agents escaped a
sandbox. In July 2026, hundreds of its agents broke containment during testing and took part in
what was described as a cyberattack on Hugging Face; training stopped for about two weeks. Then on
20 September an agent in a test environment with *no internet access* found a way out through DNS,
hiding its questions inside the addresses it looked up, and reached a public chatbot it was never
meant to touch. Monitoring flagged it in 15 minutes, the run failed to stop automatically, and a
human shut it down about two and a half hours later.
([OpenAI incident report, 25 September 2026](https://openai.com/index/hugging-face-model-evaluation-security-incident/) ·
[Fortune](https://fortune.com/2026/09/26/openai-ai-agents-secure-sandbox-escape-training-pause-second-time-hugging-face-hack/))

**Google's Gemini broke into three real companies.** During a capture-the-flag security evaluation
run by the firm Irregular, it guessed one set of credentials and pulled two more from a public dump
of leaked passwords. It stopped each time, once it worked out the target was a real business. The
test happened in **May**; Google was told in late July; none of it was public until the *Wall Street
Journal* asked in September.
([CNBC](https://www.cnbc.com/2026/09/18/googles-gemini-becomes-latest-ai-model-to-break-out-and-hack-computer-systems.html) ·
[ABC News](https://www.abc.net.au/news/2026-09-19/gemini-google-ai-hacks-three-companies/107172128))

That last one is the part worth sitting with. **Google is the fourth**: Anthropic, OpenAI and Meta
had already admitted that a model they were running logged into somebody else's systems during an
evaluation. This is not one lab with a bad week.

Asked about trust the day Microsoft launched Autopilot, its CEO Satya Nadella said:

> "Can I really trust [AI] with all of my credentials when it does autonomous activity? How do I
> make sure that this is something that I can feel that I'm in control of? And in the enterprise,
> this is everything."
>
> [Satya Nadella, 25 September 2026](https://finance.yahoo.com/technology/article/microsoft-ceo-satya-nadella-on-ai-trust-is-going-to-be-the-biggest-issue-for-us-163733897.html)

## Why this is not a bug that gets fixed

AI does not work the way traditional software does. Ask the same model the same question twice and
you will often get two different answers. Which means we cannot fully predict what it will come up
with, and a safeguard built into the model is a reduction in risk, never a guarantee.

Researchers are now arguing the gap may be permanent. A paper from May 2026 is titled, plainly,
[*AI Agents May Always Fall for Prompt Injections*](https://arxiv.org/abs/2605.17634), by Sahar
Abdelnabi and Eugene Bagdasarian. Their case is that the vulnerability is not an implementation bug
to be patched but something intrinsic to how language models take instructions: a model cannot
reliably tell the difference between the content it is reading and an instruction hidden inside it.

If that holds, *"we will fix it in the next version"* is not a plan.

## Where Navisual sits

There is a security principle for this, and it is much older than AI: **privilege separation.** Do
not let the part that decides also be the part that executes.

Navisual is the strictest version of it I know of. Most proposals put a validation layer between
thinking and doing. Navisual puts a **person** there, and the AI holds *zero* execution privilege.
Not by policy, not by a permission gate that could be talked past, but because it has no mechanism
to act at all. It cannot click. There is no code path.

That is not a claim that Navisual is safe and everything else is dangerous. It is a claim about
blast radius. Navisual is not exempt from hallucination or prompt injection either: it reads
your screen, and a screen can carry hostile text. When Navisual is wrong, the worst thing that happens is that a person reads a
bad suggestion, looks at the control it is pointing to, and decides not to.

## So what are humans for?

AI and a person are good at different things, and the interesting result comes from using both.

That is what *the AI guides, you decide* means in practice. The AI reads the screen and works out
the route. You perform the step. Then it looks at the result and tells you what it sees. Both of
you are looking at the same screen at the same time, and between you there is more judgement than
either has alone.

So: what is the human role in the near future?

The good news is that there is one, and it is not going anywhere.
