# Contributing to BloodConnect 🩸

Thank you for your interest in contributing to **BloodConnect** — a platform that connects blood donors, seekers, and hospitals during emergencies. Every contribution counts!

---

## Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Tech Stack Overview](#-tech-stack-overview)
- [Local Development Setup](#-local-development-setup)
- [Running Tests](#-running-tests)
- [Git Branching Workflow](#-git-branching-workflow)
- [Submitting a Pull Request](#-submitting-a-pull-request)
- [Common Issues & Tips](#-common-issues--tips)

---

## 🧭 Code of Conduct

We expect all contributors to treat others with empathy, kindness, and respect. Harassment or exclusionary behavior of any kind is not tolerated.

---

## 🛠️ Tech Stack Overview

| Layer    | Technology                        |
| -------- | --------------------------------- |
| Backend  | Python Django 4.2                 |
| Database | SQLite (dev) / PostgreSQL (prod)  |
| Frontend | HTML5, CSS3, Bootstrap 5          |
| Maps     | Leaflet.js (OpenStreetMap)        |
| Auth     | Django Authentication             |

Knowing this before you start will help you navigate the codebase faster.

---

## 💻 Local Development Setup

### Prerequisites

Make sure these are installed before you begin:

- **Python 3.10+**
- **pip**
- **venv** (built into Python 3)
- **Git**

### Step 1 — Fork & Clone

1. Click **Fork** on the [BloodConnect GitHub repo](https://github.com/ChronalLabs/Blood-Connect-By-ChronalLabs).
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR-USERNAME/Blood-Connect-By-ChronalLabs.git
cd Blood-Connect-By-ChronalLabs
```

3. Add the upstream remote so you can pull in future changes:

```bash
git remote add upstream https://github.com/ChronalLabs/Blood-Connect-By-ChronalLabs.git
```

### Step 2 — Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

| OS | Command |
| --- | --- |
| macOS / Linux | `source venv/bin/activate` |
| Windows (CMD) | `venv\Scripts\activate.bat` |
| Windows (PowerShell) | `venv\Scripts\Activate.ps1` |

You should see `(venv)` in your terminal prompt once activated.

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and update:

```env
SECRET_KEY=your-secure-random-key-here
DEBUG=True
```

> **Tip:** Generate a strong secret key with:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### Step 5 — Run Database Migrations

```bash
python manage.py makemigrations users donors seekers hospitals blood_requests
python manage.py migrate
```

### Step 6 — Create a Superuser

```bash
python manage.py createsuperuser
```

This gives you access to the Django Admin panel at `/admin/`.

### Step 7 — (Optional) Load Sample Data

```bash
python manage.py shell
```

Paste the following:

```python
from users.models import CustomUser
from hospitals.models import HospitalProfile, BloodStock
from donors.models import DonorProfile

u = CustomUser.objects.create_user(
    'hospital1', password='pass123', role='hospital',
    first_name='City', last_name='Hospital'
)
h = HospitalProfile.objects.create(
    user=u, hospital_name='City General Hospital',
    address='123 Main St', city='Mumbai', state='Maharashtra',
    pincode='400001', contact_number='9999888777',
    verified=True, blood_bank_available=True,
    latitude=19.0760, longitude=72.8777
)
BloodStock.objects.create(
    hospital=h, a_positive=15, b_positive=8,
    o_positive=20, ab_positive=5, a_negative=3
)
```

### Step 8 — Collect Static Files

```bash
python manage.py collectstatic
```

### Step 9 — Start the Dev Server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser. You're live!

---

## 🧪 Running Tests

**Always run tests before pushing code or opening a PR.**

Run the full test suite:

```bash
python manage.py test
```

Run a specific test module:

```bash
python manage.py test blood_requests.tests.test_compatibility
```

If your change touches a specific app (e.g. `donors`), run that app's tests too:

```bash
python manage.py test donors
```

All tests must pass before you submit a PR.

---

## 🌿 Git Branching Workflow

### Keep Your Fork Up to Date

Before starting any new work, sync with upstream:

```bash
git checkout main
git fetch upstream
git merge upstream/main
```

### Branch Naming Convention

Create a new branch from `main` using one of these prefixes:

| Prefix | Purpose | Example |
| --- | --- | --- |
| `feat/` | New feature | `feat/hospital-dashboard` |
| `fix/` | Bug fix | `fix/compatibility-test-city` |
| `docs/` | Documentation | `docs/improve-contributing-guide` |
| `refactor/` | Refactor (no logic change) | `refactor/blood-matching-logic` |
| `chore/` | Build, deps, tooling | `chore/update-requirements` |

```bash
git checkout -b feat/your-feature-name
```

### Commit Message Guidelines

Write commits in the **imperative mood**, scoped to a single logical change:

```
feat: add donor availability status toggle
fix: resolve duplicate keyword error in compatibility tests
docs: update setup instructions for Windows users
```

**Avoid:** `fixed bug`, `updates`, `wip`, or vague messages.

---

## 🚀 Submitting a Pull Request

1. **Push your branch:**

```bash
git push origin feat/your-feature-name
```

2. **Open a PR** on GitHub — you'll see a "Compare & pull request" banner on the repo page.

3. **Fill in the PR description** using this template:

```
## What does this PR do?
Brief description of the change.

## Related issue
Closes #<issue-number>

## Testing done
- [ ] Ran `python manage.py test`
- [ ] Manually tested on local dev server
- [ ] No regressions in existing functionality
```

4. **Respond to review comments** promptly. Once approved, a maintainer will merge your PR into `main`.

---

## 🐛 Common Issues & Tips

**`ModuleNotFoundError` after cloning**
→ Make sure your virtual environment is activated (`source venv/bin/activate`) and you've run `pip install -r requirements.txt`.

**Migrations conflict**
→ If you get migration conflicts, delete the `db.sqlite3` file and re-run `python manage.py migrate` from scratch on your local branch.

**Static files not loading**
→ Run `python manage.py collectstatic` and make sure `DEBUG=True` in your `.env`.

**`SECRET_KEY` error on startup**
→ Ensure your `.env` file exists (copy from `.env.example`) and has a non-empty `SECRET_KEY`.

---

Thank you for contributing to **BloodConnect**! Let's save lives together. 🩸❤️
