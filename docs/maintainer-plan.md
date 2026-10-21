# First-month maintainer plan

This is a practical plan for turning the first release into a genuinely maintained project. It is not a promise of adoption or a prediction of program selection.

## Week 1 — Validate the use case

- Run the checker on a few non-sensitive PDFs that you are allowed to inspect.
- Ask 3–5 Bengali-language students, teachers, librarians, or researchers whether the warnings are understandable and useful.
- Record only the issue and feedback; do not share private or copyrighted PDFs.
- Create issues for false positives and missing checks.

## Week 2 — Improve one real pain point

- Choose one user-reported problem.
- Reproduce it with synthetic or permissioned text.
- Add a regression test before changing the implementation.
- Explain the trade-off and limitations in the pull request.

## Week 3 — Improve the user experience

- Test installation on a clean Windows environment and one Linux/macOS environment if available.
- Improve error messages and examples based on actual user feedback.
- Ask a user who has not read the source code to follow the README.

## Week 4 — Decide whether a public release is justified

- Fix genuine bugs and confirm CI is green.
- Release a patch version only if there is a meaningful change.
- Triage issues and respond to contributors constructively.
- Summarize real usage and remaining limitations without inventing counts.

## Readiness before applying to a maintainer program

The repository should be public, tested, licensed, and have a clear use case. More importantly, you should be able to show real maintenance responsibilities and some evidence that others find it useful. A newly published repository with no external use is unlikely to be competitive for a program aimed at maintainers of important open-source projects.
