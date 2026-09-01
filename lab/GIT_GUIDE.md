# Git Reference Guide

A quick reference for getting this repo, staying up to date, and contributing changes. Aimed at anyone who isn't a daily git user.

## Getting the repo

**Clone it** (first time only) — downloads the full repo to your machine:

```
git clone <repo-url>
cd adm-genai-training
```

## Staying up to date

**Check status** — see what's changed locally vs. what's tracked:

```
git status
```

**Pull the latest changes** from the remote:

```
git pull
```

If you have local uncommitted changes that conflict with incoming ones, `git pull` will refuse until you commit, stash, or discard them (see below).

## Making changes

**Stage and commit:**

```
git add <file>        # or `git add .` to stage everything changed
git commit -m "Describe what changed and why"
```

**Push your commits** to the remote:

```
git push
```

**Create a branch** for a change you don't want directly on `main`:

```
git checkout -b <branch-name>
# ...make changes, commit...
git push -u origin <branch-name>
```

## Useful everyday commands

| Command | What it does |
|---|---|
| `git status` | Shows staged/unstaged/untracked files |
| `git log --oneline` | Compact history of commits |
| `git diff` | Shows unstaged changes line-by-line |
| `git diff --staged` | Shows staged changes not yet committed |
| `git stash` | Temporarily shelves uncommitted changes |
| `git stash pop` | Restores the most recently stashed changes |
| `git checkout -- <file>` | Discards local (unstaged) changes to a file |
| `git branch` | Lists local branches |
| `git branch -a` | Lists local and remote branches |
| `git fetch` | Downloads remote changes without merging them |
| `git merge <branch>` | Merges another branch into your current one |

## Undoing things (careful — some are destructive)

| Command | What it does |
|---|---|
| `git reset --soft HEAD~1` | Undoes the last commit, keeps changes staged |
| `git reset --hard HEAD~1` | Undoes the last commit **and discards** the changes |
| `git revert <commit>` | Creates a new commit that undoes a previous one (safe for shared history) |
| `git clean -fd` | Removes untracked files/directories — **irreversible** |

> Prefer `git revert` over `git reset --hard` on any branch others share — reset rewrites history, revert doesn't.

## Notes for this repo

- This repo's `.gitignore` excludes generated deliverables (course content, trainer notes, course outline docx, per-day demo guides) and local authoring tooling — see `.gitignore` for the exact patterns.
- If a file you expect to see is missing after `git pull`, check whether it's gitignored rather than assuming it wasn't committed.
