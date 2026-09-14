# Day 18 Lab Guide: Power Platform Automation

Source content: `course-outline/Day18_Power_Platform_Automation_Content.md` (course-content-architect output). Every UI-specific step below (menu paths, button labels, connector and action names) was checked against Microsoft's current Power Apps and Power Automate documentation before publishing. Each exercise below is self-contained — work through any one of them with nothing else open but this document.

## Module 1: Power Apps & Dataverse Essentials

### Exercise 1: Build One Canvas App Screen with a Control Bound to a Formula
**Objective:**
By the end of this exercise, you will have a canvas app with a Text input control and a Label control, where the Label's `Text` and `Color` properties are both driven by Power Fx formulas that recalculate automatically — no code, no manual refresh. Name the screen to match Exercise 2's Dataverse table, since together they form one team's hands-on activity for this module.

**Prerequisites for this exercise:**
- Your team's Power Platform environment with Dataverse enabled must already be licensed and assigned, per the course's Software Requirements — no environment setup happens in this exercise.
- You must be able to sign in at `https://make.powerapps.com`.

**Steps:**
1. Go to `https://make.powerapps.com` and sign in with your team's Power Platform environment credentials.
2. In the left navigation pane, select **Create**.
3. Select **Create from blank**.
4. In the **Start with a blank canvas** dialog, choose **Tablet size** (or **Responsive**, if your team prefers a different layout).
5. Enter an app name if prompted — for example **[Placeholder — replace with your team's actual app name]** — and select **Create**; Power Apps Studio opens with a single blank screen.
6. On the default screen, select **Insert** from the authoring menu.
7. Select **Text input** — a text input control (named something like `TextInput1`) appears on the canvas, already selected.
8. Select **Insert** again.
9. Select **Label** — a new label control (named something like `Label1`) appears on the canvas, already selected, with its selection handles visible.
10. Select the Label control directly on the canvas if it isn't already selected — remember, a control must be selected before you can configure it.
11. In the properties list above the formula bar, confirm **Text** is the selected property.
12. Click into the formula bar and type `"Preference noted for: " & TextInput1.Text` — no leading `=`, since Power Apps treats everything typed there as a formula by default — then press **Enter** to commit it.
13. Click into the Text input control on the canvas and type any text, then confirm the Label's displayed text updates the instant you type, with no separate refresh action.
14. With the Label still selected, choose **Color** from the properties list.
15. In the formula bar, type `If( IsBlank(TextInput1.Text), Color.Gray, Color.DarkGreen )` and press **Enter**.
16. Clear the Text input control's text and confirm the Label turns gray, then type any text into it again and confirm the Label turns dark green — a second, independent proof that a formula-bound property recalculates on its own.
17. In the **Tree view** pane, hover over the screen's name to reveal its overflow menu (**…**), select it, then select **Rename**.
18. Rename the screen to `GuestPreferenceIntake` — matching the Dataverse table Exercise 2 builds next — and press **Enter** to confirm.

**Expected Result:**
One canvas app screen named `GuestPreferenceIntake`, containing a Text input control and a Label control whose `Text` and `Color` properties both update automatically the instant the Text input's value changes — driven entirely by the two Power Fx formulas from steps 12 and 15, with no code written and no manual refresh.

**Troubleshooting:**
- Typed a leading `=` into the formula bar out of Excel habit → harmless but unnecessary; Power Apps treats everything typed there as a formula by default, with or without the `=`.
- A formula appears to do nothing after pressing Enter → check that the properties list actually showed **Text** (or **Color**) selected before you typed — the formula bar always applies its contents to whichever property is currently selected, so a formula typed while the wrong property was selected (for example, `OnSelect`) is saved against that wrong property instead.
- Nothing happens when clicking a control on the canvas → the control probably isn't selected yet; select it either on the canvas or from the **Tree view** list first, since the maker portal requires a control to be selected before its properties can be configured.

### Exercise 2: Model One Dataverse Table with a Relationship to a Second Table
**Objective:**
By the end of this exercise, you will have two Dataverse tables: **Guest** (Name, Email, Phone, and Loyalty Tier columns) with at least two sample rows, and **Guest Preference**, with a Lookup column pointing at **Guest** — creating a one-to-many relationship where Guest Preference is the "many" (child) side and Guest is the "one" (parent) side — plus at least two Guest Preference sample rows proving the relationship resolves correctly. Module 2, Exercise 1's flow reads directly from Guest Preference, so both tables must exist before you start that exercise.

**Prerequisites for this exercise:**
None beyond the course prerequisites — this exercise builds both Dataverse tables it needs from scratch, including **Guest**.

**Steps:**
1. In Power Apps (`https://make.powerapps.com`), select **Tables** in the left navigation pane — if it isn't visible, select **…More** first, then select **Tables**.
2. On the command bar, select **New table**.
3. Select **Set advanced properties**.
4. In the **New table** panel, enter **Guest** as the **Display name**.
5. Select the **Primary column** tab and set its **Display name** to `Name`.
6. Select **Save** — this closes the panel and opens the table hub for your new Guest table.
7. In the table hub, select **Columns**.
8. Select **New column**; set **Display Name** to `Email`, set **Data type** to **Email** (a text data type validated as an email address, listed alongside plain **Text** in the Data type picker), then select **Done**.
9. Select **New column** again; set **Display Name** to `Phone`, set **Data type** to **Phone**, then select **Done**.
10. Select **New column** again; set **Display Name** to `Loyalty Tier`, set **Data type** to **Choice** (or **Text**), then select **Done**.
11. Select **Save Table** — none of these three columns actually exist until this save completes.
12. Open the Guest table's **Data** view and select its add-row command (its exact label varies by environment — look for **New** or a plus icon on the grid's command bar) to add at least two sample guest rows, filling in Name, Email, Phone, and Loyalty Tier for each — for example **[Placeholder — replace with your team's own real or sample guest names and details]**.
13. Back on the **Tables** list, select **New table** again.
14. Select **Set advanced properties**.
15. In the **New table** panel, enter **Guest Preference** as the **Display name** (the **Plural display name** field auto-fills; leave it as-is).
16. Select **Save** — this closes the panel and opens the table hub for your new Guest Preference table.
17. In the table hub, select **Columns**.
18. Select **New column**; set **Display Name** to `Preference Type`, set **Data type** to **Text**, then select **Done**.
19. Select **New column** again; set **Display Name** to `Detail`, set **Data type** to **Text**, then select **Done**.
20. Select **New column** again; set **Display Name** to `Flagged`, set **Data type** to **Yes/No**, then select **Done**.
21. Select **New column** one more time; set **Display Name** to `Guest`, set **Data type** to **Lookup**, set its related table to the **Guest** table you created in steps 1-12, then select **Done**.
22. Select **Save Table** — none of these four columns actually exist until this save completes.
23. Confirm the four columns (Preference Type, Detail, Flagged, Guest) now appear in the Columns list.
24. In the table hub's left-hand **Schema** list, select **Relationships** (a sibling of **Columns**, not something shown on the column itself) and confirm a new one-to-many relationship is listed there, with **Guest Preference** as the related (child) table and **Guest** as the primary (parent) table.
25. Open the Guest Preference table's **Data** view and select its add-row command (its exact label varies by environment — look for **New** or a plus icon on the grid's command bar) to add a first sample row.
26. Fill in Preference Type, Detail, and Flagged for this row — for example **[Placeholder — replace with real or sample preference details]** — set the **Guest** lookup column to one of the sample guest rows from step 12, then save the row.
27. Repeat steps 25-26 to add a second sample row, again setting its Guest lookup column to one of the sample guest rows from step 12.
28. Confirm both saved rows display the related guest's name in the Guest column, proving the relationship resolves correctly rather than just existing structurally.

