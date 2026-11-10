# Architecture docs, decision records, and folder structure

Explain how a project is built, why a decision was made, or how a repo is organised, in plain words a new teammate can follow.

## When this applies

- "Explain the architecture of this project", "write an architecture doc", "write an ADR for choosing Postgres".
- "Explain our folder structure", "write a 'how this repo is organised' section", "what goes where?"
- "Suggest a folder structure for a new Flask app": give it as written advice. Don't create or move files.
- A draft design doc or decision record that sounds stiff or machine written.

Load `lists/buzzwords.md` (the developer section) with this guide. In Claude Code inside a git repo, also load `developer/repo-files.md`.

## What stays the same

- What the system really is. Describe only components, services, data flows, and folders that exist in the code or that the user describes. If something is unclear, say so or ask. Never invent a cache, a queue, a microservice, or a claim about scale or speed ("never slows down", "handles millions of requests").
- Names of services, modules, folders, tables, and tools, exactly as in the code.
- The decision and the reasons the user gives. You can make them clearer, not different.

## Steps

### Architecture doc

1. Look at the real structure: the folder tree, entry points, config, and package files. In Claude Code, list the folders and read the main entry files. Elsewhere, ask for the tree (`tree -L 2` or a screenshot).
2. Start with one paragraph: what the system does and its main parts.
3. Describe each main part in two or three sentences: what it does, what it talks to, where it lives in the repo.
4. Walk through one real request or job from start to finish. This teaches more than a list of boxes.
5. Add a Mermaid diagram only if it helps and the user's platform shows Mermaid (GitHub and GitLab do). Keep it to the parts you described, with the same names.
6. End with known limits or open questions only if the user mentioned them.

### Decision record (ADR)

Use the usual short sections: Title, Status, Context, Decision, Consequences (good and bad). One short paragraph each. Put the real alternatives the user considered in Context. Never add alternatives or numbers they didn't mention.

### Folder structure

1. Show the tree, trimmed to two or three levels, in a code block.
2. Under it, one line per folder that matters: what lives there and when you'd edit it. Skip obvious ones (`.git`, `node_modules`).
3. For a new project, suggest a layout that follows the framework's usual convention, explain each folder in one line, and say it's a suggestion.

## Output

The doc in Markdown, ready to save, then a short change summary. In Claude Code inside a git repo, edit the file in place (see `developer/repo-files.md`). Never move or create code files.

## Example

Before:

> The application leverages a resilient, scalable microservices-based architecture that seamlessly orchestrates data flow across multiple layers.

The repo has a Next.js frontend in `web/`, a FastAPI backend in `api/`, and a Postgres database.

After:

> The app has two parts. `web/` is a Next.js site that shows the dashboard. `api/` is a FastAPI service that the site calls for data, and it stores everything in one Postgres database.

What I changed
- Named the real parts and folders instead of "microservices".
- Removed claims the code doesn't show, like "scalable".
