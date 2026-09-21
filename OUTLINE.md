# Goodbye, Tutorial Hell: AI Guides and the New Documentation Layer

**Format:** Sandbox Session, 45 minutes (demo + hands-on)
**Level:** Intermediate (200)
**Audience:** Builders (engineers, developers, maintainers, founders)
**Backup format:** Breakout, 40 minutes
**Assumed setup:** GitHub account, VS Code, GitHub Copilot with agent mode enabled

**One-line thesis:** An MCP server that just wraps your API gives Copilot access. An AI Guide gives Copilot judgment. Judgment is what actually teaches. Access is what gets you a 3am incident.

**Attendee takeaways**
1. How to design an AI Guide (an opinionated, judgment-encoded MCP server) instead of a thin API wrapper.
2. How to structure docs so humans and agents read from one source, without doubling the writing.
3. How to install and adapt the open-source reference implementation in VS Code and Copilot for their own product.

---

## Timing at a glance

| Block | Minutes | Running total |
|---|---|---|
| 0. Pre-session setup | before start | 0 |
| 1. Cold open: tutorial hell | 4 | 4 |
| 2. The API wrapper problem | 4 | 8 |
| 3. How GitHub is enabling building with AI | 4 | 12 |
| 4. Live demo: wrapper vs guide, side by side in VS Code | 7 | 19 |
| 5. What an AI Guide is made of | 6 | 25 |
| 6. Hands-on 1: install and run the reference server in Copilot | 8 | 33 |
| 7. Hands-on 2: encode one piece of judgment | 6 | 39 |
| 8. Dual-consumption docs: one source, two readers | 3 | 42 |
| 9. Close and Q&A | 3 | 45 |

---

## 0. Pre-session setup (before the clock starts)

- Slide up with a QR code and short URL to the reference repo on GitHub. Slide copy: "Yes, this is a workshop. Yes, you have to do something. Start now and you'll look smart later."
- The repo ships a `.vscode/mcp.json` so the server is discoverable the moment the folder opens in VS Code. Setup is: sign in to Copilot, clone, open, click Start on the server. Four steps, and one of them is "click."
- Offer "Open in Codespaces" as the zero-install path. Everything preconfigured, nothing to debug on hotel wifi, which I have personally learned is where confidence goes to die.
- Ask people to start cloning or launching a Codespace while they sit down. This buys back time in block 6 and gives the early arrivals something to do besides judge my slide transitions.

## 1. Cold open: tutorial hell (4 min)

- Open on the shared experience: you followed the tutorial, it worked, you felt like a genius for eleven minutes, and then you tried to do the real thing and had no idea what to change.
- Ask for hands: who has completed a tutorial? Who has completed a tutorial and then built the thing? Watch the second number drop. Say "yeah" and let it sit.
- "Read the docs" is what we tell people when we don't have a teaching plan. It is the polite way of saying you're on your own. It is "good luck" in a nicer font.
- Nobody learns that way. And now we've handed the same pile of docs to Copilot and expected it to do better. It's like tutoring a very fast, very confident student by throwing the textbook at them and leaving the room.
- Set up the promise: by the end of this session you'll have a working MCP server running in Copilot that changes how it behaves, and you'll know how to build one for your own product. If it goes badly, you'll at least have a great story about the time a talk didn't work at Universe.

## 2. The API wrapper problem (4 min)

- What most MCP servers are today: one tool per endpoint, a docstring copied from the API reference, done. Ship it. Tweet about it. Add "AI-native" to the homepage.
- Why that feels like progress and isn't. Copilot now has access, but access was never the bottleneck. **Knowing what to do with it was**. Giving an agent your whole API is giving a teenager the car keys and a map of every road in the country. Technically complete. Emotionally, a disaster.
- Analogy: the fitness version. I have read a lot of fitness blogs. I know what every machine in the gym does. I do not have six-pack abs. Knowing what every endpoint does is not the same as knowing which three to use and why. API wrappers are the fitness blog. Somebody has to be the trainer.
- Symptoms attendees will recognize:
  - Generic advice that could apply to any product, or a houseplant.
  - Brittle output that breaks on the first non-tutorial case, which is also the first case anyone actually has.
  - The agent confidently doing the exact thing your team has a support macro begging customers not to do.
- Name the shift: agents need judgment, not just access. That judgment already exists. It lives in your team's heads, your best docs, and that one Slack thread everyone links to. The question is how to encode it somewhere the agent will actually read.

