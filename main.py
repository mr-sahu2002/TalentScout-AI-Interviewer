import streamlit as st
import google.generativeai as genai
import json
import os
from extract import PDFTextExtractor
from dotenv import load_dotenv
import tempfile

load_dotenv()
# Initialize Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

# Define the function to analyze the resume text and extract relevant information in JSON format
def analyze_resume(text):
    prompt = f"""
    Extract the following details from the resume text. Ensure the extracted information is consistent and structured in the following JSON format, even if some fields are missing:

    {{
        "full_name": "<Full Name>",
        "email": "<Email Address>",
        "phone_number": "<Phone Number>",
        "years_of_experience": "<Years of Experience>",
        "desired_positions": ["<Desired Position 1>", "<Desired Position 2>", ...],
        "current_location": "<Current Location>",
        "tech_stack": ["<Technology 1>", "<Technology 2>", ...],
        "skills": {{
            "soft_skills": ["<Soft Skill 1>", "<Soft Skill 2>", ...],
            "hard_skills": ["<Hard Skill 1>", "<Hard Skill 2>", ...]
        }},
        "projects": [
            {{
                "name": "<Project Name>",
                "description": "<Project Description>",
                "technologies_used": ["<Technology 1>", "<Technology 2>", ...]
            }},
            ...
        ]
    }}

    Ensure:
    - Variations in formatting or missing data do not affect the JSON structure.
    - Provide empty strings, empty lists, or placeholders for missing data.
    - Extract the information as accurately as possible.

    Resume text:
    {text}
    """
    
    response = model.generate_content(prompt)
    
    try:
        # Parse the response text as JSON
        # First, find the JSON content within the response
        response_text = response.text
        # Find the first { and last } to extract just the JSON portion
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        return json.loads(json_str)
    except Exception as e:
        st.error(f"Error parsing response: {str(e)}")
        return {}

# Define the interviewer function to generate questions based on the candidate's context and responses
def interviewer(context, question):
    import json

    prompt = f"""
    Role: Friendly technical interviewer having a conversation to assess candidate skill and technical knowledge. all the question & answering should be within the limit of context provided.

    Candidate Information:
    {json.dumps(context, indent=2)}

    Conversation History:
    {question}

    Conversation Guidelines:
    1. Maintain a casual, friendly tone while professionally assessing technical skills
    2. Mix technical questions with conversational elements
    3. Show interest in their thought process and experience
    4. Build upon their responses naturally
    5. Use everyday scenarios to explore technical concepts
    6. don't ask too many question on same topic diversify the question 
    7. keep max no. of question to 8-10 based on candidate response

    Question Types to Mix:
    - Technical problem-solving: "How would you approach..."
    - Experience-based: "What's your take on..."
    - Opinion questions: "What do you think about..."
    - Architecture discussions: "How would you design..."
    - Best practices: "How do you usually handle..."

    Style:
    - Keep the tone warm and engaging
    - Ask one question at a time
    - Show active listening by referencing their previous answers
    - Use natural transitions between topics
    - Avoid rigid or overly formal language

    Fallback Mechanism:
    - If user input is unclear or not understood, respond with:
      "I'm sorry, I didn't quite catch that. Could you elaborate or rephrase?"
    - If unexpected inputs are received, respond with:
      "That’s an interesting perspective. Could you share more details about your thought process?"
    - Stay focused on the technical assessment purpose, even when uncertain inputs are given.

    End Conversation:
    - Gracefully conclude the conversation by thanking the candidate:
      "Thank you for taking the time to speak with me today!"
    - Inform them of the next steps:
      "Our team will review your interview and get back to you soon with updates on the next steps. Have a great day!"
    """
    response = model.generate_content(prompt)
    return response.text

# Main Streamlit application code 
def main():
    st.title("Resume Analyzer & Interview Assistant")
    
    # Initialize session state
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = None
    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False
    

    # Sidebar to upload and analyze resume
    with st.sidebar:
        st.header("Resume Analysis")
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'], key="file_uploader",help="Maximum file    size: 10MB")
        MAX_FILE_SIZE = 10 * 1024 * 1024

        if uploaded_file:
            if uploaded_file.size > MAX_FILE_SIZE:
                st.error("File is too large! Maximum size is 10MB.")
            else:
                if st.button("Extract and Analyze"):
                    # Save the uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        temp_path = tmp_file.name

                    try:
                        # Use your PDF extractor
                        extractor = PDFTextExtractor(temp_path)
                        text = extractor.extract_text()
                        
                        if text:
                            with st.spinner("Analyzing resume..."):
                                resume_data = analyze_resume(text)
                                st.session_state.resume_data = resume_data
                                st.session_state.candidate_info = resume_data
                                st.session_state.interview_started = False  # Reset interview started flag
                    except Exception as e:
                        st.error(f"Error processing PDF: {str(e)}")
                    finally:
                        # Clean up temporary file
                        os.unlink(temp_path)
        
        if st.session_state.resume_data:
            st.subheader("Extracted Information")
            resume_data = st.session_state.resume_data
            
            # Editable Fields to update extracted information of the candidate
            resume_data['full_name'] = st.text_input("Full Name", resume_data.get('full_name', ''))
            resume_data['email'] = st.text_input("Email", resume_data.get('email', ''))
            resume_data['phone_number'] = st.text_input("Phone Number", resume_data.get('phone_number', ''))
            resume_data['years_of_experience'] = st.text_input("Years of Experience", resume_data.get('years_of_experience', ''))
            resume_data['desired_positions'] = st.text_area("Desired Positions (comma-separated)", 
                                                             ", ".join(resume_data.get('desired_positions', [])))
            resume_data['current_location'] = st.text_input("Current Location", resume_data.get('current_location', ''))

            # Tech Stack
            tech_stack = st.text_area("Tech Stack/Technologies (comma-separated)", 
                                       ", ".join(resume_data.get('tech_stack', [])))
            resume_data['tech_stack'] = [item.strip() for item in tech_stack.split(",") if item.strip()]

            # Skills
            st.subheader("Skills")
            soft_skills = st.text_area("Soft Skills (comma-separated)", 
                                       ", ".join(resume_data.get('skills', {}).get('soft_skills', [])))
           
            resume_data['skills'] = {
                "soft_skills": [item.strip() for item in soft_skills.split(",") if item.strip()],
            }

            if st.button("Update Information"):
                st.session_state.candidate_info = resume_data
                st.success("Information updated!")
            
            if st.session_state.candidate_info and st.button("Start Interview"):
                st.session_state.chat_history = []
                st.session_state.interview_started = True
                st.success("Interview started!")

    # Main chat interface for the interview
    if st.session_state.interview_started:
        # Display chat history
        for msg in st.session_state.chat_history:
            if msg["role"] == "assistant":
                st.write("🤖 Interviewer:", msg["content"])
            else:
                st.write("👤 You:", msg["content"])
        
        # If this is the first message, send a greeting
        if not st.session_state.chat_history:
            greeting = interviewer(st.session_state.candidate_info, "Start the interview with a greeting and first question")
            st.session_state.chat_history.append({"role": "assistant", "content": greeting})
            st.write("🤖 Interviewer:", greeting)
        
        # Chat input
        user_input = st.chat_input("Your response")
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.write("👤 You:", user_input)
            
            # Get interviewer response
            response = interviewer(st.session_state.candidate_info, 
                                           str(st.session_state.chat_history))
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.write("🤖 Interviewer:", response)
            
    else:
        st.info("Please upload, analyze resume information if you want to start the interview process.")

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Resume Analyzer & Interview Assistant")
    main()