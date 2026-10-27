# Goodbye, Tutorial Hell: AI Guides and the New Documentation Layer

**Erin Mikail Staples & Janice Niemeir · 45 minutes**  
**Format:** Sandbox session with a working scaffold and attendee exercises.  
**Audience:** Intermediate developers, maintainers, and product teams; setup instructions assume no prior experience with this workshop.  
**Source:** [OUTLINE.md](OUTLINE.md). The spoken script below expands all seven sections of that outline, including its teaching points, exercises, and closing questions.  
**Voice and conversational cues:** Erin's [MCP for EDU notes](</Users/erinmikail/Documents/HQ/30-39-Blog/2025-10-24-MCP-for-EDU.md>) supply the learning-through-play, reflection, and curiosity callbacks; the related [Universe speaker notes](</Users/erinmikail/Documents/HQ/20-29-Work/20.02-Conferences/2026-GitHub-Universe/2026-GitHub-Universe-Talk-Outline.md>) supply the tutorial, fitness-blog, and documentation jokes. These are adapted into the current workshop script.  
**Acceptance criterion:** An attendee can trace a recommendation to guidance they edited, observe its effect in their editor, and adapt that pattern to their own product.

## The learning environment and its principles

The learning environment is the whole setting in which someone practices: their editor, the problem they are working on, the data and documentation available to them, the actions they can take, and the feedback they receive. In this workshop, that setting is a local project with synthetic trivia data, an assistant connected to MCP tools, and guidance files the learner can inspect and edit. The learner makes a prediction, changes one recommendation, and checks the resulting behavior.

We design that environment around a decision the learner can explain. A small working example keeps the consequences visible. Source rules and tool results provide evidence for discussion. A changed request gives the learner a chance to decide whether the original recommendation still applies. The human remains responsible for explaining the choice, even when the assistant supplies an answer.

| Principle | What it means in this workshop |
|---|---|
| Context fits the learner's task | Start with a practice request or product decision, and provide the guidance relevant to it. Ask when a missing fact would change the advice. |
| Reasoning is inspectable | Show the recommendation's reason, source rule, and conditions. Let the learner compare those with the actual tool result. |
| Practice has clear boundaries | Use bundled synthetic data and a reversible local content edit. The deployment example supplies advice and performs no deployment. |
| Work can be revisited | Record the prompt, configuration, loaded content revision, and result. Repeat the task with the same inputs while allowing for variation in the model's wording. |
| Personalization and responsible access require design | Use the context the learner chooses to share. Define and enforce access boundaries in the application and connected services. Evaluate whether the guidance fits the learner's goal. |

These are the practical meanings of the supplied slides' “personalized,” “reproducible,” and “ethical by design” principles. They describe commitments we implement and evaluate in a learning environment.

## The learning theory behind the environment

The first concern is the learner's attention. Sweller's cognitive-load account explains how demanding problem-solving activity can consume capacity needed for acquiring reusable knowledge. Our design response is to keep infrastructure setup separate from the first content decision, show a worked example, and change one value at a time. These are applications of the theory to this workshop. [Sweller, *Cognitive Load During Problem Solving* (1988)](https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1202_4).

