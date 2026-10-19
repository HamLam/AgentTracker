# AgentTracker

AgentTracker is a project to build a real-time tracker for an AI agent during its runtime. When a user launches an agent, the tracker will let the user see where the agent is working within the system or file structure and what it is currently doing.

## Purpose

Make an agent's activity visible as it happens, so users can follow its work without guessing where it is operating. The tracker should also display the agent's current location when the agent is idle.

## Intended behavior

- **Active agent:** Show the agent's current activity and the location where that activity is happening. For example, when the agent creates files in a directory, display that it is actively creating files in that directory.
- **Idle agent:** Show that the agent is idle and retain its current location within the system or file structure.
- **Real-time updates:** Update the displayed activity and location as the agent moves between locations or changes its runtime state.

## Example

| Agent state | Location | Displayed activity |
| --- | --- | --- |
| Active | `/project/src/` | Creating files |
| Active | `/project/docs/` | Editing a file |
| Idle | `/project/docs/` | Idle; current location retained |

These examples illustrate the intended production experience. A separate proof of concept demonstrates the browser interface with simulated activity.

## Initial scope

The initial goal is to track a user-launched AI agent and present its runtime state, current working location, and ongoing activity. A location may be a directory, a file being worked on, or another identifiable place within the system.

## Project status and layout

The production agent tracker is in planning. The runnable browser prototype
is isolated in `Demo_PoC/`; it is a proof of concept, not the production app.

```text
AgentTracker/
├── README.md
├── .gitignore
└── Demo_PoC/
    ├── README.md             # Setup, backend launch, and browser access
    ├── app.py                # NiceGUI dashboard with simulated activity
    ├── requirements.txt      # Prototype dependencies
    └── discussion-notes.txt  # Design notes and proposed architecture
```

See [Demo_PoC/README.md](Demo_PoC/README.md) for detailed launch instructions.
The demo does not launch or monitor a real AI agent. Live collectors and
persistent activity storage remain future work.

All AgentTracker project files are kept in this repository. A local `.venv/`
at the repository root may be reused to run the prototype; it is ignored
by Git.
