# secrets/

This folder holds keys and credentials on **your own machine only**. Everything in here except this README is ignored by git, so nothing you put here can be pushed by accident.

| File | What it is | How to get it |
|---|---|---|
| `gcp-service-account.json` | Key used by containers to read and write the team GCS bucket | Ask Mostafa or Owen. It's shared privately, never in chat groups. |
| `wandb.env` | One line: `WANDB_API_KEY=<your key>` | Log in to wandb.ai → User settings → API keys (use your own key) |

Rules:
- Never paste a key into code, a notebook, an issue, a pull request or a chat message.
- Containers mount this folder read-only (for example `-v ./secrets:/secrets:ro`).
- If a key leaks, tell the team right away and we rotate it.
