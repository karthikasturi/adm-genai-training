# Day 18 Lab Guide: Power Platform Automation

Source content: `course-outline/Day18_Power_Platform_Automation_Content.md` (course-content-architect output). Every UI-specific step below (menu paths, button labels, connector and action names) was checked against Microsoft's current Power Apps, Power Automate, and Power BI documentation before publishing. Each exercise below is self-contained — work through any one of them with nothing else open but this document.

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

## Module 3: Power BI Reporting (Individual Assignment)

Module 2's own Topic 4 teaches Power BI at overview level only — what a report and a dashboard are, and that Dataverse is a supported data source — because the outline's own Module 18B hands-on bullets don't ask for a built report in the shared classroom activity. The individual assignment does: "Build one Canvas app screen + one Power Automate flow + one Power BI report against sample data," submitted on your own. Module 1 and Module 2 above already cover the first two artifacts; this module covers the third, on your own time, against sample data rather than your team's shared environment.

This exercise stays entirely inside the Power BI **service** at `https://app.powerbi.com` — the same cloud surface Power Apps and Power Automate already run in — rather than the Power BI Desktop application. No software installation is required: uploading data, modeling relationships and measures, building the report, and pinning to a dashboard are all done in the browser, using Power BI's web-based semantic model editor.

**Sample data:** six CSV files at `lab/day09/sample-data/` — synthetic, not real guest data — modeled on the same Meridian Hospitality Group schema every module this week has used: `properties.csv` (10 rows), `rate_plans.csv` (12 rows), `guests.csv` (60 rows), `reservations.csv` (180 rows), `folios.csv` (180 rows, one per reservation), and `guest_preferences.csv` (50 rows, the same table Module 1 modeled in Dataverse — this module works from the flat CSV copy, not the Dataverse table itself, so it doesn't depend on your team's shared environment still being available).

### Exercise 1: Build a Power BI Report Against Sample Hospitality Data
**Objective:**
By the end of this exercise, you will have a Power BI semantic model in your workspace connected to all six sample tables, related to each other through six manually-built relationships, with six DAX measures, a report page with three cards, a bar chart, a line chart, a donut chart, a table, and a slicer that filters every visual on the page at once — with three of those visuals pinned to a new dashboard. Everything is built and saved directly in the Power BI service; there is no separate publish step.

**Prerequisites for this exercise:**
- A Power BI account (a work/school account, or a free Microsoft account) you can sign in with at `https://app.powerbi.com`, and write access to at least one workspace — your own **My workspace** is enough for this individual assignment.
- No software installation — this exercise does not use Power BI Desktop.
- None of Module 1 or Module 2 is required to complete this exercise using the CSV sample data path.

