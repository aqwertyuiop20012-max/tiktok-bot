import os, threading
from flask import Flask
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "9252867816:AAEfW6QSMjoZd-tQ8Y3sy5yKqte8yEmEDSU"
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا! ابعتلي رابط تيك توك وأنا بحملك الفيديو بدون علامة مائية 🎬")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "tiktok.com" not in text and "vt.tiktok.com" not in text:
        await update.message.reply_text("ابعتلي رابط تيك توك صحيح")
        return
    msg = await update.message.reply_text("عم حمل... ⏳")
    try:
        ydl_opts = {"format": "mp4", "outtmpl": "video.mp4", "quiet": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([text])
        await update.message.reply_video(video=open("video.mp4", "rb"), caption="تفضل 🎬")
        os.remove("video.mp4")
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"ما قدرت حمله، جرب رابط تاني\n{e}")

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
