🧠 Agentic Quiz System

An intelligent quiz generation platform that leverages AI to automatically create questions, evaluate user responses, and store results in a structured and scalable manner using Google Sheets.

📌 Overview

The Agentic Quiz System is designed to streamline quiz creation and evaluation by integrating AI capabilities with persistent storage. It eliminates manual effort in generating assessments while ensuring efficient tracking of user performance.

✨ Key Features

AI-Powered Question Generation.
Automatically generates context-aware quiz questions using the OpenAI API.
Automated Evaluation System.
Evaluates user responses with intelligent scoring mechanisms.
Cloud-Based Result Storage
Stores quiz data and results using the Google Sheets API
Secure Configuration Management
Uses environment variables for handling sensitive credentials
Modular & Scalable Design
Structured Python codebase for maintainability and future enhancements

## Installation

### 1. Clone the repository

git clone https://github.com/yourusername/agentic-quiz-system.git

cd agentic-quiz-system

### 2. Create a virtual environment

python -m venv venv

### 3. Activate the environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

### 4. Install dependencies

pip install -r requirements.txt

## Environment Variables

Create a `.env` file using `.env.example`.

Example:

OPENAI_API_KEY=your_api_key_here
GOOGLE_SHEET_ID=your_sheet_id
GOOGLE_CREDENTIALS_PATH=credentials.json

## Running the Project

Run the server using:

python test_ai.py

Or run the batch file:

run_server.bat

## Output Screenshots

### AI Response

![AI Response](Screenshots/ai_response.jpeg)

### Quiz Generation

![Quiz Output](Screenshots/quiz_output.jpeg)




## Technologies Used

* Python
* OpenAI API
* Google Sheets API
* Environment Variables
* Virtual Environments

## Future Improvements

* Web interface for quizzes
* User authentication
* Dashboard for quiz analytics
* Better answer evaluation

## License

This project is for learning and demonstration purposes.
