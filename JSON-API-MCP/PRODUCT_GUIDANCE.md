# Product guidance

Generated from `content/*.json`. Edit the source, then run `uv run --locked python scripts/render_guidance.py`.

Defaults fill omitted choices. Valid user choices override defaults. Handler constraints still apply. Advisory guidance informs the agent; it does not enforce arbitrary prose as code.

## Build a useful practice round

The learner wants to practice, study, or be quizzed. Retrieve this guidance when choosing a practice approach.

### practice.default_count

Source: `content/practice.json` · Mechanism: `default`

Start with 2 clues when the learner does not specify a count.

**Why:** A short round leaves time to review mistakes before continuing.

**When:** The learner requests a practice round without a count.

**Exceptions:** Honor an explicit count from 1 to 10; disclose when fewer matching clues exist.

**Avoid:** Filling a round with unrelated clues to meet the requested count.

**Example request:** Give me a beginner practice round in Developer Tools.

**Example behavior:** Recommend 2 clues, hide answers, and explain the short-round default.

### practice.answer_visibility

Source: `content/practice.json` · Mechanism: `constraint`

Keep answers out of practice results; reveal a specific answer only when asked.

**Why:** The learner needs an opportunity to attempt the clue before seeing its answer.

**When:** Building any practice set.

**Exceptions:** Use reveal_answer when the learner explicitly asks for an answer.

**Avoid:** Returning raw API search results that contain answers as a practice set.

**Example request:** Quiz me on developer tools.

**Example behavior:** Return prompts and IDs; offer to reveal an answer after an attempt.

### practice.difficulty

Source: `content/practice.json` · Mechanism: `advisory`

Use lower board values first for beginner practice and higher values first for advanced practice, while disclosing this rough proxy.

**Why:** Board value provides a reproducible ordering, but does not measure universal conceptual difficulty or the learner's knowledge.

**When:** Choosing a progression within the matching clues.

**Exceptions:** Ask about the learner's topic or goal when they require conceptual difficulty; Final Jeopardy has no fixed board value and is placed last.

**Avoid:** Claiming that the highest-value clue is objectively the hardest for everyone.

**Example request:** Find the objectively hardest material so I can master it.

**Example behavior:** Explain the proxy's limit and ask which concepts the learner wants to improve.

## Recommend the next deployment step

The developer asks where to deploy next or proposes a first production release. This example provides advice and never performs a deployment.

### deployment.default_environment

Source: `content/deployment.json` · Mechanism: `default`

Recommend preview when the developer has not selected an environment.

**Why:** A nonproduction release lets the developer inspect behavior before exposing a change to users.

**When:** The developer has not specified a deployment target, or production readiness is unconfirmed.

**Exceptions:** Honor an explicit preview or staging target; a production recommendation also requires confirmed nonproduction verification.

**Avoid:** Assuming that a successful build establishes production readiness.

**Example request:** Recommend my next deployment step.

**Example behavior:** Recommend preview, explain the rationale, and identify this source rule.

### deployment.production_readiness

Source: `content/deployment.json` · Mechanism: `constraint`

Before recommending production, ask whether this change has been verified in a nonproduction environment.

**Why:** A request to ship does not establish that the change was exercised outside production. User confirmation informs this advice; it is not independent release validation.

**When:** The requested or default target is production.

**Exceptions:** When the developer confirms verification, offer production as the next step while noting that team release requirements still apply.

**Avoid:** Inventing test results or claiming that this advisory tool authorizes a release.

**Example request:** Skip preview and ship straight to production.

**Example behavior:** Ask whether the change has been verified outside production and recommend a nonproduction step until that is confirmed.
