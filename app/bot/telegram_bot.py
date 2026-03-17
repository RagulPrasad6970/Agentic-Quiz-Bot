from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from app.google.form_creator import create_google_form, add_questions
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from app.config import TELEGRAM_TOKEN
from app.ai.quiz_generator import generate_quiz
from app.google.form_creator import create_google_form, add_questions


user_state = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 Welcome to AI Quiz Generator!\n\n"
        "Please type the quiz topic."
    )

    user_state[update.message.from_user.id] = {"step": "topic"}


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_state:
        user_state[user_id] = {"step": "topic"}

    step = user_state[user_id]["step"]

    if step == "topic":

        user_state[user_id]["topic"] = text
        user_state[user_id]["step"] = "num_questions"

        await update.message.reply_text(
            "📝 Enter the number of questions."
        )

    elif step == "num_questions":

        try:
            num = int(text)
        except:
            await update.message.reply_text("Please enter a valid number.")
            return

        user_state[user_id]["num_questions"] = num
        user_state[user_id]["step"] = "difficulty"

        keyboard = [
            [
                InlineKeyboardButton("Easy", callback_data="easy"),
                InlineKeyboardButton("Medium", callback_data="medium"),
                InlineKeyboardButton("Hard", callback_data="hard"),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "⚙️ Select difficulty level:",
            reply_markup=reply_markup
        )


async def difficulty_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    difficulty = query.data

    topic = user_state[user_id]["topic"]
    num_questions = user_state[user_id]["num_questions"]

    await query.edit_message_text(
        "⏳ Generating your quiz and creating Google Form... please wait 🤖"
    )

    try:

        # Generate quiz with AI
        quiz = generate_quiz(topic, difficulty, num_questions)

        questions = quiz["questions"]

        # Create Google Form
        form_title = f"{topic} Quiz"
        form_id, form_url = create_google_form(form_title)

        # Insert questions
        add_questions(form_id, questions)

        await query.message.reply_text(
            f"✅ Quiz created successfully!\n\n"
            f"📋 Take the quiz here:\n{form_url}"
        )

    except Exception as e:

        await query.message.reply_text(
            f"❌ Error creating quiz.\n\n{str(e)}"
        )

    user_state[user_id] = {"step": "topic"}


def run_bot():

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.add_handler(CallbackQueryHandler(difficulty_handler))

    app.run_polling()