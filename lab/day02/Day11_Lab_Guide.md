# Day 11 Lab Guide: Azure Cloud Foundations & Security Hardening

Source content: `Day11_Azure_Cloud_Foundations_Content.md` (course-content-architect output). Each exercise below is self-contained — work through any one of them with nothing else open but this document.

## Module 1: Azure App Service & Microsoft Entra ID Essentials

### Exercise 1: Deploy a web app to Azure App Service using a deployment slot for staged rollout
**Objective:**
By the end of this exercise, you will have a web app running in Azure App Service, reachable at its own production URL, plus a `staging` deployment slot you used to test a change before swapping it live — so a bad release gets caught by your team, not by users, and a swap gives you a clean way back.

**Prerequisites for this exercise:**
- The team's Azure subscription access and per-team resource group must be active (course prerequisite).
- Have the capstone's architecture diagram from the Day 6-to-9 kickoff sprint open — it names the application you're deploying and the framework it's built in, which you'll need to pick the right runtime stack and operating system in steps 7 and 8.

**Steps:**
1. In the Azure portal, open **App Services**.
2. Select **Create**.
3. From the menu that appears, select **Web App** — not **Web App + Database**, **Static Web App**, or any of the other app-creation options listed alongside it; those provision extra resources (a database, extra networking, and so on) this exercise doesn't need. **[Verified current: App Services > Create now opens a menu of app types instead of going straight to the Basics tab — Web App is the plain option that matches the rest of these steps.]**
4. On the **Basics** tab, under **Resource Group**, select the team's resource group.
5. Under **Name**, enter a unique name for the app, for example **[Placeholder — replace with your team's actual capstone/application name]-web**.
6. Under **Publish**, choose **Code** (or **Container** if the team is deploying a pre-built image).
7. Under **Runtime stack**, select the language and version matching the capstone's architecture diagram.
8. Under **Operating System**, choose the OS the capstone's architecture diagram calls for (Linux is the common default for most modern stacks; choose Windows only if the app specifically needs it).
9. Under **Region**, choose a region — agree on this as a team before continuing, since it's a sticky choice today's storage account (Module 2, Exercise 1) will also need to match.
10. Under **App Service Plan**, select **Create new** and choose the **Standard** tier or higher — deployment slots aren't available on the Free, Shared, or Basic tiers, so this choice is what makes step 17 possible later.
11. Select **Review + create**.
12. Review the settings shown, then select **Create**.
13. Wait for the deployment to finish — you'll see a "Your deployment is complete" confirmation — then select **Go to resource**.
14. On the app's **Overview** page, find the app's default URL near the top of the page and open it in a new tab to confirm the app loads.
15. Deploy the team's actual application code to this app, using whichever method the team's toolchain already supports (for example, VS Code's Azure extension, a ZIP deploy, or an existing CI/CD pipeline).
16. Reload the default URL from step 14 and confirm the deployed code is now what's showing.
17. From the app's left menu, select **Deployment**, then **Deployment slots**.
18. Select **Add**.
19. In the panel that opens, enter `staging` as the slot's **Name**.
20. Under **Clone settings from**, select the production slot (listed under the app's own name), so the new slot starts with the same configuration.
21. Select **Add** — the new slot appears on the **Deployment slots** page with **Traffic %** at 0, meaning no live traffic reaches it yet.
22. Select the new `staging` slot to open its own resource page, and note its URL, shown as `<app-name>-staging.azurewebsites.net`.
23. Deploy a small, visible change (for example, an updated page title) to the `staging` slot specifically, using the same deployment method as step 15.
24. Open the `staging` slot's own URL from step 22 and confirm the change is visible there.
25. Open the production URL from step 14 again and confirm it still shows the old version — the change hasn't reached production yet.
26. Return to the app's **Deployment slots** page.
27. Select **Swap**.
28. Under **Source**, select `staging`.
29. Under **Target**, confirm **production** is selected.
30. Select the **Source slot changes** tab and review what will change.
31. Select the **Target slot changes** tab and review what will change.
32. Select **Start Swap**, and wait for a confirmation that the swap completed.
33. Open the production URL from step 14 once more and confirm it now shows the change you tested in staging in step 24.

**Expected Result:**
The production URL shows the change that was deployed and tested in the `staging` slot first — the same page title update (or whatever change you made in step 23) is now live at the app's default URL, and the `staging` slot's own URL still works independently at `<app-name>-staging.azurewebsites.net`.

**Troubleshooting:**
- **Deployment slots > Add is greyed out or missing** → The App Service plan is on the Free, Shared, or Basic tier. Go back to the app's **Scale up (App Service plan)** page and upgrade to Standard or higher; deployment slots simply don't exist below that tier.
- **You deployed straight to production and only created the staging slot afterward** → This skips the entire point of the exercise. Undo it: deploy the next change to `staging` first, confirm it there, and only then swap — don't treat staging as an afterthought once production is already updated.
- **A custom domain or IP restriction didn't move with the swap** → This is expected, not a bug. Custom domain names, publishing endpoints, scale settings, and IP restrictions never swap and always stay attached to their own slot; only settings not explicitly marked slot-specific move by default.

### Exercise 2: Register an application in Microsoft Entra ID
**Objective:**
By the end of this exercise, you will have registered the capstone application in Microsoft Entra ID, giving the application itself an identity, separate from any person's sign-in, that a later role assignment (Module 2, Exercise 2) can grant access to Azure resources.

**Prerequisites for this exercise:**
None beyond the course prerequisites.

**Steps:**
1. Go to the **Microsoft Entra admin center** at `entra.microsoft.com` and sign in with the team's Azure credentials. **[Verified current: app registration now happens in the Microsoft Entra admin center rather than the classic Azure portal — Microsoft's own current registration guide directs users to entra.microsoft.com for this task, not portal.azure.com.]**
2. In the left-hand navigation, expand **Entra ID**, then select **App registrations**.
3. Select **New registration**.
4. Under **Name**, enter a name identifying the capstone application, for example **[Placeholder — replace with your team's actual capstone/application name]-app**.
5. Under **Supported account types**, choose **Accounts in this organizational directory only** — the correct scope for an internal capstone application with no external tenant users.
6. Leave **Redirect URI (optional)** blank — this registration is standing in for the application's resource-access identity today, not its user sign-in flow.
7. Select **Register**.
8. On the app's **Overview** page, find and record the **Application (client) ID** — you'll need it in Module 2, Exercise 2.
9. On the same **Overview** page, find and record the **Directory (tenant) ID** — you'll need this one too.

**Expected Result:**
An app registration exists in Microsoft Entra ID under the name you chose in step 4, and you have both its Application (client) ID and its Directory (tenant) ID written down for later use.

**Troubleshooting:**
- **Unsure whether the Application (client) ID needs to be kept secret** → It doesn't. It identifies the app but isn't itself a credential, so it's fine to record it in a shared document. The distinction matters once the team eventually adds authentication (out of scope for today), but don't guard this value like a password.
- No other common pitfalls noted for this exercise.

## Module 2: Azure Storage & Cross-Cloud Security Essentials

### Exercise 1: Create Blob and Table storage for the capstone application
**Objective:**
By the end of this exercise, you will have one Azure storage account holding a Blob container (for unstructured files) and a Table (for schemaless structured records), giving the capstone application a place to store data on its second cloud.

**Prerequisites for this exercise:**
The App Service app from Module 1, Exercise 1 should exist, since this exercise creates the storage account in the same region for consistency — if it doesn't exist yet, pick any region and continue.

**Steps:**
1. In the Azure portal, open **Storage accounts**.
2. Select **Create**.
3. On the **Basics** tab, under **Resource group**, select the team's resource group.
4. Under **Storage account name**, enter a globally unique name, for example **[Placeholder — replace with your team's actual capstone name]storage**.
5. Under **Region**, choose the same region used for the App Service app in Module 1, Exercise 1.
6. Under **Preferred storage type**, leave the default selected — this field only shapes Azure's in-portal guidance, not which services the account can use, so it doesn't matter that this account will hold both a container and a table.
7. Leave **Performance** set to **Standard** (the default).
8. Leave **Redundancy** at its default for this exercise.
9. Select **Review + create**.
10. Review the settings shown, then select **Create**.
11. Wait for the deployment to finish — you'll see a "Your deployment is complete" confirmation — then select **Go to resource**.
12. From the storage account's left menu, under **Data storage**, select **Containers**.
13. Select **+ Container**.
14. Under **Name**, enter a container name, for example `capstone-artifacts`.
15. Leave the anonymous access level set to **Private (no anonymous access)** (the default).
16. Select **Create** — the new container appears in the Containers list.
17. From the storage account's left menu, select **Storage browser**. **[Verified current: table creation now goes through the storage account's Storage browser rather than a standalone "Tables" menu item, per Microsoft's current Table storage guidance.]**
18. In the Storage browser's resource tree, select **Tables**.
19. Select **Add table**.
20. Enter a table name, for example `capstonemetadata`, then select **OK** — the new table appears in the Tables list.

**Expected Result:**
The storage account's **Containers** page lists the new container (for example `capstone-artifacts`), and its **Tables** page lists the new table (for example `capstonemetadata`) — one storage account, two purpose-built places to put data.

**Troubleshooting:**
- **The container was created with public access instead of private** → Open the container's **Change access level** option and set it back to **Private (no anonymous access)**. Public access reverses the least-privilege posture this whole day is building toward — Module 2, Exercise 2 assumes this container started private.
- No other common pitfalls noted for this exercise.

### Exercise 2: Write a least-privilege RBAC policy set spanning the capstone's AWS IAM and Microsoft Entra ID resources
**Objective:**
By the end of this exercise, you will have assigned the app registration from Module 1, Exercise 2 a least-privilege role on today's storage account, and written a two-cloud document confirming that both the capstone's AWS identity (from yesterday) and its Azure identity (from today) are scoped to specific resources, not wildcards.

**Prerequisites for this exercise:**
- The storage account, container, and table from Module 2, Exercise 1 must exist.
- The app registration and Application (client) ID from Module 1, Exercise 2 must exist.
- Have Module 10B's AWS IAM role name and policy details (specifically, the resource ARN it names) on hand.
- Read Topic 2's concrete role-assignment example in the source content (or Slide 5's speaker notes) before starting — it shows actual Principal/Role/Scope values for this exact scenario, which makes step 3 and step 14 easier than reasoning from the abstract definition alone.

**Steps:**
1. From the storage account's left menu, select **Access Control (IAM)**.
2. Select **Add**, then **Add role assignment**.
3. On the **Role** tab, use the search box to find a storage-data-scoped built-in role matching what the app actually needs (for example, a role granting read/write access to blob data specifically — not **Owner** or **Contributor**).
4. Select the role, then select **Next**.
5. On the **Members** tab, select **User, group, or service principal**.
6. Select **+ Select members**.
7. In the search box, type the name of the app registration created in Module 1, Exercise 2, select it from the results, then select **Select**.
8. Select **Next**. **[Verified current: the portal may now show optional **Conditions** and **Assignment type** tabs here before **Review + assign**.]** If either appears, select **Next** again without changing anything on them — neither applies to this exercise.
9. On the **Review + assign** tab, confirm the **Scope** shown is this specific storage account — not the resource group or subscription.
10. Select **Review + assign** — the new role assignment appears on the storage account's **Access control (IAM) > Role assignments** tab.
11. As a team, open the shared document tracking the capstone's architecture.
12. Create a two-column table headed **AWS IAM** and **Azure RBAC**.
13. In the **AWS IAM** column, record Module 10B's actual IAM role name and the specific resource ARN(s) its policy names.
14. In the **Azure RBAC** column, record today's app registration name, its Application (client) ID, the built-in role assigned in step 10, and the storage account name it's scoped to.
15. Under each column, write one sentence confirming that side's assignment names a specific resource rather than a broad wildcard or subscription-wide scope.
16. Save the document — it's the capstone's cross-cloud identity record for the rest of the course, and later modules extend it rather than starting a new one.

**Expected Result:**
The storage account's **Role assignments** tab lists the app registration as principal, a storage-data-scoped role (not Owner or Contributor), and the storage account itself as scope. The saved document names both cloud identities by their actual resource names — not by resource type — and each side has one sentence confirming it isn't scoped to a wildcard.

**Troubleshooting:**
- **You assigned Owner or Contributor "to make sure it works"** → Remove that assignment and re-do steps 2–10 with a storage-data-scoped role instead. Owner and Contributor at subscription or resource-group scope grant far more than the app needs, and is exactly the over-privileged mismatch this exercise exists to catch.
- **The document lists "an S3 bucket" or "a storage account" instead of the actual resource name** → Go back and replace the resource type with the specific name and ARN or resource ID. A scope check that names a category instead of one resource doesn't actually confirm least privilege.
- **Treating this document as a one-time task** → It isn't. Every later module's cloud resources build on this least-privilege baseline, so keep it updated as the capstone grows rather than filing it away as finished.

