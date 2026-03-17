import time
from googleapiclient.discovery import build
from app.google.form_creator import get_credentials
from app.database import SessionLocal
from app.models.models import Quiz


processed_responses = set()


def watch_forms():

    print("👀 Form watcher started")

    creds = get_credentials()
    service = build("forms", "v1", credentials=creds)

    db = SessionLocal()

    while True:

        try:

            quizzes = db.query(Quiz).all()

            for quiz in quizzes:

                form_id = quiz.form_id

                print(f"Checking responses for form: {form_id}")

                result = service.forms().responses().list(
                    formId=form_id
                ).execute()

                responses = result.get("responses", [])

                for r in responses:

                    response_id = r["responseId"]

                    if response_id in processed_responses:
                        continue

                    processed_responses.add(response_id)

                    answers = []

                    for item in r["answers"].values():

                        answer = item["textAnswers"]["answers"][0]["value"]
                        answers.append(answer)

                    print("✅ New submission detected:", answers)

        except Exception as e:

            print("❌ Watcher error:", e)

        time.sleep(10)