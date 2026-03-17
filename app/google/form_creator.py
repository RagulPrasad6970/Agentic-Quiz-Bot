from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

# Required scopes
SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.responses.readonly"
]

TOKEN_FILE = "token.pickle"


def get_credentials():

    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return creds


def create_google_form(title):

    creds = get_credentials()

    service = build("forms", "v1", credentials=creds)

    form = {
        "info": {
            "title": title
        }
    }

    result = service.forms().create(body=form).execute()

    form_id = result["formId"]

    # Enable quiz mode
    service.forms().batchUpdate(
        formId=form_id,
        body={
            "requests": [
                {
                    "updateSettings": {
                        "settings": {
                            "quizSettings": {
                                "isQuiz": True
                            }
                        },
                        "updateMask": "quizSettings.isQuiz"
                    }
                }
            ]
        }
    ).execute()

    form_url = f"https://docs.google.com/forms/d/{form_id}/viewform"

    return form_id, form_url


def add_questions(form_id, questions):

    creds = get_credentials()

    service = build("forms", "v1", credentials=creds)

    requests = []

    index = 0

    # Name field
    requests.append({
        "createItem": {
            "item": {
                "title": "Name",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {}
                    }
                }
            },
            "location": {"index": index}
        }
    })

    index += 1

    # Email field
    requests.append({
        "createItem": {
            "item": {
                "title": "Email",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {}
                    }
                }
            },
            "location": {"index": index}
        }
    })

    index += 1

    # Quiz questions
    for q in questions:

        options = q["options"]
        answer = q["answer"]

        if answer not in options:
            answer = options[0]

        requests.append({
            "createItem": {
                "item": {
                    "title": q["question"],
                    "questionItem": {
                        "question": {
                            "required": True,
                            "grading": {
                                "pointValue": 1,
                                "correctAnswers": {
                                    "answers": [
                                        {"value": answer}
                                    ]
                                }
                            },
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": opt} for opt in options
                                ],
                                "shuffle": True
                            }
                        }
                    }
                },
                "location": {"index": index}
            }
        })

        index += 1

    service.forms().batchUpdate(
        formId=form_id,
        body={"requests": requests}
    ).execute()