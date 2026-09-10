# 05 Principles

The design principles are maintained in the README, where users read them before installing:
[Design principles](../../README.md#design-principles). The reasoning behind each is in the
[decision log](14-decision-log.md).

Two further principles govern how the skill itself is built:

- **Judgement in the instructions, mechanics in the harness.** Deciding what a chapter should say
  is the agent's job, guided by `SKILL.md` and `conventions.md`. The rules listed under
  [Checks](06-software-architecture.md#checks) are enforced by `scripts/verify.py` instead, so
  they do not depend on the agent following an instruction; the known gaps are in
  [chapter 03](03-quality-attributes.md).
- **Rule and check move together.** A rule in `conventions.md` that the harness enforces is
  changed together with its check under `scripts/checks/` and a test, as
  [`CONTRIBUTING.md`](../../CONTRIBUTING.md#rules-and-conventions) describes.
