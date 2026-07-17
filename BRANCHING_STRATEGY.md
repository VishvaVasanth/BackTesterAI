# Git Branching Strategy: Dual-Trunk Development (Dev/Main)

Our project utilizes a structured workflow using two permanent core trunks to ensure stability.

## Core Permanent Branches
1. **`main`**: The production branch. It contains only stable, tested code that is confirmed to work perfectly.
2. **`dev`**: The integration branch. All active feature development is combined and verified here first.

## Feature Deployment Pipeline

      [main]  ========================================> [main] (Production Deploy)
                                                        ^
                                                       / (Only when dev is 100% stable)
      [dev]   ===============[dev]====================/
                             ^              \
                            /                \
    [feature]  ---> [feat/indicator] --------> [Merged & Deleted]

### 1. The Development Lifecycle
1. Always pull the latest changes from `dev`: `git checkout dev && git pull`
2. Spin up your short-lived branch *from* `dev`: `git checkout -b feat/your-feature`
3. Push your feature changes and open a Pull Request (PR) targeting **`dev`**.
4. Once the PR is merged, the temporary feature branch **must be deleted immediately**.
5. Once `dev` passes all verification runs and works perfectly, open a PR from **`dev` -> `main`** to push to production.

### 2. Branch Naming Conventions
* **Features:** `feat/short-description` (e.g., `feat/trade-ledger`)
* **Bug Fixes:** `fix/short-description` (e.g., `fix/pnl-rounding`)
