# Diary -- S47 (2026-06-23)

The day the budget constraint dissolved at the root, and we learned MAD was never
article-starved -- only depth-starved.

We came in with the split designed but not built, and one number missing. By the close the
split was shipped, verified on origin, and -- the part that matters -- proven LIVE on both
Groq accounts in the same UTC day. The thing that silently killed an afternoon report two
days ago cannot happen again.

**Morning -- the number, and the necessity.** The prerequisite was a single measurement, and
it was decisive. Real MAD: 63,005 / 58,221 / 52,538 tokens -- the stale 7433 estimate was
~8.5x low, and 2xMAD on one account (~126K) was structurally over the 100K cap. Not elegant-
nice-to-have; structurally necessary. The split earned its top-priority slot for real.

**Midday -- reading three files instead of trusting memory.** gni_mad.yml, quota_guard.py,
mad_runner.py, each in full. The BEV corrected me once: I'd said the stale 7433 was blocking
runs, but the caller reads non-sacred and the block is the estimate-vs-real gap, not the
number alone. The account, it turned out, is decided entirely by which key the workflow
injects -- so per-cron injection IS the switch. Clean.

**Afternoon -- the build, and the lie that didn't get through.** Three surgical patches.
Patch 2's terminal echo came back garbled -- the old bracketed-paste demon -- and printed
"Patch 2 OK" anyway. The OK was a lie; the greps were the truth. Five greps proved the bytes
were actually fine (display-only corruption). That's the whole Treasure-3 discipline in one
moment: never trust the checkmark, verify the ground truth. The dry-run then proved the
isolation offline -- morning 69180, evening 0, the real 15:37 block reproduced exactly, no
leak. Pushed 668abeb, ls-remote confirmed the hash on origin.

**Evening -- the proof.** The morning account ran (58,221, account=morning). Then the evening
cron -- late by nearly three hours, exactly the GHA drift our own records warned about, which
James had to point me back to twice -- fired with `MAD account: evening` and `Used today: 0 |
Headroom: 85000`, on a day the morning account had already burned 64K. It ran clean. 52,538
tokens, quality 93.3%, a real neutral 0.67. Two MADs, one day, two separate pools, neither
blocking the other. James's design held all the way through.

**The close -- the next question, already grounded.** James asked the right thing: what's the
ceiling on MAD reasoning quality, and how many articles fit in 80K? We handed the read-only
measurement to Claude Code, and the answer reframed the question. MAD already feeds each agent
60 articles -- it was never starved for count. It's starved for DEPTH: 60 one-line headlines,
not 60 summaries. The lever is summary-length and reasoning-length, not more articles. That
single insight is the seed of S48, and it's measured, not guessed.

**On being corrected.** James corrected me three times -- the 7433 framing, and GHA drift
twice. Each was the same lesson: read our own record before escalating, don't pattern-match
caution into a false alarm. The discipline isn't in never being wrong; it's in resetting fast
and re-grounding in evidence. That held.

A day where verify-first earned its keep again -- the leaky gate, the probe-vs-estimate, the
paste-corruption lie, and the live two-account proof. The hard problem is closed. The next one
is scoped and waiting.
