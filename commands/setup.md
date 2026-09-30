---
description: One-time setup — make plain /folio start folio's guided flow (plan mode, questions, page plan) in Claude Code
---
Create the personal command file `~/.claude/commands/folio.md` (create the folder if it is missing). If that file already exists and was not written by folio, show it to the user and ask before replacing it. Write exactly:

```
---
description: folio — make a magazine, brochure or poster, guided step by step (plan mode, questions from logo to page plan)
argument-hint: "[what to make + your content: PDF, pasted text, website, photos, logo]"
---
Use the folio skill (from the folio plugin) to make a new piece from: $ARGUMENTS

Follow its `reference/wizard.md` from the start: enter plan mode, scan everything supplied, the question rounds, the page plan for approval, a first look, then the build.
```

Then tell the user in two lines: plain `/folio` now starts the guided flow (restart Claude Code if it doesn't appear yet); `/folio:new` does the same.
