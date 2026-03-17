from app.google.form_creator import create_google_form

form_id, form_url = create_google_form("Test Quiz")

print("Form ID:", form_id)
print("Form URL:", form_url)