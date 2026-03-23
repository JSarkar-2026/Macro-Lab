# Deployment Guide — Step-by-Step for Beginners
## WS/PS Labour Market & Phillips Curve Simulation

This guide walks you through three things:
1. Storing your code safely on **GitHub**
2. Publishing the app live on **Streamlit Community Cloud** (free)
3. Tracking student usage with **Google Analytics** and quiz scores with **Google Sheets**

No prior experience needed. Follow each section in order.

---

## PART 1 — GitHub: Storing Your Code Safely

### What is GitHub and why do you need it?

GitHub is a free website that stores your code files and tracks every change you make.
Think of it like Dropbox for code, but with a complete history of every edit.
Streamlit (the service that runs your app online) reads your files directly from GitHub,
so you need GitHub before you can publish.

### Step 1 — Create a GitHub account

1. Go to **https://github.com** and click **Sign up**.
2. Choose a username (e.g. your name or institution), enter your email and a password.
3. Choose the free plan. Verify your email.

### Step 2 — Create a repository ("repo")

A repository is a folder on GitHub that holds all your project files.

1. After logging in, click the green **New** button (top-left, or at github.com/new).
2. Fill in:
   - **Repository name**: `macroeconomics-lab` (or any name you like, no spaces)
   - **Description**: `WS/PS Labour Market and Phillips Curve simulation`
   - **Visibility**: choose **Public** (required for free Streamlit deployment)
   - Tick **Add a README file**
3. Click **Create repository**.

### Step 3 — Install GitHub Desktop (easiest for beginners)

Rather than using the command line, use the free GitHub Desktop app.

1. Download from **https://desktop.github.com** and install it.
2. Open GitHub Desktop → **Sign in to GitHub.com** → authorise it.

### Step 4 — Clone (download) your repository to your computer

1. In GitHub Desktop: **File → Clone repository**.
2. Select `macroeconomics-lab` from your list.
3. Choose where to save it (e.g. `C:\Users\YourName\macroeconomics-lab`).
4. Click **Clone**.

You now have a local folder on your computer that is connected to GitHub.

### Step 5 — Copy your simulation files into the repository

Copy the entire `Phillips-Curve` folder (containing `app.py`, `model.py`,
`requirements.txt`, `.streamlit/`, and the markdown files) into the cloned
repository folder. The structure should look like this:

```
macroeconomics-lab/
├── Phillips-Curve/
│   ├── app.py
│   ├── model.py
│   ├── requirements.txt
│   ├── README.md
│   ├── INSTRUCTIONS.md
│   ├── DEPLOYMENT.md
│   └── .streamlit/
│       └── config.toml
└── README.md
```

### Step 6 — Upload ("push") your files to GitHub

1. Open GitHub Desktop. It will show all the new files under **Changes**.
2. At the bottom-left, type a summary (e.g. `Initial upload of Phillips Curve app`).
3. Click **Commit to main**.
4. Click **Push origin** (top bar).

Your files are now on GitHub. You can see them at
`https://github.com/YOUR-USERNAME/macroeconomics-lab`.

### How to update files in the future

Whenever you edit `app.py` or `model.py` on your computer:
1. Open GitHub Desktop — it shows which files changed.
2. Write a brief summary of what you changed.
3. Click **Commit to main** → **Push origin**.

Streamlit will automatically redeploy the updated app within a minute or two.

---

## PART 2 — Publishing the App with Streamlit Community Cloud

Streamlit Community Cloud hosts your app for free, reading files from your GitHub repo.

### Step 1 — Create a Streamlit account

1. Go to **https://share.streamlit.io** and click **Sign up**.
2. Choose **Continue with GitHub** — this links the two accounts automatically.

### Step 2 — Deploy the app

1. Once logged in, click **New app**.
2. Fill in:
   - **Repository**: select `YOUR-USERNAME/macroeconomics-lab`
   - **Branch**: `main`
   - **Main file path**: `Phillips-Curve/app.py`
3. Click **Deploy**.

Streamlit will install the packages from `requirements.txt` and start the app.
This takes 2–5 minutes the first time.

