# Day 19 Lab Guide: UiPath RPA

Source content: `course-outline/Day19_UiPath_RPA_Content.md` (course-content-architect output). Every UI-specific step below (menu paths, button labels, activity and property names) was checked against UiPath's current Studio Web and Orchestrator documentation before publishing. Each exercise below is self-contained — work through any one of them with nothing else open but this document.

Module 1 uses **Studio Web** (`https://studio.uipath.com`) instead of the installed Studio Desktop application. Both target screens this lab reads from — your team's own reservations screen and the Day 18 lab guide's Guest Preference Power Apps screen — are browser-based, which is exactly what Studio Web automates; it has no desktop-application automation, so a team whose *real* Sprint-3 screen (Exercise 3, Module 2) turns out to be a non-browser desktop app would need Studio Desktop for that one real extension, even though the classroom exercise itself stays entirely in the browser. Studio Web still needs two small things installed, neither of which is the full Studio Desktop IDE: the UiPath browser extension (for targeting elements at design time) and UiPath Assistant (a lightweight companion app, needed to run/debug a workflow against your own locally-open browser tab). Module 2's Orchestrator-side work (publishing, deploying, scheduling, queues) is identical either way, since it happens in Orchestrator itself regardless of which Studio built the workflow.

## Module 1: UiPath Workflow Basics & Selectors

