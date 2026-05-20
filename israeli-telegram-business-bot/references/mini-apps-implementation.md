# Telegram Mini Apps (TWA): Implementation Guide for Israeli SMBs

A **Mini App** is a full web page (HTML/CSS/JS) that opens inline inside Telegram, with access to Telegram-specific APIs: user identity, theme, haptics, MainButton, and the native payment sheet. Official documentation: `core.telegram.org/bots/webapps`.

By 2026 Mini Apps have become a mainstream commerce surface globally. Telegram crossed 1 billion monthly active users, and TON-based in-chat wallets are in widespread use.

## When a Mini App makes sense

For an Israeli SMB, Mini Apps make sense when the bot needs richer UX than inline keyboards can provide:

- A real catalog grid with images
- A date/time picker calendar for bookings
- A multi-step order form with validation
- A custom checkout that needs an Israeli provider iframe (Tranzila, PayMe)

The flow stays inside Telegram. The customer never opens a browser tab, and the same Mini App URL works on iOS, Android, and Desktop with no app-store review.

## When NOT to use a Mini App

A simple FAQ/booking bot with five inline-keyboard buttons does not need a Mini App. Adding one introduces a frontend codebase to maintain and an HTTPS host to pay for. Stick with inline keyboards until the customer journey actually demands more.

## Setup via @BotFather

1. Open a chat with @BotFather.
2. Send `/newapp` (or `/myapps` -> "Edit Bot" -> "Configure Mini App").
3. Attach a Mini App to your bot by giving it a name, short description, photo, and the public HTTPS URL where the Mini App is hosted.
4. @BotFather registers the app and exposes a button users can tap to open it.

The page itself is served from your own HTTPS URL. @BotFather does not host the code; it just registers the URL.

## Israeli payment providers inside a Mini App

Israeli payment providers do not need a Telegram-specific integration to work inside a Mini App. You can embed the same Tranzila iframe, PayMe payment page, or Green Invoice payment link you would use on a regular website. The Mini App is just a web page, so any HTTPS-embeddable Israeli checkout works.

This is the practical workaround for the "Telegram native Payment API does not support Israeli soleks" limitation: build a thin Mini App, embed the Israeli provider iframe, settle through your existing merchant account.

## Cost and maintenance considerations

- HTTPS host (Vercel free tier, Netlify, or a small VPS): typically free to ~$5/month.
- Frontend codebase to maintain (HTML/JS, or a React/Vue/Svelte app).
- Theme handling: respect Telegram's light/dark theme via the `themeParams` API so the Mini App matches the user's Telegram appearance.
- Authentication: validate Telegram's `initData` signature server-side before trusting user identity (`core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app`).
