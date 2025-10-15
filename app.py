import streamlit as st
from openai import OpenAI
import json

st.set_page_config(
    page_title="AI Powered Excel Mock Interviewer"
)

# AI and PROMPT CONFIGURATION

# Initializing the OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# This is the "brain" of our AI interviewer. It defines its role, rules, and the topics to cover.
SYSTEM_PROMPT = """
You are an expert AI Mock Interviewer named "Alex" specializing in Microsoft Excel. Your goal is to conduct a professional and realistic mock interview.

**Interview Flow & Rules:**
1.  **Introduction:** Start with a brief introduction and explain the process.
2.  **Conducting the Interview:**
    - Ask the predefined questions one by one. Do not reveal the list or the ideal answers.
    - Once satisfied with a topic, smoothly transition to the next one.
3.  **Conclusion:** After all topics are covered, state that the interview is complete.
4.  **Feedback Generation:** When asked to generate the final report, use the provided structured evaluations to create a single, comprehensive feedback summary with strengths and areas for improvement.

**Excel Topics to Cover:**
1.  Lookup Functions (e.g., VLOOKUP, XLOOKUP)
2.  Pivot Tables
3.  Conditional Formatting
4.  Data Validation and Protection
5.  Macros and basic VBA
"""
# KNOWLEDGE BASE AND EVALUATION PROMPT 
EVALUATION_PROMPT = """
You are a strict but fair Excel Interview Examiner. Your only task is to evaluate a candidate's answer based on the provided question and the ideal, expert-level answer.

**Instructions:**
1.  **Compare:** Read the candidate's answer and compare it point-by-point against the provided ideal answer.
2.  **Score:** Rate the answer's technical accuracy on a scale from 1 (completely wrong) to 5 (perfectly correct and comprehensive).
3.  **Format Output:** Provide your evaluation in a JSON format. Do NOT add any other text outside the JSON object.

{
  "score": <integer_from_1_to_5>,
  "feedback": "<A concise, one-sentence summary of the candidate's performance on this specific question.>",
  "strengths": "<A brief bulleted list of what the candidate answered correctly.>",
  "weaknesses": "<A brief bulleted list of what the candidate missed or got wrong.>"
}
"""
EXCEL_TOPICS_KNOWLEDGE_BASE = {
    "Lookup Functions": {
        "question": "Can you explain the difference between VLOOKUP and XLOOKUP, and tell me which one you would generally prefer and why?",
        "ideal_answer": "VLOOKUP searches for a value in the first column of a table and returns a value from a specified column to the right. Its limitations are that it can't look left, and it can break if columns are added or deleted. XLOOKUP is the modern successor; it can look in any column and return from any column, defaults to a safer exact match, and is more resilient to table changes. XLOOKUP is almost always preferred."
    },
    "Pivot Tables": {
        "question": "Describe a scenario where you would use a Pivot Table and walk me through the basic steps to create one.",
        "ideal_answer": "A scenario is summarizing a large sales data table to see total revenue per region and product category. Steps: 1. Select your data. 2. Go to Insert > PivotTable. 3. Drag the 'Region' and 'Product Category' fields to the Rows area, and drag the 'Revenue' field to the Values area to automatically sum it up."
    },
    "Conditional Formatting": {
        "question": "What is Conditional Formatting used for? Give an example.",
        "ideal_answer": "Conditional Formatting is used to automatically change a cell's format (like its color or font) based on its value or a formula. An example is highlighting all sales figures below $1000 in red to quickly identify underperforming areas."
    },
    "Data Validation and Protection": {
        "question": "How would you ensure that users can only enter a date in a specific cell in Excel?",
        "ideal_answer": "You would use Data Validation. Select the cell, go to the Data tab, click Data Validation. In the 'Allow' dropdown, choose 'Date'. You can then set criteria, like dates between a start and end date."
    },
    "Macros and basic VBA": {
        "question": "What is a Macro in Excel and why would you use one?",
        "ideal_answer": "A Macro is a recorded sequence of actions, commands, and functions that you can run automatically. You use them to automate repetitive tasks to save time and reduce errors. For example, you could record a macro that formats a monthly report the same way every time."
    }
}
# Function to get a response from the OpenAI API
def get_ai_response(chat_history):
    """
    Sends the chat history to the OpenAI API and returns the AI's response.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error communicating with OpenAI: {e}")
        return "Sorry, I'm having connection issues at the moment. Please try again later."

# DEDICATED EVALUATION FUNCTION
def evaluate_answer(question, user_answer, ideal_answer):
    """
    Sends the user's answer to the LLM for structured evaluation.
    """
    try:
        messages = [
            {"role": "system", "content": EVALUATION_PROMPT},
            {"role": "user", "content": f"""
                **Question Asked:**
                {question}

                **Ideal Answer:**
                {ideal_answer}

                **Candidate's Answer:**
                {user_answer}
            """}
        ]
        
        # Used a powerful model for the evaluation step
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=messages,
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        
        # Safely parsing the JSON string from the response
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        st.error(f"Error during evaluation: {e}")
        return {"score": 0, "feedback": "Could not evaluate this answer.", "strengths": "N/A", "weaknesses": "N/A"}

# SESSION STATE INITIALIZATION
if 'interview_started' not in st.session_state:
    st.session_state['interview_started'] = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
# Adding keys to track progress and store evaluations
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'evaluations' not in st.session_state:
    st.session_state.evaluations = []

# Preparing questions from the new knowledge base
topics = list(EXCEL_TOPICS_KNOWLEDGE_BASE.keys())

#  WELCOME SCREEN 
if not st.session_state['interview_started']:
    st.image("cn.png", width=400)
    st.title("AI-Powered Excel Mock Interviewer")
    st.markdown("Welcome! This interview aims to evaluate the candidate's technical expertise in Excel.")
    st.info("💡 **Instructions for the Interview:**")
    st.success("""
        - The interview will have a series of questions.
        - Answer clearly and concisely.
        - A performance summary will be provided at the end.
    """)
    st.write("---")
    if st.button("**Begin Interview**", type="primary"):
        st.session_state['interview_started'] = True
        # Get the first question from the knowledge base
        first_question = EXCEL_TOPICS_KNOWLEDGE_BASE[topics[0]]['question']
        initial_ai_message = f"Hello! I am Alex, your AI interviewer. We will cover 5 topics. Let's start with **{topics[0]}**. {first_question}"
        st.session_state.messages.append({"role": "assistant", "content": initial_ai_message})
        st.rerun()

# INTERVIEW CHAT INTERFACE
else:
    st.title("Excel Mock Interview")
    
    # Displaying all the messages in the chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Checking if the interview is over before showing the chat input
    if st.session_state.current_question_index >= len(topics):
        st.info("The interview is complete. Thank you for your time!")
        # The final report is already displayed as the last message
    else:
        # Input box for the user's answer
        if user_input := st.chat_input("Your answer..."):
            # Adding user's message to the history and display it
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # CORE EVALUATION LOGIC ---
            with st.chat_message("assistant"):
                with st.spinner("Alex is evaluating your answer..."):

                    # 1. Evaluate the user's last answer
                    current_topic = topics[st.session_state.current_question_index]
                    knowledge_item = EXCEL_TOPICS_KNOWLEDGE_BASE[current_topic]
                    
                    evaluation_result = evaluate_answer(
                        question=knowledge_item['question'],
                        user_answer=user_input,
                        ideal_answer=knowledge_item['ideal_answer']
                    )
                    st.session_state.evaluations.append(evaluation_result)
                    
                    # 2. Move to the next question or conclude
                    st.session_state.current_question_index += 1
                    
                    if st.session_state.current_question_index < len(topics):
                        # Ask the next question
                        next_topic = topics[st.session_state.current_question_index]
                        next_question = EXCEL_TOPICS_KNOWLEDGE_BASE[next_topic]['question']
                        ai_response = f"Thank you. Let's move on to **{next_topic}**. {next_question}"
                        st.markdown(ai_response)
                        # Add the AI's response to the chat history
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    else:
                        # Ended the interview, generated the final report
                        # Combined all stored evaluations into a single string for the final prompt
                        final_feedback_prompt = (
    "The interview is now complete. Generate a final feedback report with the following structure:\n"
    "1. A 'Per-Topic Breakdown' section where you list EACH topic, its score, and a brief summary of the feedback for that topic.\n"
    "2. An 'Overall Summary' section that provides comprehensive feedback, strengths, and areas for improvement based on all the answers.\n\n"
    "Here is the structured evaluation data for each answer:\n\n"
)
# END OF PROMPT

                        for i, eval_item in enumerate(st.session_state.evaluations):
                          final_feedback_prompt += f"Topic: {topics[i]}\nScore: {eval_item['score']}/5\nFeedback: {eval_item['feedback']}\nStrengths: {eval_item['strengths']}\nWeaknesses: {eval_item['weaknesses']}\n\n"

                        # Added this special request to the end of the message history to guide the final AI response
                        st.session_state.messages.append({"role": "user", "content": final_feedback_prompt})
                        
                        final_report = get_ai_response(st.session_state.messages)
                        st.markdown(final_report)
                        # Added the final report to the chat history
                        st.session_state.messages.append({"role": "assistant", "content": final_report})