**Expected Result:**
Two Dataverse tables exist: **Guest**, with Name, Email, Phone, and Loyalty Tier columns and at least two sample rows; and **Guest Preference**, with Preference Type, Detail, Flagged, and Guest (Lookup) columns, a working one-to-many relationship to **Guest**, and at least two sample rows, each correctly showing its related guest's name.

**Troubleshooting:**
- Columns configured in the **Column properties** panel don't appear to exist anywhere → columns aren't actually created until that table's own **Save Table** is selected (step 11 for Guest, step 22 for Guest Preference) — go back and select it if you skipped it.
- Lookup column added to the wrong table (a Guest lookup added on **Guest** instead of on **Guest Preference**) → this either fails outright or creates the relationship backwards, with Guest Preference no longer correctly positioned as the "many" side. Delete the column and re-add it on Guest Preference.
- A sample row's Guest lookup column left blank → the relationship is still structurally correct, but Module 2, Exercise 1's flow has nothing to find when it looks up a guest from this row. Go back to step 25 or 26 and set the lookup before continuing.
- Guest table's primary column left at its default display name instead of renamed to `Name` (step 5) → Exercise 3's guest picker control expects a column named `Name`; either go back and rename it now, or adjust Exercise 3's `DisplayFields` formula to match whatever the primary column is actually called.