## 3. How GitHub is enabling building with AI (4 min)

- Frame: while everyone argued about whether AI would replace developers, GitHub quietly built the plumbing for teaching AI how your stuff works. The pieces are already in the editor and the repo. Most people just haven't connected them, because there was no tutorial. Ironic. I know.
- Walk the stack, one slide each, fast:
  - **Copilot agent mode in VS Code.** Copilot went from finishing your sentences to finishing your tickets. It plans, edits across files, runs commands, and calls tools. Tools are where MCP servers plug in, and where this talk lives.
  - **Native MCP support.** VS Code reads `.vscode/mcp.json` in the repo, so a project can ship its own tools to every contributor. The server travels with the code. Nobody has to read a setup wiki page that was last updated by someone who no longer works there.
  - **The GitHub MCP server.** GitHub's own server gives Copilot issues, PRs, Actions, and repo context. It is the reference case for "agent with real context," and quietly the bar for what a first-party server should feel like. If GitHub had shipped a thin wrapper here, this talk would have a different title.
  - **Custom instructions.** `.github/copilot-instructions.md` and path-scoped instruction files let a repo tell Copilot how the team works. This is judgment encoding at the repo level. It is also the first time "read the CONTRIBUTING file" has been an instruction anyone followed.
  - **Copilot coding agent.** Assign an issue, Copilot opens a PR in a GitHub Actions runner. It reads the same instructions and MCP config, so whatever you teach in the editor also teaches the agent working your backlog at 2am. Teach it once, it shows up everywhere. Like a good habit, or glitter.
  - **Codespaces.** One click to a fully configured environment, which is why this workshop has a zero-install path and why I am not currently sweating.
- The point: every one of these is a place to put judgment. Instructions files carry team norms. MCP servers carry product knowledge. GitHub made the sockets. This talk is about what to plug into them, and why most of what's getting plugged in right now is a power strip with nothing attached.
- Transition: so what does it actually look like when you plug in a wrapper versus a guide? Let's find out live, because I enjoy risk.

## 4. Live demo: wrapper vs guide, side by side in VS Code (7 min)

- Two VS Code windows, both in Copilot agent mode, same prompt, two servers. Same model. Same everything. This is a controlled experiment, or the closest thing to one you can run on a conference stage.
  - Left: a thin wrapper that exposes the raw API surface. I built this one in about an hour, which is the point.
  - Right: the AI Guide, the open-source reference implementation. This one took a year, most of it spent deleting things.
- Prompt 1: a realistic beginner ask ("set up X for my project and make it fast").
  - Left gives a plausible, confident, completely generic answer. It's the Stack Overflow answer from 2019 wearing a trench coat.
  - Right asks the one clarifying question that matters, picks the opinionated default, and explains why. Like a senior engineer who's had coffee.
- Prompt 2: a trap. Ask for something the product technically allows but the team recommends against. The thing the docs have a yellow warning box about.
  - Left does it. Cheerfully. With a summary of what it just did.
  - Right pushes back, names the tradeoff, and offers the recommended path. It says no the way a good colleague says no: with a better idea attached.
- Pause on the diff. Same Copilot, same model, same protocol, same access. The only difference is what the server taught the agent. Nothing got smarter. Something got wiser.
- Quick flash of the Copilot tool picker showing the two servers' tool lists. The wrapper has 30 tools that mirror endpoints. The guide has 6 that mirror tasks. One of these is a menu. The other is a recommendation from the chef.
- Plant the question for block 5: what is actually in the right-hand server that makes it behave this way? Spoiler: it's mostly writing. Sorry.

## 5. What an AI Guide is made of (6 min)

- Walk the repo structure on GitHub. Keep it to the parts that carry judgment. Skip the parts that carry a package.json.
- Content patterns that survived production:
  - **Opinionated defaults.** Every tool description says what to do first and what to skip. "It depends" is banned. It always depends. Say what it depends on.
  - **Decision guidance, not option lists.** "Use A when X, use B when Y," instead of a table of everything. A table of everything is how you get an agent that picks C.
  - **Anti-patterns, stated plainly.** The things support tickets are made of, written down where the agent reads them. If your support team has a macro for it, it belongs here.
  - **Worked examples over abstract descriptions.** Short, real, copy-adaptable. Agents, like people, would rather steal a working example than understand a paragraph.
  - **Scoped tools.** Fewer, task-shaped tools beat one tool per endpoint. Six good tools is a toolbox. Thirty is a garage sale.
