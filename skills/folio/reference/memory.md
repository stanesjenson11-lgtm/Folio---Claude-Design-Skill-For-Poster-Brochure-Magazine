# memory — learning across projects with claude-mem

The pattern library (`library/`) is folio's explicit, file-based memory and works everywhere. When the claude-mem plugin is installed (Claude Code), its knowledge-agent adds implicit memory: what clients corrected, which directions were approved, which crops or fonts caused trouble. Use it if the tools exist; skip silently otherwise.

Taste verdicts (what the user loved or rejected) have their own loop in `reference/taste.md`; `library/TASTE.md` is the portable record.

## Before a project (brief stage)
If `list_corpora` shows a `folio-craft` corpus, prime it once per session and ask focused questions:
```
prime_corpus name="folio-craft"
query_corpus name="folio-craft" question="What did <client> or similar <register> clients ask us to change in past brochures?"
query_corpus name="folio-craft" question="Which fonts, colours or layout patterns were rejected or approved before for <client>?"
query_corpus name="folio-craft" question="What print or preflight problems recurred in past jobs?"
```
Fold the answers into BRIEF.md under "Known preferences / past corrections".

## Create or refresh the corpus
```
build_corpus name="folio-craft" description="Brochure, report, catalog and magazine design decisions, client corrections and print issues" query="brochure layout print design client feedback preflight" types="decision,bugfix,discovery,change" limit=500
prime_corpus name="folio-craft"
```
After new projects: `rebuild_corpus name="folio-craft"` then `reprime_corpus name="folio-craft"`.

## After a project
Say the durable lessons plainly in the conversation so claude-mem's observer records them — e.g. "Decision: FD Sports uses Poppins + red #EE2C27 progress-rail headers; client rejected serif body text." — and add any new pattern cards to the library. A custom claude-mem mode (see its mode-creator skill) with observation types like `layout-pattern`, `client-correction` and `print-defect` makes these easier to filter.