### Exercise 3: Wire the Canvas Screen to Write Directly into the Guest Preference Table
**Objective:**
By the end of this exercise, submitting Exercise 1's `GuestPreferenceIntake` screen will create one real row in Exercise 2's **Guest Preference** table, with a working **Guest** lookup — turning the screen, both tables, and Module 2's flow into one connected pipeline instead of separate pieces.

**Prerequisites for this exercise:**
- Module 1, Exercise 1 (the `GuestPreferenceIntake` canvas screen) must be complete.
- Module 1, Exercise 2 (the **Guest** table and the **Guest Preference** table, with the Lookup relationship between them) must be complete.

**Steps:**
1. Reopen the canvas app from Exercise 1 in Power Apps Studio and select the `GuestPreferenceIntake` screen.
2. Select **Data** from the app authoring menu on the left pane, then select **Add data** at the top of the **Data** pane.
3. In the search box, type `Dataverse`, select the **Microsoft Dataverse** connector from the results list, confirm the environment shown is your team's own (Dataverse connections let you pick the environment before picking a table), then select the **Guest Preference** table — repeat this same **Add data** step to also add the **Guest** table if the table picker doesn't let you select both at once.
4. Select **Insert**, then select **Combo box** — a new combo box control appears on the canvas.
5. With the combo box selected, set its **Items** property to `Guest`.
6. Set this control's **DisplayFields** property to `["Name"]` — if that doesn't resolve, open the Guest table's Columns list in the maker portal and use its actual primary-column display name instead. Rename this control to `GuestPicker` (Tree view → overflow menu → **Rename**, the same way you renamed the screen in Exercise 1).
7. Select **Insert**, then select **Text input** — a new text input control appears on the canvas. Rename this control to `PreferenceTypeInput`.
8. Select **Insert**, then select **Button** — a new button control appears.
9. Rename this button to `SubmitButton` and set its **Text** property to `"Submit"`.
10. Set `SubmitButton`'s `OnSelect` property to `Patch('Guest Preferences', Defaults('Guest Preferences'), { 'Preference Type': PreferenceTypeInput.Text, Detail: TextInput1.Text, 'Guest': GuestPicker.Selected })` — replace `Guest Preferences` if your environment generated a different plural table name (check the table's own **Plural display name** in the maker portal).
11. Select **Save**.
12. Select the **Play** button (▷, top-right) to open the app in Play mode.
13. In Play mode, select a guest in `GuestPicker`, type a preference type into `PreferenceTypeInput` (for example, `Dietary`), type detail text into the original text input control, then select **Submit**.
14. Go back to the Guest Preference table's **Data** view in the maker portal (Exercise 2) and confirm a new row now exists, with Preference Type, Detail, and Guest set to exactly what you entered in Play mode.
15. In Power Automate, go to **My flows**, select Module 2, Exercise 1's flow, then select **Details** to see its run history (a **28-day run history** section, or a **Run history** tab in some environments) and confirm this new row fired a new run — proof the screen, the table, and the flow are now one live pipeline, not three separate exercises.