- Patterns I had to throw out, with love:
  - Mirroring the API reference one-to-one. Copilot already knows how to read a reference. You are not adding information, you are adding a middleman.
  - Marketing language. It reads as noise to an agent and eats context. No model has ever made a better decision because something was "blazing fast."
  - Long prose blocks. Agents skim too. Structure wins. Every model is a busy reader with a short attention span. Write for the person you are in your inbox.
- Where this sits next to GitHub's own layers: instructions files are for how *your team* works, the AI Guide is for how *the product* is meant to be used. They compose. House rules versus the instruction manual. The reference repo ships both so attendees can see the split instead of taking my word for it.
- Guardrails angle (secondary theme): VS Code asks for confirmation on tool calls, servers are scoped to what you expose, and every call is visible in the chat. Designing the guide well is also designing the guardrails. Opinionated defaults are seatbelts you don't have to remember to fasten.

## 6. Hands-on 1: install and run the reference server in Copilot (8 min)

- Goal: every attendee has the reference server running in Copilot agent mode. This is the part where it stops being my talk and starts being your afternoon.
- Steps on screen, also in the repo README:
  1. Clone the repo, or open it in Codespaces (most people did this in block 0, and the rest of you are about to find out why I asked).
  2. Open the folder in VS Code. VS Code detects `.vscode/mcp.json` and offers to start the server. Click Start. Yes, that's it. Yes, it's suspicious. No, there's no catch.
  3. Open Copilot Chat, switch to Agent mode, open the tool picker, confirm the guide's tools are listed. If you see six tools, you're done. If you see thirty, you've opened the wrong folder and also proven my point.
  4. Run demo prompt 1 from block 4 and compare with what they saw on screen.
- While people work: walk the room, surface common failures on the mic (Copilot not signed in, agent mode not enabled, server not started, trust prompt dismissed by reflex because we all dismiss every dialog by reflex).
- Fallback: Codespaces link on the slide the whole time. Nobody should sit idle. Idle people start checking Slack, and then I've lost you to your own backlog.
- Checkpoint: hands up when Copilot gives the opinionated answer. Small cheer. We've earned it.

## 7. Hands-on 2: encode one piece of judgment (6 min)

- Goal: attendees make one change that visibly alters Copilot's behavior, so they leave knowing the loop. Not knowing about the loop. Knowing the loop.
- Exercise: pick one tool in the reference server and add an anti-pattern or a "prefer this, not that" rule that reflects something they believe about their own stack. Something you'd say in a code review with feeling.
  - Template provided in the repo under a clearly named exercise file. It is called something like EXERCISE.md, because I am not going to make you hunt for it after everything we've been through together.
  - Show one example live: edit the rule, restart the server from the VS Code MCP panel, re-run the trap prompt, watch Copilot change its mind. This is the moment. If you remember one thing from today, make it this.
- Prompt attendees to think about their own product: what is the one thing your support team says every week? The thing they have a macro for. The thing they say in their sleep. Write that down as the rule. Congratulations, you just started your AI Guide.
- Stretch: put the same rule in `.github/copilot-instructions.md` instead and compare. Where does it belong? This is the house-rules-versus-manual split from block 5 made concrete, and it's a great argument to have with a coworker later.
- Share-out: two or three people say what rule they added and what changed. Fast, no slides. Bonus points for anyone whose rule is clearly about a specific person on their team.

## 8. Dual-consumption docs: one source, two readers (3 min)

- The maintenance objection: "I don't want to write docs twice." Correct. You barely want to write them once. Nobody's judging.
- Show the content design diagram: one source of structured guidance, rendered for humans as docs pages and served to Copilot through the MCP server. Same words, two audiences, one place to fix the typo.
- What makes it work:
  - Structure is the shared layer (headings, decision blocks, examples). Prose is the human layer, where you get to have a personality.
  - Judgment lives in the structure, so both readers get it. The agent skips your jokes. It does not skip your decision blocks.
  - Docs review becomes agent-behavior review. When the docs PR merges, the agent improves. Copilot code review on that PR is, in a very real sense, reviewing its own future personality. Try not to think about that too hard.
- Concrete starting point: begin with your top five support questions, encode those, ship, measure, expand. Do not start by documenting everything. That's how you end up back in the fitness blog.

## 9. Close and Q&A (3 min)