### Step 3 — Get your public URL

When deployment finishes, Streamlit gives you a URL like:
```
https://your-username-macroeconomics-lab-phillips-curve-app-xxxxx.streamlit.app
```
Share this URL with students. It works on any device — desktop, tablet, phone.

### Troubleshooting

| Problem | Solution |
|---------|----------|
| App shows an error about a missing package | Check `requirements.txt` has all packages listed |
| App shows old version after you edited files | Click **Reboot app** in the Streamlit dashboard, or wait 2 minutes |
| App is sleeping (Streamlit puts idle apps to sleep after inactivity) | Click **Wake up** on the Streamlit dashboard. Consider upgrading to a paid plan for always-on apps |

---

## PART 3 — Tracking Usage with Google Analytics

Google Analytics (GA) is free and tells you: how many students visited, from where,
how long they stayed, and which pages they used.

### Step 1 — Create a Google Analytics account

You need a Google account (Gmail). If you have Gmail, you already have one.

1. Go to **https://analytics.google.com** and sign in.
2. Click **Start measuring**.
3. Fill in:
   - **Account name**: e.g. `Macroeconomics Lab`
4. Click **Next** → create a **Property**:
   - **Property name**: `Phillips Curve Simulation`
   - **Time zone** and **currency**: set to your location
5. Click **Next** → fill in your organisation type (Education) → **Create**.

### Step 2 — Set up a Web Data Stream

1. Under **Data Streams**, choose **Web**.
2. Enter your Streamlit URL (from Part 2, Step 3).
3. Give it a name: `Phillips Curve App`.
4. Click **Create stream**.