**Expected Result:**
Submitting the `GuestPreferenceIntake` screen in Play mode creates a real row in the Guest Preference table with the exact Guest, Preference Type, and Detail values entered on the screen, and that new row fires Module 2, Exercise 1's flow automatically.

**Troubleshooting:**
- `GuestPicker`'s `DisplayFields: ["Name"]` shows blank or errors → your Guest table's primary column has a different display name; open the Guest table's Columns list and use its actual primary-column name instead.
- Selecting **Submit** in Play mode does nothing visible → confirm the app was saved (step 11) before switching to Play mode; an unsaved `OnSelect` formula doesn't run in Play mode.
- A new row appears in the Guest Preference table but Module 2, Exercise 1's flow never fires → confirm that flow is turned **On** in the **My flows** list, not **Off**.
- Module 2, Exercise 1's approval branch never triggers even for a preference you expect to be cost-bearing → **Preference Type** is a plain Text column with no enforced list of values, so that flow's condition (an exact `is equal to Amenity` check) only matches if `PreferenceTypeInput`'s typed text is spelled and capitalized exactly like the value that condition checks for. Type it exactly, or loosen that condition in Module 2, Exercise 1.

## Module 2: Power Automate Essentials

### Exercise 1: Build One Flow with a Trigger, an Action, and an Approval Step, Reading from the Dataverse Table
**Objective:**
By the end of this exercise, you will have one working Power Automate flow — a Dataverse trigger, a lookup action, a compose action, a condition, an approval step, and two outcome actions — reading directly from the **Guest Preference** table and its **Guest** relationship built in Module 1, Exercise 2. Run against a no-cost sample row, the flow notifies housekeeping directly; run against a cost-bearing sample row, it pauses for a manager's approval first.

**Prerequisites for this exercise:**
- Module 1, Exercise 2 must be complete: the **Guest Preference** table and its **Guest** Lookup relationship must already exist, with at least two sample rows.
- You must be able to open Power Automate in the same licensed environment as Module 1.

