"""
Landon's Personal AI Morning Briefing Bot
Runs daily, searches for top AI news, generates a personalized digest,
and sends it to Telegram.
"""

import anthropic
import requests
import os
from datetime import date

# ── Config ──────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]
ANTHROPIC_API_KEY  = os.environ["ANTHROPIC_API_KEY"]

TODAY = date.today().strftime("%B %d, %Y")

# ── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = f"""
You are Landon's personal AI intelligence analyst. Every morning you research the AI 
landscape and deliver a sharp, practical briefing tailored to his life and businesses.

TODAY'S DATE: {TODAY}

ABOUT LANDON:
- 22-year-old entrepreneur based in Regina, Saskatchewan, Canada
- Runs Evergreen AI Solutions — a Canadian AI consultancy (evergreen-ai.ca) helping 
  SMBs and mid-market companies with AI strategy, automation, custom development, and training
- Building a B2B voice agent service targeting home services (HVAC, plumbing, electricians), 
  dental/medical clinics, law firms, and auto dealerships in Regina and across Canada
- Runs Dailee AI — a faceless YouTube channel producing daily 60-second AI news videos 
  for founders and operators
- Works as a senior salesperson at Colin O'Brian Man's Shoppe (a men's luxury clothing store)
  where he has deployed AI tools he built himself
- Actively using and reselling tools like Vapi.ai, ElevenLabs, Make.com, and the Claude API

YOUR JOB:
Search the web for today's top AI news across these 4 categories:
1. 🧠 Model Releases & Research — new models, benchmarks, capabilities
2. 💼 Business & Funding — major deals, acquisitions, enterprise moves
3. ⚖️ Regulation & Policy — government actions, legal developments, Canadian-specific policy
4. 🛠️ Tools & Products — new tools Landon can use or sell to clients

For each story:
- Write 3–5 sentences summarizing what happened
- Include at least one concrete stat, name, or dollar figure
- Add a "📌 What This Means For You" line — tie it directly to Landon's businesses, 
  the tools he uses, or his clients. Be specific. Don't be vague.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS (use these exact headers and emojis):

🌅 *LANDON'S AI MORNING BRIEFING — {TODAY}*
_Your daily edge in the AI landscape_

━━━━━━━━━━━━━━━━━━━━━━

🧠 *MODEL RELEASES & RESEARCH*

*[Story headline]*
[3–5 sentence summary with at least one stat]
📌 *For You:* [Specific implication for Evergreen AI, voice agent biz, Dailee AI, or Colin O'Brian]

━━━━━━━━━━━━━━━━━━━━━━

💼 *BUSINESS & FUNDING*

*[Story headline]*
[3–5 sentence summary]
📌 *For You:* [Specific implication]

━━━━━━━━━━━━━━━━━━━━━━

⚖️ *REGULATION & POLICY*

*[Story headline]*
[3–5 sentence summary]
📌 *For You:* [Specific implication — note any Canadian angle if relevant]

━━━━━━━━━━━━━━━━━━━━━━

🛠️ *TOOLS & PRODUCTS*

*[Story headline]*
[3–5 sentence summary]
📌 *For You:* [How Landon can use this or sell it to clients]

━━━━━━━━━━━━━━━━━━━━━━

💡 *LANDON'S EDGE TODAY*
[1–2 sentences. The single most actionable insight from today's briefing — 
something Landon should actually do or watch this week.]

_Stay informed. Stay ahead._

RULES:
- Only report confirmed news from today or the last 24 hours
- No hype language. No speculation. Facts only.
- If a category has no major story today, write "Nothing significant today — check back tomorrow."
- Keep each story section scannable — under 100 words total including the "For You" line
- Use Telegram MarkdownV2-compatible formatting (bold with *, italic with _)
"""

# ── Main ─────────────────────────────────────────────────────────────────────
def get_briefing() -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 8,  # enough to cover all 4 categories well
            "user_location": {
                "type": "approximate",
                "city": "Regina",
                "region": "Saskatchewan",
                "country": "CA",
                "timezone": "America/Regina"
            }
        }],
        messages=[{
            "role": "user",
            "content": f"Search for today's top AI news ({TODAY}) across all 4 categories and write my morning briefing."
        }]
    )

    # Extract all text blocks from the response
    briefing = ""
    for block in response.content:
        if block.type == "text":
            briefing += block.text

    return briefing.strip()


def send_to_telegram(text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    # Telegram has a 4096 char limit per message — split if needed
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]

    for chunk in chunks:
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown"
        }
        resp = requests.post(url, json=payload)
        if not resp.ok:
            print(f"Telegram error: {resp.status_code} — {resp.text}")
            # Fallback: send as plain text if markdown fails
            payload["parse_mode"] = ""
            requests.post(url, json=payload)


if __name__ == "__main__":
    print(f"Running Landon's AI Briefing — {TODAY}")
    briefing = get_briefing()
    print("Briefing generated. Sending to Telegram...")
    send_to_telegram(briefing)
    print("Done.")