**Steps:**
1. Go to `https://app.powerbi.com` and sign in with your Power BI account.
2. In the left navigation pane, select the workspace you want to build this assignment in (your own **My workspace** is fine).
3. Select **New item**, then, under **Store data**, select **Semantic model**. **[Verified current: a new semantic model in the Power BI service is started from a workspace's New item button, under Store data — confirmed against Power BI's current CSV data-source documentation.]**
4. In the window that appears, select **CSV**.
5. Select **Upload file**, browse to `lab/day09/sample-data/properties.csv`, select it, then select **Open**.
6. Select **Next**.
7. Preview the data to confirm the column headers (`property_id`, `name`, `brand`, `address`, `timezone`) and a few sample rows look correct, then select **Next**.
8. Select **Create a semantic model only** (not **Create a report**) — you'll add the other five tables before building the report.
9. Enter a name for the semantic model — for example **[Placeholder — replace with your own semantic model name]** — then select **Create**. Confirm the web model editor opens, showing one table, **properties**, in the **Data** pane.
10. If the page shows **Viewing mode** near the top, switch it to **Editing mode** — every step below needs Editing mode. **[Verified current: semantic models opened in the Power BI service default to read-only Viewing mode; switching to Editing mode is required before any change (including Get data, relationships, and measures) can be made — confirmed against Power BI's current web-modeling documentation.]**
11. Select the **properties** table in the **Data** pane and check its column names. Because every column in `properties.csv` is text (there's no number, date, or true/false column anywhere in the file for Power Query to notice as "different" from a header row), Power Query's automatic header detection has nothing to go on and the table can land with generic headers — `Column1`, `Column2`, `Column3`, `Column4`, `Column5` — instead of `property_id`, `name`, `brand`, `address`, `timezone`; the other five files each have at least one number, date, or true/false column and don't hit this. **[Verified current: Power Query only auto-promotes a file's first row to column headers when it detects a different pattern in that row versus the rows below it; a file where every column is text, like properties.csv, gives it nothing to detect on, so the header row can be left as plain data under generic Column1/Column2/... names — confirmed against Power Query's current header-promotion documentation.]**
12. With **properties** still selected, select **Transform data** in the ribbon — this opens the Power Query editor for the **properties** query.
13. In the Power Query editor's preview grid, select the small table icon in the upper-left corner, then select **Use First Row as Headers** — confirm the column headers change from `Column1`-`Column5` to `property_id`, `name`, `brand`, `address`, `timezone`, and the row that held those five label values is gone from the data grid (it's now the header row, not a data row).
14. Select the button that applies your change and returns you to the model editor — labeled **Close & Apply**, **Apply**, or **Save & close** depending on your tenant's version; look for whichever option isn't **Cancel** or **Discard** — then confirm you're back in the model editor and the **properties** table in the **Data** pane now shows the five real column names.
15. In the ribbon, select **Get data**.
16. In the Power Query **Get data** window, select **Text/CSV** (CSV files use the same connector as plain text files).
17. Select **Upload file**, browse to `lab/day09/sample-data/rate_plans.csv`, select it, select **Open**, then complete the connector's steps to add it to the model — confirm a second table, **rate_plans**, now appears in the **Data** pane with its real column names (`rate_plan_id`, `property_id`, `name`, `nightly_rate`, `cancellation_policy`), not `Column1`/`Column2`/etc. — the `nightly_rate` numeric column gives Power Query the pattern it needs to auto-promote headers correctly here.
18. Repeat steps 15-17 for the remaining four files, one at a time: `guests.csv`, `reservations.csv`, `folios.csv`, and `guest_preferences.csv` — confirm the **Data** pane lists all six tables when you're done: **properties**, **rate_plans**, **guests**, **reservations**, **folios**, **guest_preferences**, each with real column names.
19. In the **Data** pane, expand **reservations** and confirm `check_in` and `check_out` show a date icon; expand **folios** and confirm `balance` shows a numeric icon — if a column shows a text icon instead, select that column, then use the **Properties** pane to set its correct **Data type**.
20. Select the **reservations** table in the **Data** pane, then in the ribbon select **New column**.
21. In the formula bar, replace the default text with `Nights = DATEDIFF(reservations[check_in], reservations[check_out], DAY)` and press **Enter** — confirm a new **Nights** column appears in **reservations**, showing a whole number of nights for every row.
22. Look at the relationship diagram in the model editor and confirm no lines connect any of the six tables yet. **[Verified current: unlike Power BI Desktop, importing tables with Get data in the Power BI service does not auto-detect or import relationships — they must be created manually in the web model editor, even when the joining columns are named identically — confirmed against Power BI's current web-modeling documentation.]**
23. In the ribbon, select **Manage relationships**.
24. In the **Manage relationships** dialog, select **New relationship**.
25. Select **rate_plans** as the first table and `property_id` as its column; select **properties** as the second table and `property_id` as its column; confirm **Cardinality** shows **Many to one (\*:1)** with **rate_plans** on the many side, then select **OK**.
26. Repeat steps 23-25 four more times to create the remaining relationships, always picking the "many" table first: **reservations** `property_id` → **properties** `property_id`; **reservations** `guest_id` → **guests** `guest_id`; **reservations** `rate_plan_id` → **rate_plans** `rate_plan_id`; **folios** `reservation_id` → **reservations** `reservation_id`; and **guest_preferences** `guest_id` → **guests** `guest_id` — six relationships in total once you're done (the one from step 25 plus these five).
27. Close the **Manage relationships** dialog and confirm the relationship diagram now shows six lines connecting the six tables, each ending in "1" on the one side and an asterisk "\*" on the many side.
28. Select the **reservations** table in the **Data** pane, then in the ribbon select **New measure**. **[Verified current: a measure is created by selecting a table in the Data pane and choosing New measure in the ribbon, with a DAX formula bar carrying the same autocomplete/IntelliSense as Power BI Desktop — confirmed against Power BI's current web-modeling documentation.]**
29. In the formula bar, enter `Total Reservations = COUNTROWS(reservations)` and press **Enter** — confirm the new measure appears under **reservations** in the **Data** pane, marked with a calculator icon.
30. With **reservations** still selected, select **New measure** again and enter `Total Room Nights = SUM(reservations[Nights])`, then press **Enter**.
31. Select **folios** in the **Data** pane, select **New measure**, and enter `Total Revenue = SUM(folios[balance])`, then press **Enter**.
32. With **folios** still selected, select **New measure** again and enter `Average Daily Rate = DIVIDE([Total Revenue], [Total Room Nights])`, then press **Enter** — `DIVIDE` returns a blank instead of an error when the denominator is zero, which a plain `/` operator would not.
33. Select **guest_preferences**, select **New measure**, and enter `Flagged Preferences = CALCULATE(COUNTROWS(guest_preferences), guest_preferences[flagged] = TRUE)`, then press **Enter**.
34. With **guest_preferences** still selected, select **New measure** again and enter `Flagged Preference Rate = DIVIDE([Flagged Preferences], COUNTROWS(guest_preferences))`, then press **Enter** — confirm the **Data** pane now shows six calculator-icon measures in total, spread across **reservations** (Total Reservations, Total Room Nights), **folios** (Total Revenue, Average Daily Rate), and **guest_preferences** (Flagged Preferences, Flagged Preference Rate).
35. In the ribbon, select **New report** — confirm a new browser tab opens with the report editor, built on this semantic model.
36. On the report canvas, select a blank area, then in the **Visualizations** pane select the **Card** visual.
37. Drag **folios**[Total Revenue] onto the card's field well — confirm the card displays a single number.
38. Repeat steps 36-37 twice more to add a second card showing **reservations**[Total Room Nights] and a third card showing **folios**[Average Daily Rate].
39. Select a new blank area, then in the **Visualizations** pane select the **Clustered column chart** visual.
40. Drag **properties**[name] onto the **X-axis** field well and **folios**[Total Revenue] onto the **Y-axis** field well — confirm the chart shows one bar per property, with the three Meridian Resorts & Spa properties among the tallest bars (they carry this sample data's highest nightly rates).
41. Select a new blank area, then select the **Line chart** visual.
42. Drag **reservations**[check_in] onto the **X-axis** field well — Power BI adds it as a date hierarchy; select the field's dropdown arrow in the field well and choose **Month** instead of **Date**.
43. Drag **reservations**[Total Reservations] onto the **Y-axis** field well — confirm the line shows reservation counts rising and falling by month across 2026.
44. Select a new blank area, then select the **Donut chart** visual.
45. Drag **guest_preferences**[preference_type] onto the **Legend** field well, then drag it a second time onto the **Values** field well — because it's a text field, Power BI automatically aggregates it as **Count of preference_type** — confirm the donut shows four slices: Dietary, Room, Amenity, and Accessibility.
46. Select a new blank area, then select the **Table** visual.
47. Drag **guests**[loyalty_tier], **reservations**[Total Reservations], and **folios**[Total Revenue] onto the table's **Columns** field well, in that order — confirm the table lists four rows (None, Silver, Gold, Platinum), each with its own reservation count and revenue total, proving `loyalty_tier` on **guests** correctly rolls up through the **guests** → **reservations** → **folios** relationship chain.
48. Select a new blank area, then select the **Slicer** visual.
49. Drag **properties**[brand] onto the slicer's field well — confirm the slicer lists four checkboxes: The Aldwyn House, Meridian Resorts & Spa, Meridian Stays, and Meridian Residences.
50. Select one checkbox in the new slicer (for example, Meridian Resorts & Spa) and confirm every other visual on the page — both remaining cards, the bar chart, the line chart, the donut chart, and the table — updates to reflect only that brand's data.
51. Clear the slicer selection (select the small eraser/filter icon in the slicer's top-right corner) so the report returns to showing all properties.
52. Select **Save** near the top of the page (or press **Ctrl+S**), enter a name for the report — for example **[Placeholder — replace with your own report name]** — confirm the destination workspace matches the one from step 2, then select **Save** again — confirm a save confirmation appears and the report tab's title updates to the name you entered.
53. Hover over the bar chart (Total Revenue by property), then select its pin icon in the visual's top-right corner. **[Verified current: dashboards exist only in the Power BI service (they cannot be created in Power BI Desktop even when Desktop is used) — a visual is pinned to one from its hover pin icon, choosing New dashboard or Existing dashboard in the Pin to dashboard dialog — confirmed against Power BI's current dashboard-creation documentation.]**
54. In the **Pin to dashboard** dialog, select **New dashboard**, enter a name — for example **[Placeholder — replace with your own dashboard name]** — then select **Pin**.
55. When the "Pinned to dashboard" confirmation appears, select **Go to dashboard** — confirm a new dashboard opens with one tile showing the pinned bar chart.
56. Return to the report (select the tile, or use the left-hand navigation pane to reopen the report), then repeat steps 53-54 two more times to pin the Total Revenue card and the donut chart to the same dashboard — this time, select **Existing dashboard** and choose the dashboard you just created instead of **New dashboard**.
57. Reopen the dashboard from the left-hand navigation pane and confirm it now shows three tiles: the bar chart, the revenue card, and the donut chart.

**Expected Result:**
One Power BI semantic model in your workspace, built entirely in the browser, connected to all six sample hospitality tables and related through six manually-built relationships; six DAX measures (Total Reservations, Total Room Nights, Total Revenue, Average Daily Rate, Flagged Preferences, Flagged Preference Rate); a saved report page with three cards, a bar chart, a line chart, a donut chart, a table, and a slicer that filters every other visual at once when a brand is selected; and a dashboard with three pinned tiles — fulfilling the individual assignment's "one Power BI report against sample data" requirement, with no Power BI Desktop installation used at any point.

**Troubleshooting:**
- The page opens in **Viewing mode** and none of the ribbon's editing buttons (Get data, New column, Manage relationships, New measure) respond → switch to **Editing mode** first (step 10); Viewing mode intentionally blocks changes.
- A table's columns show generic names — `Column1`, `Column2`, and so on — instead of your CSV's real header row → expected for **properties.csv** specifically, since every one of its columns is text with nothing for Power Query's auto-detection to key off (steps 11-14 fix it); if it happens on another table too, fix it the same way: select that table → **Transform data** → the table icon in the preview grid's upper-left corner → **Use First Row as Headers** → apply your changes back to the model.
- Every column in a CSV preview shows as plain text instead of Date, Number, or True/False → select that column and set its **Data type** manually in the **Properties** pane rather than relying on autodetection.
- No relationship lines appear after loading all six tables, even though the `_id` columns match exactly → this is expected, not a bug — the web Get data experience never auto-detects relationships the way Power BI Desktop does; build all six manually with **Manage relationships** → **New relationship** (steps 23-26).
- A card or chart shows blank or shows the same total for every category → almost always a missing or wrong relationship, not a wrong measure — reopen the relationship diagram and check all six lines before touching the DAX formula.
- **Average Daily Rate** shows an error instead of a blank for a filter with zero room nights → confirm the measure uses `DIVIDE(...)`, not a plain `/` operator; `DIVIDE` returns blank on a zero denominator instead of raising a divide-by-zero error.
- **Save** on the report gives a permissions error → you need write (Build) permission on the semantic model and write permission on the destination workspace; **My workspace** always grants both to its owner, so switch the save destination there if your organizational workspace is the problem.
- The pin icon doesn't appear when hovering over a visual → pin icons only appear once the report is open in **Edit** mode, not **Reading** view — select **Edit** first.

**Sources:**
- [Get data from comma separated value (CSV) files](https://learn.microsoft.com/en-us/power-bi/connect-data/service-comma-separated-value-files)
- [Edit semantic models in the Power BI service](https://learn.microsoft.com/en-us/power-bi/transform-model/service-edit-data-models)
- [Promote or demote column headers](https://learn.microsoft.com/en-us/power-query/table-promote-demote-headers)
- [Create a Power BI dashboard from a report](https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboard-create)
- [What is Power BI?](https://learn.microsoft.com/en-us/power-bi/fundamentals/power-bi-overview)
- [Create a Power BI report using the Microsoft Dataverse connector](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-platform-powerbi-connector)
