from googleapiclient.discovery import build
from app.google.form_creator import get_credentials


def read_form_responses(form_id):

    creds = get_credentials()

    service = build("forms", "v1", credentials=creds)

    result = service.forms().responses().list(
        formId=form_id
    ).execute()

    responses = result.get("responses", [])

    parsed = []

    for r in responses:

        answers = []

        for item in r["answers"].values():

            text = item["textAnswers"]["answers"][0]["value"]
            answers.append(text)

        parsed.append(answers)

    return parsed