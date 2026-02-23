// Telegram Bot with Payments
// Requires: npm install node-telegram-bot-api

const TelegramBot = require('node-telegram-bot-api');

// Replace with your bot token from @BotFather
const BOT_TOKEN = process.env.BOT_TOKEN || 'YOUR_BOT_TOKEN_HERE';

// Payment provider token from @BotFather /payments
const PAYMENT_TOKEN = process.env.PAYMENT_TOKEN || 'YOUR_TEST_PAYMENT_TOKEN_HERE';

const bot = new TelegramBot(BOT_TOKEN, { polling: true });

// Mini App URL (Hostinger deployment)
const MINI_APP_URL = 'https://your-domain.com';

console.log('Bot starting...');

// Start command - shows Mini App button
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  
  bot.sendMessage(chatId, 
    '🛒 *Payment Test*\n\nTry our demo payment flow:', {
    parse_mode: 'Markdown',
    reply_markup: {
      inline_keyboard: [[
        { text: '💳 Open Payment App', web_app: { url: MINI_APP_URL } }
      ]]
    }
  });
});

// Alternative: Direct invoice command
bot.onText(/\/pay/, async (msg) => {
  const chatId = msg.chat.id;
  
  const title = 'Test Product';
  const description = 'This is a test payment for $5.00';
  const payload = `payment_${Date.now()}_${chatId}`;
  const providerToken = PAYMENT_TOKEN;
  const currency = 'USD';
  const prices = [{ label: 'Test Product', amount: 500 }]; // $5.00 in cents
  
  try {
    await bot.sendInvoice(chatId, title, description, payload, 
      providerToken, currency, prices);
    console.log(`Invoice sent to ${chatId}`);
  } catch (err) {
    console.error('Failed to send invoice:', err.message);
    bot.sendMessage(chatId, '❌ Payment setup failed. Please try again.');
  }
});

// Handle pre-checkout (validate before payment)
bot.on('pre_checkout_query', async (query) => {
  console.log('Pre-checkout:', query.id);
  
  // Validate the order here if needed
  await bot.answerPreCheckoutQuery(query.id, true);
});

// Handle successful payment
bot.on('successful_payment', (msg) => {
  const payment = msg.successful_payment;
  
  console.log('✅ Payment received!');
  console.log('  Amount:', payment.total_amount / 100, payment.currency);
  console.log('  Payload:', payment.invoice_payload);
  console.log('  Charge ID:', payment.telegram_payment_charge_id);
  
  bot.sendMessage(msg.chat.id, 
    '✅ *Payment Successful!*\n\n' +
    `Amount: $${payment.total_amount / 100}\n` +
    `Transaction ID: ${payment.telegram_payment_charge_id.slice(-8)}`,
    { parse_mode: 'Markdown' }
  );
});

console.log('Bot is running. Commands: /start, /pay');
