import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import httpx

# إعداد نظام التنبيهات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ضع مفتاح Gemini API هنا
GEMINI_API_KEY = "AQ.Ab8RN6L_v25zEHtZwOJz_4dmiIzEeaK_mo4clXuXDu-ni6rTLw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ازيك يا باشا! أنا جاهز للرد.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": user_text}]}]}
    
    try:
        async with httpx.AsyncClient() as client: response = await client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            reply_text = result['candidates'][0]['content']['parts'][0]['text']
            await update.message.reply_text(reply_text)
        else:
            await update.message.reply_text("معلش، مش قادر اتصل دلوقتي.")
    except Exception as e:
        await update.message.reply_text("حصلت مشكلة وأنا بفكر.")

if __name__ == '__main__':
    # ضع توكن البوت هنا
    TOKEN = "8821618204:AAGTb5YAVTa99IuoWRJaDuCICTmUoOi0WTk"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    app.run_polling()
