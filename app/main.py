from fastapi import FastAPI
from app.database import engine
from app.models.models import Base
from app.bot.telegram_bot import run_bot
from app.worker.form_watcher import watch_forms
import threading

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Agentic Quiz System Running"}


@app.on_event("startup")
def start_services():

    print("🚀 FastAPI started")

    threading.Thread(target=run_bot, daemon=True).start()
    threading.Thread(target=watch_forms, daemon=True).start()