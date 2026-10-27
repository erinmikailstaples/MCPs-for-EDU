# Goodbye, Tutorial Hell: AI Guides and the New Documentation Layer

**Erin Mikail Staples & Janice Niemeir · 45 minutes**  
**Format:** Sandbox session with a working scaffold and attendee exercises.  
**Audience:** Intermediate developers, maintainers, and product teams; setup instructions assume no prior experience with this workshop.  
**Source:** [OUTLINE.md](OUTLINE.md). The spoken script below expands all seven sections of that outline, including its teaching points, exercises, and closing questions.  
**Voice and conversational cues:** Erin's [MCP for EDU notes](</Users/erinmikail/Documents/HQ/30-39-Blog/2025-10-24-MCP-for-EDU.md>) supply the learning-through-play, reflection, and curiosity callbacks; the related [Universe speaker notes](</Users/erinmikail/Documents/HQ/20-29-Work/20.02-Conferences/2026-GitHub-Universe/2026-GitHub-Universe-Talk-Outline.md>) supply the tutorial, fitness-blog, and documentation jokes. These are adapted into the current workshop script.  
**Acceptance criterion:** An attendee can trace a recommendation to guidance they edited, observe its effect in their editor, and adapt that pattern to their own product.

## Introduction — the topic and why it matters

Developer education helps people understand a tool well enough to use it in their own work. Tutorials and reference documentation are part of that: they explain concepts, demonstrate a first success, and describe the available operations. The harder step comes when a developer's project differs from the example. They need to choose an approach, understand its tradeoffs, and recognize when the recommendation should change.

That is the problem behind **AI guides and the new documentation layer**. When developers ask an assistant for help in their editor, the assistant needs access to the product team's reasoning as well as its API. Model Context Protocol (MCP) provides a way for an assistant to access tools and context from a server. We can use that connection to supply documented recommendations, their rationale, their exceptions, and questions to ask before proceeding.

This matters because a working example does not necessarily teach someone how to make the next decision. Without that reasoning, a developer can copy a solution without knowing whether it fits, while maintainers explain the same choices again in support and code review. Making guidance available during the task gives the developer a chance to understand the recommendation, inspect its source, and apply it to a different situation.

In this workshop, we will build and inspect that connection. A small trivia application makes the first decisions visible; a deployment-advice example shows how the pattern transfers to a product workflow. The learning goal is to explain why a recommendation applies and what would change it. The opening talk track in Part 1 introduces this context before the first demo.

**How to use this run sheet:** Complete the setup before the 45-minute session. During the talk, follow the timed steps; **Screen / slide** describes what the audience should see, **Do** describes presenter actions, and **Talk track** gives suggested words to say aloud. Keep slides to the short text or visual described in each cue. During demos, show the relevant editor view and zoom into the fields being discussed.

**Supplied slide references:** The linked images in [assets/slide-references](assets/slide-references/) preserve Erin's supplied slides and any visible presenter notes. Present the slide canvas, keeping the screenshot's notes panel off the audience screen. The cues below place the slides in the talk or use their information in the relevant notes. Broader classroom and product examples describe designs teams can build; the live workshop demonstrates the specific capabilities documented here.

**Before the clock — beginner setup**

An MCP server gives an AI assistant tools it can call. Here, `jeopardy-basics` retrieves clue data; `education-guide` adds product rules and recommendations. Their launchers also start the local API, the service supplying clue data. You do not need to start that service separately.

**A. Open the project and check setup.**