- Bring it back: tutorial hell was never a content-volume problem. We have never had more docs. It was a judgment problem. Agents have the exact same problem, and GitHub has built the layer where we can fix it once for both of them.
- Thesis restated: AI Guides will replace API wrappers. MCP is in VS Code, Copilot reads it, and the repo can ship it. The difference between a wrapper and a guide is now obvious to anyone who runs the side-by-side. Which you just did. So you're stuck knowing this now.
- Leave-behinds on the final slide:
  - Reference repo (with `.vscode/mcp.json`, instructions file, and exercise template)
  - Open in Codespaces link
  - Published long-form post, for people who like their arguments with more paragraphs
  - Where to send feedback and PRs. Especially PRs. Especially the ones that delete things.
- Q&A. Seed question if the room is quiet: "How do you keep the guide honest as the product changes?" Backup seed: "What's the worst thing an agent has confidently done to you?" That one always gets hands.

---

# Demo design: the "wrapper twin"

The wrapper twin is the control group for the demo. It's a second MCP server, deliberately built the way most MCP servers get built today, so the room can see the AI Guide's behavior next to something familiar rather than in isolation.

## What a wrapper looks like

Take an API. For every endpoint, write one MCP tool. Copy the endpoint's description from the API reference into the tool description. Pass the parameters straight through. Return the raw response. Done.

If your recipe API has `GET /recipes/{id}`, `GET /recipes/search`, `GET /ingredients/{id}/substitutes`, and `POST /recipes/{id}/scale`, the wrapper has four tools named exactly that, described exactly that, doing exactly that.

This is how most MCP servers in the wild are built right now, and it's not because people are lazy. It's because it feels complete. Every capability of the API is exposed. Nothing is missing. You can generate it from an OpenAPI spec in an afternoon, and a lot of people do.

## Why it's a poor MCP server anyway

The agent now has access to everything and guidance about nothing. It has to figure out, at prompt time, from a beginner's question, which of your tools matters, in what order, with what defaults, and what not to do. That's the exact judgment a new user lacks too. You've given a confused person a confused assistant.

Concretely, the wrapper fails in three predictable ways:

- **It picks the wrong tool.** Thirty equally described tools means the agent guesses from the names. "Make this recipe bigger" might hit `scale`, might hit `search`, might do both.
- **It does what's asked instead of what's meant.** "Double everything" calls `scale` with a factor of two. The API happily complies. Nowhere in the tool description does it say leavening doesn't scale linearly, because the API reference never said that either. That knowledge lived in a blog post, or a support ticket, or a cook's head.
- **It never pushes back.** There is no place in a wrapper for "you probably don't want to do that." The API doesn't have an opinion, so the tool doesn't, so the agent doesn't.

## Why you build one on purpose

Because the guide's behavior doesn't look impressive by itself. If you only show the AI Guide correctly refusing to double the baking soda, the room thinks "sure, the model is smart." When the wrapper sits next to it, running the same model on the same prompt and cheerfully ruining the cake, the room sees that the model isn't the variable. The server is. Same Copilot, same access, different judgment.

It also makes the "patterns I threw out" section in block 5 land. You're not describing a hypothetical bad server. You're pointing at one.

## How to build the twin well

Build it honestly. Don't sabotage it. It should be exactly what a competent engineer would ship if they were told "make an MCP server for our API" and had an afternoon. Accurate tool descriptions, working calls, nothing broken. Its failure has to come from what it lacks, not from bugs you planted. If someone in the room could look at the code and say "well, that's just badly written," you've lost the argument. They should look at it and say "that's how I would have built it," and then feel the floor shift a little.

The clean version of the point: a wrapper answers "what can the agent do." A guide answers "what should the agent do." Most MCP servers today only answer the first question, and that's the gap the talk is about.

## Candidate demo domains

| Domain | Wrapper does | Guide does | Trap prompt | Notes |
|---|---|---|---|---|
| Jeopardy training | Serves clues, checks answers | Coaches wagering math, category strategy, "form of a question" | "I'm behind going into Final Jeopardy, bet it all" | Everyone knows the format. Exercise rule is easy. Slightly toy-ish for a 200 room. |
| Recipe / meal planning | Recipe lookup, substitutes, scaling | Substitutions that work, scaling rules, pan care | "Double this baking recipe by doubling everything" | Biggest laugh when the wrapper ruins dinner. Maps cleanly to "docs with opinions." |
| Git workflow coach | GitHub API surface | Team git culture: rebase vs squash, PR hygiene | "Just force push it" | On-theme at Universe. Sits right next to GitHub's own MCP server, which is awkward. |
| Postgres tuning | `run_query`, `explain`, `list_indexes` | DBA judgment: index selection, pooling, no `SELECT *` | "Add an index on every column to make it fast" | Closest to the production version. Best as the reveal, not the workshop server. |
| Board game referee (Monopoly) | Returns rules text | Adjudicates the rules as intended | "We landed on Free Parking, give me the pot" | Dark horse. Rules-as-written vs rules-as-intended is the whole talk in one metaphor. |
| Houseplant care | Plant database | A person who has killed many plants | "My fern looks sad, water it more" | Low stakes, very recognizable failure mode. |

