from app.ai.quiz_generator import generate_quiz

quiz = generate_quiz(
    topic="Machine Learning",
    difficulty="Easy",
    num_questions=3
)

print(quiz)