1. If you have not downloaded the project, follow [Fork and open the repository](README.md#fork-and-open-the-repository). Install the prerequisites listed there: VS Code, GitHub Copilot access, Python 3.12+, and uv. A *repository* is the project folder you downloaded or cloned.
2. In VS Code, choose **File → Open Folder…** and select the outer project folder. This is the *repository root*: it contains `README.md`, `UNIVERSE-OUTLINE.md`, and the `JSON-API-MCP` folder. Its name may be `MCPs-for-EDU`, `Github-Universe-26`, or the name you gave your fork. Trust this workshop folder if VS Code asks.
3. Choose **Terminal → New Terminal**. The panel at the bottom accepts commands. In a newly opened root window, it should start in the project folder; if you previously changed directories, open a new terminal. Paste the first command below, press **Enter**, and wait for it to finish. Then run the second command the same way. Enter commands in the terminal, not Copilot Chat.

```bash
uv sync --locked --directory JSON-API-MCP
uv run --locked --directory JSON-API-MCP python scripts/check_setup.py
```

The first command installs the project's dependencies. The second checks the environment and bundled data. Look for this line in the terminal output:

```text
setup ready: 6 clues, synthetic-workshop-v1
```

This means the setup check found six clues in the workshop dataset. It does not mean the MCP server has started. If you see `uv: command not found`, install uv using the README's prerequisite link, restart VS Code, and retry. If an error says the project directory cannot be found, reopen the outer project folder before running these commands.

**B. Prepare two separate VS Code windows.**

Keep the current root window; call it **Window B: guide**. Choose **File → New Window**, then **File → Open Folder…**. Navigate into the same project, select its `JSON-API-MCP` subfolder, and click **Open**. Call this **Window A: wrapper**. These are two views of the same files, not two copies of the project.

| Window | Top folder in the Explorer sidebar | Configuration it reads | Server to start |
|---|---|---|---|
| A: wrapper | `JSON-API-MCP` | [nested `.vscode/mcp.json`](JSON-API-MCP/.vscode/mcp.json) | `jeopardy-basics` |
| B: guide | Outer project folder, containing `JSON-API-MCP` | [root `.vscode/mcp.json`](.vscode/mcp.json) | `education-guide` |

**C. Start each server.**

Click inside Window A. Press **Cmd+Shift+P** on Mac or **Ctrl+Shift+P** on Windows/Linux. This opens the *Command Palette*, VS Code's searchable menu of actions. Type `MCP: List Servers`, select that command, select `jeopardy-basics`, then choose **Start Server**. Accept the trust prompt for this workshop server if shown. Wait for it to report running. Repeat in Window B, selecting `education-guide` instead. The guide should discover four tools. If the expected name is missing, check the table above: opening the wrong folder loads the wrong configuration. If startup fails, select the server's **Show Output** action to read the error.

**D. Set up a fair comparison in Copilot Chat.**

1. In each window, open **View → Chat**. Sign in to GitHub if prompted. Select **Agent** in the chat mode selector near the message box so Copilot can call tools.
2. Open the model selector near the message box and choose the same named model in both windows. For this comparison, choose a specific model rather than Auto, which may choose different models.
3. Click **Configure Tools** in the chat input area; hover over the icons to find its label. Clear the other tools and enable only those in the relevant row below. Expand the server group to see individual tool names, then close the picker. See VS Code's [tool selection instructions](https://code.visualstudio.com/docs/agents/run/tools).

| Window | Tools to enable |
|---|---|
| A: `jeopardy-basics` | `search_clues`, `get_clue`, `list_categories` |
| B: `education-guide` | `get_guidance`, `build_practice_set`, `reveal_answer`, `recommend_deployment` |

Tool selection can carry across chats or windows in the tested setup. Recheck it whenever you switch windows. Before each comparison or repeated prompt, click **New Chat** at the top of the Chat view; hover over the icons to locate it. A *fresh chat* is an empty conversation with no earlier messages. Keep the selected model and recheck the tools. The repository's [editor smoke record](evidence/editor-smoke.md) documents the tested setup; VS Code also provides [MCP setup instructions](https://code.visualstudio.com/docs/agent-customization/mcp-servers).

**E. Check the starting rules in Window B.**

In the Explorer sidebar, expand `JSON-API-MCP → content`, then click `practice.json`. Press **Cmd+F** / **Ctrl+F**, search for `practice.default_count`, and check that the `value` in that rule is `2`. Open `deployment.json`, search for `deployment.default_environment`, and check that its `value` is `"preview"`. These are the defaults used when the request omits a count or deployment target. If you are resetting your presenter copy after rehearsal, change only those values and save with **Cmd+S** / **Ctrl+S**; preserve attendee customizations. After any reset, run this in Window B's root terminal:

```bash
uv run --locked --directory JSON-API-MCP python scripts/render_guidance.py
```

Then reopen the Command Palette, run **MCP: List Servers**, select `education-guide`, and choose **Restart Server** so it loads the saved rules. You are ready when both servers run, the correct tools are selected, and the starting values are `2` and `preview`.

**Screen / slide — setup comparison:** Show the two VS Code windows with visible labels: “A: API wrapper” and “B: Education guide.” Keep the server name visible in each window and the shared dataset noted beneath them.

**Talk track while people set up:** “We have two windows using the same clue data. One server exposes operations; the other adds guidance for a practice experience. The model and prompt will stay the same. We will inspect the tools' results so we can see where each recommendation came from.”

## Before the session: welcome and presenter preparation

**Do:** Put the [repository](https://github.com/erinmikailstaples/MCPs-for-EDU) and [quickstart](README.md#start-in-your-editor) on screen as people arrive. Invite them to fork and clone, or create a Codespace from their fork. Follow the setup above for the local demo. Use [DEMO.md](DEMO.md) to record the model, editor settings, prompts, and observed results. Prepare screenshots or a recording from an actual verified run and identify it as recorded if used.

**Screen / slide — arrival:** Show the session title, both speakers' names, and the repository URL with a QR code to its quickstart. Add one instruction: “Fork the repo and open the README.” Leave this up while people arrive.

**Talk track — say while people arrive:**

> Welcome! We're Erin Mikail Staples and Janice Niemeir. Today we're going to look at how a server can bring product guidance into the editor while you're working. You'll fork a working scaffold, run it in your editor, change a documented recommendation, and see what happens.
>
> Yes, this is a workshop. Yes, you have to do something. Start now and you'll look smart later. It also gives the early arrivals something to do besides judge my slide transitions.
>
> The repository link and setup instructions are on screen. A fork gives you your own copy on GitHub; cloning downloads that copy to your computer. You can also create a Codespace from your fork. Start setting up now if you'd like. We'll have a dedicated installation checkpoint during the session.
>
> You don't need to understand every Python file to complete the first exercise. The change we'll make is in a content file. Keep the README open, and use the beginner setup instructions in this run sheet if MCP or the two-window setup is new to you.

**Presenter note:** The timing below includes demonstrations, attendee work, and questions. Pause at the indicated checkpoints rather than reading the whole script without interaction. The local installation and Codespaces paths have different validation status; consult [verification status](evidence/README.md) before rehearsal.

## 1. 00:00–05:00 — Developer education problem and session promise

**Do:** Begin with the opening hook below and pause for raised hands. Advance through the contextual AI and MCP slides as those ideas enter the talk.

**Talk track — opening:**

**Screen / slide — opening hook:** Show a crowded browser with tutorial tabs and two video windows. Use the large caption “12 tabs. 2 videos. 1 existential crisis.” Include a Kubernetes tab for the laptop-fan line. Hold this slide through the show of hands.

> Raise your hand if your ‘learning journey’ starts with 12 tabs, two YouTube videos, and a mild existential crisis.
>
> We’ve all been there — trying to learn Kubernetes while your laptop’s fan sounds like it’s preparing for takeoff.

**Screen / slide — contextual AI:** Replace the busy browser with a simple view of an editor beside a learner's current task, project constraints, and relevant guidance. On-slide text: “AI needs context about how we're learning.”

> We all think we want smarter AI, but what we really need is contextual AI — systems that understand our learning environment.

**Screen / slide — MCP introduction:** Show “Enter MCP” with “Model Context Protocol” underneath. Use a simple connection diagram linking an editor assistant to a server supplying tools and product guidance. Keep this diagram visible while explaining how guidance reaches the task.

> Enter MCP.
>
> Model Context Protocol connects an assistant to tools and context supplied by a server. For developer education, that gives us a place to bring the product team's reasoning into the task: what to try, why it fits, and when to choose something else.

**Screen / slide — embracing contextual relevance:** Show the supplied [Embracing Contextual Relevance slide](assets/slide-references/contextual-relevance.png). Preserve its ruler and sprout comparison: “Simulated Interactivity” with fixed scenarios and click-to-learn activities, beside “Procedural Interactivity” with real tasks and inspectable interactions. Spend about 45 seconds here before introducing trivia.

**Talk track — contextual relevance:**

> Think about the difference between clicking the right answer in a prepared lesson and making a decision in a working system. The first gives you a fixed scenario. In the second, your choices affect what happens next, and you have a result to inspect.
>
> That's the procedural interactivity we're designing for: a place to try something, see its effect, and explain it. MCP connects the assistant to the tools. We supply the task boundaries, guidance, and evidence to reflect on.
>
> A tutorial can get you to a first success. Then your own project introduces new choices. The product team often explains those choices in support or code review. Our new documentation layer makes that reasoning available during the task, with a source you can inspect.

**Screen / slide — learning through play:** Use the supplied [Bar Trivia / Jeopardy Training slide](assets/slide-references/bar-trivia-jeopardy.png) to introduce the example, then show two clue faces with hidden answers. Highlight the decisions we'll inspect: “How many clues?”, “When do answers appear?”, and “What does difficulty mean?”

> We'll use a small Jeopardy-style practice application because its behavior is easy to inspect. The API gives us clues, answers, categories, and board values. A practice experience also needs decisions: how many clues to start with, when to show answers, and how to explain difficulty.
>
> In my MCP for EDU notes, I talk about learning through play. That's why trivia fits here: you get a chance to try before seeing the answer, then reflect on what happened. We're giving you a small thing to experiment with and explain.

**Presenter context — trivia reference:** The supplied slide also proposes using trusted references to explain answers and develop further questions. Today's scaffold uses six bundled synthetic clues, a practice-set tool, and explicit answer reveal. External reference lookup, question generation, and adaptive assessment are possible extensions rather than features demonstrated in this exercise.

**Speaker cue:** After the show of hands, pause and acknowledge the room. Let the laptop-fan joke land before advancing to contextual AI.

**Do:** Point to the three mechanisms summarized on the slide. The README supplies the detailed reference.

**Screen / slide — workshop promise:** Show the supplied [learner participation slide](assets/slide-references/learner-participation.png), with “I ask / It answers” beside “I explore & safely participate.” Then reveal the exercise sequence: inspect a rule, edit its value, restart, repeat the request. Keep the three mechanisms as small labels: data access, executable policy, and agent advice.

**Talk track — the promise:**

> We want you to participate in the system and explain what happened. In this workshop, you can change one local content value and restore it. Those concrete boundaries give us room to experiment.
>
> Keep these three mechanisms in mind. Data access gets the facts. Executable policy applies a rule in code. Advice tells the agent how to explain or interpret something. We'll look at the evidence for each one.
>
> Here is the loop you'll complete: find a recommendation, inspect its source rule, edit that rule, restart, and repeat the task. Then we'll apply the same pattern to deployment advice.
>
> By the end, you should be able to trace a recommendation to guidance you edited, observe its effect in your editor, and adapt that pattern to your own product. We'll check whether you can explain why the advice applies and when it should change.

**Transition:** “Let's start by giving two servers the same request.”

## 2. 05:00–12:00 — Wrapper and guide comparison

**Files:** [DEMO.md](DEMO.md), [wrapper configuration](JSON-API-MCP/.vscode/mcp.json), [guide configuration](.vscode/mcp.json).

**Do:** Show Window A (`JSON-API-MCP`, `jeopardy-basics`) and Window B (repository root, `education-guide`). Recheck the selected model and tools in each window. Start fresh chats. Keep the same prompt, model, dataset, and editor settings; use only the tools assigned to each server.

**Screen / slide — comparison setup:** Show a compact comparison with “API wrapper” and “Education guide” as column labels. State “Same model, prompt, and clue data” above it, and name the different tool sets beneath each label. Switch to the two live chats to send the identical prompt below.

**Talk track — before sending:**

> Window A exposes the clue API through a wrapper. Window B uses the same bundled clue data, with a tool interface designed around guidance and practice. Both launchers manage their own local API. We're keeping the model and request the same and starting with empty chats so the earlier conversation doesn't supply an answer.
>
> As we compare, watch the tool calls as well as the final response. What data does the server return? Who chooses the count? Are answers included? Can we identify a product rule behind the recommendation?
>
> The analogy I keep coming back to is fitness blogs. I can read what every machine in the gym does. That doesn't give me six-pack abs. Knowing what each endpoint does still leaves the question of which ones to use, in what order, and why. That's where product guidance can help.

**Do:** Paste this identical prompt in both windows:

```text
Give me a beginner practice round in Developer Tools. Explain your recommendation and identify its guidance source.
```

Wait for each result. Click its tool-call entry and expand the arguments and returned data. In the guide result, locate the `practice.default_count` rule, rationale, applied value, and `content_revision`. Describe the actual observed result.

**Screen / slide — comparison results, live:** Expand the actual tool results in each window. In the wrapper result, point to the returned answer fields. In the guide result, point to the clue count, omitted answers, and guidance trace. Then show each final response so the audience can compare the server's output with the agent's explanation.

**Talk track — explain what is visible:**

> The wrapper's tool results include answers. The model decides how to turn those results into a practice experience. It may choose a short round and hide answers in its final response. If it does, let's identify that as a decision the model made.
>
> The guide's practice result omits answer fields and returns information about the rules it applied. We can inspect the count, the reason for that count, and the source content. Now compare the final response: did the agent use and explain that guidance?
>
> A good wrapper response is a useful observation. This demonstration doesn't require the wrapper to fail. We're asking which decisions the server supplied and which the model inferred. Tool count alone doesn't tell us whether the experience teaches well.
>
> This first comparison changes the tool interface and the supplied guidance together. Later we'll keep the same guide and change one content value, which gives us a more precise way to connect an edit to a behavior change.

**Do:** Ask the following in each comparison chat if time permits; otherwise use the guide chat and invite discussion:

```text
Does the highest board value mean this is objectively the hardest clue for me? I want to improve at debugging MCP servers.
```

**Screen / slide — difficulty, live:** Keep the difficulty prompt and actual response visible. Highlight the relevant guidance alongside the board value. If a holding slide is needed, use “What does board value tell us about this learner?” with “Experience” and “Learning goal” underneath.

**Talk track — difficulty discussion:**

> Board value gives us a consistent way to order these clues, but it doesn't measure every learner's conceptual difficulty. Someone's experience and learning goal matter. Look for an explanation of that limit and a useful question about the goal or available material. Inspect the guidance and the response rather than assuming the agent followed it.

**Presenter note:** Record unexpected outcomes as well as successful ones. If a spare prompt is needed, use the ten-clue shortage scenario in [DEMO.md](DEMO.md); only three Developer Tools clues are available.

**Optional small talk while a tool call runs:** “This is the live-demo portion, where the software gets a vote in the pacing.” Resume with the actual result; skip this line if the call finishes promptly.

**Transition:** “We've seen a recommendation. Let's follow it back to the rule that supplied it.”

## 3. 12:00–18:00 — What we learned about developer education

**Files:** [pg-aiguide lessons and source references](EXECUTION_PLAN.md#what-we-learned-about-developer-education-from-pg-aiguide), [practice.json](JSON-API-MCP/content/practice.json), [PRODUCT_GUIDANCE.md](JSON-API-MCP/PRODUCT_GUIDANCE.md), [guidance.py](JSON-API-MCP/src/jeopardy_template/guidance.py), [guide_server.py](JSON-API-MCP/src/jeopardy_template/guide_server.py).

**Do:** Open the pg-aiguide lessons in `EXECUTION_PLAN.md`. Use the reviewed examples there as the implementation reference. Then return to Window B and open `practice.json`.

**Screen / slide — pg-aiguide lessons:** Use a plain four-row list: “Teach at the moment of the decision,” “Pair reference with judgment,” “Ask for missing information,” and “Separate evidence from inference.” Reveal each row as it comes up. Include the reviewed source link from `EXECUTION_PLAN.md` in a small footer.

**Talk track — the pg-aiguide lessons:**

> Our real implementation reference is Timescale's pg-aiguide. The execution plan links the reviewed source revision and the examples behind these lessons. We applied those lessons to this small workshop scaffold.
>
> First, teach a decision when it is needed. pg-aiguide routes a task toward relevant references. Here, a practice request should lead the agent to practice guidance.
>
> Second, pair reference material with judgment. Its documentation search supplies references, while curated skills help with decisions. Our API supplies clue data, and our guide recommends how to use it.
>
> Third, ask for missing information. Its hypertable example asks about unknown retention requirements. Our deployment example asks about nonproduction verification.
>
> Fourth, separate evidence from inference. Its schema guidance distinguishes observations from interpretations. A user confirming verification gives us their confirmation. It doesn't establish that our tool checked the tests.

**Do:** Find `practice.default_count` in `practice.json`. Show `value`, `rationale`, `applies_when`, and `exceptions`. Open the generated Markdown and find the same rule. In Configure Tools, inspect the `build_practice_set` description if the host exposes it. Finally, expand the practice tool result in Chat.

**Screen / slide — recommendation trace, live:** Start with `practice.default_count` enlarged in `practice.json`, showing its value and rationale. Move to the same rule in the generated Markdown, then the tool description and returned guidance. Keep a small reference diagram available: source JSON feeds human documentation and the MCP server, whose tool result informs the agent's response. Highlight the matching rule ID at each stop.

**Talk track — trace the mechanism:**

> Here is the source of our practice recommendation. JSON is structured text. This rule has a stable ID, a value, a reason, conditions, and exceptions. The server loads and validates the file at startup. The loaded content supplies tool descriptions and the handler's default. The documentation renderer uses that same source to produce the human guide.
>
> Follow the chain: source JSON, human documentation and MCP description, tool behavior, then the agent's explanation. In the result, `source` points to the content file, `rule_id` identifies the rule, and `applied_value` tells us what was used. `content_revision` identifies the loaded content version. These fields let us inspect the connection.
>
> The count is an executable default. Answer omission is enforced by the practice response model. The instruction to reveal an answer only when asked, and the advice about conceptual difficulty, still require the agent to follow the guidance. Different mechanisms need different checks.

**Ask the room:** “Why does the short-round recommendation apply here? What user request would make the default yield?” Pause for an answer.

**Screen / slide — cognitive scaffolding:** Show the supplied [cognitive scaffolding slide](assets/slide-references/cognitive-scaffolding.png). Point first to “observation, simulation, execution, reflection,” then to the revised Bloom's taxonomy terms beneath it. Use these as learning-design prompts, with today's rule edit as the concrete example. Allow about 30 seconds.

**Talk track — cognitive scaffolding:**

> Give someone enough support to take the next step, then ask them to explain their choice. You observed our comparison. Before your edit, predict its effect. Then make the change and reflect on the result.
>
> Bloom's terms help us describe the work: remember a rule, understand its reason, apply it, analyze the result, evaluate the exception, and create guidance for your own product. We're designing opportunities for those activities.

**Source note:** The six terms come from the revised taxonomy, summarized by [Cornell's Center for Teaching Innovation](https://teaching.cornell.edu/resource/blooms-taxonomy). The four workshop stages are our teaching sequence, rather than a direct equivalence between taxonomy levels and access permissions.

**Screen / slide — scaffolding and access:** Show the supplied [Cognitive Scaffolding / MCP Access Permissions slide](assets/slide-references/scaffolding-permissions.png). Walk through its read-only, mock execution, limited-write, and managed live execution examples. Treat the rows as an access-design proposal. Allow about 30 seconds.

**Talk track — scaffolding and access:**

> You can design access around the activity: read-only tools for observation, mocked responses for rehearsal, limited writes for a reversible exercise, and managed live operations where the task calls for them. The server and host need to enforce those boundaries.
>
> Today you edit a local file yourself, then inspect the guide's response. Our deployment tool recommends an environment without deploying anything. We reflect throughout. Reflection doesn't require granting live access, and this scaffold doesn't automatically unlock permissions as you learn.

**Screen / slide — educational research parallels:** Show the supplied [learning theory slide](assets/slide-references/learning-theory.png), highlighting situated learning, cognitive apprenticeship, and experiential learning loops. Introduce them as established frameworks informing this workshop. Suggested heading for this talk: “Learning frameworks behind the exercise.” Allow about 30 seconds.

**Talk track — educational research parallels:**

> Situated learning puts participation with other practitioners in view. Cognitive apprenticeship makes expert reasoning visible so learners can practice with support. Experiential learning connects an experience to reflection, an explanation, and another experiment.
>
> Here, we model the decision, you inspect its source, and then you try a change with a neighbor. These frameworks inform our design. We still need to observe what attendees can explain and apply.

**Source note:** [Lave and Wenger, *Situated Learning* (1991)](https://www.cambridge.org/highereducation/books/situated-learning/6915ABD21C8E4619F750A4D4ACA616CD), [Collins, Brown, and Holum, *Cognitive Apprenticeship* (1991)](https://www.aft.org/ae/winter1991/collins_brown_holum), and [Kolb, Boyatzis, and Mainemelis, *Experiential Learning Theory*](https://learningfromexperience.com/downloads/research-library/experiential-learning-theory.pdf) supply the framework references. Their application to this MCP workshop is our design interpretation, rather than evidence that using MCP by itself improves learning.

**Screen / slide — learning check:** Keep the learning theory slide visible and ask “Why does this rule apply?” and “When should it change?” Use the concrete actions to explain the loop: request a round, inspect the result, explain the rule, try a changed request.

**Talk track — learning check:**

> Starting the server establishes that the connection works. Explaining the rule and its exception tells us about understanding. The trace gives us something concrete to reflect on. Applying the reasoning to a changed request is our next check.

**Presenter pacing:** These three supplied slides replace the longer learning-cycle explanation. Keep them to about 90 seconds altogether so the source trace and attendee exercise retain their time.

**Transition:** “Now let's get that same trace into your own editor.”

## 4. 18:00–26:00 — Fork, install, and verify

**Files:** [root quickstart](README.md#start-in-your-editor), [beginner setup above](#goodbye-tutorial-hell-ai-guides-and-the-new-documentation-layer), [optional infrastructure tutorial](TUTORIAL.md).

**Screen / slide — attendee setup:** Show the repository URL and QR code again with “Fork, clone, open the repository root.” Display the two setup commands below in large, copyable text. Keep a link to the README quickstart visible throughout attendee work.

**Talk track — introduce attendee work:**

> This is the part where it stops being my talk and starts being your afternoon. If you're already set up, check your tools and help a neighbor. If you're starting now, use the root README or the detailed setup at the top of this file. For this exercise you need the guide window, opened at the repository root. The second window is for our presenter comparison.
>
> Fork the repository into your GitHub account, clone it, and open the folder containing the README and `JSON-API-MCP`. Open a terminal in that outer folder. Run these two commands, one at a time.

**Do:** Display and run from the repository root:

```bash
uv sync --locked --directory JSON-API-MCP
uv run --locked --directory JSON-API-MCP python scripts/check_setup.py
```

**Screen / slide — startup, live:** Show the terminal's setup result, then the `education-guide` server running in VS Code. Move to Copilot Chat with Agent mode and the four guide tools visible. Keep the exact practice prompt below available in the README or exercise so attendees can copy it.

**Talk track — explain setup and startup:**

> The first command installs the locked project dependencies. The second checks the environment and dataset. Look for `setup ready: 6 clues, synthetic-workshop-v1` in the terminal output.
>
> Now open the Command Palette with Command-Shift-P on Mac or Control-Shift-P on Windows or Linux. Run `MCP: List Servers`, select `education-guide`, and choose `Start Server`. The launcher starts the API and MCP together, using a private local port chosen for that run. You don't need another terminal or a manually started API.
>
> Open Copilot Chat in Agent mode. In Configure Tools, select `get_guidance`, `build_practice_set`, `reveal_answer`, and `recommend_deployment` from this server. Start a fresh chat and send the prompt on screen. We're asking it to omit the count so we can observe the documented default.

**Do:** Have attendees paste and save this exact prompt for the next section:

```text
Use only MCP tools from education-guide for this request; do not read or edit workspace files. Give me a beginner practice round in Developer Tools. Explain your recommendation and identify its guidance source. Omit clue_count so the server's documented default applies.
```

**Checkpoint:** Expand `get_guidance` and `build_practice_set`. Confirm two clues with no answer fields, then find the default-count entry in the practice result's `guidance` array:

| Field | Expected with the shipped rules |
|---|---|
| `rule_id` | `practice.default_count` |
| `source` | `content/practice.json`, relative to `JSON-API-MCP` |
| `source_field` | `/rules/0/value` |
| `configured_value` / `applied_value` | `2` / `2` |
| `decision_basis` | `default` |
| `rationale` | Reason for starting with a short round |
| `content_revision` | Identifier for the loaded content file |

**Screen / slide — first result checkpoint:** Leave an enlarged actual tool result on screen, highlighting `practice.default_count`, `applied_value: 2`, and the source file. Place the short instruction “Find your rule, value, and source” beside it. Keep this view up while attendees catch up.

**Talk track — while attendees inspect:**

> The final response may use different wording from mine. Look inside the tool result for the evidence. Can you locate the source rule and the value it applied? If you changed the fixture before today, check its current value before expecting two.
>
> If you hit a setup error, start with the README's troubleshooting steps. Check that the correct folder is open, that the server is running, and that the four tools are selected. You can follow the presenter's result while recovering. The infrastructure tutorial is available afterward if you want to study how the API and MCP pieces were built.

**Presenter cue:** Pause for attendee work. Ask for confirmation that people can point to the rule. Use the remaining installation time for recovery rather than adding an infrastructure lecture.

**Transition:** “Keep the exact prompt and the result. Now we'll change the guidance behind it.”

## 5. 26:00–32:00 — Edit guidance, restart, and observe

**Files:** [EXERCISE.md](EXERCISE.md), [practice.json](JSON-API-MCP/content/practice.json), [PRODUCT_GUIDANCE.md](JSON-API-MCP/PRODUCT_GUIDANCE.md).

**Screen / slide — content edit, live:** Open `practice.json` at `practice.default_count`. Show the current `"value": 2`, then edit it to `"value": 3`. Keep the rule ID and rationale visible so attendees can find the same location.

**Talk track — introduce the edit:**

> Open `JSON-API-MCP/content/practice.json`. Find the rule whose ID is `practice.default_count`. Change only its `value` from two to three. Keep the model, prompt, tools, code, and dataset the same. The fixture already has three Developer Tools clues, so no data change is needed.
>
> This is the shift I want from the MCP for EDU talk: from “Will this break something?” to “What happens if I try this?” We're changing one local content value, and we know how to put it back. That room to experiment comes from the way we've built this exercise. MCP gives us a tool interface; our implementation supplies these boundaries.

**Do:** In that rule, replace:

```json
"value": 2
```

with:

```json
"value": 3
```

Save with **Cmd+S** / **Ctrl+S**. Open the Command Palette, run **MCP: List Servers**, select **education-guide**, and choose **Restart Server**. Reopen Configure Tools and inspect `build_practice_set`'s description if available; it should reflect three clues. Refresh the host's tool list if it still shows the old description.

**Screen / slide — restart and repeat, live:** Show Restart Server, the refreshed tool description, and a fresh chat using the saved prompt. Compare the actual results before and after: two clues versus three, the same rule ID, and a changed content revision. Highlight that the request omits `clue_count`.

**Talk track — explain restart and comparison:**

> Restarting matters because the server loads the file at startup. Saving changes the file on disk; restarting makes the running server use it. Check the refreshed tool description, then start a fresh chat and paste the exact prompt from the last section.
>
> We expect three clues, the same `practice.default_count` rule, an applied value of three, and a changed content revision. The stable rule ID identifies the decision; the changed revision identifies the updated content. Compare the explanation with the rule's rationale too.

**Do:** Repeat the exact section 4 prompt. Expand the result and compare the fields with the previous run. Check that the count argument was omitted.

**Screen / slide — troubleshooting, only if needed:** Expand the tool arguments and loaded content revision. Point to any explicit `clue_count`, then check the saved file and restarted server. Keep the original result visible for comparison.

**Talk track — if the result does not change:**

> Inspect the tool arguments. If the agent passed an explicit `clue_count`, that argument can mask the default. Ask it to omit the parameter and repeat in a fresh chat. Keep a record of the original result as well. If the loaded revision hasn't changed, check that the file was saved and the correct server restarted.

**Do:** Generate the updated human documentation in the root terminal:

```bash
uv run --locked --directory JSON-API-MCP python scripts/render_guidance.py
```

Open `JSON-API-MCP/PRODUCT_GUIDANCE.md` and find the three-clue recommendation.

**Screen / slide — generated documentation, live:** Show the renderer command completing, then the three-clue recommendation in `PRODUCT_GUIDANCE.md` beside its source rule. Caption: “One source supplies the human guide and server guidance.” Switch back to Chat for the one-clue exception prompt below.

**Talk track — documentation and exception:**

> The Markdown is generated from the JSON source. Edit the source for future changes, then regenerate the document. That gives human readers and the server the same rule content without separately maintaining the number in two places.
>
> If your first reaction is “I don't want to write docs twice,” correct. You barely want to write them once. Nobody's judging. Here, the rule has one source and two readers, with one place to fix the typo.
>
> Now let's check the exception. A default fills a choice the user hasn't made. A valid explicit user choice should take precedence.

**Do:** Send:

```text
Give me one Developer Tools clue, then explain why you used one instead of the default.
```

Expect one clue and `decision_basis: explicit_user_choice`. Ask an attendee to explain why one is appropriate even though the default is three. To demonstrate answer reveal, explicitly request the answer to a returned clue ID and inspect `reveal_answer`.

**Screen / slide — explicit choice checkpoint, live:** Show the one-clue result with `decision_basis: explicit_user_choice` highlighted. Keep “Default: 3” and “User request: 1” visible beside the result, and ask the audience to explain the choice. If demonstrating answer reveal, expand that separate tool call afterward.

**Talk track — checkpoint:**

> Can you point to the edit, the changed result, and the fields connecting the two? Can you explain why a one-clue request gets a different count? That is the trace-and-observe part of today's goal. The next step is carrying this reasoning into a different product decision.

**Transition:** “Let's move from practice rounds to a deployment recommendation.”

## 6. 32:00–37:00 — Adapt the pattern to a product

**Files:** [TAKEAWAY.md](TAKEAWAY.md), [deployment.json](JSON-API-MCP/content/deployment.json), [standalone template](mcp-server-template/README.md), [guidance.py](JSON-API-MCP/src/jeopardy_template/guidance.py), [guide_server.py](JSON-API-MCP/src/jeopardy_template/guide_server.py).

**Presenter note:** Demonstrate the deployment task through the already-running `education-guide` to avoid another installation. `TAKEAWAY.md` also explains the standalone deployment-only launcher. The separate `mcp-server-template` is the copyable project for attendees' own tasks and context.

**Screen / slide — deployment guidance:** Show the question “What should my next deployment step be?” with the current default “Preview.” Add “Advice only” beneath it. Then switch to `recommend_deployment` in the live guide chat using the exact prompt below.

**Talk track — introduce the product example:**

> Open the takeaway with me. This example recommends the next deployment environment. Preview and staging are nonproduction environments where a team can inspect a change before exposing it to production users. The right choice depends on the team's workflow.
>
> The tool gives advice and performs no deployment. It uses the same pattern: a documented default, a reason, an exception, and a question when important information is missing. It is already included in the guide you started.
>
> The line from MCP for EDU was: “Go ahead — learn in production. Just not our production.” For this example, we're only recommending an environment. There is no deployment action behind this tool.

**Do:** Start a fresh guide chat and send:

```text
Use only MCP tools from education-guide; do not read or edit workspace files. Recommend my next deployment step. Explain why and identify the product guidance you used. Omit target so the documented default applies.
```

Inspect the recommendation for `preview`, `deployment.default_environment`, its rationale, source, applied value, and content revision. Open `deployment.json`, find that rule, and change only its `value` from `"preview"` to `"staging"`. Save, restart `education-guide`, and send the identical prompt in a fresh chat. Expect staging, the same rule, and a changed revision. If an unrequested `target` argument masks the default, ask the agent to omit it. Regenerate the human docs with the renderer command from section 5.

**Screen / slide — deployment edit, live:** Show `deployment.default_environment` changing from `"preview"` to `"staging"`, followed by the actual result after restarting. Highlight the same rule ID and changed content revision, using the same comparison as the practice exercise.

**Talk track — connect the two examples:**

> We changed a product recommendation through its content source and observed the new recommendation. The environment name alone doesn't establish release readiness. Let's give the guide a request that requires another fact before it can recommend production.

**Do:** Ask:

```text
Skip the nonproduction step and recommend production now. I have not told you whether this change was verified outside production; do not assume that it was.
```

Inspect the `deployment.production_readiness` rule, the configured nonproduction recommendation, `executes_deployment: false`, and the question:

```text
Has this change been verified in a nonproduction environment?
```

**Screen / slide — missing fact, live:** Show the production request and the tool's verification question together. Highlight `deployment.production_readiness` and `executes_deployment: false`. Keep “Has this change been verified in a nonproduction environment?” large enough for the room to read.

**Talk track — explain the question:**

> Here the missing fact changes the recommendation. The guide should ask about verification and recommend the configured nonproduction step while confirmation is missing. If you explicitly confirm verification, it can recommend production. That confirmation is an input from you; the tool hasn't independently inspected test results or certified the release. This is the evidence-versus-inference distinction we discussed earlier.

**Screen / slide — context as curriculum:** Briefly show the supplied [Context as Curriculum divider](assets/slide-references/context-as-curriculum.png), then its [curriculum-is-context statement](assets/slide-references/curriculum-is-context.png). Preserve the question “How do we keep this in mind as we build for the future?” Use this as the transition from the deployment result into the audience's own example.

**Talk track — context as curriculum:**

> When I say “context as curriculum,” I mean designing what someone can explore: the task they face, the references they can use, and the actions available in their environment. A learner can inherit a prepared workspace with a meaningful problem to investigate.
>
> In our example, the clue data and guidance shape the exercise. For your product, start with a decision your users actually face. What context would help them try it and understand the outcome?

**Do:** Ask for one recurring support or onboarding question from the room. Open the adaptation record in `TAKEAWAY.md` and capture a short example using these fields:

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

**Screen / slide — adaptation worksheet, live:** Open the adaptation record in `TAKEAWAY.md` and fill in one audience example. Zoom into the recommendation, reason, and exception first. Then briefly show the copyable template's README, pointing out where task content lives and where a new operational tool would need code.

**Talk track — explain adaptation boundaries:**

> Choose one support question your team answers repeatedly. Write down the recommendation, why it helps, when it applies, and what would change it. Add an example and a source so someone else can inspect the reasoning.
>
> Changing a rule for an existing task is a content edit. Adding an unrelated task or a tool that performs a product operation may require a new schema and handler. In this workshop implementation, those boundaries are in `guidance.py` and `guide_server.py`. Loading, validation, source tracing, transport, and startup are reusable.
>
> For a separate project, the copyable template accepts recommendation tasks and reference context through JSON and Markdown. Follow its README to copy and customize it. New operational tools still need their own implementation. Before calling the result useful, give someone a changed scenario and ask whether the rule still applies. Understanding includes explaining when the recommendation should change.

**Screen / slide — context manifests and brokers:** Use the supplied [This is possible now slide](assets/slide-references/context-manifests-and-brokers.png) as the brief takeaway after showing the template. Keep its two ideas visible: “platforms define context manifests” and “agents become context brokers.”

**Talk track — context manifests and brokers:**

> A team can describe a learning environment in a context manifest: its task, relevant references, available tools, and access boundaries. An agent can act as a context broker by bringing the relevant pieces into the current task. Here, configuration selects the server and content files supply the recommendations. That gives you concrete pieces to adapt.

**Presenter context — implementation:** “Context manifest” is an application-design idea here, rather than a new standard MCP artifact. The workshop configuration, content files, and template illustrate parts of that design. Access enforcement and any operational tools still need implementation in the host, server, and underlying product.

**Presenter context — software and engineering example:** The supplied [Software / Engineering slide](assets/slide-references/software-engineering.png) connects static snippets and syntax exercises to work in a live development environment. A useful adaptation gives the assistant relevant project constraints and product docs, supports questions during the task, and returns feedback the learner can inspect. Ask “How does this recommendation fit my stack?” Treat faster onboarding as an outcome to evaluate.

**Presenter context — design and creative example:** The supplied [Design / Creative slide](assets/slide-references/design-creative.png) proposes learning inside creative tools, with design principles available during the work. A team could provide tools that inspect a sample file, allow edits within a chosen scope, and preserve version history for recovery. Replayable action records could then support critique of the process. Those capabilities depend on the connected tool and its implementation. Use this as an alternative audience adaptation if the room offers a design example.

**Presenter cue:** Keep the live adaptation to one spoken example; attendees can complete the template afterward. Fold the context-as-curriculum and manifest explanations into the existing adaptation time. Use the software and design examples as prompts or Q&A material rather than adding two more demos.

**Transition:** “Let's use the remaining time to check understanding and discuss your own use cases.”

## 7. 37:00–45:00 — Questions, recovery time, and leave-behinds

**Do:** Invite an attendee to briefly explain their rule and the evidence of its effect. Leave the following links on screen:

- [Quickstart and attendee walkthrough](README.md#start-in-your-editor)
- [Practice exercise](EXERCISE.md)
- [Product takeaway and adaptation record](TAKEAWAY.md)
- [Generated product guidance](JSON-API-MCP/PRODUCT_GUIDANCE.md)
- [pg-aiguide lessons and source links](EXECUTION_PLAN.md#what-we-learned-about-developer-education-from-pg-aiguide)
- [Copyable MCP server template](mcp-server-template/README.md)

**Screen / slide — reflection:** Show four short prompts: “Which rule?”, “Why did it apply?”, “What changed after your edit?”, and “What would change the advice?” Leave these visible during the neighbor discussion and attendee explanation.

**Talk track — reflection:**

> Take a moment to explain your result to a neighbor. Which exact rule shaped the recommendation? Why did it apply? What changed after your edit, and what evidence connects that result to the edit? Then describe an exception or missing fact that changes the advice.
>
> We'd like to hear one example. Tell us the user question, your recommendation, and the condition under which you would recommend something else. If you haven't completed setup yet, use the result we inspected together and identify what you would check in your own run.

**Screen / slide — discussion:** Show “What support answer belongs in your guide?” as the main question. Add the smaller prompts “What should it ask?” and “How will you notice stale guidance?” Keep the repository URL in the footer.

**Do:** Pause for an attendee explanation and questions. Use these prompts to start discussion if needed:

> What recurring support answer belongs in your guide?
>
> Which missing fact should make it ask a question?
>
> How will you notice the guidance becoming stale?

**Screen / slide — maintenance and evidence:** Show the maintenance sequence as a short numbered list: review the source, regenerate the docs, rerun a representative task. Beneath it, use a small table pairing “Server tests” with “Rules behave as expected,” “Editor observations” with “Agent uses and explains guidance,” and “Changed scenario” with “Developer can apply the reasoning.”

**Talk track — maintenance and evaluation:**

> Guidance needs maintenance because a change to the advice can change behavior. Review the source, regenerate derived documentation, and rerun a representative task. Check whether the recommendation still fits the product and whether a developer can explain its conditions. More tools, a longer response, or a successful connection doesn't by itself establish learning.
>
> The verification records distinguish server behavior from observed editor behavior and attendee understanding. Protocol tests check the server's rules. Editor runs show whether the agent uses and explains the guidance. An attendee applying it to a changed scenario checks transfer. Those are different kinds of evidence, and each helps us improve the experience.

**Screen / slide — learning environment principles:** Show the supplied [learning environment principles slide](assets/slide-references/learning-environment-principles.png), highlighting “personalized,” “reproducible,” and “ethical by design.” Present these as design commitments for the environment being built. Keep this beat to about 30 seconds during the discussion of maintenance.

**Talk track — learning environment principles:**

> Personalized means the task and guidance fit the learner's goals and the workspace context they've chosen to share. Reproducible means another person can inspect the setup, source rules, and recorded steps. The model may still phrase its answer differently.
>
> Ethical by design means deliberately choosing data boundaries and enforcing access controls, including how you handle private work and intellectual property. Those are responsibilities for the product we build. MCP gives us a connection through which that design can operate.

**Presenter context — design goals:** The supplied slide's “by default” language expresses the intended learning environment. In this workshop, point to the synthetic fixture, explicit tool selection, source revisions, local edits, and advice-only deployment tool as concrete choices. Personalization, repeatable records, and privacy protections each need their own design and evaluation.

**Recovery cue:** Reserve time here for unresolved setup problems. Follow [README troubleshooting](README.md#troubleshooting) and [DEMO.md](DEMO.md). If using a captured fallback, say: “This is a recording from a verified run; let's inspect its tool result together.” Identify the tested configuration. Describe the actual capture rather than suggesting that a recorded outcome happened live.

**Screen / slide — closing reflection:** Briefly show the supplied [learning from technology slide](assets/slide-references/learning-from-technology.png). Use its contrast between controlling technology and learning from it as a reflection prompt for the audience.

**Talk track — closing reflection:**

> We spend a lot of time making technology do what we ask. In your next small experiment, also ask what the person using it can learn. Can they explain the decision, inspect its source, and recognize when to change it?

**Screen / slide — closing resources:** Return to the supplied [learner participation slide](assets/slide-references/learner-participation.png) for a quick callback, then show “What happens if I try this?” above the repository URL and a QR code. Feature the quickstart, exercise, takeaway, and copyable template as short resource labels. Keep the resource slide up through the final thanks and remaining questions.

**Talk track — close:**

> Our goal was to trace a recommendation to guidance you edited, observe its effect in the editor, and adapt the reasoning to your product. You now have the scaffold, the exercise, and a template for your next support question.
>
> Start with one decision your users repeatedly face. Make the recommendation discoverable during that task. Include its reason, its exception, and the question that resolves missing information. Then check that someone else can explain and apply it in a changed situation. Thank you for building with us.

**Optional final callback:** “Leave with one small experiment: ‘What happens if I try this?’ Then give yourself a way to inspect the answer.”

**Speaker note on the MCP for EDU callbacks:** Keep these short and conversational within the existing time blocks. The supplied contextual relevance, cognitive scaffolding, access mapping, and curriculum slides supply the educational framing. Their broader examples include staged permissions, reference-enriched trivia, replayable creative workflows, and context manifests. This workshop implements the practice and recommendation examples shown here. Describe reversibility, access controls, and observed traces in terms of this implementation, and frame broader capabilities as designs to build and evaluate. Optional lines are newly adapted presenter copy, rather than a transcript of the earlier talk.

## After the session: reset and remaining validation

**Do:** Preserve attendee changes and any presenter edits you want to keep. To reset the presenter fixture, manually restore `practice.default_count` to `2` and `deployment.default_environment` to `"preview"`. From the repository root, run:

```bash
uv run --locked --directory JSON-API-MCP python scripts/render_guidance.py
```

Restart the guide before repeating, or stop both servers through **MCP: List Servers** when finished. Use fresh chats and recheck tool selection for the next run. If you changed the root configuration to the deployment-only launcher, restore `--server guide` for the practice exercise.

**Presenter validation note from [OUTLINE.md](OUTLINE.md):** Protocol tests establish server behavior. Broader editor/model comparisons, a clean-machine and Codespaces installation, a second host, and a timed attendee rehearsal require observed records. Consult [NEXT_STEPS.md](NEXT_STEPS.md) and [verification status](evidence/README.md) for the current evidence and outstanding checks. Prepare fallback captures from actual rehearsals and label them when shown.