**Sources for this module:**
- [Studio Web - Overview](https://docs.uipath.com/studio-web/automation-cloud/latest/user-guide/overview)
- [Studio Web - Creating a project](https://docs.uipath.com/studio-web/automation-cloud/latest/user-guide/creating-a-project)
- [Studio Web - Using UI Automation for browser interactions](https://docs.uipath.com/studio-web/automation-cloud/latest/user-guide/using-ui-automation)
- [Studio Web - Managing the data in a project](https://docs.uipath.com/studio-web/automation-cloud/latest/user-guide/managing-the-data-in-a-project)
- [Studio Web - Debugging app projects](https://docs.uipath.com/studio-web/automation-cloud/latest/user-guide/debugging-app-projects)
- [Activities - Use Application/Browser](https://docs.uipath.com/activities/other/latest/ui-automation/n-application-card)
- [Activities - Get Text](https://docs.uipath.com/activities/other/latest/ui-automation/n-get-text)
- [Activities - Selection Helper](https://docs.uipath.com/activities/other/latest/ui-automation/selection-options)
- [Studio - Full versus partial selectors](https://docs.uipath.com/studio/standalone/2024.10/user-guide/full-versus-partial-selectors)

### Exercise 1: Build a Basic UiPath Workflow Using Selectors to Identify UI Elements Reliably
**Objective:**
By the end of this exercise, you will have one Studio Web project — a **Use Application/Browser** activity containing a **Get Text** activity — that opens your team's own reservations screen (or, if that screen isn't reachable in the classroom, the Guest Preference Power Apps screen built in the Day 18 lab guide's Module 1), locates one on-screen value with a selector, stores it in a variable, and logs it. No Studio Desktop installation is used. Module 2 deploys and schedules this same workflow.

**Prerequisites for this exercise:**
- A Studio Web project accessible at `https://studio.uipath.com` — part of your Orchestrator/Automation Cloud tenant (per the course's Software Requirements) — opened in Chrome, Edge, or Safari, with the UiPath browser extension installed in that same browser.
- UiPath Assistant installed and running on this machine — a lightweight companion app, not the full Studio Desktop application — needed to debug/run the workflow against your own locally-open browser tab.
- Your team's own reservations screen (built earlier in the program) reachable in a tab of the same browser — or, if that screen isn't reachable in the classroom, the Guest Preference Power Apps screen from the Day 18 lab guide's Module 1.

**Steps:**
1. In a browser with the UiPath extension installed, go to `https://studio.uipath.com` and sign in with your Orchestrator tenant credentials. **[Verified current: Studio Web is accessed at studio.uipath.com, signed in with your Automation Cloud/Orchestrator account — confirmed against UiPath's current Studio Web documentation.]**
2. On the **Workspace** page, select **Create New**.
3. Select **RPA Workflow** — confirm a new project opens with a blank canvas, named **Untitled** by default.
4. Open the project name's context menu in the Project explorer and select **Rename**, then enter a name for the project — for example **[Placeholder — replace with your team's actual project name]**.
5. When prompted to select an automation trigger type for the project, select **Manual** — Module 2 teaches Orchestrator's own scheduled trigger as a separate, later step, so this project doesn't need a built-in schedule yet.
6. In a new tab of this same browser, open your team's reservations screen (already built earlier in the program) — Studio Web and the application it automates must render in the same browser, so this has to be a tab here, not a separate browser window.
7. Back in the Studio Web tab, select the **+** icon beneath the trigger block, search for `Use Application/Browser`, and select it to add it to the canvas.
8. On the activity, select **Indicate application to automate**, then select the reservations-screen tab you opened in step 6 — confirm the activity now shows that tab as its target.
9. Inside the **Use Application/Browser** container, select its own **+** icon, search for `Get Text`, and select it to add it inside the container — not outside it.
10. On the **Get Text** activity, use the same indication flow to target one specific on-screen value on the reservations screen — for example **[Placeholder — replace with your team's actual reservations-screen element: a reservation count, an occupancy figure, or a guest name currently shown on screen]** — confirm the targeted element highlights.
11. While still hovering over the newly-indicated target, select the settings icon in its hover menu to open its target details, review which attribute(s) were chosen to identify the element — for example a name, an automation ID, or a role attribute — and confirm none look like they would change between runs (a timestamp, a live count). **[Unverified — confirm the exact icon against your own tenant: UiPath's Selection Helper documentation confirms a settings-style button appears in the hover menu for editing a target's attributes, but doesn't give its exact literal label; look for whichever hover-menu icon opens attribute/selector details.]**
12. If any chosen attribute does look unstable, replace it with a more stable one; otherwise leave it as-is, then select **Confirm** (or press **Enter**) to close.
13. The same full-versus-partial selector split this program's earlier Power Automate content didn't need applies here: the **Use Application/Browser** activity's own target (step 8) carries the top-level tab/window information, while the **Get Text** activity's target (steps 10-12) relies on sitting inside that container rather than repeating it — open each activity's own target details in turn to see the difference.
14. On the left side of the Designer panel, select **Open Data Manager**, then select the **+** (add new item) button next to **Variables**.
15. In the **Name** field, enter `occupancyValue`; set **Type** to `String`; then select **Create**.
16. On the **Get Text** activity's property panel, find its **Text value** field, select it, and choose your new `occupancyValue` variable from the list so the read value is stored there.
17. Select the **+** icon directly after the **Get Text** activity, still inside the **Use Application/Browser** container, search for `Log Message`, and add it.
18. On the **Log Message** activity, set its **Message** property to reference your new variable — for example `"Occupancy value read: " + occupancyValue`.
19. Near the top of the page, expand the drop-down next to the debug button and select **On local machine**, then run the workflow — confirm the **Output** panel logs the real, current on-screen value from your reservations screen, not a placeholder or hard-coded string. **[Verified current: Studio Web can run/debug a project either "On local machine" (requires UiPath Assistant installed and running) or "On cloud" — reading your own locally-open reservations screen specifically requires the local-machine option — confirmed against Studio Web's current debugging documentation.]**
20. In your team's reservations screen (or its underlying data), create or edit one sample reservation so the on-screen value you targeted actually changes, then rerun (repeat step 19) and confirm the **Output** panel now logs the new value — proving the selector locates the element itself, not a cached screen position.

**Expected Result:**
One working Studio Web project that opens your team's reservations screen, reads one on-screen value through a selector-driven **Get Text** activity into a `String` variable, and logs it — rerunning the workflow after the underlying value changes produces the new value, not the old one.

**Troubleshooting:**
- The selector was built while the screen was in an unusual state (empty search results, a modal dialog open) and now can't find the element on a normal run → re-indicate the target (steps 9-10) with the screen back in its ordinary, expected state.
- The Selection Helper picked a selector attribute that changes on every load (a session ID, a live count baked into a label's own name) → reopen the target's details (step 11) and manually replace that attribute with a more stable one.
- **Get Text** was added outside the **Use Application/Browser** container by mistake — for example, by using the canvas's own top-level **+** instead of the container's **+** → delete it and re-add it from inside the container (step 9).
- Rerunning the workflow after changing the on-screen value still logs the old value → confirm you actually indicated a value-bearing element, not a static label next to it, and that the underlying screen has fully refreshed before the workflow re-reads it.
- Selecting **Run**/debug does nothing, hangs, or errors about not finding a local robot → confirm UiPath Assistant is actually installed and running on this machine, and that **On local machine** (not **On cloud**) is selected in the debug drop-down (step 19); **On cloud** runs in an isolated cloud session that can't see your own open browser tab.
- Studio Web can't find or target the reservations screen tab at all → confirm both Studio Web and the reservations screen are open in the **same** browser with the UiPath extension installed; Studio Web can't target a tab in a different browser or a different browser profile.

## Module 2: Orchestrator & Queues Essentials

**Sources for this module:**
- [Orchestrator - About Processes](https://docs.uipath.com/orchestrator/standalone/2023.10/user-guide/about-processes)
- [Orchestrator - Managing Processes](https://docs.uipath.com/orchestrator/standalone/2023.10/user-guide/managing-processes)
- [Studio - About Publishing Automation Projects](https://docs.uipath.com/studio/standalone/2023.4/user-guide/about-publishing-automation-projects)
- [Orchestrator - About triggers](https://docs.uipath.com/orchestrator/standalone/2023.10/user-guide/about-triggers)
- [Orchestrator - Creating a time trigger](https://docs.uipath.com/orchestrator/automation-cloud/latest/user-guide/creating-a-time-trigger)
- [Orchestrator - About Queues and Transactions](https://docs.uipath.com/orchestrator/standalone/2024.10/user-guide/about-queues-and-transactions)
- [Orchestrator - Managing Queues in Orchestrator](https://docs.uipath.com/orchestrator/standalone/2023.4/user-guide/managing-queues-in-orchestrator)
- [Orchestrator - Studio Activities Used With Queues](https://docs.uipath.com/orchestrator/automation-cloud/latest/user-guide/studio-activities-used-with-queues)

### Exercise 1: Deploy the Module 1 Workflow to Orchestrator and Schedule It
**Objective:**
By the end of this exercise, Module 1's workflow will be published from Studio, deployed as a runnable Orchestrator process, confirmed working outside Studio, and running on its own on a short recurring schedule — with nobody selecting Run.

**Prerequisites for this exercise:**
- Module 1, Exercise 1 must be complete and running successfully from Studio Web.
- You must be able to open your team's already-licensed Orchestrator tenant.

**Steps:**
1. In Studio Web, with Module 1's project open, select **Publish** near the top of the page. **[Verified current: Studio Web's Publish button sits at the top of the project page rather than on a Desktop-style ribbon — confirmed against Studio Web's current publishing documentation.]**
2. In the **Publish** dialog, confirm the **Name** field and, optionally, add a description.
3. Under the feed/destination options, select **Orchestrator Folder Feed**, then select your team's folder — unlike the default **Personal Workspace** feed, a Folder Feed publish doesn't auto-create a process for you, which keeps the explicit **Add Process** step (step 8 below) as its own visible lesson rather than something Studio Web does invisibly on your behalf.
4. Confirm or set the **Version** field — for example `1.0.0`.
5. Select **Publish** — confirm a success confirmation appears and the package now appears in Orchestrator's package feed for your team's folder.
6. Go to your Orchestrator tenant in a browser and sign in.
7. In the left navigation pane, select your team's folder, then select **Automations** > **Processes**.
8. Select **Add** — confirm the **Add Process** window opens.
9. From the **Package** drop-down, select your published project's name; from **Package Version**, select the version you published in step 3.
10. In the **Display Name** field, enter a name for the process — for example **[Placeholder — replace with your own process name]** — then select **Add** — confirm the new process now appears in the **Processes** list.
11. Select the new process's **Start** action to run it manually once, then confirm the job completes successfully and its log shows the same value Module 1's local run produced.
12. Select **Automations** > **Triggers**, then, on the **Time Triggers** page, select **Add a new trigger**.
13. From the **Process Name** drop-down, select the process you deployed in step 10.
14. In the **Name** field, enter a name for the trigger — for example **[Placeholder — replace with your own trigger name]**.
15. Under the recurrence settings, select **Minute by minute** and set the interval to a short value — for example, every 5 minutes — rather than Meridian Residences' real monthly cadence, so the room can observe it fire without waiting; leave the remaining fields (Job Priority, Runtime type, Timezone, Execution Target, Non-working day restrictions) at their defaults for this classroom exercise.
16. Confirm the **Enabled** toggle is on, then select **Save** — confirm the new trigger appears on the **Time Triggers** page.
17. Wait for the schedule to fire once, then check the process's **Jobs** history and confirm a new job started on its own, with nobody selecting **Start**.

**Expected Result:**
One deployed Orchestrator process, confirmed running Module 1's workflow both from a manual start and from a time trigger firing on its own — visible in the process's **Jobs** history with no one having selected Start for the second run.

**Troubleshooting:**
- **Publish** fails, or the **Orchestrator Folder Feed** option doesn't list your team's folder → confirm you're signed into Studio Web with the same Orchestrator tenant account your team's folder actually lives in, since Studio Web publishes into whichever tenant you're currently signed into.
- The new process doesn't appear after selecting **Add** in step 10 → confirm you selected both a **Package** and a **Package Version** in step 9; the **Add** action is disabled until both are chosen.
- The trigger never fires → confirm the **Enabled** toggle from step 16 is actually on, and that enough time has passed for at least one interval from step 15 to elapse.
- The time trigger's interval doesn't line up with what you configured (for example, you set 7 minutes but it fires on the hour and every 7 minutes oddly) → Orchestrator's minute-by-minute scheduling only hits your exact configured interval when that number divides evenly into 60; use a divisor of 60 (5, 6, 10, 15, and so on) for a clean recurring interval in the classroom.

### Exercise 2: Create a Queue and Process Transactions From It Through the Deployed Workflow
**Objective:**
By the end of this exercise, you will have one Orchestrator queue holding sample items, and Exercise 1's workflow extended with **Get Transaction Item** and **Set Transaction Status** so it pulls one queue item at a time, reuses Module 1's selector-driven read, and reports back a **Successful** or classified-**Failed** status — visible in Orchestrator's own queue Transactions view.

**Prerequisites for this exercise:**
- Exercise 1 in this module must be complete: the workflow must already be published, deployed, and running on a time trigger.

**Steps:**
1. In Orchestrator, select your team's folder, then select **Automations** > **Queues**.
2. Select **Add Queue**, then select **Create a new queue**.
3. In the **Name** field, enter a name for the queue — for example `PropertyOccupancyCheck`.
4. Select the **Auto Retry** checkbox, and in **Max # of retries**, enter a small number — for example `3`.
5. Select **Add** — confirm the new queue appears on the **Queues** page, empty.
6. On the queue's own page (or via its **Upload Items** option), add two or three sample queue items, each carrying a small piece of structured data your workflow will need — for example **[Placeholder — replace with your team's actual per-property or per-lease queue item fields: a property id and expected-occupancy threshold, or a lease id and balance]**.
7. Back in Studio Web (`https://studio.uipath.com`), reopen Module 1's project from the **Workspace** page.
8. Select the **+** icon at the very start of the workflow, before the existing **Use Application/Browser** activity, search for `Get Transaction Item`, and add it there.
9. On the **Get Transaction Item** activity, set its **QueueName** property to your queue's name in quotation marks — for example `"PropertyOccupancyCheck"`.
10. Create a `QueueItem` variable — for example `currentItem` — and set the activity's output to store into it, so the item's own data is available to the activities after it; confirm the queue's own **Transactions** view will show this item's status change to **In Progress** the moment the workflow runs this activity.
11. Select the **+** icon directly after the existing **Get Text** activity, still inside the **Use Application/Browser** container, search for `Set Transaction Status`, and add it there.
12. On this **Set Transaction Status** activity, set its **Status** property to **Successful** — this is the path a normal, complete read follows.
13. Select the **+** icon just before this **Set Transaction Status** activity, search for `If`, and add it so the condition wraps the success path — checking whether the queue item's own data is genuinely usable — for example **[Placeholder — replace with your team's actual "can't succeed" condition, e.g., a property with no occupancy data at all]**. **[Unverified — confirm against your own tenant: whether Studio Web lets you insert an If activity so it wraps an already-placed activity, or whether it's easier to delete step 11's Set Transaction Status first, add the If, then re-add Set Transaction Status inside its Then branch — both reach the same result.]**
14. On the **If** activity's **Else** branch, select its own **+** icon, search for `Set Transaction Status`, and add a second one; set its **Status** property to **Failed**, its **ErrorType** property to **Business**, and its **Reason** property to a short string describing why — for example `"Property has no occupancy data on file."`
15. Around the **Use Application/Browser** container as a whole, add a **Try Catch** activity so the container sits inside its **Try** block — search `Try Catch` from the **+** icon immediately before the container, the same way step 13 wrapped the success path, moving the existing container inside the new **Try** block afterward if it isn't placed there automatically — then, in the **Catch** block, add a third **Set Transaction Status** activity; set its **Status** property to **Failed**, its **ErrorType** property to **Application**, and its **Reason** property to a short string — for example `"The reservations screen did not load or the selector could not resolve."`
16. Repeat Exercise 1's steps 1-5 to republish the project with a new version number, then repeat Exercise 1's steps 8-10 to redeploy the updated package to the same process, selecting the new version.
17. Select the process's **Start** action to run it manually once, then, in the queue's own **Transactions** view, confirm one of your sample items transitions from **New** to **In Progress** to **Successful**.
18. Edit one sample queue item so it deliberately fails the condition from step 13 — for example, remove its occupancy data — rerun the process, and confirm that item ends in **Failed** with a **Business Exception**, and, checking the queue's **Auto Retry** setting from step 4, confirm it is **not** retried.
19. Temporarily break the workflow's own read — for example, close the reservations screen before running, or point the selector at a screen that isn't open — so a normal item's **Get Text** step itself fails, rerun the process, confirm that item ends in **Failed** with an **Application Exception** and is retried automatically up to the **Max # of retries** you set in step 4, then restore the screen before continuing.

**Expected Result:**
One queue with sample items, each picked up one at a time by the extended workflow, ending in **Successful**, **Failed** (Business Exception, not retried), or **Failed** (Application Exception, retried) depending on the item — all visible in Orchestrator's own queue Transactions view.

**Troubleshooting:**
- Forgot to republish and redeploy after adding **Get Transaction Item** and **Set Transaction Status** → Orchestrator keeps running the older, queue-unaware version from Exercise 1; repeat step 16.
- Every failure lands as a generic failure instead of a classified Business or Application exception → double-check each **Set Transaction Status** activity's **ErrorType** property is actually set, not left at its default.
- An Application-Exception item isn't retried → confirm **Auto Retry** is actually checked on the queue itself (step 4), not just assumed; Orchestrator only retries Application Exceptions when the queue is configured to.
- A queue item you expect to succeed instead throws an unrelated error → check the item's own data fields for typos or missing values first (step 6's placeholders); a malformed queue item can produce an Application Exception that looks like a selector problem.

### Exercise 3: For a Team Choosing UiPath as Its Sprint-3 Automated Workflow, Apply This to That Capstone Task
**Objective:**
By the end of this exercise, a team whose real Sprint-3 automated workflow is UiPath (Meridian Resorts & Spa, Meridian Residences, or any other team that has chosen UiPath as its path) will have used Exercises 1-2's publish-schedule-queue-transaction skeleton as a template to identify the real screen, queue design, and failure classification their own automation needs, then rebuilt it against their own data. A team whose real deliverable is a Power Automate flow instead confirms today's skills exercise is complete and records what carries forward.

**Prerequisites for this exercise:**
- Module 2, Exercise 2 must be complete and working.
- Know which of the two paths — UiPath or Power Automate — your team chose for its real Sprint-3 automated workflow (decided the immediately preceding day).

**Steps:**
1. Confirm which path your team chose for its real Sprint-3 automated workflow: UiPath or Power Automate.
2. **If your team's real workflow is a UiPath automation:** write down your team's actual source screen(s) and the selector(s) your real automation needs — **[Placeholder — replace with your team's actual Sprint-3 automated workflow's real source screen(s) and the selector(s) it needs]** — and note whether that screen is browser-based (Studio Web, same as Module 1, works) or a desktop application (Studio Web has no desktop-automation support, so rebuilding this one workflow in the installed Studio Desktop application is required for that real screen specifically).
3. Write down your team's actual queue design — one item per property, per lease, or per whatever unit your real automation processes — **[Placeholder — replace with your team's actual queue design]**.
4. Write down your team's actual success/business-exception/application-exception classification for your real automation's failure cases — **[Placeholder — replace with your team's actual success/business-exception/application-exception classification for your real automation's failure cases]**.
5. Using Exercises 1-2's publish-schedule-queue-transaction skeleton as your starting template, rebuild it against your own team's real screen, queue, and failure classification instead of the classroom's generic property-occupancy example.
6. Publish and redeploy the new workflow, then test it against a real or realistic sample queue item from your own team's own data, the same way you tested Exercise 2's workflow.
7. **If your team's real workflow is a Power Automate flow** (The Aldwyn House, Meridian Kitchens Collective, or Meridian Stays): confirm Module 1, Exercise 1 and Module 2, Exercises 1-2 are complete — that workflow, deployment, and queue are today's finished skills exercise for your team.
8. Note, in your team's shared planning document, that your real automation deliverable was already built the immediately preceding day using this same trigger-and-processing mental model, expressed through Dataverse connectors and an approval action instead of a selector-driven screen read and an Orchestrator queue.

**Expected Result:**
A UiPath-choosing team has a working workflow, deployment, and queue built against its own real screen and data, tested against at least one real or realistic sample item, with a written failure classification. A Power-Automate-choosing team has confirmed today's exercises are complete and has a written note connecting today's skeleton to its already-built Power Automate deliverable.

**Troubleshooting:**
- Unsure whether a failure in your team's real automation is a Business Exception or an Application Exception → ask whether the automation itself worked correctly and the data was simply unusable (Business) or whether the automation's own mechanics broke, such as a screen not loading or a selector not resolving (Application).
- No further common pitfalls noted for this exercise beyond the classification judgment call above — the rest of this exercise is a direct application of Exercises 1-2's already-tested mechanics to different data.