You will now see your **Measurement ID** — it looks like `G-XXXXXXXXXX`
(the X's are letters and numbers). **Copy this ID.**

### Step 3 — Add your Measurement ID to the app

1. Open `Phillips-Curve/app.py` in any text editor.
2. Find this line near the top (around line 38):
   ```python
   GA_ID = "G-XXXXXXXXXX"
   ```
3. Replace `G-XXXXXXXXXX` with your actual ID, e.g.:
   ```python
   GA_ID = "G-ABC123DEF4"
   ```
4. Save the file.
5. In GitHub Desktop: commit and push the change (as in Part 1, Step 6).

### Step 4 — Check that it is working

1. Visit your Streamlit app URL.
2. In Google Analytics, go to **Reports → Realtime**.
3. You should see **1 user** appear within a minute or two.

If nothing appears after 5 minutes, try a different browser (some ad-blockers
block GA tracking).

### What Google Analytics tracks automatically

Once your ID is in the app, GA records:
- Number of visitors per day / week / month
- Country and city of visitors
- Device type (desktop, tablet, phone)
- Time spent on the page
- How users found the app (direct link, search, etc.)

### What Google Analytics does NOT track automatically

GA cannot see inside your Streamlit app (slider values, quiz answers, scores).
It only sees page-level behaviour. For quiz scores you need a separate approach —
see Part 4 below.

---

## PART 4 — Tracking Quiz Performance with Google Sheets

The simplest way to collect quiz scores without a database is to write results
to a Google Sheet using a free Google account. Here is how to set it up.

### Overview of what this does

When a student completes the quiz, their score and the time they spent on the
simulation are written as a new row in a Google Sheet that only you can see.

### Step 1 — Create a Google Sheet to receive data

1. Go to **https://sheets.google.com** and create a new spreadsheet.
2. Name it `Phillips Curve — Student Results`.
3. In row 1, add these column headers:
   ```
   Timestamp | Pre-Quiz Score (%) | Time on Simulation (min) | Session ID
   ```
4. Note the **Spreadsheet ID** — it is the long string in the URL:
   `https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit`

### Step 2 — Create a Google Service Account (the "robot" that writes to the sheet)

This sounds technical but takes about 5 minutes.

1. Go to **https://console.cloud.google.com**.
2. Click **Select a project → New Project**. Name it `macro-lab`. Click **Create**.
3. In the search bar, type **Google Sheets API** → click it → **Enable**.
4. In the search bar, type **Google Drive API** → click it → **Enable**.
5. Go to **IAM & Admin → Service Accounts → Create Service Account**.
   - Name: `macro-lab-writer`
   - Click **Create and Continue → Done**.
6. Click the service account you just created → **Keys tab → Add Key →
   Create new key → JSON → Create**.
   A `.json` file downloads to your computer. **Keep this file private.**

### Step 3 — Give the service account access to your Google Sheet

1. Open the downloaded `.json` file in a text editor.
2. Find the line `"client_email"` — copy that email address
   (it looks like `macro-lab-writer@macro-lab-xxxxx.iam.gserviceaccount.com`).
3. Open your Google Sheet → click **Share** → paste that email address →
   give it **Editor** access → **Send**.

### Step 4 — Add your credentials to Streamlit as a Secret

Streamlit has a secure place to store private keys called **Secrets**.
Never put your JSON key inside `app.py` or upload it to GitHub.

1. In the Streamlit dashboard, click your app → **Settings → Secrets**.
2. Paste the entire contents of your `.json` file, wrapped like this:
   ```toml
   [gcp_service_account]
   type = "service_account"
   project_id = "macro-lab-xxxxx"
   private_key_id = "..."
   private_key = "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
   client_email = "macro-lab-writer@macro-lab-xxxxx.iam.gserviceaccount.com"
   client_id = "..."
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"

   SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"
   ```
3. Click **Save**.

### Step 5 — Add the logging code to app.py

Add `gspread` and `google-auth` to `requirements.txt`:
```
gspread==6.1.2
google-auth==2.29.0
```

Then add this function near the top of `app.py` (after the imports):
```python
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import uuid

def _log_quiz_result(pre_score_pct: float, sim_minutes: float) -> None:
    """Write one row of results to the instructor's Google Sheet."""
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        gc     = gspread.authorize(creds)
        sh     = gc.open_by_key(st.secrets["SPREADSHEET_ID"])
        ws     = sh.sheet1
        ws.append_row([
            datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            round(pre_score_pct, 1),
            round(sim_minutes, 1),
            str(uuid.uuid4())[:8],   # anonymous session ID
        ])
    except Exception:
        pass   # never crash the app due to logging failure
```

Call this function immediately after the quiz is submitted and marked:
```python
_log_quiz_result(
    pre_score_pct = st.session_state["pre_score"],
    sim_minutes   = (time.time() - st.session_state["time_start_sim"]) / 60,
)
```

### What you will see in the Google Sheet

Each row is one student session:
```
2025-09-14 09:32 UTC | 71.4 | 8.3 | a1b2c3d4
2025-09-14 09:45 UTC | 57.1 | 12.1 | e5f6g7h8
```

From this you can compute:
- Average pre-quiz score (prior knowledge)
- Average time spent on the simulation
- Distribution of scores across the class

---

## PART 5 — Summary Checklist

Use this list to make sure everything is set up correctly before sharing
the app URL with students.

- [ ] GitHub account created and files pushed to a public repository
- [ ] Streamlit Community Cloud account created and linked to GitHub
- [ ] App deployed — public URL confirmed working
- [ ] Google Analytics account created; Measurement ID (`G-XXXXXXXXXX`) added to `app.py`
- [ ] GA Realtime view confirms at least one visit is being tracked
- [ ] (Optional) Google Sheet and service account set up for quiz logging
- [ ] `requirements.txt` updated with `gspread` and `google-auth` if using Sheets
- [ ] Service account JSON saved as a Streamlit Secret (NOT in GitHub)
- [ ] App URL shared with students via the course VLE or email

---

## Quick Reference — Important URLs

| Service | URL |
|---------|-----|
| GitHub | https://github.com |
| GitHub Desktop | https://desktop.github.com |
| Streamlit Community Cloud | https://share.streamlit.io |
| Google Analytics | https://analytics.google.com |
| Google Cloud Console | https://console.cloud.google.com |
| Google Sheets | https://sheets.google.com |
