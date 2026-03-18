[README_briefingbot.md](https://github.com/user-attachments/files/26077798/README_briefingbot.md)
# Landon's AI Morning Briefing Bot

A personal daily AI news digest delivered to your Telegram every morning.
Covers model releases, business & funding, regulation, and tools — with a 
"What This Means For You" section tied to your actual businesses.

---

## Stack
- **Claude API** (`claude-sonnet-4-6`) with web search enabled
- **Telegram Bot API** for delivery
- **GitHub Actions** for free, serverless scheduling

---

## Setup (One-Time)

### Step 1 — Create Your Telegram Bot
1. Message `@BotFather` on Telegram
2. Send `/newbot` and follow the prompts
3. Copy your **Bot Token** (looks like `123456:ABCdef...`)

### Step 2 — Get Your Chat ID
1. Start a conversation with your new bot (send it any message)
2. Open this URL in your browser (replace `YOUR_TOKEN`):
   ```
   https://api.telegram.org/botYOUR_TOKEN/getUpdates
   ```
3. Find `"chat":{"id":XXXXXXXXX}` — that number is your **Chat ID**

### Step 3 — Create GitHub Repo
1. Create a new GitHub repo (can be private)
2. Add these two files:
   - `briefing_bot.py` (root of repo)
   - `.github/workflows/daily_briefing.yml`

### Step 4 — Add Secrets
In your GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**

Add these 3 secrets:
| Secret Name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Your chat ID from Step 2 |

### Step 5 — Enable Actions & Test
1. Push your files to GitHub
2. Go to **Actions** tab → click your workflow → **Run workflow** (manual trigger)
3. Watch it run — you should get a Telegram message within ~30 seconds

---

## Schedule
Default: **7:00 AM CST, Monday–Friday**

To change the time, edit the cron line in `.github/workflows/daily_briefing.yml`:
```yaml
- cron: '0 13 * * 1-5'   # 13:00 UTC = 7:00 AM CST
```
[Cron schedule helper →](https://crontab.guru)

---

## Estimated Cost
- Claude API: ~$0.03–0.08 per briefing (Sonnet 4.6 + web search)
- ~$1–2/month running every weekday
- GitHub Actions: Free (well within free tier limits)

---

## Files
```
├── briefing_bot.py                    # Main script
├── .github/
│   └── workflows/
│       └── daily_briefing.yml         # GitHub Actions scheduler
└── README.md
```
