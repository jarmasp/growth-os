Run a pre-mortem BEFORE coding starts on a ticket. Captures business context, probable
failure points, design pattern, and key assumptions. Writes a draft reflection note to
the vault with status: in-progress.

When the ticket is resolved, run /growth:reflect — it detects the draft automatically,
preserves the pre-mortem content, and replaces the Assumptions question with a bridge
question comparing predictions to reality.

Load config and follow the full workflow:

```bash
cat ~/Documents/growth-os/config.json
```

Then load and follow: `~/Documents/growth-os/workflows/premortem.md`
