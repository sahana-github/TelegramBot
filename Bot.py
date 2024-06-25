import os
import telebot
from google import generativeai as gen_ai
import logging

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = 'YOUR_TELEGRAM_API'
GOOGLE_API_KEY = "YOUR_GOGGLE_GEMINI_API"

try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel('gemini-pro')
except Exception as e:
    logging.error(f"Error configuring Google Gemini API: {e}")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

def get_answer(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Error generating content: {e}")
        return "Sorry, I couldn't process your request at the moment."

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    user_first_name = message.from_user.first_name
    bot.reply_to(message, f"Howdy, {user_first_name}! How are you doing? I can help you with various tasks. Type /help to see what I can do.")

@bot.message_handler(commands=['help', 'contact'])
def help(message):
    bot.reply_to(message, """
Here are the commands you can use:
/start, /hello - Greet the bot
/help, /contact - Get help and contact information
/joke - Get a random joke
/quote - Get an inspirational quote
/news - Get the latest news headlines
GitHub Profile: https://github.com/sahana-github
LinkedIn Profile: https://www.linkedin.com/in/sahana-durgekar
""")

@bot.message_handler(commands=['joke'])
def send_joke(message):
    joke = get_answer("Tell me a joke.")
    bot.reply_to(message, joke)

@bot.message_handler(commands=['quote'])
def send_quote(message):
    quote = get_answer("Give me an inspirational quote.")
    bot.reply_to(message, quote)

@bot.message_handler(commands=['news'])
def send_news(message):
    news = get_answer("Give me the latest news headlines.")
    bot.reply_to(message, news)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    output = get_answer(message.text)
    bot.reply_to(message, output)

if __name__ == "__main__":
    bot.infinity_polling()