**Steps:**
1. Go to `https://make.powerautomate.com` and sign in with the same environment credentials used in Module 1.
2. In the left navigation pane, select **My flows**.
3. Select **New flow**, then select **Automated cloud flow**.
4. In the **Flow name** field, enter a name for the flow — for example **[Placeholder — replace with your team's actual flow name]**.
5. In the trigger search field, enter `row is added`.
6. Select **When a row is added, modified or deleted** under the Microsoft Dataverse connector. **[Verified current: the trigger's exact name carries no comma before "or" — "modified or deleted," not "modified, or deleted."]**
7. At the bottom of the screen, select **Create** — the flow editor opens with the trigger already on the canvas.
8. On the trigger card, set **Change type** to **Added**.
9. On the trigger card, set **Table name** to **Guest Preferences**. **[Verified current: the Table name picker lists Dataverse tables by their plural display name, not the singular name you typed when creating the table — so it's "Guest Preferences" here, not "Guest Preference."]**
10. Select **+ New step** (or the **+** below the trigger, if your environment shows the new designer).
11. In the search field, enter `get a row by id`.
12. Select **Get a row by ID** under the Microsoft Dataverse connector.
13. On this action's card, set **Table name** to **Guests** (the plural form, same reason as step 9).
14. On this action's card, set **Row ID** using the dynamic content picker, selecting the trigger's own **Guest** lookup output.
15. Select **+ New step** again.
16. In the search field, enter `compose`.
17. Select **Compose** under the Data Operation connector.
18. In the Compose action's **Inputs** field, build the notification text using dynamic content from the trigger's Preference Type and Detail fields plus the Get-a-row-by-ID action's retrieved guest-name field — for example **[Placeholder — replace with your team's own notification wording, referencing the trigger's preference-type and detail fields and the guest-lookup action's name field]**.
19. Select **Save** in the top-right corner of the flow editor.
20. In a separate browser tab, open the Guest Preference table's data grid and add a new row with a no-cost preference type (for example, `Pillow type`), with its Guest lookup set to an existing sample guest.
21. Back in Power Automate, go to **My flows**, select this flow's name to open it, then select **Details** — its run history appears there, listed under a **28-day run history** section (some environments show a **Run history** tab directly instead).
22. Open the run that just fired and confirm it shows a completed **Get a row by ID** step and a **Compose** step whose output is the notification text you built in step 18 — proving the routine, no-gate path works before the approval step is added.
23. From **My flows**, select this flow's **Edit** action (or its pencil icon) to reopen the flow designer, then select **+ New step** directly after the Compose action.
24. In the search field, enter `condition`.
25. Select **Condition**.
26. In the condition's first field, choose the trigger's **Preference Type** dynamic content.
27. Set the operator to **is equal to**.
28. In the value field, enter `Amenity` (or your team's chosen cost-bearing preference-type value).
29. In the **If yes** branch, select **Add an action**.
30. In the search field, enter `start and wait for an approval`.
31. Select **Start and wait for an approval** under the Approvals connector.
32. Set **Approval type** to **Approve/Reject - First to respond**.
33. Set **Title** to the Compose action's output, using the dynamic content picker.
34. Set the approver field (labeled **Assigned to**) to one manager's email address — for example **[Placeholder — replace with your team's actual approver's email address]**.
35. Still in the **If yes** branch, directly below the approval action, select **Add an action**.
36. In the search field, enter `condition`.
37. Select **Condition**, and set its first field to the approval action's **Outcome** dynamic content, operator **is equal to**, value `Approve`.
38. In this inner condition's **If yes** branch, add an **Update a row** action against the Microsoft Dataverse connector, set **Table name** to **Guest Preferences** (plural, same reason as step 9), set **Row ID** to the trigger's own row-identifier dynamic content (the table's primary key field, generated automatically for every Dataverse table), and set the **Flagged** column to reflect approval.
39. In this inner condition's **If no** branch, add a second **Update a row** action the same way, setting **Flagged** to reflect rejection instead, so a rejected request is logged rather than silently dropped.
40. In the outer condition's (step 25) **If no** branch, select **Add an action**.
41. In the search field, enter `send an email`.
42. Select **Send an email (V2)** under Office 365 Outlook (or your team's preferred notification connector, such as Teams), addressed to housekeeping, using the Compose action's output as the message body — with no approval gate on this branch.
43. Select **Save**.
44. Add another sample row to Guest Preference with the same no-cost preference type as step 20, then confirm, in **Run history**, that this run still reaches the **If no** branch's notification with no approval requested.
45. Add a sample row to Guest Preference with the cost-bearing preference type from step 28 (for example, `Amenity`), then confirm, in **Run history**, that this run pauses at the **Start and wait for an approval** step, shown as still running and waiting on a response.
46. Respond to the pending approval as the named approver, from the email, the Teams adaptive card, or the Power Automate action center.
47. Reopen the flow's run history (as in step 21) and confirm the run completed down the branch matching your response, with the Guest Preference row's **Flagged** column updated accordingly.

**Expected Result:**
One flow that, run against a no-cost sample preference row, notifies housekeeping directly with no gate; and, run against a cost-bearing sample preference row, pauses at a manager approval step and only proceeds to the approved or rejected outcome action once that manager responds, updating the Guest Preference row's status either way.

**Troubleshooting:**
- Dataverse trigger's **Change type** left at all three events (added, modified, *and* deleted) instead of just **Added** → this fires the flow again on every later edit to the same row, producing duplicate notifications for what should be a one-time event. Reopen the trigger card and confirm **Change type** is set to **Added** only.
- Notification text references the trigger's raw **Guest** lookup field directly instead of the Get-a-row-by-ID action's retrieved name field → the lookup column resolves to an internal record reference, not a human-readable name, which is exactly why step 12's lookup action exists. Rebuild the Compose action's input using the Get-a-row-by-ID action's name field instead.
- A rejected approval silently ends the flow with no logged outcome → check that step 39's **If no** branch under the inner condition actually exists and updates the row; without it, "approved" and "never resolved" are indistinguishable later.
- Named more than one approver but chose **Approve/Reject - First to respond**, expecting to need everyone's sign-off → these are genuinely different decision shapes; **First to respond** completes on any one approver's answer, while **Approve/Reject - Everyone must approve** waits for all of them. Reopen the approval action and change **Approval type** if this isn't the behavior you tested for.
- Condition (step 28) never routes to the approval branch even for a row you expect to match → **Preference Type** is a plain Text column with no enforced list of values, so the exact `is equal to Amenity` check only matches text spelled and capitalized exactly that way. Check the actual value in the sample row (or whatever Exercise 3's screen submitted) and match it exactly, or change the condition's comparison to something less strict.

### Exercise 2: For a Team Choosing Power Automate as Its Sprint 3 Automated Workflow, Apply This Flow to That Capstone Task
**Objective:**
By the end of this exercise, a team whose real Sprint 3 automated workflow is a Power Automate flow (The Aldwyn House, Meridian Kitchens Collective, Meridian Stays, or any other team that has chosen Power Automate as its path) will have used Exercise 1's trigger-action-approval skeleton as a template to identify the real trigger, actions, and approval decision their own flow needs, then rebuilt it against their own data. A team whose real deliverable is a UiPath automation (Meridian Resorts & Spa or Meridian Residences) instead confirms today's skills exercise is complete and records what carries forward.

**Prerequisites for this exercise:**
- Module 2, Exercise 1 must be complete and working.
- Know which of the two paths — Power Automate or UiPath — your team has chosen for its real Sprint 3 automated workflow.

**Steps:**
1. Confirm which path your team has chosen for its real Sprint 3 automated workflow: Power Automate or UiPath.
2. **If your team's real workflow is a Power Automate flow:** write down your team's actual Dataverse trigger table and event — **[Placeholder — replace with your team's actual Sprint 3 automated workflow's real Dataverse trigger table and event]**.
3. Write down your team's actual lookup/compose actions and the data they need — **[Placeholder — replace with your team's actual Sprint 3 automated workflow's real lookup/compose actions and the data they need]**.
4. Decide, using the same reasoning Exercise 1 applied when it introduced the approval step, whether your team's real flow needs a genuine approval step at all, and if so, name its approver and branch logic — **[Placeholder — replace with your team's decision on whether your real flow needs a genuine approval step, and if so, its approver and branch logic]**.
5. Using Exercise 1's flow as your starting template, rebuild its trigger, actions, and (if you decided you need one) approval step against your own team's real Dataverse table and data instead of Guest Preference.
6. Save the new flow, then test it against a real or realistic sample row from your own team's own table, the same way you tested Exercise 1's flow.
7. **If your team's real workflow is a UiPath automation:** confirm Exercise 1's steps 1-47 are complete — that flow is today's finished skills exercise for your team.
8. Note, in your team's shared planning document, that your real automation deliverable is built on the later UiPath day, using this same trigger-action-approval mental model, expressed through Orchestrator queues instead of Power Automate connectors.

**Expected Result:**
A Power-Automate-choosing team has a working flow built against its own real Dataverse table and data, tested against at least one real or realistic sample row, with an explicit written decision on whether it needs an approval step. A UiPath-choosing team has confirmed Exercise 1's flow is complete and has a written note connecting today's skeleton to its later UiPath deliverable.

**Troubleshooting:**
- Unsure whether your team's real flow needs an approval step → none of the five teams' named Sprint 3 automations obviously need one by nature, since all are described as fully automatic ("automatically notify," "automatically send," "automatically generate and flag"). Add one only if a real customer-facing or cost-bearing action in your own flow genuinely warrants a human check first.
- No further common pitfalls noted for this exercise beyond the approval-step judgment call above — the rest of this exercise is a direct application of Exercise 1's already-tested mechanics to different data.
