# ai-excel-interviewer

AI-Powered Excel Mock Interviewer
This project is a sophisticated, AI-powered web application designed to automate the technical screening process for roles requiring proficiency in Microsoft Excel. Built with Streamlit and powered by the OpenAI API, this tool simulates a real interview, evaluates candidate responses, and provides comprehensive, structured feedback.

🚀 Live Demo
<< Link to Deployed Streamlit App >>

(Note: Replace the link above with your actual deployment URL.)

✨ Key Features
Interactive Chat Interface: A clean and intuitive web-based interface where candidates can interact with "Alex," the AI interviewer.

Structured Interview Flow: The interview follows a predefined sequence of questions covering five core Excel topics, ensuring a consistent and fair evaluation for every candidate.

Dual-Model AI Architecture: The application intelligently uses two different AI models:

GPT-3.5-Turbo: For cost-effective and fluid conversation (greetings, asking questions, transitions).

GPT-4o: For high-accuracy, nuanced evaluation of the candidate's technical answers.

Expert-Grounded Evaluation: To solve the "cold start" problem, the AI evaluates answers against a built-in, expert-defined knowledge base, ensuring high-quality and consistent scoring from day one.

Comprehensive Feedback Reports: At the end of the interview, the system automatically generates a detailed performance summary, including:

A per-topic breakdown with a score (1-5) and specific feedback.

An overall summary with identified strengths and areas for improvement.

🏛️ System Architecture
The application operates on a simple yet powerful architecture designed for real-time interaction and intelligent processing.

Frontend (Streamlit): The user interacts with the application through the Streamlit interface.

State Management: Streamlit's session state is used to manage the entire interview flow, including the conversation history, the current question index, and all evaluation results.

Conversational Engine (GPT-3.5): Standard dialogue and questions are handled by this efficient model.

Evaluation Engine (GPT-4o): When a user submits an answer, it is sent to a dedicated evaluation function that uses GPT-4o's advanced reasoning and JSON mode to return a structured, unbiased assessment.

Report Generation: The collected JSON evaluations are aggregated and used to prompt the AI for a final, user-friendly report.

🛠️ Technology Stack
Core Language: Python

Frontend Framework: Streamlit

AI & LLMs: OpenAI API (GPT-4o & GPT-3.5-Turbo)

⚙️ Setup and Installation
To run this project locally, follow these steps:

1. Clone the Repository

git clone [https://github.com/your-username/ai-excel-interviewer.git](https://github.com/your-username/ai-excel-interviewer.git)
cd ai-excel-interviewer

2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install Dependencies

pip install -r requirements.txt

(Note: Make sure your requirements.txt file includes streamlit and openai.)

4. Set Up Environment Variables
The application requires an OpenAI API key. Create a file named .streamlit/secrets.toml and add your key to it:

# .streamlit/secrets.toml

OPENAI_API_KEY="your_openai_api_key_here"

5. Run the Streamlit App

streamlit run app.py

The application should now be running in your web browser!

🔧 Configuration & Customization
The interview questions, topics, and ideal answers can be easily customized by editing the EXCEL_TOPICS_KNOWLEDGE_BASE dictionary directly in the app.py file. This allows you to tailor the interview for different roles or difficulty levels.

📈 Future Roadmap
This Proof-of-Concept is a strong foundation. The architecture is designed for future enhancements, including:

Expanding the Knowledge Base: Add more Excel topics (e.g., Power Query, Advanced Charting) and introduce difficulty levels (Beginner, Intermediate, Advanced).

Adaptive Questioning: Implement logic for the AI to ask harder follow-up questions if a candidate answers well, or simplify if they are struggling.

Feedback & Integration: Build a feedback mechanism for recruiters to rate the AI's evaluation, creating a data loop for continuous improvement, and integrate with Applicant Tracking Systems (ATS).