The second concern is making expert judgment available for practice. Cognitive apprenticeship asks teachers to expose their reasoning, support learners as they attempt the work, and gradually reduce that support. Here, the presenter models a decision and the guidance exposes its rationale. Attendees then explain the exception and adapt the pattern to their own product. [Collins, Brown, and Holum, *Cognitive Apprenticeship* (1991)](https://www.aft.org/ae/winter1991/collins_brown_holum).

Participation matters too. Situated learning emphasizes learning through participation in a community's practices. This workshop borrows that lens by placing decisions in a working project and asking attendees to discuss their reasoning with a neighbor. Experiential learning supplies another lens: an experience becomes material for reflection, an explanation, and another experiment. Our sequence is to request, inspect, explain, and try a changed scenario. [Lave and Wenger, *Situated Learning* (1991)](https://www.cambridge.org/highereducation/books/situated-learning/6915ABD21C8E4619F750A4D4ACA616CD), [Kolb, Boyatzis, and Mainemelis, *Experiential Learning Theory*](https://learningfromexperience.com/downloads/research-library/experiential-learning-theory.pdf).

Finally, the learner needs to do some of the thinking. Chi and colleagues studied how learners' own explanations connected worked examples to underlying principles. That motivates asking attendees why a rule applies instead of accepting the assistant's explanation as proof of understanding. Retrieval-practice research also motivates giving someone a chance to attempt a clue before revealing the answer; the cited experiments concern later retention, while this workshop provides a brief opportunity to practice that activity. [Chi and colleagues, *Self-Explanations* (1989)](https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog1302_1), [Roediger and Karpicke, *Test-Enhanced Learning* (2006)](https://pubmed.ncbi.nlm.nih.gov/16507066/).

Together, these frameworks explain our teaching choices. Whether an MCP-based guide improves learning still needs evaluation with learners. A successful connection, a correct server result, and an attendee's ability to apply the reasoning are separate observations.

## Introduction — the topic and why it matters

Developer education helps people understand a tool well enough to use it in their own work. Tutorials and reference documentation are part of that: they explain concepts, demonstrate a first success, and describe the available operations. The harder step comes when a developer's project differs from the example. They need to choose an approach, understand its tradeoffs, and recognize when the recommendation should change.

That is the problem behind **AI guides and the new documentation layer**. When developers ask an assistant for help in their editor, the assistant needs access to the product team's reasoning as well as its API. Model Context Protocol (MCP) provides a way for an assistant to access tools and context from a server. We can use that connection to supply documented recommendations, their rationale, their exceptions, and questions to ask before proceeding.

MCP is an open standard for connecting AI applications to external capabilities and information. A host application, such as VS Code, uses an MCP client to communicate with a server. The server advertises what it offers, and the application can request information or invoke its tools. This brings selected external context into the task without retraining the underlying model. [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro), [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture).

Documentation teams already use this connection to deliver content where developers work. Microsoft Learn offers documentation and code-sample retrieval; Mintlify supplies search and content retrieval for hosted documentation; Stripe combines knowledge-base search with product tools. pg-aiguide adds a useful reference for this workshop: version-aware documentation alongside curated database guidance. These examples show several ways to publish expertise through an agent-accessible interface. [Microsoft Learn MCP](https://learn.microsoft.com/en-us/training/support/mcp), [Mintlify search MCP](https://www.mintlify.com/docs/ai/model-context-protocol), [Stripe MCP](https://docs.stripe.com/mcp), [reviewed pg-aiguide implementation](https://github.com/timescale/pg-aiguide/tree/5d3b76b5c986693b30753828b404aa66ba34c31a).

This matters because a working example does not necessarily teach someone how to make the next decision. Without that reasoning, a developer can copy a solution without knowing whether it fits, while maintainers explain the same choices again in support and code review. Making guidance available during the task gives the developer a chance to understand the recommendation, inspect its source, and apply it to a different situation.

In this workshop, we will build and inspect that connection. A small trivia application makes the first decisions visible; a deployment-advice example shows how the pattern transfers to a product workflow. The learning goal is to explain why a recommendation applies and what would change it. The opening talk track in Part 1 introduces this context before the first demo.

**How to use this run sheet:** Complete presenter setup before the 45-minute session. Each numbered 🖥️ screen cue starts a new slide or live-demo view. Under that heading, follow the actions and read the matching 🎤 talk track. Screen numbers identify cue order in this run sheet, including setup views; they are not final deck slide numbers. Keep slides to the short text or visual described in each cue. During demos, zoom into the fields being discussed.

| Cue | Meaning |
|---|---|
| 🖥️ Screen / slide | What the audience sees; each heading starts the next screen cue |
| 🎤 Talk track / transition | Words to say aloud |
| ⌨️ Terminal / file edit | Text to type, with the destination named explicitly |
| 💬 Copilot Chat | Prompt to paste into the chat input |
| 🖱️ Do | Clicks, navigation, and presenter actions |
| ✅ Checkpoint / expected output | Evidence that the step worked |
| 🛠️ Troubleshooting | A symptom and a recovery action |
| 📝 Presenter note / context | Background for the speaker |
| ⏱️ Pacing | Timing and optional cuts |
| 🔗 Files / source note | Reference material |
| 🙋 Ask the room | Audience participation |

**🧭 Quick navigation:** [Start both demo servers](#comparison-startup) · [Begin the live comparison](#live-comparison) · [pg-aiguide in daily work](#pg-aiguide-daily)

**🔗 Supplied slide references:** The linked images in [assets/slide-references](assets/slide-references/) preserve Erin's supplied slides and any visible presenter notes. Present the slide canvas, keeping the screenshot's notes panel off the audience screen. The cues below place the slides in the talk or use their information in the relevant notes. Broader classroom and product examples describe designs teams can build; the live workshop demonstrates the specific capabilities documented here.

<a id="comparison-startup"></a>

<details>
<summary>🛠️ Presenter setup: install, start both MCP servers, and troubleshoot</summary>

### 🛠️ Install, open both windows, and start the servers

**📝 Presenter note:** Prepare both servers before the session. The seven-minute comparison begins with working connections. Attendees only need Window B for their exercise.

**🖱️ Do — 1. Open Window B at the repository root:** In VS Code, choose **File → Open Folder…** and select the folder containing `README.md`, `UNIVERSE-OUTLINE.md`, and `JSON-API-MCP`. In this checkout that folder is `Github-Universe-26`; your fork may have another name. Keep this window open.

**⌨️ Terminal — Window B, repository root:** Choose **Terminal → New Terminal**. Run each line separately and wait for it to finish:

```bash
uv sync --locked --directory JSON-API-MCP
uv run --locked --directory JSON-API-MCP python scripts/check_setup.py
```

**✅ Expected terminal output:**

```text
setup ready: 6 clues, synthetic-workshop-v1
```

**✅ Checkpoint:** This confirms dependencies and clue data. The MCP server still needs to be started through VS Code in step 3.

**🖱️ Do — 2. Open Window A at the nested project:** Choose **File → New Window**, then **File → Open Folder…** and select the `JSON-API-MCP` folder inside the same checkout. Its Explorer should show `pyproject.toml`, `src`, `content`, and `data` at the top level. These windows share files and the installed environment.

| Check | Window A: wrapper | Window B: guide |
|---|---|---|
| Folder open in Explorer | `JSON-API-MCP` | Outer repository folder |
| Configuration loaded | `JSON-API-MCP/.vscode/mcp.json` | `.vscode/mcp.json` |
| Server to start | `jeopardy-basics` | `education-guide` |
| Launcher mode | `--server wrapper` | `--server guide` |
| Tools to select | `search_clues`, `get_clue`, `list_categories` | `get_guidance`, `build_practice_set`, `reveal_answer`, `recommend_deployment` |

**🖱️ Do — 3. Start the Jeopardy wrapper in Window A:**

1. Click inside **Window A**, the one whose top folder is `JSON-API-MCP`.
2. Press **Cmd+Shift+P** on Mac or **Ctrl+Shift+P** on Windows/Linux.
3. Type **MCP: List Servers** into the Command Palette and select the command. This is a VS Code action, not a terminal command.
4. Select **jeopardy-basics**, then **Start Server**. Accept the trust prompt for this workshop server if shown.
5. Wait for the server to report running. Confirm that its three tools appear in the tool list.

**🖱️ Do — 4. Start the guide in Window B:** Click inside the outer repository window. Repeat **Command Palette → MCP: List Servers → education-guide → Start Server**. Confirm its four tools appear. If a server is disabled, enable it first. If **Restart Server** is unavailable later, use **Stop Server** followed by **Start Server**.

**📝 Presenter note — what starts:** Each checked-in configuration launches Python through uv. The launcher starts its own clue API on a private loopback port, then runs the MCP server over stdio. VS Code owns that connection. You can use the tools in Chat once discovery finishes; there is no browser page to open and no separate FastAPI command to run.

**🖱️ Do — 5. Prepare Copilot in each window:** Open **View → Chat**, sign in if needed, and select **Agent** mode. Choose the same specific named model in both windows. In **Configure Tools**, deselect other optional tools and enable only the row's server tools. If your VS Code uses the Copilot harness and has no Configure Tools button, run **Chat: Open Customizations → Tools** to manage tool availability. Recheck the active selection whenever switching windows because it can persist in the profile.

**💬 Copilot Chat — optional preflight in Window A:**

```text
Call list_categories from jeopardy-basics and show the returned categories. Do not read or edit workspace files.
```

**💬 Copilot Chat — optional preflight in Window B:**

```text
Call get_guidance from education-guide for the practice task. Show its source and practice.default_count rule. Do not read or edit workspace files.
```

**✅ Checkpoint — ready to compare:** You can expand a real tool call from each server. The guide's starting `practice.default_count` is `2`. Open **New Chat** in both windows after preflight so those messages do not influence the comparison. Confirm the same model and the assigned tools once more.

**🛠️ Troubleshooting — getting connected:**

| Where someone gets lost | What to check or do |
|---|---|
| Only `education-guide` appears when looking for Jeopardy | You're in the outer folder. Open `JSON-API-MCP` in Window A to load `jeopardy-basics`. |
| Only the three clue tools appear when looking for guidance | You're in Window A. Switch to the outer repository window and start `education-guide`. |
| `uv: command not found` in the terminal | Install uv using the README prerequisite link, reopen VS Code, and rerun setup. |
| uv works in the terminal but VS Code cannot launch it | ⌨️ In the terminal, run `which uv` on macOS/Linux or `where.exe uv` on Windows. Use that absolute executable path for `command` in the affected window's MCP config, then restart its server. |
| The command cannot find `JSON-API-MCP` | The setup commands above run in Window B's outer repository terminal. A terminal in Window A already starts inside `JSON-API-MCP`. |
| The setup check succeeds, but no tools appear | The check only loads data. Start the relevant MCP server through the Command Palette, then check the tool picker. |
| A server starts and then errors | Select its **Show Output** action and read the first error. Check dependency installation, executable path, and the active config before retrying. |
| Server or chat controls are unavailable | Check workspace trust, Copilot sign-in, Agent mode, and whether MCP is disabled by editor or organization settings. Use the current VS Code server controls linked below if the UI differs. |
| No Configure Tools button appears | For the Copilot harness, use **Chat: Open Customizations → Tools**. For a Local harness session, use **Configure Tools** in Chat. |
| The agent answers without calling the demo tools | Check the enabled tools, then explicitly ask it to use the intended server. Treat a response without a tool call as an unverified comparison result. |
| The wrapper calls the guide, or the agent reads project files | Reselect the assigned tools and start a new chat. Inspect the actual call names before comparing results. |
| Someone looks for a localhost website | This is a stdio MCP server. Interact through Copilot's tools. Its private API port is managed by the launcher. |

**🔗 Source note — editor controls:** [VS Code server management](https://code.visualstudio.com/docs/agents/run/manage-mcp-servers) documents start, stop, restart, and output controls. [VS Code tool selection](https://code.visualstudio.com/docs/agents/run/tools) describes the Local and Copilot harness interfaces. The repository's [editor smoke record](evidence/editor-smoke.md) identifies the observed setup; UI labels can vary by version.

**🛠️ Troubleshooting — terminal-only startup diagnostic, outside the timed demo:** If the editor reports a Python startup error, run just the affected launcher from Window B's **repository-root terminal** to see the error directly.

**⌨️ Terminal — diagnose the wrapper:**

```bash
uv run --locked --directory JSON-API-MCP python -m jeopardy_template.launcher --server wrapper
```

**⌨️ Terminal — diagnose the guide instead:**

```bash
uv run --locked --directory JSON-API-MCP python -m jeopardy_template.launcher --server guide
```

**✅ Expected terminal behavior:** A healthy stdio launcher may sit waiting for an MCP host. That is not a chat prompt or a browser server. Press **Ctrl+C** to stop this diagnostic, then start the server from VS Code. A separately launched terminal process is not the connection Copilot uses.

**🖱️ Do — 6. Check or reset the presenter defaults:**

In the Explorer sidebar, expand `JSON-API-MCP → content`, then click `practice.json`. Press **Cmd+F** / **Ctrl+F**, search for `practice.default_count`, and check that the `value` in that rule is `2`. Open `deployment.json`, search for `deployment.default_environment`, and check that its `value` is `"preview"`. These are the defaults used when the request omits a count or deployment target. If you are resetting your presenter copy after rehearsal, change only those values and save with **Cmd+S** / **Ctrl+S**; preserve attendee customizations. After any reset, run this in Window B's root terminal:

**⌨️ Terminal — repository root (Window B):**

```bash
uv run --locked --directory JSON-API-MCP python scripts/render_guidance.py
```

Then reopen the Command Palette, run **MCP: List Servers**, select `education-guide`, and choose **Restart Server** so it loads the saved rules. You are ready when both servers run, the correct tools are selected, and the starting values are `2` and `preview`.

### 🖥️ Screen 01 — setup comparison

**🖥️ On screen:** Show the two VS Code windows with visible labels: “A: API wrapper” and “B: Education guide.” Keep the server name visible in each window and the shared dataset noted beneath them.

**🎤 Talk track while people set up:** “We have two windows using the same clue data. One server exposes operations; the other adds guidance for a practice experience. The model and prompt will stay the same. We will inspect the tools' results so we can see where each recommendation came from.”

</details>

## Before the session: welcome and presenter preparation

### 🖥️ Screen 02 — arrival

**🖥️ On screen:** Show the session title, both speakers' names, and the repository URL with a QR code to its quickstart. Add one instruction: “Fork the repo and open the README.” Leave this up while people arrive.

**🖱️ Do:** Put the [repository](https://github.com/erinmikailstaples/MCPs-for-EDU) and [quickstart](README.md#start-in-your-editor) on screen as people arrive. Invite them to fork and clone, or create a Codespace from their fork. Follow the setup above for the local demo. Use [DEMO.md](DEMO.md) to record the model, editor settings, prompts, and observed results. Prepare screenshots or a recording from an actual verified run and identify it as recorded if used.

**🎤 Talk track — say while people arrive:**

> Welcome! We're Erin Mikail Staples and Janice Niemeir. Today we're going to look at how a server can bring product guidance into the editor while you're working. You'll fork a working scaffold, run it in your editor, change a documented recommendation, and see what happens.
>
> Yes, this is a workshop. Yes, you have to do something. Start now and you'll look smart later. It also gives the early arrivals something to do besides judge my slide transitions.
>
> The repository link and setup instructions are on screen. A fork gives you your own copy on GitHub; cloning downloads that copy to your computer. You can also create a Codespace from your fork. Start setting up now if you'd like. We'll have a dedicated installation checkpoint during the session.
>
> You don't need to understand every Python file to complete the first exercise. The change we'll make is in a content file. Keep the README open, and use the beginner setup instructions in this run sheet if MCP or the two-window setup is new to you.

**📝 Presenter note:** The timing below includes demonstrations, attendee work, and questions. Pause at the indicated checkpoints rather than reading the whole script without interaction. The local installation and Codespaces paths have different validation status; consult [verification status](evidence/README.md) before rehearsal.

## 1. 00:00–09:00 — Learning environment, MCP foundations, and session promise

### 🖥️ Screen 03 — opening hook

**🖥️ On screen:** Show a crowded browser with tutorial tabs and two video windows. Use the large caption “12 tabs. 2 videos. 1 existential crisis.” Include a Kubernetes tab for the laptop-fan line. Hold this slide through the show of hands.

**🖱️ Do:** Begin with the opening hook below and pause for raised hands. Advance through the contextual AI and MCP slides as those ideas enter the talk.

**🎤 Talk track — opening hook:**

> Raise your hand if your ‘learning journey’ starts with 12 tabs, two YouTube videos, and a mild existential crisis.
>
> We’ve all been there — trying to learn Kubernetes while your laptop’s fan sounds like it’s preparing for takeoff.

**📝 Speaker cue:** After the show of hands, pause and acknowledge the room. Let the laptop-fan joke land before advancing to contextual AI.

### 🖥️ Screen 04 — contextual AI

**🖥️ On screen:** Replace the busy browser with a simple view of an editor beside a learner's current task, project constraints, and relevant guidance. On-slide text: “AI needs context about how we're learning.”

**🎤 Talk track — contextual AI:**

> We all think we want smarter AI, but what we really need is contextual AI — systems that understand our learning environment.

### 🖥️ Screen 05 — learning environment principles

**🖥️ On screen:** Show the supplied [learning environment principles slide](assets/slide-references/learning-environment-principles.png), highlighting “personalized,” “reproducible,” and “ethical by design.” Present these as design commitments for the environment being built. Use it to define the learning environment before introducing the protocol.

**🎤 Talk track — learning environment principles:**

> By learning environment, I mean the whole setting: your editor, the task you face, the data and guidance you can use, and the actions available to you. We get to design those conditions.
>
> Personalized means the task and guidance fit the learner's goals and the workspace context they've chosen to share. Reproducible means another person can inspect the setup, source rules, and recorded steps. The model may still phrase its answer differently.
>
> Ethical by design means deliberately choosing data boundaries and enforcing access controls, including how you handle private work and intellectual property. Those are responsibilities for the product we build. MCP gives us a connection through which that design can operate.

**📝 Presenter context — design goals:** The supplied slide's “by default” language expresses the intended learning environment. In this workshop, point to the synthetic fixture, explicit tool selection, source revisions, local edits, and advice-only deployment tool as concrete choices. Personalization, repeatable records, and privacy protections each need their own design and evaluation.

### 🖥️ Screen 06 — MCP introduction

**🖥️ On screen:** Show “Enter MCP” with “Model Context Protocol” underneath. Use a simple connection diagram linking an editor assistant to a server supplying tools and product guidance. Keep this diagram visible while explaining how guidance reaches the task.

**🎤 Talk track — MCP introduction:**

> Enter MCP.
>
> Model Context Protocol connects an assistant to tools and context supplied by a server. For developer education, that gives us a place to bring the product team's reasoning into the task: what to try, why it fits, and when to choose something else.

> A protocol is an agreed way for programs to communicate. The application you're using is the host. It creates a client connection to an MCP server, which is a program offering particular capabilities. In our demo, VS Code is the host and our Python program is the server. The assistant's model works with the information the application makes available.

**🔗 Source note — architecture:** The official [MCP architecture overview](https://modelcontextprotocol.io/docs/learn/architecture) defines the host, client, and server roles. The server can run locally or remotely; this workshop's configurations launch local stdio servers. The host manages how returned information enters the model's context.

### 🖥️ Screen 07 — one MCP interaction

**🖥️ On screen:** Show a simple sequence: the user's request in VS Code; the available tool names and descriptions; a call to `get_guidance` for `practice`; the returned rule and rationale; the assistant's explanation. Label the local connection “stdio.” Keep the model inside the host application's workflow and the clue API behind our server.

**🎤 Talk track — one MCP interaction:**

> When we connect, the application can discover the server's tools and their expected inputs. When we ask for a practice round, the assistant can request practice guidance, then call the tool that builds the round. The application receives the results and the assistant uses them in its response.
>
> That is how a rule from this project becomes relevant to an answer in Chat. We aren't training a new model when we edit the rule. We're changing information and behavior the running application can access during a task.

**📝 Presenter depth — the three server building blocks:**

| MCP building block | Plain-language explanation | Documentation example |
|---|---|---|
| Tools | Functions the application can invoke, with descriptions and input schemas | Search a documentation collection or retrieve task guidance |
| Resources | Addressable information a client can read | A reference document or schema exposed by the server |
| Prompts | Reusable interaction templates a client can obtain | A prepared review or troubleshooting workflow |

**🎤 Talk track — the building blocks:**

> Servers can offer tools to call, resources to read, and reusable prompt templates. This workshop uses tools, including one that returns documentation. A tool can return text as well as perform an operation. Your documentation server can choose the interface that fits its users' tasks.

**🔗 Source note — protocol features:** See [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts). Our `get_guidance` function is a tool returning guidance; the Markdown files in this repository do not automatically become MCP resources. Remote documentation servers can use Streamable HTTP, while our local launcher communicates with its host through standard input and output.

### 🖥️ Screen 08 — documentation through MCP today

**🖥️ On screen:** Use a plain table titled “Documentation in the developer's workflow.” Show Microsoft Learn, Mintlify, Stripe, and pg-aiguide with the capabilities below. Under the table, show the task sequence “Find the relevant source, read it, apply it, check the result.”

| Example | Documented use of MCP | Teaching opportunity for our workshop |
|---|---|---|
| Microsoft Learn | Search documentation, fetch full articles, and find code samples | Bring official reference material into the current task |
| Mintlify | Search a hosted documentation site and retrieve its content | Make the team's published knowledge available in an assistant's workflow |
| Stripe | Search the knowledge base alongside access to product tools | Place relevant guidance near a product operation |
| pg-aiguide | Version-aware documentation search and curated database guidance | Explain how a recommendation depends on the task and its conditions |

**🎤 Talk track — documentation through MCP today:**

> This is already a documentation delivery pattern. Microsoft Learn lets assistants search its docs and fetch articles or code samples. Mintlify makes hosted documentation searchable and retrievable through MCP. Stripe places knowledge search alongside product tools. We'll examine pg-aiguide as our example of documentation paired with curated task guidance.
>
> The next design question is what the developer needs from that content. Finding the right page helps. We also want the person to understand why a recommendation fits, recognize an exception, and check their result. That is the learning experience we're building on top of the connection.

**🔗 Source note — documentation examples, checked October 27, 2026:** [Microsoft Learn MCP overview](https://learn.microsoft.com/en-us/training/support/mcp), [Mintlify search MCP](https://www.mintlify.com/docs/ai/model-context-protocol), [Stripe MCP](https://docs.stripe.com/mcp), and the [reviewed pg-aiguide README](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/README.md) support the capability descriptions. The teaching opportunities in the last column are our design interpretation.

**📝 Presenter depth — how the documentation pieces fit:** Retrieval-augmented generation describes supplying retrieved material for a model's response. MCP can expose that retrieval through a tool. The server still needs a way to find relevant content, which might use keyword search, semantic search, or a direct lookup. A Markdown export or `llms.txt` provides readable content or an index; an MCP server supplies a callable interface. Skills can supply task instructions and work alongside that interface. In this workshop, a direct content lookup is enough, so we can study the teaching behavior without adding a search system.

**🔗 Source note — complementary content:** Mintlify documents [Markdown export](https://www.mintlify.com/docs/ai/markdown-export), [llms.txt](https://www.mintlify.com/docs/ai/llmstxt), and [skills](https://www.mintlify.com/docs/ai/skillmd) separately from its search MCP. The distinction between retrieval strategy and MCP transport follows the protocol's scope; MCP does not prescribe how an application selects or uses context.

### 🖥️ Screen 09 — embracing contextual relevance

**🖥️ On screen:** Show the supplied [Embracing Contextual Relevance slide](assets/slide-references/contextual-relevance.png). Preserve its ruler and sprout comparison: “Simulated Interactivity” with fixed scenarios and click-to-learn activities, beside “Procedural Interactivity” with real tasks and inspectable interactions. Spend about 45 seconds here before introducing trivia.

**🎤 Talk track — contextual relevance:**

> Think about the difference between clicking the right answer in a prepared lesson and making a decision in a working system. The first gives you a fixed scenario. In the second, your choices affect what happens next, and you have a result to inspect.
>
> That's the procedural interactivity we're designing for: a place to try something, see its effect, and explain it. MCP connects the assistant to the tools. We supply the task boundaries, guidance, and evidence to reflect on.
>
> A tutorial can get you to a first success. Then your own project introduces new choices. The product team often explains those choices in support or code review. Our new documentation layer makes that reasoning available during the task, with a source you can inspect.

### 🖥️ Screen 10 — cognitive scaffolding

**🖥️ On screen:** Show the supplied [cognitive scaffolding slide](assets/slide-references/cognitive-scaffolding.png). Point first to “observation, simulation, execution, reflection,” then to the revised Bloom's taxonomy terms beneath it. Use these as learning-design prompts, with today's rule edit as the concrete example. Allow about 30 seconds.

**🎤 Talk track — cognitive scaffolding:**

> Give someone enough support to take the next step, then ask them to explain their choice. First you will observe our comparison. Before your own edit, predict its effect. Then make the change and reflect on the result.
>
> Bloom's terms help us describe the work: remember a rule, understand its reason, apply it, analyze the result, evaluate the exception, and create guidance for your own product. We're designing opportunities for those activities.

**🔗 Source note:** The six terms come from the revised taxonomy, summarized by [Cornell's Center for Teaching Innovation](https://teaching.cornell.edu/resource/blooms-taxonomy). The four workshop stages are our teaching sequence, rather than a direct equivalence between taxonomy levels and access permissions.

### 🖥️ Screen 11 — scaffolding and access

**🖥️ On screen:** Show the supplied [Cognitive Scaffolding / MCP Access Permissions slide](assets/slide-references/scaffolding-permissions.png). Walk through its read-only, mock execution, limited-write, and managed live execution examples. Treat the rows as an access-design proposal. Allow about 30 seconds.

**🎤 Talk track — scaffolding and access:**

> You can design access around the activity: read-only tools for observation, mocked responses for rehearsal, limited writes for a reversible exercise, and managed live operations where the task calls for them. The server and host need to enforce those boundaries.
>
> Today you edit a local file yourself, then inspect the guide's response. Our deployment tool recommends an environment without deploying anything. We reflect throughout. Reflection doesn't require granting live access, and this scaffold doesn't automatically unlock permissions as you learn.

### 🖥️ Screen 12 — educational research parallels

**🖥️ On screen:** Show the supplied [learning theory slide](assets/slide-references/learning-theory.png), highlighting situated learning, cognitive apprenticeship, and experiential learning loops. Introduce them as established frameworks informing this workshop. Suggested heading for this talk: “Learning frameworks behind the exercise.” Allow about 30 seconds.

**🎤 Talk track — educational research parallels:**

> Situated learning puts participation with other practitioners in view. Cognitive apprenticeship makes expert reasoning visible so learners can practice with support. Experiential learning connects an experience to reflection, an explanation, and another experiment.
>
> Here, we will model the decision, you will inspect its source, and then you will try a change with a neighbor. These frameworks inform our design. We still need to observe what attendees can explain and apply.

> We also want to manage what the learner has to juggle. We'll prepare the infrastructure first and change one value at a time. Then we ask you to explain the result yourself. The assistant can supply a useful explanation; your explanation gives us evidence about your understanding. Keeping answers hidden gives you a chance to attempt the clue before checking it.

**🔗 Source note:** [Lave and Wenger, *Situated Learning* (1991)](https://www.cambridge.org/highereducation/books/situated-learning/6915ABD21C8E4619F750A4D4ACA616CD), [Collins, Brown, and Holum, *Cognitive Apprenticeship* (1991)](https://www.aft.org/ae/winter1991/collins_brown_holum), and [Kolb, Boyatzis, and Mainemelis, *Experiential Learning Theory*](https://learningfromexperience.com/downloads/research-library/experiential-learning-theory.pdf) supply the framework references. Their application to this MCP workshop is our design interpretation, rather than evidence that using MCP by itself improves learning.

**📝 Presenter depth — the learning mechanisms:**

| Mechanism | What it asks us to design for | Where the attendee experiences it |
|---|---|---|
| Cognitive load | Leave attention available for understanding the decision | A prepared scaffold, a worked example, and one content edit |
| Self-explanation | Have the learner connect a step to its reason | Explain why the default applies and why the one-clue exception changes the result |
| Retrieval practice | Provide an opportunity to attempt recall | Try a clue before explicitly requesting its answer |
| Transfer | Check whether the reasoning applies to another situation | Apply the pattern to deployment guidance and then to an audience example |

**🔗 Source note — mechanism evidence:** [Sweller (1988)](https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1202_4) supplies the cognitive-load account; [Chi and colleagues (1989)](https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog1302_1) studied learners' self-explanations; [Roediger and Karpicke (2006)](https://pubmed.ncbi.nlm.nih.gov/16507066/) compared recall practice with restudy and assessed delayed retention. The workshop activities are design applications. A correct answer during this session cannot establish long-term retention, and this workshop has not measured an MCP-specific learning effect.

### 🖥️ Screen 13 — learning through play

**🖥️ On screen:** Use the supplied [Bar Trivia / Jeopardy Training slide](assets/slide-references/bar-trivia-jeopardy.png) to introduce the example, then show two clue faces with hidden answers. Highlight the decisions we'll inspect: “How many clues?”, “When do answers appear?”, and “What does difficulty mean?”

**🎤 Talk track — learning through play:**

> We'll use a small Jeopardy-style practice application because its behavior is easy to inspect. The API gives us clues, answers, categories, and board values. A practice experience also needs decisions: how many clues to start with, when to show answers, and how to explain difficulty.
>
> In my MCP for EDU notes, I talk about learning through play. That's why trivia fits here: you get a chance to try before seeing the answer, then reflect on what happened. We're giving you a small thing to experiment with and explain.

**📝 Presenter context — trivia reference:** The supplied slide also proposes using trusted references to explain answers and develop further questions. Today's scaffold uses six bundled synthetic clues, a practice-set tool, and explicit answer reveal. External reference lookup, question generation, and adaptive assessment are possible extensions rather than features demonstrated in this exercise.

### 🖥️ Screen 14 — workshop promise

**🖥️ On screen:** Show the supplied [learner participation slide](assets/slide-references/learner-participation.png), with “I ask / It answers” beside “I explore & safely participate.” Then reveal the exercise sequence: inspect a rule, edit its value, restart, repeat the request. Keep the three mechanisms as small labels: data access, executable policy, and agent advice.

**🖱️ Do:** Point to the three mechanisms summarized on the slide. The README supplies the detailed reference.

**🎤 Talk track — the promise:**

> We want you to participate in the system and explain what happened. In this workshop, you can change one local content value and restore it. Those concrete boundaries give us room to experiment.
>
> Keep these three mechanisms in mind. Data access gets the facts. Executable policy applies a rule in code. Advice tells the agent how to explain or interpret something. We'll look at the evidence for each one.
>
> Here is the loop you'll complete: find a recommendation, inspect its source rule, edit that rule, restart, and repeat the task. Then we'll apply the same pattern to deployment advice.
>
> By the end, you should be able to trace a recommendation to guidance you edited, observe its effect in your editor, and adapt that pattern to your own product. We'll check whether you can explain why the advice applies and when it should change.

**⏱️ Opening pacing:** Allow about one minute for the hook and contextual AI, one minute for the environment principles, two minutes for MCP and the tool-call walkthrough, one minute for documentation examples, three minutes for contextual relevance and the learning frameworks, and one minute for trivia and the workshop promise. Keep the tables as reference material while speaking to the main idea. The longer publication introduction and presenter-depth notes support explanation and Q&A rather than requiring a verbatim reading.

**🎤 Transition:** “Let's start by giving two servers the same request.”

## 2. 09:00–15:00 — Wrapper and guide comparison

**🔗 Files:** [DEMO.md](DEMO.md), [wrapper configuration](JSON-API-MCP/.vscode/mcp.json), [guide configuration](.vscode/mcp.json).

**🛠️ Setup:** Open the [presenter setup toggle](#comparison-startup) before starting this block. It contains installation, the two-window configuration, server startup, preflight prompts, and startup troubleshooting.

<a id="live-comparison"></a>

### ▶️ Live comparison begins here

### 🖥️ Screen 15 — comparison setup

**🖥️ On screen:** Show a compact comparison with “API wrapper” and “Education guide” as column labels. State “Same model, prompt, and clue data” above it, and name the different tool sets beneath each label. Switch to the two live chats to send the identical prompt below.

**🖱️ Do:** Show the two prepared windows. Keep the same prompt, model, dataset, and editor settings; use only the tools assigned to each server.

**🎤 Talk track — before sending:**

> Window A exposes the clue API through a wrapper. Window B uses the same bundled clue data, with a tool interface designed around guidance and practice. Both launchers manage their own local API. We're keeping the model and request the same and starting with empty chats so the earlier conversation doesn't supply an answer.
>
> As we compare, watch the tool calls as well as the final response. What data does the server return? Who chooses the count? Are answers included? Can we identify a product rule behind the recommendation?
>
> The analogy I keep coming back to is fitness blogs. I can read what every machine in the gym does. That doesn't give me six-pack abs. Knowing what each endpoint does still leaves the question of which ones to use, in what order, and why. That's where product guidance can help.

**💬 Copilot Chat — identical comparison prompt in both windows:**

```text
Give me a beginner practice round in Developer Tools. Explain your recommendation and identify its guidance source.
```

**🖱️ Do:** Wait for each result. Click its tool-call entry and expand the arguments and returned data. In the guide result, locate the `practice.default_count` rule, rationale, applied value, and `content_revision`. Describe the actual observed result.

### 🖥️ Screen 16 — comparison results, live

**🖥️ On screen:** Expand the actual tool results in each window. In the wrapper result, point to the returned answer fields. In the guide result, point to the clue count, omitted answers, and guidance trace. Then show each final response so the audience can compare the server's output with the agent's explanation.

**🎤 Talk track — explain what is visible:**

> The wrapper's tool results include answers. The model decides how to turn those results into a practice experience. It may choose a short round and hide answers in its final response. If it does, let's identify that as a decision the model made.
>
> The guide's practice result omits answer fields and returns information about the rules it applied. We can inspect the count, the reason for that count, and the source content. Now compare the final response: did the agent use and explain that guidance?
>
> A good wrapper response is a useful observation. This demonstration doesn't require the wrapper to fail. We're asking which decisions the server supplied and which the model inferred. Tool count alone doesn't tell us whether the experience teaches well.
>
> This first comparison changes the tool interface and the supplied guidance together. Later we'll keep the same guide and change one content value, which gives us a more precise way to connect an edit to a behavior change.

### 🖥️ Screen 17 — difficulty, live

**🖥️ On screen:** Keep the difficulty prompt and actual response visible. Highlight the relevant guidance alongside the board value. If a holding slide is needed, use “What does board value tell us about this learner?” with “Experience” and “Learning goal” underneath.

**💬 Copilot Chat — difficulty prompt, if time permits:** Send in both comparison chats, or use just the guide chat for discussion:

```text
Does the highest board value mean this is objectively the hardest clue for me? I want to improve at debugging MCP servers.
```

**🎤 Talk track — difficulty discussion:**

> Board value gives us a consistent way to order these clues, but it doesn't measure every learner's conceptual difficulty. Someone's experience and learning goal matter. Look for an explanation of that limit and a useful question about the goal or available material. Inspect the guidance and the response rather than assuming the agent followed it.

**📝 Presenter note:** Record unexpected outcomes as well as successful ones. If a spare prompt is needed, use the ten-clue shortage scenario in [DEMO.md](DEMO.md); only three Developer Tools clues are available.

**🛠️ Troubleshooting — interpreting the comparison:**

| Pitfall | Recovery or explanation |
|---|---|
| The wrapper gives a good beginner round | Keep the result. Ask which choices came from the model and which came from tool data. The demo works without a wrapper failure. |
| The guide returns a different count than expected | Check the saved default and actual `clue_count` argument. A supplied argument can override the default; part 5 uses an explicit omission prompt to isolate the content edit. |
| The final response hides evidence | Expand the tool-call details and inspect inputs and returned data. Polished prose alone doesn't establish which rule applied. |
| Someone expects enough material to master MCP debugging | The fixture contains six synthetic clues, with three in Developer Tools. It demonstrates a guidance pattern rather than a complete debugging curriculum. |
| The prompt changes between windows | Paste the exact same text into fresh chats. Recheck the named model and tool selection before drawing a comparison. |
| The tool is waiting for approval | Inspect and approve the intended workshop tool call in Chat, then continue. A waiting approval is different from a server startup failure. |

**⏱️ Pacing — demo recovery:** If startup or a call remains blocked after a quick check, use a captured result from an actual rehearsal and identify it as recorded. Keep the source rule and tool result available to inspect together. Use section 7 for longer recovery.

**🎤 Optional small talk while a tool call runs:** “This is the live-demo portion, where the software gets a vote in the pacing.” Resume with the actual result; skip this line if the call finishes promptly.

**🎤 Transition:** “We've seen a recommendation. Let's follow it back to the rule that supplied it.”

## 3. 15:00–21:00 — pg-aiguide in practice and tracing a recommendation

**🔗 Files:** [pg-aiguide lessons and source references](EXECUTION_PLAN.md#what-we-learned-about-developer-education-from-pg-aiguide), [practice.json](JSON-API-MCP/content/practice.json), [PRODUCT_GUIDANCE.md](JSON-API-MCP/PRODUCT_GUIDANCE.md), [guidance.py](JSON-API-MCP/src/jeopardy_template/guidance.py), [guide_server.py](JSON-API-MCP/src/jeopardy_template/guide_server.py).

### 🖥️ Screen 18 — what pg-aiguide provides

**🖥️ On screen:** Show “PostgreSQL expertise during the task” above two labeled sources: “Versioned documentation” and “Curated task guidance.” Place the developer's editor beside them. Label the connections `search_docs` and `view_skill` for the MCP route, with “Native agent skills also available” as a short footnote.

**🎤 Talk track — pg-aiguide in context:**

> pg-aiguide is Timescale's project for bringing PostgreSQL and TimescaleDB expertise into coding assistants. Think about adding a table to an application. The assistant needs to know which PostgreSQL version you're using and which design choices fit the feature.
>
> Documentation search retrieves the relevant manual. Curated skills explain how to approach tasks such as table design or schema exploration. The MCP route exposes that knowledge through tools; compatible agents can also load the skills directly. This is the product expertise we want available while a developer is working.

**🔗 Source note — reviewed implementation:** See the pinned [project overview](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/README.md), [MCP API](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/API.md), and [Postgres task routing](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/postgres/SKILL.md). In this revision, `search_docs` selects a manual through `source`, such as `postgres_17`; `view_skill` retrieves a named skill. Native skill installations can supply the guidance without that tool.

<a id="pg-aiguide-daily"></a>

### 🖥️ Screen 19 — pg-aiguide in day-to-day work

**🖥️ On screen:** Show a small table with “Developer task,” “Context needed,” and “Guidance used.” Use the three examples below. Walk through the first example and keep the others as concrete follow-ups; this is an illustrated workflow rather than another live installation.

| Developer task | Context to supply or establish | How pg-aiguide fits |
|---|---|---|
| Add a table for a new feature | PostgreSQL version, feature requirements, existing schema conventions | Table-design guidance helps choose types, keys, and constraints; versioned docs help check syntax. The developer reviews the proposal before applying it. |
| Write or review a query against an unfamiliar schema | The business question, authorized schema, join keys, expected result grain | Schema-exploration guidance directs the assistant to relevant catalog objects and asks it to distinguish observed structure from inferred business meaning. Database inspection uses a separate authorized connection. |
| Design a sensor or event-data table | TimescaleDB availability, query patterns, data volume, retention requirements | Hypertable guidance supplies configuration considerations and asks about retention when unknown. The team can evaluate the recommendation against its actual workload. |

**🎤 Talk track — a daily workflow example:**

> Here's a normal development task: “I'm adding a feature that stores device readings. Help me design the table and explain the tradeoffs.” We supply the database version, the queries we need, and the existing schema context. The assistant retrieves the relevant guidance, proposes a design, and explains what information could change it. If retention is unknown, it asks.
>
> Later, when we're reviewing a query, the question changes: “Which tables and joins actually support this answer?” Schema-exploration guidance helps inspect the relevant structure and separate facts from assumptions. We review and validate the SQL using our normal workflow. The guide provides knowledge; database access comes from our separately authorized tools.
>
> That is the everyday pattern we're borrowing: bring guidance into the decision, explain the reason, and leave the developer with something they can verify. Our Jeopardy example makes that pattern small enough to inspect together.

**💬 Copilot Chat — illustrative pg-aiguide prompts, for later use in a separately configured project:**

```text
Use pg-aiguide to propose a table for device readings for my project's PostgreSQL version. Explain the keys, data types, and constraints. Ask for missing requirements before recommending a retention policy. Propose SQL for review without applying it.
```

**💬 Copilot Chat — illustrative schema exploration prompt:**

```text
Use pg-aiguide's schema-exploration guidance to plan how to answer this question against the schema I've provided. Explain the join keys and result grain. Separate observed structure from assumptions about what the data means.
```

**📝 Presenter note — connection to this repository:** pg-aiguide is the implementation reference for our teaching patterns, not a dependency of the Jeopardy server. This workshop uses a local JSON fixture and API rather than PostgreSQL. Keep pg-aiguide and other optional tools unselected in the wrapper/guide comparison. The examples above illustrate how to use its guidance; they are not claims about a recorded production workflow or benchmark.

**🔗 Source note — everyday tasks:** The examples adapt the reviewed [table-design skill](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/design-postgres-tables/SKILL.md), [schema-exploration skill](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/schema-exploration/SKILL.md), and [hypertable setup skill](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/setup-timescaledb-hypertables/SKILL.md). The schema skill directs structural exploration first, requires approval for data-derived inspection, and distinguishes a valid plan from proof of business meaning.

### 🖥️ Screen 20 — pg-aiguide lessons

**🖥️ On screen:** Use a plain four-row list: “Teach at the moment of the decision,” “Pair reference with judgment,” “Ask for missing information,” and “Separate evidence from inference.” Reveal each row as it comes up. Include the reviewed source link from `EXECUTION_PLAN.md` in a small footer.

**🎤 Talk track — the pg-aiguide lessons:**

> Here are the four lessons we carried into our workshop scaffold.
>
> First, teach a decision when it is needed. pg-aiguide routes a task toward relevant references. Here, a practice request should lead the agent to practice guidance.
>
> Second, pair reference material with judgment. Its documentation search supplies references, while curated skills help with decisions. Our API supplies clue data, and our guide recommends how to use it.
>
> Third, ask for missing information. Its hypertable example asks about unknown retention requirements. Our deployment example asks about nonproduction verification.
>
> Fourth, separate evidence from inference. Its schema guidance distinguishes observations from interpretations. A user confirming verification gives us their confirmation. It doesn't establish that our tool checked the tests.

### 🖥️ Screen 21 — recommendation trace, live

**🖥️ On screen:** Start with `practice.default_count` enlarged in `practice.json`, showing its value and rationale. Move to the same rule in the generated Markdown, then the tool description and returned guidance. Keep a small reference diagram available: source JSON feeds human documentation and the MCP server, whose tool result informs the agent's response. Highlight the matching rule ID at each stop.

**🖱️ Do:** Find `practice.default_count` in `practice.json`. Show `value`, `rationale`, `applies_when`, and `exceptions`. Open the generated Markdown and find the same rule. In Configure Tools, inspect the `build_practice_set` description if the host exposes it. Finally, expand the practice tool result in Chat.

**🎤 Talk track — trace the mechanism:**

> Here is the source of our practice recommendation. JSON is structured text. This rule has a stable ID, a value, a reason, conditions, and exceptions. The server loads and validates the file at startup. The loaded content supplies tool descriptions and the handler's default. The documentation renderer uses that same source to produce the human guide.
>
> Follow the chain: source JSON, human documentation and MCP description, tool behavior, then the agent's explanation. In the result, `source` points to the content file, `rule_id` identifies the rule, and `applied_value` tells us what was used. `content_revision` identifies the loaded content version. These fields let us inspect the connection.
>
> The count is an executable default. Answer omission is enforced by the practice response model. The instruction to reveal an answer only when asked, and the advice about conceptual difficulty, still require the agent to follow the guidance. Different mechanisms need different checks.

**🙋 Ask the room:** “Why does the short-round recommendation apply here? What user request would make the default yield?” Pause for an answer.

### 🖥️ Screen 22 — learning check

**🖥️ On screen:** Keep the learning theory slide visible and ask “Why does this rule apply?” and “When should it change?” Use the concrete actions to explain the loop: request a round, inspect the result, explain the rule, try a changed request.

**🎤 Talk track — learning check:**

> Starting the server establishes that the connection works. Explaining the rule and its exception tells us about understanding. The trace gives us something concrete to reflect on. Applying the reasoning to a changed request is our next check.

**⏱️ Presenter pacing — section 3:** The learning environment and theory now appear in the opening. Use about two minutes here for pg-aiguide and its daily workflow, one minute for the lessons, two minutes for the source trace, and one minute for the explanation check and transition. Keep the illustrative prompt examples as reference material rather than running another demo.

**🎤 Transition:** “Now let's get that same trace into your own editor.”

## 4. 21:00–28:00 — Fork, install, and verify

**🔗 Files:** [root quickstart](README.md#start-in-your-editor), [beginner setup above](#goodbye-tutorial-hell-ai-guides-and-the-new-documentation-layer), [optional infrastructure tutorial](TUTORIAL.md).

### 🖥️ Screen 23 — attendee setup

**🖥️ On screen:** Show the repository URL and QR code again with “Fork, clone, open the repository root.” Display the two setup commands below in large, copyable text. Keep a link to the README quickstart visible throughout attendee work.

**🎤 Talk track — introduce attendee work:**

> This is the part where it stops being my talk and starts being your afternoon. If you're already set up, check your tools and help a neighbor. If you're starting now, use the root README or the detailed setup at the top of this file. For this exercise you need the guide window, opened at the repository root. The second window is for our presenter comparison.
>
> Fork the repository into your GitHub account, clone it, and open the folder containing the README and `JSON-API-MCP`. Open a terminal in that outer folder. Run these two commands, one at a time.

**⌨️ Terminal — install and check from the repository root:**

```bash
uv sync --locked --directory JSON-API-MCP
uv run --locked --directory JSON-API-MCP python scripts/check_setup.py
```

### 🖥️ Screen 24 — startup, live

**🖥️ On screen:** Show the terminal's setup result, then the `education-guide` server running in VS Code. Move to Copilot Chat with Agent mode and the four guide tools visible. Keep the exact practice prompt below available in the README or exercise so attendees can copy it.

**🎤 Talk track — explain setup and startup:**

> The first command installs the locked project dependencies. The second checks the environment and dataset. Look for `setup ready: 6 clues, synthetic-workshop-v1` in the terminal output.
>
> Now open the Command Palette with Command-Shift-P on Mac or Control-Shift-P on Windows or Linux. Run `MCP: List Servers`, select `education-guide`, and choose `Start Server`. The launcher starts the API and MCP together, using a private local port chosen for that run. You don't need another terminal or a manually started API.
>
> Open Copilot Chat in Agent mode. In Configure Tools, select `get_guidance`, `build_practice_set`, `reveal_answer`, and `recommend_deployment` from this server. Start a fresh chat and send the prompt on screen. We're asking it to omit the count so we can observe the documented default.

**💬 Copilot Chat — attendee practice prompt:** Paste this into a fresh guide chat and save it for the next section:

```text
Use only MCP tools from education-guide for this request; do not read or edit workspace files. Give me a beginner practice round in Developer Tools. Explain your recommendation and identify its guidance source. Omit clue_count so the server's documented default applies.
```

**✅ Checkpoint:** Expand `get_guidance` and `build_practice_set`. Confirm two clues with no answer fields, then find the default-count entry in the practice result's `guidance` array:

| Field | Expected with the shipped rules |
|---|---|
| `rule_id` | `practice.default_count` |
| `source` | `content/practice.json`, relative to `JSON-API-MCP` |
| `source_field` | `/rules/0/value` |
| `configured_value` / `applied_value` | `2` / `2` |
| `decision_basis` | `default` |
| `rationale` | Reason for starting with a short round |
| `content_revision` | Identifier for the loaded content file |

### 🖥️ Screen 25 — first result checkpoint

**🖥️ On screen:** Leave an enlarged actual tool result on screen, highlighting `practice.default_count`, `applied_value: 2`, and the source file. Place the short instruction “Find your rule, value, and source” beside it. Keep this view up while attendees catch up.

**🎤 Talk track — while attendees inspect:**

> The final response may use different wording from mine. Look inside the tool result for the evidence. Can you locate the source rule and the value it applied? If you changed the fixture before today, check its current value before expecting two.
>
> If you hit a setup error, start with the README's troubleshooting steps. Check that the correct folder is open, that the server is running, and that the four tools are selected. You can follow the presenter's result while recovering. The infrastructure tutorial is available afterward if you want to study how the API and MCP pieces were built.

**📝 Presenter cue:** Pause for attendee work. Ask for confirmation that people can point to the rule. Use the remaining installation time for recovery rather than adding an infrastructure lecture.

**🎤 Transition:** “Keep the exact prompt and the result. Now we'll change the guidance behind it.”

## 5. 28:00–34:00 — Edit guidance, restart, and observe

**🔗 Files:** [EXERCISE.md](EXERCISE.md), [practice.json](JSON-API-MCP/content/practice.json), [PRODUCT_GUIDANCE.md](JSON-API-MCP/PRODUCT_GUIDANCE.md).

### 🖥️ Screen 26 — content edit, live

**🖥️ On screen:** Open `practice.json` at `practice.default_count`. Show the current `"value": 2`, then edit it to `"value": 3`. Keep the rule ID and rationale visible so attendees can find the same location.

**🎤 Talk track — introduce the edit:**

> Open `JSON-API-MCP/content/practice.json`. Find the rule whose ID is `practice.default_count`. Change only its `value` from two to three. Keep the model, prompt, tools, code, and dataset the same. The fixture already has three Developer Tools clues, so no data change is needed.
>
> This is the shift I want from the MCP for EDU talk: from “Will this break something?” to “What happens if I try this?” We're changing one local content value, and we know how to put it back. That room to experiment comes from the way we've built this exercise. MCP gives us a tool interface; our implementation supplies these boundaries.

**⌨️ File edit — practice.json, before:** In `practice.default_count`, replace:

```json
"value": 2
```

**⌨️ File edit — practice.json, after:**

```json
"value": 3
```

### 🖥️ Screen 27 — restart and repeat, live

**🖥️ On screen:** Show Restart Server, the refreshed tool description, and a fresh chat using the saved prompt. Compare the actual results before and after: two clues versus three, the same rule ID, and a changed content revision. Highlight that the request omits `clue_count`.

**🖱️ Do:** Save with **Cmd+S** / **Ctrl+S**. Open the Command Palette, run **MCP: List Servers**, select **education-guide**, and choose **Restart Server**. Reopen Configure Tools and inspect `build_practice_set`'s description if available; it should reflect three clues. Refresh the host's tool list if it still shows the old description.

**🖱️ Do:** Repeat the exact section 4 prompt. Expand the result and compare the fields with the previous run. Check that the count argument was omitted.

**🎤 Talk track — explain restart and comparison:**

> Restarting matters because the server loads the file at startup. Saving changes the file on disk; restarting makes the running server use it. Check the refreshed tool description, then start a fresh chat and paste the exact prompt from the last section.
>
> We expect three clues, the same `practice.default_count` rule, an applied value of three, and a changed content revision. The stable rule ID identifies the decision; the changed revision identifies the updated content. Compare the explanation with the rule's rationale too.

### 🖥️ Screen 28 — troubleshooting, only if needed

**🖥️ On screen:** Expand the tool arguments and loaded content revision. Point to any explicit `clue_count`, then check the saved file and restarted server. Keep the original result visible for comparison.

**🎤 Talk track — if the result does not change:**

> Inspect the tool arguments. If the agent passed an explicit `clue_count`, that argument can mask the default. Ask it to omit the parameter and repeat in a fresh chat. Keep a record of the original result as well. If the loaded revision hasn't changed, check that the file was saved and the correct server restarted.

### 🖥️ Screen 29 — generated documentation, live

**🖥️ On screen:** Show the renderer command completing, then the three-clue recommendation in `PRODUCT_GUIDANCE.md` beside its source rule. Caption: “One source supplies the human guide and server guidance.” Switch back to Chat for the one-clue exception prompt below.

**⌨️ Terminal — regenerate human documentation from the repository root:**

```bash
uv run --locked --directory JSON-API-MCP python scripts/render_guidance.py
```

**🖱️ Do:** Open `JSON-API-MCP/PRODUCT_GUIDANCE.md` and find the three-clue recommendation.

**🎤 Talk track — documentation and exception:**

> The Markdown is generated from the JSON source. Edit the source for future changes, then regenerate the document. That gives human readers and the server the same rule content without separately maintaining the number in two places.
>
> If your first reaction is “I don't want to write docs twice,” correct. You barely want to write them once. Nobody's judging. Here, the rule has one source and two readers, with one place to fix the typo.
>
> Now let's check the exception. A default fills a choice the user hasn't made. A valid explicit user choice should take precedence.

### 🖥️ Screen 30 — explicit choice checkpoint, live

**🖥️ On screen:** Show the one-clue result with `decision_basis: explicit_user_choice` highlighted. Keep “Default: 3” and “User request: 1” visible beside the result, and ask the audience to explain the choice. If demonstrating answer reveal, expand that separate tool call afterward.

**💬 Copilot Chat — explicit one-clue request:**

```text
Give me one Developer Tools clue, then explain why you used one instead of the default.
```

**✅ Checkpoint:** Expect one clue and `decision_basis: explicit_user_choice`. Ask an attendee to explain why one is appropriate even though the default is three. To demonstrate answer reveal, explicitly request the answer to a returned clue ID and inspect `reveal_answer`.

**🎤 Talk track — checkpoint:**

> Can you point to the edit, the changed result, and the fields connecting the two? Can you explain why a one-clue request gets a different count? That is the trace-and-observe part of today's goal. The next step is carrying this reasoning into a different product decision.

**🛠️ Troubleshooting — after the practice edit:**

| Symptom | Check in this order |
|---|---|
| Still two clues | Save `practice.json`; restart `education-guide` in Window B; start a fresh chat; inspect whether `clue_count` was supplied. Compare the loaded revision. |
| The wrapper still behaves the same | The content edit targets the guide. Switch to Window B and call `build_practice_set`. |
| The server errors after editing | Look at Show Output for the file/rule location. Change only the numeric `value`, preserve valid JSON, and keep the practice default an integer from 1 to 10. |
| More than three Developer Tools clues were requested | Only three match this fixture. Inspect the returned count and shortage note; don't fill the round with another category. |
| The generated Markdown still says two | Run `scripts/render_guidance.py` using the root-terminal command above. The JSON file supplies runtime guidance; rendering updates the human document. |
| The tool description still shows the old default | Restart the guide and refresh the host's tool discovery if needed. Check the returned revision and applied value rather than relying on cached wording. |

**🎤 Transition:** “Let's move from practice rounds to a deployment recommendation.”

## 6. 34:00–39:00 — Adapt the pattern to a product

**🔗 Files:** [TAKEAWAY.md](TAKEAWAY.md), [deployment.json](JSON-API-MCP/content/deployment.json), [standalone template](mcp-server-template/README.md), [guidance.py](JSON-API-MCP/src/jeopardy_template/guidance.py), [guide_server.py](JSON-API-MCP/src/jeopardy_template/guide_server.py).

**📝 Presenter note:** Demonstrate the deployment task through the already-running `education-guide` to avoid another installation. `TAKEAWAY.md` also explains the standalone deployment-only launcher. The separate `mcp-server-template` is the copyable project for attendees' own tasks and context.

### 🖥️ Screen 31 — deployment guidance

**🖥️ On screen:** Show the question “What should my next deployment step be?” with the current default “Preview.” Add “Advice only” beneath it. Then switch to `recommend_deployment` in the live guide chat using the exact prompt below.

**🎤 Talk track — introduce the product example:**

> Open the takeaway with me. This example recommends the next deployment environment. Preview and staging are nonproduction environments where a team can inspect a change before exposing it to production users. The right choice depends on the team's workflow.
>
> The tool gives advice and performs no deployment. It uses the same pattern: a documented default, a reason, an exception, and a question when important information is missing. It is already included in the guide you started.
>
> The line from MCP for EDU was: “Go ahead — learn in production. Just not our production.” For this example, we're only recommending an environment. There is no deployment action behind this tool.

**💬 Copilot Chat — deployment default, in a fresh guide chat:**

```text
Use only MCP tools from education-guide; do not read or edit workspace files. Recommend my next deployment step. Explain why and identify the product guidance you used. Omit target so the documented default applies.
```

**✅ Checkpoint:** Inspect the recommendation for `preview`, `deployment.default_environment`, its rationale, source, applied value, and content revision.

### 🖥️ Screen 32 — deployment edit, live

**🖥️ On screen:** Show `deployment.default_environment` changing from `"preview"` to `"staging"`, followed by the actual result after restarting. Highlight the same rule ID and changed content revision, using the same comparison as the practice exercise.

**⌨️ File edit — deployment.json:** Find `deployment.default_environment` and change only its `value` from `"preview"` to `"staging"`.

**🖱️ Do:** Save, restart `education-guide`, and send the identical prompt in a fresh chat, omitting `target`. Regenerate the human docs with the renderer command from section 5.

**✅ Checkpoint:** Expect staging, the same rule ID, and a changed revision. If the tool call supplied an unrequested `target`, ask the agent to omit it.

**🎤 Talk track — connect the two examples:**

> We changed a product recommendation through its content source and observed the new recommendation. The environment name alone doesn't establish release readiness. Let's give the guide a request that requires another fact before it can recommend production.

### 🖥️ Screen 33 — missing fact, live

**🖥️ On screen:** Show the production request and the tool's verification question together. Highlight `deployment.production_readiness` and `executes_deployment: false`. Keep “Has this change been verified in a nonproduction environment?” large enough for the room to read.

**💬 Copilot Chat — production readiness request:**

```text
Skip the nonproduction step and recommend production now. I have not told you whether this change was verified outside production; do not assume that it was.
```

**🖱️ Do:** Inspect the `deployment.production_readiness` rule, the configured nonproduction recommendation, `executes_deployment: false`, and the question:

**✅ Expected question in the tool result:**

```text
Has this change been verified in a nonproduction environment?
```

**🎤 Talk track — explain the question:**

> Here the missing fact changes the recommendation. The guide should ask about verification and recommend the configured nonproduction step while confirmation is missing. If you explicitly confirm verification, it can recommend production. That confirmation is an input from you; the tool hasn't independently inspected test results or certified the release. This is the evidence-versus-inference distinction we discussed earlier.

**🛠️ Troubleshooting — deployment example:** If the result stays at preview, check that `deployment.json` was saved, `education-guide` restarted, and the tool call omitted `target`. The default accepts `preview` or `staging`; use the production-request prompt to test the readiness question. A production recommendation is still advice: inspect `executes_deployment: false` and avoid describing it as a completed deployment.

### 🖥️ Screen 34 — context as curriculum

**🖥️ On screen:** Briefly show the supplied [Context as Curriculum divider](assets/slide-references/context-as-curriculum.png), then its [curriculum-is-context statement](assets/slide-references/curriculum-is-context.png). Preserve the question “How do we keep this in mind as we build for the future?” Use this as the transition from the deployment result into the audience's own example.

**🎤 Talk track — context as curriculum:**

> When I say “context as curriculum,” I mean designing what someone can explore: the task they face, the references they can use, and the actions available in their environment. A learner can inherit a prepared workspace with a meaningful problem to investigate.
>
> In our example, the clue data and guidance shape the exercise. For your product, start with a decision your users actually face. What context would help them try it and understand the outcome?

### 🖥️ Screen 35 — adaptation worksheet, live

**🖥️ On screen:** Open the adaptation record in `TAKEAWAY.md` and fill in one audience example. Zoom into the recommendation, reason, and exception first. Then briefly show the copyable template's README, pointing out where task content lives and where a new operational tool would need code.

**🖱️ Do:** Ask for one recurring support or onboarding question from the room. Open the adaptation record in `TAKEAWAY.md` and capture a short example using these fields:

**⌨️ Adaptation record — type into your copy of TAKEAWAY.md:**

```text
Recurring user question:
Recommended first step and reason:
Applies when:
Exception or missing fact to ask about:
Anti-pattern to avoid:
Source file and rule ID:
Example request:
Expected result before and after one edit:
Changed scenario and why the advice changes:
```

**🎤 Talk track — explain adaptation boundaries:**

> Choose one support question your team answers repeatedly. Write down the recommendation, why it helps, when it applies, and what would change it. Add an example and a source so someone else can inspect the reasoning.
>
> Changing a rule for an existing task is a content edit. Adding an unrelated task or a tool that performs a product operation may require a new schema and handler. In this workshop implementation, those boundaries are in `guidance.py` and `guide_server.py`. Loading, validation, source tracing, transport, and startup are reusable.
>
> For a separate project, the copyable template accepts recommendation tasks and reference context through JSON and Markdown. Follow its README to copy and customize it. New operational tools still need their own implementation. Before calling the result useful, give someone a changed scenario and ask whether the rule still applies. Understanding includes explaining when the recommendation should change.

### 🖥️ Screen 36 — context manifests and brokers

**🖥️ On screen:** Use the supplied [This is possible now slide](assets/slide-references/context-manifests-and-brokers.png) as the brief takeaway after showing the template. Keep its two ideas visible: “platforms define context manifests” and “agents become context brokers.”

**🎤 Talk track — context manifests and brokers:**

> A team can describe a learning environment in a context manifest: its task, relevant references, available tools, and access boundaries. An agent can act as a context broker by bringing the relevant pieces into the current task. Here, configuration selects the server and content files supply the recommendations. That gives you concrete pieces to adapt.

**📝 Presenter context — implementation:** “Context manifest” is an application-design idea here, rather than a new standard MCP artifact. The workshop configuration, content files, and template illustrate parts of that design. Access enforcement and any operational tools still need implementation in the host, server, and underlying product.

**📝 Presenter context — software and engineering example:** The supplied [Software / Engineering slide](assets/slide-references/software-engineering.png) connects static snippets and syntax exercises to work in a live development environment. A useful adaptation gives the assistant relevant project constraints and product docs, supports questions during the task, and returns feedback the learner can inspect. Ask “How does this recommendation fit my stack?” Treat faster onboarding as an outcome to evaluate.

**📝 Presenter context — design and creative example:** The supplied [Design / Creative slide](assets/slide-references/design-creative.png) proposes learning inside creative tools, with design principles available during the work. A team could provide tools that inspect a sample file, allow edits within a chosen scope, and preserve version history for recovery. Replayable action records could then support critique of the process. Those capabilities depend on the connected tool and its implementation. Use this as an alternative audience adaptation if the room offers a design example.

**📝 Presenter cue:** Keep the live adaptation to one spoken example; attendees can complete the template afterward. Fold the context-as-curriculum and manifest explanations into the existing adaptation time. Use the software and design examples as prompts or Q&A material rather than adding two more demos.

**🎤 Transition:** “Let's use the remaining time to check understanding and discuss your own use cases.”

## 7. 39:00–45:00 — Questions, recovery time, and leave-behinds

**🖱️ Do:** Invite an attendee to briefly explain their rule and the evidence of its effect. Leave the following links on screen:

- [Quickstart and attendee walkthrough](README.md#start-in-your-editor)
- [Practice exercise](EXERCISE.md)
- [Product takeaway and adaptation record](TAKEAWAY.md)
- [Generated product guidance](JSON-API-MCP/PRODUCT_GUIDANCE.md)
- [pg-aiguide lessons and source links](EXECUTION_PLAN.md#what-we-learned-about-developer-education-from-pg-aiguide)
- [Copyable MCP server template](mcp-server-template/README.md)

### 🖥️ Screen 37 — reflection

**🖥️ On screen:** Show four short prompts: “Which rule?”, “Why did it apply?”, “What changed after your edit?”, and “What would change the advice?” Leave these visible during the neighbor discussion and attendee explanation.

**🎤 Talk track — reflection:**

> Take a moment to explain your result to a neighbor. Which exact rule shaped the recommendation? Why did it apply? What changed after your edit, and what evidence connects that result to the edit? Then describe an exception or missing fact that changes the advice.
>
> We'd like to hear one example. Tell us the user question, your recommendation, and the condition under which you would recommend something else. If you haven't completed setup yet, use the result we inspected together and identify what you would check in your own run.

### 🖥️ Screen 38 — discussion

**🖥️ On screen:** Show “What support answer belongs in your guide?” as the main question. Add the smaller prompts “What should it ask?” and “How will you notice stale guidance?” Keep the repository URL in the footer.

**🖱️ Do:** Pause for an attendee explanation and questions. Use these prompts to start discussion if needed:

**🎤 Talk track — discussion prompts:**

> What recurring support answer belongs in your guide?
>
> Which missing fact should make it ask a question?
>
> How will you notice the guidance becoming stale?

### 🖥️ Screen 39 — maintenance and evidence

**🖥️ On screen:** Show the maintenance sequence as a short numbered list: review the source, regenerate the docs, rerun a representative task. Beneath it, use a small table pairing “Server tests” with “Rules behave as expected,” “Editor observations” with “Agent uses and explains guidance,” and “Changed scenario” with “Developer can apply the reasoning.”

**🎤 Talk track — maintenance and evaluation:**

> Guidance needs maintenance because a change to the advice can change behavior. Review the source, regenerate derived documentation, and rerun a representative task. Check whether the recommendation still fits the product and whether a developer can explain its conditions. More tools, a longer response, or a successful connection doesn't by itself establish learning.
>
> The verification records distinguish server behavior from observed editor behavior and attendee understanding. Protocol tests check the server's rules. Editor runs show whether the agent uses and explains the guidance. An attendee applying it to a changed scenario checks transfer. Those are different kinds of evidence, and each helps us improve the experience.

**📝 Presenter callback:** Return to the opening environment principles if the audience asks how to extend this design.

**🛠️ Recovery cue:** Reserve time here for unresolved setup problems. Follow [README troubleshooting](README.md#troubleshooting) and [DEMO.md](DEMO.md). If using a captured fallback, say: “This is a recording from a verified run; let's inspect its tool result together.” Identify the tested configuration. Describe the actual capture rather than suggesting that a recorded outcome happened live.

### 🖥️ Screen 40 — closing reflection

**🖥️ On screen:** Briefly show the supplied [learning from technology slide](assets/slide-references/learning-from-technology.png). Use its contrast between controlling technology and learning from it as a reflection prompt for the audience.

**🎤 Talk track — closing reflection:**

> We spend a lot of time making technology do what we ask. In your next small experiment, also ask what the person using it can learn. Can they explain the decision, inspect its source, and recognize when to change it?

### 🖥️ Screen 41 — closing resources

**🖥️ On screen:** Return to the supplied [learner participation slide](assets/slide-references/learner-participation.png) for a quick callback, then show “What happens if I try this?” above the repository URL and a QR code. Feature the quickstart, exercise, takeaway, and copyable template as short resource labels. Keep the resource slide up through the final thanks and remaining questions.

**🎤 Talk track — close:**

> Our goal was to trace a recommendation to guidance you edited, observe its effect in the editor, and adapt the reasoning to your product. You now have the scaffold, the exercise, and a template for your next support question.
>
> Start with one decision your users repeatedly face. Make the recommendation discoverable during that task. Include its reason, its exception, and the question that resolves missing information. Then check that someone else can explain and apply it in a changed situation. Thank you for building with us.

**🎤 Optional final callback:** “Leave with one small experiment: ‘What happens if I try this?’ Then give yourself a way to inspect the answer.”

**📝 Speaker note on the MCP for EDU callbacks:** Keep these short and conversational within the existing time blocks. The supplied contextual relevance, cognitive scaffolding, access mapping, and curriculum slides supply the educational framing. Their broader examples include staged permissions, reference-enriched trivia, replayable creative workflows, and context manifests. This workshop implements the practice and recommendation examples shown here. Describe reversibility, access controls, and observed traces in terms of this implementation, and frame broader capabilities as designs to build and evaluate. Optional lines are newly adapted presenter copy, rather than a transcript of the earlier talk.

## After the session: reset and remaining validation

**🖱️ Do:** Preserve attendee changes and any presenter edits you want to keep. To reset the presenter fixture, manually restore `practice.default_count` to `2` and `deployment.default_environment` to `"preview"`. From the repository root, run:

**⌨️ Terminal — repository root (Window B):**

```bash
uv run --locked --directory JSON-API-MCP python scripts/render_guidance.py
```

Restart the guide before repeating, or stop both servers through **MCP: List Servers** when finished. Use fresh chats and recheck tool selection for the next run. If you changed the root configuration to the deployment-only launcher, restore `--server guide` for the practice exercise.

**📝 Presenter validation note from [OUTLINE.md](OUTLINE.md):** Protocol tests establish server behavior. Broader editor/model comparisons, a clean-machine and Codespaces installation, a second host, and a timed attendee rehearsal require observed records. Consult [NEXT_STEPS.md](NEXT_STEPS.md) and [verification status](evidence/README.md) for the current evidence and outstanding checks. Prepare fallback captures from actual rehearsals and label them when shown.
