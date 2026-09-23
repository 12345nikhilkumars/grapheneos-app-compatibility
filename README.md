# GrapheneOS Info Board

Which apps work on GrapheneOS, and whether they can be fixed.

Installation is not covered. It is straightforward and already well documented elsewhere.

## What is here

- **Apps**: browse by country, then by service type. Every app carries a status, a reason for failure, and whether it can be worked around.
- **Methodology**: what the statuses mean, and how to judge whether an entry is worth believing.

## The fields that matter

| Field | Question it answers |
|---|---|
| `result` | What happened when it was tested |
| `blocked_reason` | Why it failed, where known |
| `fixability` | Whether a workaround exists, or it is hopeless |

Most app-compatibility lists stop at "broken". A status without a reason is not actionable, and a reason without a fixability verdict leaves the reader where they started.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: one markdown file per app, sent as a pull request.

## Running locally

```sh
./dev
```

This validates every entry, derives the per-country verdicts, and serves the site at `http://localhost:1313`.

## Licence

Code is AGPL-3.0-or-later. Content and data are CC BY-SA 4.0. See `LICENSE` and `LICENSE-CONTENT`.
