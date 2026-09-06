# Sprint 2 Backlog: Requirements Broken Down into Epics, Stories & Tasks

**Who this is for:** every capstone team, working from `Sprint2_Kickoff_Planning_Guide.md` Step 4. Tool-agnostic on purpose — copy whatever's below into a shared doc, a spreadsheet, a physical board, or a tool like Jira or Trello later. Nothing here depends on which one you pick.

**Source grounding:** `capstone/Meridian_Hospitality_Capstone_Case_Study.docx` Section 2 (Shared Starter Baseline) and Section 3 (Sprint 2's deliverable lines, shared across all teams). Epic 1's stories are fully written out because they're identical for every team, grounded directly in the Shared Starter Baseline. Epic 2 and Epic 3 are templates — they depend on your Team Brief (Section 4), so fill in every **[Placeholder]** with your team's own specifics before use.

**How to read this:** an **Epic** groups several Stories that together deliver one bigger piece of Sprint 2. A **Story** is one demonstrable slice of that epic — small enough to estimate, assign, and mark done on its own. A Story's **Tasks** are the actual technical to-dos under it, small enough to finish in under a day.

---

## Epic 1: Cloud Deployment

Everything needed to get the app live on both required clouds. Identical for every team — grounded in the Shared Starter Baseline, not your Team Brief.

### Story 1.1: Deploy the capstone app to a single EC2 instance
**User story:** As the team's DevOps owner, I want the provided Docker image running on a single EC2 instance, so that the app has a public, working AWS endpoint for the rest of the sprint to build against.
**Acceptance criteria:** The Docker image runs on the EC2 instance; the app is reachable at a public URL; the container restarts automatically if the instance reboots.
**Owner role:** DevOps
**Size:** M
**Dependencies:** None — this is a starting point for the sprint.

**Tasks:**
- Launch an EC2 instance sized for the provided Docker image.
- Install Docker (or choose a Docker-ready AMI) on the instance.
- Pull and run the provided Docker image on the instance.
- Open the correct inbound port in the instance's security group.
- Confirm the app loads at the instance's public URL.
- Set the container to restart automatically (a restart policy or a systemd unit).

### Story 1.2: Deploy the capstone app to an Azure App Service container
**User story:** As the team's DevOps owner, I want the same Docker image running as an Azure App Service container, so that the app has a second, independent cloud endpoint matching AWS.
**Acceptance criteria:** The same image runs as an Azure App Service container; it's reachable at its own public URL; its configuration matches the AWS deployment.
**Owner role:** DevOps
**Size:** M
**Dependencies:** None — can run in parallel with Story 1.1.

**Tasks:**
- Create an Azure App Service configured for a container.
- Point it at the same Docker image used for the EC2 deployment (same registry and tag).
- Set the same environment variables and configuration as the AWS deployment.
- Confirm the app loads at the App Service's public URL.
- Run a basic smoke test and confirm it behaves the same as the AWS deployment.

### Story 1.3: Confirm the frontend and API work end-to-end on both AWS and Azure
**User story:** As the team, we want the full app — frontend talking to the API — reachable and working on both cloud URLs at once, so that Sprint 2's deliverable is actually demonstrable, not just individually-deployed pieces.
**Acceptance criteria:** Opening the AWS URL and the Azure URL both show the working frontend, each successfully calling the API and displaying real data.
**Owner role:** Integration
**Size:** S
**Dependencies:** Stories 1.1, 1.2, and at least one Epic 3 story must be done first.

**Tasks:**
- Point the deployed frontend build at the correct API base URL for each cloud.
- Smoke-test the core workflow on the AWS URL.
- Smoke-test the same workflow on the Azure URL.
- Fix any configuration drift between the two environments (environment variables, CORS, base URLs).
- Record both working URLs for the sprint demo.

---

## Epic 2: AI-Assisted Feature Work *(template — fill in from your Team Brief)*

The AI-coding-assistant scaffold and the early prompt prototype for Sprint 3's feature. Both come from your Team Brief, not the shared baseline.

### Story 2.1: Scaffold [Placeholder — feature named in your Team Brief's Sprint 2 AI-assisted build note] with an AI coding assistant
**User story:** As [Placeholder — the app's user this feature serves], I want [Placeholder — what the feature does], so that [Placeholder — the reason, from your Team Brief].
**Acceptance criteria:** The AI-generated scaffold matches the shared data model and API contract; no guest PII appears anywhere in the prompts used; a teammate reviewed the full diff before merging (the review practice from Day 13).
**Owner role:** Frontend/AI
**Size:** M
**Dependencies:** None.

**Tasks:**
- Write a clear description of the feature for the AI assistant — inputs, outputs, and one concrete example, not just a function name.
- Generate the scaffold with the AI coding assistant.
- Review the diff line by line before accepting anything (Day 13's review practice).
- Confirm no guest PII appears anywhere in the prompts used to generate it.
- Merge the reviewed scaffold into the team's codebase.

### Story 2.2: Prototype the prompt for [Placeholder — the Sprint 3 AI feature named in your Team Brief]
**User story:** As the team, we want an early, working prompt for [Placeholder], so that Sprint 3's full build starts from a proven prompt instead of a blank page.
**Acceptance criteria:** The prompt reliably produces the intended output on at least [Placeholder — a small number, e.g. 5] realistic test inputs drawn from your Team Brief's scenario; failure modes are written down, not hidden.
**Owner role:** Frontend/AI
**Size:** S
**Dependencies:** None.

**Tasks:**
- Draft an initial prompt for the Sprint 3 feature named in your Team Brief.
- Test it against a handful of realistic inputs from your Team Brief's scenario.
- Note where it fails, or gives a wrong or unsafe answer.
- Revise the prompt at least once based on those failures.
- Save the final prompt version, plus its test inputs and outputs, for Sprint 3 to start from.

---

## Epic 3: React Frontend for the Core Workflow *(template — fill in from your Team Brief)*

One Story per screen or component your core workflow needs — copy Story 3.1's template as many times as your workflow requires (3.1, 3.2, 3.3, …).

### Story 3.1: Build [Placeholder — component or screen name] for the core workflow
**User story:** As [Placeholder — the workflow's real user, e.g. front-desk staff], I want [Placeholder — what this screen lets them do], so that [Placeholder — the reason, from your Team Brief].
**Acceptance criteria:** The component renders real data from the shared REST API, not mock data; both loading and error states are handled; it matches your Team Brief's description of the core workflow.
**Owner role:** Frontend/AI
**Size:** M
**Dependencies:** The API this component calls must be reachable — either the shared practice API, or Epic 1's deployed API once that's done.

**Tasks:**
- Identify the exact API endpoint(s) this component needs.
- Build the component's UI structure.
- Wire up the state and props this component needs.
- Add the API call, with both loading and error states handled.
- Confirm it renders correctly against real API data, not a hardcoded example.

*(Repeat as Story 3.2, 3.3, … for each additional screen or component.)*

---

## Quick Reference: All Epics & Stories at a Glance

| Epic | Stories | Team-specific? | Typical owner |
|---|---|---|---|
| 1. Cloud Deployment | 1.1 Deploy to AWS, 1.2 Deploy to Azure, 1.3 Confirm live integration | No — identical for every team | DevOps / Integration |
| 2. AI-Assisted Feature Work | 2.1 Scaffold the feature, 2.2 Prototype the Sprint 3 prompt | Yes — from your Team Brief | Frontend/AI |
| 3. React Frontend | 3.1, 3.2, … one per component | Yes — from your Team Brief | Frontend/AI |
