# BFG: Redact credential placeholders from full history

This rewrites **all commits** to replace placeholder strings (e.g. `your_password`, `dapi123...`) with `REDACTED` so old revisions never show credential-like text.

## Prerequisites

- **BFG Repo-Cleaner** installed:
  ```bash
  brew install bfg
  ```
  Or download the JAR: https://rtyley.github.io/bfg-repo-cleaner/

- **Clean working tree** (commit or stash your current changes first).

## Steps

### 1. Commit or stash your work

```bash
cd "/Users/som.natarajan/SOTA Agent Framework"
git status   # see what’s changed
git add -A && git commit -m "chore: credential sweep and BFG replacement list"
# OR: git stash -u
```

### 2. Run BFG with the replacements file

From the **repo root**:

```bash
bfg --replace-text bfg-replacements.txt .
```

BFG will rewrite history and replace the strings listed in `bfg-replacements.txt` with `REDACTED` in **every commit** that contains them.

### 3. Prune and garbage-collect

```bash
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### 4. Push the rewritten history (destructive)

**This rewrites `main` on the remote.** Anyone who has cloned the repo will need to re-clone or reset.

```bash
git push origin main --force
```

If you use a **mirror** (e.g. GitHub at `somasekar278/databricks-agent-toolkit`), push there:

```bash
git push origin main --force
```

## What gets replaced

Strings in `bfg-replacements.txt` (from repo root):

- `your_password` → `REDACTED`
- `your_user` → `REDACTED`
- `your-password` → `REDACTED`
- `your-user` → `REDACTED`
- `your-token` → `REDACTED`
- `dapi123...` → `REDACTED`
- `your-lakebase-host.cloud.databricks.com` → `REDACTED`
- `your-lakebase-instance-name` → `REDACTED`

## Optional: add more patterns

Edit `bfg-replacements.txt` (one rule per line):

- `literal==>REPLACEMENT`  — replace literal text with REPLACEMENT
- `literal`                — replace with `***REMOVED***`

Then run step 2 again (no need to re-clone; run BFG again on the same repo).

## If BFG is not on PATH (JAR)

```bash
java -jar /path/to/bfg.jar --replace-text bfg-replacements.txt .
```

Then run steps 3 and 4 as above.
