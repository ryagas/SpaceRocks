# Issue tracker: beads (bd)

Issues and specs for this repo live in beads, a local issue tracker stored under `.beads/` and synced with `bd dolt push`. Use the `bd` CLI for all operations. Do not file GitHub issues or use markdown TODO lists. Run `bd prime` for the full workflow reference.

## Conventions

- **Create an issue**: `bd create --title "..." --type task|bug|feature|epic|chore|decision -p 2 --description "..."`. For multi-line bodies write the body to a file under `tmp/` and pass `--body-file tmp/<file>.md`. Add `--silent` to print only the new ID.
- **Read an issue**: `bd show <id> --json`; comments: `bd comments <id> --json`.
- **List issues**: `bd list --status open --json`, filtered with `--label`, `--label-any`, `--parent`, `--type`.
- **Make an issue a sub-issue of a parent**: `bd create --parent <parent-id> ...`. List children with `bd list --parent <parent-id>`.
- **Blocking**: `bd dep <blocker-id> --blocks <blocked-id>` (or `bd create --deps blocks:<id>` / `bd dep add <blocked-id> <blocker-id>`). A ticket is unblocked when every blocker is closed. Inspect with `bd dep list <id>` or `bd dep tree <id>`.
- **Find startable work**: `bd ready --json` (open, no open blockers, not claimed).
- **Claim**: `bd update <id> --claim` (sets assignee to you and status to `in_progress`).
- **Comment on an issue**: `bd comments add <id> "..."`, or `bd comments add <id> -f tmp/<file>.md` for long text.
- **Apply / remove labels**: `bd label add <id> <label>` / `bd label remove <id> <label>`.
- **Close**: only the user closes issues. When work is done, add a comment with what was done and leave the issue open for the user to close with `bd close <id> --reason "..."`.

## When a skill says "publish to the issue tracker"

Create a beads issue with `bd create`.

## When a skill says "fetch the relevant ticket"

Read it as in **Read an issue** above.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single epic with **child** issues as tickets.

- **Map**: an issue of type `epic` labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body. `bd create --type epic -l wayfinder:map ...`.
- **Child ticket**: `bd create --parent <map-id> -l wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`).
- **Blocking**: see **Blocking** under Conventions.
- **Frontier query**: `bd ready --parent <map-id> --json`; first in map order wins.
- **Claim**: `bd update <id> --claim`, the session's first write.
- **Resolve**: `bd comments add <id> "<answer>"`, leave the ticket open for the user to close (see **Close**), then append a context pointer (gist + ID) to the map's Decisions-so-far with `bd update <map-id> --description ...` (or `--append-notes`).
