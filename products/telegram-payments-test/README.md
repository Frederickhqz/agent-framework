# Telegram Payments Test

Simple test of Telegram Payments API with Stripe.

## Setup Required

### 1. Stripe Setup
- Create/connect Stripe account to Telegram: https://stripe.com/partners/telegram
- Get Stripe publishable key for Telegram

### 2. Telegram Bot Setup
```bash
# Talk to @BotFather
/newbot  # Create bot
/payments  # Set up payment provider
```

### 3. Payment Provider Token
BotFather will give you a **TEST** payment provider token like:
`284685063:TEST:ODI0ODk2M2Y0Y2Y4`

## Files

- `bot.js` - Telegram bot with payment commands
- `mini-app/` - Web app with payment button
- `server.js` - Express server hosting the Mini App

## Test Flow

1. User opens Mini App from bot
2. Clicks "Pay $5.00"
3. Telegram native payment UI opens
4. User enters test card: `4242 4242 4242 4242`
5. Payment processed → confirmation sent

## Test Cards

| Card | Result |
|------|--------|
| 4242 4242 4242 4242 | Success |
| 4000 0000 0000 0002 | Declined |

## Run

```bash
cd mini-app && npm install && npm start
```
