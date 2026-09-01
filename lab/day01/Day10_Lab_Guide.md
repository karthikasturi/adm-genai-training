# AWS Cloud Foundations — Participant Lab Guide

Follow this guide on your own, in order. You don't need the slides or a facilitator open next to
you — everything you need to complete each exercise is on this page. Built from
`Day10_AWS_Cloud_Foundations_Content.md`'s two Hands-On Activities, split into one exercise per
named hands-on task, with every console step checked against current official AWS documentation
before this guide was written.

## Module 1: AWS Compute Essentials

### Exercise 1: Launch an EC2 instance from an AMI
**Objective:**
By the end of this exercise you will have one running EC2 instance, launched from a ready-made
AMI. This instance is what Exercise 2 and Exercise 3 both build on next.

**Prerequisites for this exercise:**
- Your team's AWS console and programmatic account access is active (from Software Requirements).
- Your team has agreed, out loud, on one AWS Region to use for the rest of the week. Write it down
  if you need to — every later exercise today depends on it.

**Steps:**
1. Open the Amazon EC2 console. Check the Region name in the top right corner of the screen. If it does not match your team's agreed Region, click it and choose the correct Region now, before doing anything else.
2. On the EC2 dashboard, click **Launch instance**.
3. Under **Name and tags**, click the **Name** field and type a name for this instance. Use your team/capstone name, for example **[Placeholder — replace with your team's actual capstone/application name]**-web-01.
4. Under **Application and OS Images (Amazon Machine Image)**, click a free-tier eligible AMI card (Amazon Linux or Ubuntu Server). A blue outline appears around the AMI you selected — that's how you know it's chosen.
5. Under **Instance type**, click a free-tier eligible instance type from the list (for example, t2.micro or t3.micro, if either is marked "Free tier eligible").
6. Under **Key pair (login)**, click the **Key pair name** dropdown and choose **Create new key pair**.
7. In the **Create key pair** window, type a name for the key pair, leave the key pair type and file format at their defaults, and click **Create key pair**. Your browser will download a file — keep it, you'll need it later to connect to this instance over SSH.
8. Under **Network settings**, click **Edit**. Do not change anything on this screen — just look at the **VPC** and **Subnet** fields and note that they're already filled in. This is your account's default VPC, provided automatically so you don't have to design a network today.
9. Scroll down to **Configure storage**. Leave every setting here at its default and do not change anything.
10. Scroll down to the **Summary** panel on the right side of the page and check that the AMI, instance type, and key pair name all show what you chose in steps 4 through 6.
11. Click **Launch instance**.
12. Click **View all instances**. Find your new instance in the list and watch the **Instance state** column. It starts as "Pending" and changes to "Running" within about a minute — wait for "Running" before starting Exercise 2.

**Expected Result:**
One EC2 instance listed in the EC2 console with an **Instance state** of "Running."

**Troubleshooting:**
- You skipped the key pair in step 6 and now can't connect to the instance over SSH → This is fine for today's exercise, but if your team plans to SSH into this instance later this week, go back to the instance's **Actions → Security → Get Windows password** menu (Windows) or relaunch with a key pair attached (Linux) rather than trying to add one after the fact.
- Your instance is stuck on "Pending" for more than a couple of minutes → Refresh the Instances page. If it's still Pending, check the **Status Check** column for a failure reason before assuming something is wrong.

**Sources:**
- [Amazon EC2: Launch an EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial-launch-my-first-ec2-instance.html)

### Exercise 2: Configure a basic auto-scaling group for the instance
**Objective:**
By the end of this exercise your Exercise 1 instance will be part of a small Auto Scaling group,
so a lost instance can be automatically replaced.

**Prerequisites for this exercise:**
- The instance from Exercise 1 must show **Running** in the EC2 console.

**Steps:**
1. In the EC2 console's Instances list, select the checkbox next to your running instance, then click **Actions**, then **Image and templates**, then **Launch more like this**.
2. On the **Launch an instance** page that opens, scroll to the bottom and click the **consider EC2 Auto Scaling** link.
3. In the **Launch into Auto Scaling Group** window that appears, click **Continue**.
4. On the **Create launch template** page, type a name and a short description for the launch template.
5. Check that **Key pair (login)** and the security group under **Network settings** already show the same key pair and security group from Exercise 1. Do not change them.
6. Click **Create launch template**.
7. On the confirmation page, click **Create Auto Scaling group**.
8. On the **Choose launch template or configuration** page, type a name for the Auto Scaling group. Check that **Launch template** shows the template you just created, then click **Next**.
9. On the **Choose instance launch options** page, under **Network**, click the **VPC** dropdown and select the same default VPC noted in Exercise 1, step 8.
10. Under **Availability Zones and subnets**, select at least two subnets, and check that they show two different Availability Zone names (for example, one ending in "a" and one ending in "b"). Picking two subnets in the same Availability Zone would remove the resilience this step is meant to add.
11. If an **Availability Zone distribution** section appears on this page, leave it at its default setting.
12. Click **Next**.
13. On the next **Choose instance launch options** page (compute options, if shown), click **Next** again without changing anything.
14. On the **Configure group size and scaling policies** page, under **Group size**, set **Desired capacity** to 1.
15. Under **Scaling limits**, set **Min desired capacity** to 1 and **Max desired capacity** to 2. Do not add a scaling policy today.
16. Click **Skip to review**.
17. On the **Review** page, click **Create Auto Scaling group**.
18. Click the new Auto Scaling group's name, then click the **Activity** tab. You should see one activity entry showing your existing instance now counted as part of the group, with **Desired capacity: 1** shown near the top of the page.

**Expected Result:**
One Auto Scaling group showing **Desired capacity: 1**, with **Min desired capacity: 1** and **Max
desired capacity: 2**, and your Exercise 1 instance listed under its **Instance management** tab.

**Troubleshooting:**
- The launch template in step 4 used a different AMI or security group than the instance you tested in Exercise 1 → Delete the launch template, go back to step 1, and rebuild it from "Launch more like this" so it copies the tested configuration exactly.
- You picked two subnets in the same Availability Zone in step 10 → Edit the Auto Scaling group, go to its **Details** tab, click **Edit** next to **Availability Zones and subnets**, and reselect subnets so at least two different Availability Zones are represented.

**Sources:**
- [Amazon EC2 Auto Scaling: Create an Auto Scaling group using the launch wizard](https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-asg-ec2-wizard.html)
- [Amazon EC2 Auto Scaling: Create a launch template](https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-template.html)

### Exercise 3: Open the security group port the capstone application needs
**Objective:**
By the end of this exercise your Exercise 1 instance will accept traffic on the one port your
capstone application actually needs, from your own network only.

**Prerequisites for this exercise:**
- The instance from Exercise 1 must exist (running or stopped).
- Have your capstone's architecture diagram open in another tab or on paper — you'll need the
  port number it lists.

**Steps:**
1. Find the exact port your application will listen on in your architecture diagram (for example, 3000, 5000, or 8080 — **[Placeholder — replace with the port your team's architecture actually specifies]**).
2. In the EC2 console, click **Instances**, select your Exercise 1 instance, and click the **Security** tab in the details panel below the list.
3. Click the security group link shown under **Security groups**.
4. Click the **Inbound rules** tab.
5. Click **Edit inbound rules**.
6. Click **Add rule**.
7. Click the **Type** dropdown and choose **Custom TCP**.
8. In the **Port range** field, type your application's port number from step 1.
9. Click the **Source** dropdown and choose **My IP**. **[Verified current: the console now offers a "My IP" option that fills in your current IP address automatically — use this instead of typing a CIDR range by hand, so a mistyped address can't accidentally open the port wider than intended.]** Never choose **Anywhere-IPv4** (`0.0.0.0/0`) for this rule.
10. Click **Save rules**. You should see the new rule listed immediately under the Inbound rules tab, showing your port and your specific IP address as the source.

**Expected Result:**
The security group attached to your instance shows exactly one inbound rule beyond the account
default, using your application's port and your own IP address as the source, never `0.0.0.0/0`.

**Troubleshooting:**
- You accidentally saved a rule with Source set to **Anywhere-IPv4** (`0.0.0.0/0`) → Go back to steps 5 through 10 immediately, delete that rule, and re-add it with **My IP** as the source. Do not leave it open "to fix later."

**Sources:**
- [Amazon VPC: Control traffic with security groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [Amazon VPC: Configure security group rules](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-security-group-rules.html)

## Module 2: AWS Storage & Identity Essentials

### Exercise 1: Create an S3 bucket and apply a lifecycle policy
**Objective:**
By the end of this exercise you will have an S3 bucket, correctly secured by default, with a rule
that automatically ages and deletes old objects without anyone touching them by hand.

**Prerequisites for this exercise:**
- Know the AWS Region your team used for the Module 1 exercises — this bucket must use the same
  one, and it cannot be changed after the bucket is created.

**Steps:**
1. Open the Amazon S3 console and check the Region selector in the top right matches your Module 1 Region.
2. Click **Create bucket**.
3. In the **Bucket name** field, type a globally unique name using only lowercase letters, numbers, periods, and hyphens — for example, **[Placeholder — replace with your team's actual capstone name]**-artifacts.
4. Under **Object Ownership**, leave **Bucket owner enforced** selected — do not change it.
5. Under **Block Public Access settings for this bucket**, leave all four checkboxes checked — do not uncheck any of them.
6. Under **Default encryption**, leave **Server-side encryption with Amazon S3 managed keys (SSE-S3)** selected — do not change it.
7. Scroll to the bottom and click **Create bucket**. You should see a green success banner and your new bucket listed at the top of the bucket list.
8. Click your new bucket's name to open it, then click the **Management** tab.
9. Click **Create lifecycle rule**.
10. In the **Lifecycle rule name** field, type a name for the rule (for example, `age-out-logs`).
11. Under **Choose a rule scope**, click **This rule applies to all objects in the bucket**.
12. Check the box labeled **I acknowledge that this rule applies to all objects in the bucket**.
13. Under **Lifecycle rule actions**, check the box for **Transition current versions of objects between storage classes**.
14. In the transition settings that appear, set the storage class to **Standard-IA** and the number of days to **30**.
15. Under **Lifecycle rule actions**, also check the box for **Expire current versions of objects**.
16. In the expiration settings that appear, set the number of days to **180**.
17. Click **Create rule**. You should see your new rule listed under the Management tab with status **Enabled**.

**Expected Result:**
An S3 bucket with all four Block Public Access settings enabled, default encryption on, and one
active lifecycle rule visible under its Management tab.

**Troubleshooting:**
- Step 2 fails with a name-already-taken error → Bucket names are unique across every AWS account in the world, not just yours. Add a distinguishing suffix (your initials, a number) to the name from step 3 and try again.
- You created the bucket in a different Region than your Module 1 instance → You cannot change a bucket's Region after creation. Delete the bucket and repeat steps 2 through 7 with the correct Region selected.
- You unchecked a Block Public Access setting "to test something" → Go back to the bucket's **Permissions** tab and re-enable all four settings immediately — this is exactly the setting AWS recommends leaving on unless your use case specifically requires public objects.

**Sources:**
- [Amazon S3: Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)
- [Amazon S3: Setting a lifecycle configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-set-lifecycle-configuration-intro.html)

### Exercise 2: Create a least-privilege IAM role and attach it to the EC2 instance
**Objective:**
By the end of this exercise your Module 1 EC2 instance will be able to read and write your
Exercise 1 bucket, using a role instead of a long-term credential. Together with Module 1's
exercises, this completes your capstone's compute, storage, and identity foundation for the week.

**Prerequisites for this exercise:**
- The EC2 instance from Module 1, Exercise 1 must still exist and be running.
- The S3 bucket from Exercise 1 of this module must already be created.

**Steps:**
1. Open the IAM console in a new tab.
2. In the navigation pane on the left, click **Roles**.
3. Click **Create role**.
4. Under **Trusted entity type**, click **AWS service**.
5. Under **Service or use case**, click the dropdown and choose **EC2**, then click the **EC2** use case option that appears below it.
6. Click **Next**.
7. On the **Add permissions** page, use the search box to find a managed policy that grants S3 access (for example, search "S3" and choose a policy such as AmazonS3FullAccess as today's starting point).
8. Check the box next to that policy.
9. Click **Next**.
10. On the **Name, review, and create** page, type a role name that identifies your team and its purpose — for example, **[Placeholder — replace with your team's actual capstone name]**-ec2-s3-role.
11. Scroll down to review the trusted entity and permissions shown, then click **Create role**. You should see a green success banner and the new role listed at the top of the Roles list.
12. Switch to the EC2 console tab. Click **Instances** and select the Module 1 instance.
13. Click **Actions**, then **Security**, then **Modify IAM role**.
14. Click the **IAM role** dropdown and select the role you created in step 10.
15. Click **Update IAM role**. You should see a confirmation message and, on the instance's **Security** tab, the new role name listed under **IAM Role**.
16. Write down, in your team's own notes, that this managed policy is a starting point, not the finished state: before this goes further, plan to replace it with a narrower policy naming only this one bucket's ARN.

**Expected Result:**
The Module 1 EC2 instance's Security tab shows the new IAM role attached, with no access keys
stored anywhere on the instance. Together with the running instance, the Auto Scaling group, the
open security group rule, and the S3 bucket from the earlier exercises, your team now has a
complete AWS cloud foundation, compute, storage, and identity, ready for the capstone application
to run on for the rest of the week.

**Troubleshooting:**
- Step 13's **Modify IAM role** menu doesn't show your new role yet → IAM role changes can take a minute to appear across the console. Wait a minute, refresh the page, and try step 13 again.
- You're attaching a second role and had a different one attached earlier while testing → The console replaces the existing role rather than adding a second one. After step 15, check the instance's **Security** tab to confirm which single role is now active.

**Sources:**
- [IAM: Creating a role for an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html)
- [Amazon EC2: Attach an IAM role to an instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/attach-iam-role.html)
