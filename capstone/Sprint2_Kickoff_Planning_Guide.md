# Sprint 2 Kickoff & Planning Guide

**Who this is for:** every capstone team, at the official start of Sprint 2. Work through it together as a team, with your Team Brief and the Shared Starter Baseline (Case Study, Section 2) open alongside this document. By the end, your team will have a written Sprint Goal, a real backlog, and a sprint that's officially started with dates — not just a shared understanding of what Sprint 2 is. This guide is tool-agnostic on purpose: track the backlog in a shared doc, a spreadsheet, a physical board, or a tool like Jira or Trello if your team already has one set up — nothing here requires setting one up first.

**Source grounding:** `capstone/Meridian_Hospitality_Capstone_Case_Study.docx` (Section 2: Shared Starter Baseline; Section 3: Sprint Structure; Section 4: your Team Brief), `capstone/Meridian_Hospitality_Capstone_Trainer_Notes.docx` (Section 1.3: role rotation), and `capstone/Sprint2_Backlog.md` (the actual Epic/Story/Task breakdown this guide's Step 4 uses).

## Before You Start

- Every team member knows where the team will track work this sprint (see Step 3 — this can be decided in the moment, it doesn't need to be set up in advance).
- Your Team Brief (Case Study, Section 4 — your team's entry) is open.
- The Shared Starter Baseline (Case Study, Section 2 — reference architecture, core data model, API contract, stack) is open.
- Confirm who is rotating into which role for this sprint — backend, frontend/AI, integration, DevOps — per the Trainer Notes' rotation requirement. **[Placeholder — replace with your team's actual role assignments for Sprint 2]**.

## Step 1: Recap What Sprint 2 Actually Delivers

This part is shared across every team, word for word from the Case Study — don't rewrite it, just make sure everyone on the team has actually read it before Step 2:

- Use an AI coding assistant (Cursor/Codex) within compliance guardrails — no guest PII in prompts — to scaffold one feature.
- Apply prompt engineering to prototype the AI feature planned for Sprint 3.
- Build a React frontend for the one core workflow specified in your team brief, consuming the shared REST API.
- Deploy the provided Docker image to a single EC2 instance on AWS and to an Azure App Service container on Azure — your team's first live deployment.
- **Deliverable:** AI-assisted code module + working frontend for your core workflow, live on both AWS and Azure.

## Step 2: Write Your Team's Sprint Goal

**Steps:**
1. As a team, reread your Team Brief's "Sprint 2 - core workflow to build" line.
2. Reread your Team Brief's "Sprint 2 - AI-assisted build note" line.
3. Combine the shared deliverable (Step 1 above) with your own two lines from steps 1–2 into one sentence: what you're building, for which workflow, live on which two clouds.
4. Write that sentence down as your Sprint Goal — you'll record it wherever you're tracking the sprint in Step 6. **[Placeholder — replace with your team's actual Sprint Goal sentence]**.

**Expected Result:**
One written sentence naming your team's specific core workflow, the AI-assisted scaffold, and both target clouds — not a restatement of the generic deliverable with nothing team-specific in it.

## Step 3: Choose Where You'll Track This Sprint

No specific tool is required — pick whatever your team can start using in the next five minutes.

**Steps:**
1. As a team, decide where you'll track Sprint 2's work: a shared document, a spreadsheet, a physical board with sticky notes, or a tool like Jira or Trello if your team already has one set up.
2. Set up a place in it for three things: the Sprint Goal (Step 2), the backlog (Step 4), and each story's status (to do / in progress / done).
3. If you don't already have a tool and don't want to set one up right now, `Sprint2_Backlog.md` itself is a valid tracking doc — copy it into your own working copy and update statuses directly in it.

**Expected Result:**
The whole team knows, in one sentence, where to look for and update Sprint 2's status — and getting there took minutes, not a setup project of its own.

**Troubleshooting:**
No common pitfalls noted for this step.

## Step 4: Build the Sprint 2 Backlog

Turn the single Sprint 2 deliverable into separate, concrete stories — one per thread — so each can be estimated, assigned, and marked done on its own. The stories and tasks themselves are already broken down in `Sprint2_Backlog.md` — this step is about bringing them into your own tracking place from Step 3, not writing them from scratch.

**Steps:**
1. Open `Sprint2_Backlog.md` alongside this guide.
2. Copy all of Epic 1 (Cloud Deployment — Stories 1.1, 1.2, and 1.3) into your tracking place exactly as written — it's identical for every team.
3. Copy Epic 2 (AI-Assisted Feature Work — Stories 2.1 and 2.2) into your tracking place, then fill in every **[Placeholder]** using your Team Brief's Sprint 2 AI-assisted build note and Sprint 3 AI feature.
4. Copy Epic 3's Story 3.1 template into your tracking place once per screen or component your core workflow needs (as Story 3.1, 3.2, 3.3, …), filling in every **[Placeholder]** from your Team Brief's description of that workflow.
5. For every story you copied, keep its Tasks list attached — those are what a teammate actually works through day to day, not just the Story line.

**Expected Result:**
Your tracking place lists one story per thread (AWS deploy, Azure deploy, AI-assisted scaffold with the PII guardrail written into its acceptance criteria, prompt-engineering prototype, one story per frontend component, and the live-integration check), each with its own tasks — not one giant "build Sprint 2" entry with no way to track partial progress.

**Troubleshooting:**
- **One story is trying to cover more than one thread** (for example, "build the frontend and deploy it") → Split it, following `Sprint2_Backlog.md`'s epic boundaries. A story that can't be marked done until two unrelated things both happen is a sign it should be two stories.
- No other common pitfalls noted for this step.

## Step 5: Estimate, Assign, and Set Definition of Done

**Steps:**
1. As a team, estimate each backlog story (story points or t-shirt sizes — whichever your team already uses).
2. Assign each story to the teammate whose rotated role it matches this sprint (backend, frontend/AI, integration, DevOps), per the Trainer Notes' rotation requirement.
3. As a team, agree on one Definition of Done that applies to every story this sprint, for example: "code is reviewed by at least one other teammate, the AI-assisted scaffold's diff was reviewed per Day 13's review practice, and the story's acceptance criteria are demonstrated working, not just merged."
4. Write that Definition of Done somewhere visible in your tracking place from Step 3 so it's in view for the whole team for the rest of the sprint.

**Expected Result:**
Every backlog story has an estimate and an assignee matching this sprint's role rotation, and the team has one shared, written Definition of Done — not an unstated assumption that differs teammate to teammate.

**Troubleshooting:**
- **Everyone assigns themselves the frontend stories and no one takes AWS/Azure deployment** → Stop and revisit the role rotation from Trainer Notes 1.3 — it exists specifically so individual contribution across every architectural layer is visible in grading, not just the layer people find most comfortable.

## Step 6: Start the Sprint

**Steps:**
1. In your tracking place from Step 3, write the Sprint Goal from Step 2 somewhere every teammate will see it first.
2. Next to it, write Sprint 2's start date (today) and end date (the last day of Day 14).
3. Mark every story from Step 4 as "to do" — not started, but visibly part of this sprint's scope, not a general backlog for later.
4. Tell the team out loud (or in your team's chat) that Sprint 2 is officially started, so there's one clear moment everyone agrees work has begun.

**Expected Result:**
Anyone on the team can look at your tracking place and immediately see the Sprint Goal, the start and end dates, and every story that's officially in scope for this sprint — not a backlog with no sense of what's "this sprint" versus "someday."

**Troubleshooting:**
No common pitfalls noted for this step.

## Step 7: Run a Short Daily Standup for This Sprint

**Steps:**
1. Pick one fixed time each day of Sprint 2 for a standup, no longer than 10 minutes.
2. Each teammate answers three questions in turn: what I finished since yesterday, what I'm working on today, and anything blocking me.
3. Update any story whose status changed in your tracking place live during the standup, so it stays accurate without a separate update step later.
4. If a blocker comes up that the team can't resolve in the standup itself, note it and follow up right after — don't let the standup itself run long solving it.

**Expected Result:**
Your tracking place's story statuses match what the team just said out loud, every day of the sprint — not something that's accurate on kickoff day and stale by Day 12.

**Troubleshooting:**
No common pitfalls noted for this step.

## Sprint 2 Kickoff Checklist

Before you close this document, confirm all of the following are actually true, not just planned:

- [ ] Every teammate has read the Shared Starter Baseline and your Team Brief's Sprint 2 lines (Step 1).
- [ ] Your team has one written Sprint Goal, specific to your team, not the generic deliverable alone (Step 2).
- [ ] Your team has picked a place to track Sprint 2's work, and it took minutes, not a setup project (Step 3).
- [ ] The backlog has a separate story for AWS deploy, Azure deploy, the AI-assisted scaffold (with the PII guardrail written into its acceptance criteria), the prompt-engineering prototype, each major frontend component, and the live-integration check, each with its tasks (Step 4).
- [ ] Every story is estimated and assigned to match this sprint's role rotation (Step 5).
- [ ] The team has one shared, written Definition of Done (Step 5).
- [ ] The Sprint Goal, start date, and end date (Days 10–14) are written somewhere visible, and the team agrees the sprint has started (Step 6).
- [ ] The team has agreed on a daily standup time (Step 7).

If every box is checked, Sprint 2 is officially kicked off — start on the first story.

**If your team adopts a board tool later:** the backlog and stories above paste directly into Jira, Trello, or similar — nothing here needs rewriting to move into one. Current steps for setting one up, if you want them: [How to Start & Use Sprints in Jira — Atlassian](https://www.atlassian.com/agile/tutorials/sprints); [Create a new space — Jira Cloud, Atlassian Support](https://support.atlassian.com/jira-software-cloud/docs/create-a-new-project/).
