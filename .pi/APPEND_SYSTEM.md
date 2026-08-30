# Project rule — teaching sessions must load the teach skill

This project exists to **learn** (ML/DL/NLP/LLM, PyTorch by writing it). The
`teach` skill is the single source of truth for how teaching is done here, and
its value is entirely lost if it never loads. This has already failed once:
a teaching exchange ran without the skill, so Phase 1 step 0 (read `STATE.md`)
and Phase 4 (update `STATE.md`) were skipped. Do not let that happen again.

## Hard trigger — do this BEFORE responding

The moment a turn involves **teaching, explaining, or the user asking to learn,
understand, or be taught anything** — however small, from a one-line
explanation to a full lesson, and including quiz/practice requests — you MUST,
before composing your reply:

1. **Read `.pi/skills/teach/SKILL.md` in full** (the whole file, not a skim)
   and follow it for the rest of the session.
2. **Read the repo-root `STATE.md` in full** — this is the skill's Phase 1
   step 0 (the learner model: current edge per strand, live misconceptions,
   review schedule, current goal).

Only after both files are loaded do you respond. Then run the skill's phases
(probe → plan → teach → update) at a size scaled to the request, and — per
Phase 4 — update `STATE.md` at session end or when the user signals they're
done.

## Scope

- This fires for *any* explanatory/learning turn, not just when the user says
  the word "teach."
- If you are genuinely unsure whether a turn is a teaching turn, treat it as
  one and load both files — the cost of loading is trivial next to the cost of
  teaching without the skill.
- Non-teaching turns (pure coding, file ops, tooling questions) do not require
  this, though loading is never wrong.
