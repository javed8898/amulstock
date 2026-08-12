# Amul Stock Alert — Free 24/7 Setup via GitHub Actions

Runs entirely on GitHub's servers, checking every ~5 minutes. Your computer
does not need to be on. Currently tracks:

- Amul Whey Protein, 32g | Pack of 60 Sachets
- Amul Chocolate Whey Protein, 34g | Pack of 60 Sachets

## 1. Create a Telegram bot (2 minutes)

1. Open Telegram, search **@BotFather**, start a chat.
2. Send `/newbot`, give it any name (e.g. `AmulStockBot`).
3. Save the **token** it gives you, e.g. `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxx`.

## 2. Get your chat ID

1. Search for your new bot in Telegram and send it any message (e.g. "hi").
2. In a browser, open:
   `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Find `"chat":{"id":123456789,...}` — that number is your chat ID.

## 3. Create a GitHub repo

1. Go to github.com → New repository → name it e.g. `amul-stock-alert` →
   **Private** is fine → Create.
2. Upload these two files, keeping this exact folder structure:

   ```
   amul_stock_checker.py
   .github/workflows/check-stock.yml
   ```

   The file I gave you is named `check-stock.yml` — when you upload it,
   put it inside a folder path `.github/workflows/` in the repo (GitHub's
   web uploader lets you type that path when adding the file, or create
   the folders first).

## 4. Add your secrets

In the repo: **Settings → Secrets and variables → Actions → New repository secret**

- Name: `TELEGRAM_BOT_TOKEN` → Value: your bot token
- Name: `TELEGRAM_CHAT_ID` → Value: your chat ID

## 5. Done — it's live

- Go to the **Actions** tab in your repo to watch it run.
- It runs automatically every 5 minutes on GitHub's schedule.
- You can also click **Run workflow** there anytime to test it manually.
- You'll get a Telegram message the moment either product shows
  "Add to Cart" instead of "Sold Out".

## Adding more products later

Open `amul_stock_checker.py` and add another entry to the `PRODUCTS` list
at the top, following the same `{"name": ..., "url": ...}` format. Just
tell me the product link and I can do this for you too.

## Notes

- Free tier: GitHub Actions gives ~2,000–3,000 free minutes/month for
  private repos (public repos are unlimited) — a 5-minute check that
  finishes in seconds uses only a couple of minutes/day, so you're
  comfortably within the free tier.
- This only *notifies* you — it doesn't auto-buy, since that would require
  storing your Amul login and payment details, which isn't safe and likely
  breaks the site's terms of use.
- If Amul changes the page layout, the "Sold Out" detection may need a
  small tweak — let me know and I'll fix it.