**Current lean:** run the workshop on Jeopardy or recipes, use the Postgres guide as the "here's what this looks like in production" reveal in block 5 or the close. Whichever domain, the wrapper's failure in the trap prompt should be funny rather than subtle. Confidently ruining a cake beats confidently choosing a suboptimal index.

---

# What needs to be built

Everything below lives in one public GitHub repo unless noted. The repo is the leave-behind, so it has to work on a clean machine with nothing but VS Code and Copilot.

## 1. The backing API (or fake of one)

- A small local service the two MCP servers both talk to, so the comparison is fair. For a toy domain this can be a JSON file and a few functions, no network.
- Must expose enough surface that the wrapper has visibly "too many" tools (target: 20 to 30 endpoints) and the guide can collapse them into 5 or 6 tasks.
- Deterministic responses. No randomness on stage.

## 2. The wrapper twin server

- One MCP tool per endpoint, descriptions lifted verbatim from the API's own docstrings, parameters passed straight through.
- Ideally generated from an OpenAPI spec so I can say "this took an afternoon" and mean it.
- Working, tested, no planted bugs. Its only flaw is having no opinions.
- Lives in its own folder with its own `.vscode/mcp.json` so it can be opened as a separate VS Code window for the split-screen demo.

## 3. The AI Guide server

- 5 or 6 task-shaped tools. Each description carries: the opinionated default, when to use it vs its sibling, the anti-pattern, one worked example.
- Must refuse or redirect on the trap prompt with a stated tradeoff and a recommended path.
- Structured guidance lives in a content directory the server reads at startup, not hardcoded in the tool definitions, so block 7's exercise is an edit to a markdown or YAML file and a server restart.
- Same `.vscode/mcp.json` pattern so VS Code auto-detects it on folder open.

## 4. Repo-level files

- `.vscode/mcp.json` at the root pointing at the guide server, with the wrapper commented out and labeled.
- `.github/copilot-instructions.md` with a short, real set of team norms, so block 5's "house rules vs instruction manual" split is visible in the repo and block 7's stretch exercise has a target.
- `EXERCISE.md` with the block 7 template: where the rule file is, the format of a rule, one filled-in example, and the trap prompt to re-run.
- `README.md` with the four-step install, the Codespaces button, the two demo prompts, and troubleshooting for the failures I expect (not signed in, agent mode off, server not started, trust prompt dismissed).
- `.devcontainer/devcontainer.json` so the Codespaces path installs dependencies and starts nothing extra.

## 5. Demo assets

- Three rehearsed prompts: the beginner ask, the trap, and one spare. Written down and taped to the laptop.
- A "reset" script that returns both servers and the fake API to a known state between runs.
- Screenshot fallbacks of both panes for every prompt, in case the wifi or Copilot has opinions of its own.
- The Copilot tool picker screenshot showing 30 tools vs 6, for the flash in block 4.

## 6. Slides

- Block 0 QR slide (repo, Codespaces link, "start now" copy).
- Block 3 stack walk: six slides, one per GitHub piece, minimal text.
- Block 5 repo structure slide highlighting the content directory.
- Block 8 content design diagram: one source, two renderers (docs site and MCP).
- Final leave-behinds slide with the same QR code as block 0.
- A timer I can see.

## 7. The production reveal (optional, block 5 or close)

- A link and a 30-second screen recording of the real Postgres AI Guide doing the same wrapper-vs-guide split on a real question.
- Kept separate from the workshop repo so the workshop stays vendor-neutral.

## Build order

1. Fake API and content directory first. Everything else depends on the domain being locked.
2. Guide server, until the trap prompt reliably redirects.
3. Wrapper server, generated, until the trap prompt reliably fails in a funny way.
4. Repo files and Codespaces. Test on a machine that has never seen the repo.
5. EXERCISE.md, then run block 7 on a coworker who wasn't in the room for any of this.
6. Slides last. They're the least likely to break.
