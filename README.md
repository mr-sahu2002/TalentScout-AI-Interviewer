# Resume Analyzer & Interview Assistant

## Project Overview
The **Resume Analyzer & Interview Assistant** is a Streamlit-based application designed to streamline the hiring process. It allows users to upload resumes, extract and analyze relevant information, and conduct AI-driven mock interviews. By leveraging Google's Generative AI and advanced text extraction tools, this assistant provides insights into candidate profiles and assists in evaluating their skills and experience.

### Key Features
- Upload and analyze resumes (PDF format).
- Extract candidate information in structured JSON format.
- Allow users to edit extracted information.
- Conduct interactive interviews with AI-driven question generation.
- Mix technical, conversational, and situational questions tailored to the candidate's profile.

---

## Installation Instructions

### Prerequisites
- Python 3.10+
- Streamlit
- Google Generative AI API access (Gemini Model)
- Libraries listed in `requirements.txt`

### Steps to Install
1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up environment variables:
    - Create a `.env` file in the root directory and add your Google Generative AI API key:
      ```
      GOOGLE_API_KEY=<your_api_key>
      ```
    - Alternatively, if deploying via Streamlit, set the API key using Streamlit's `secrets` feature.
4. Run the application locally:
    ```bash
    streamlit run app.py
    ```
5. Open the app in your browser at [http://localhost:8501](http://localhost:8501).

---

## Usage Guide

### Analyzing a Resume
      1. Upload a resume (PDF format) via the sidebar.
      2. Click on **Extract and Analyze** to process the resume.
      3. Review and update the extracted information in the sidebar.
      4. Save changes by clicking **Update Information**.

### Starting an Interview
      1. Ensure candidate information is complete and updated.
      2. Click **Start Interview** to initiate the mock interview.
      3. Use the chat interface to interact with the AI interviewer.
      4. Review the chat history and responses in real-time.

---

## Technical Details

### Libraries Used
- **Streamlit**: For the frontend and interactive UI.
- **google.generativeai**: To interface with Google's Gemini Model for content generation.
- **PDFTextExtractor**: A custom utility for extracting text from PDF resumes.
- **dotenv**: To manage environment variables.
- **tempfile & os**: For temporary file handling.

### Model Details
- **Generative Model**: Gemini-1.5-Flash by Google Generative AI.
- **Purpose**: Used for structured information extraction and generating tailored interview questions.

### Architectural Decisions
- **Resume Analysis**: Designed to handle missing fields gracefully by providing placeholders or defaults.
- **Interview Questions**: Dynamically generated based on the context to simulate a real interview.
- **Interactive UI**: Streamlit’s session state enables persistent state management for chat history and candidate data.

## Prompt Design

### Resume Analysis Prompt
The prompt is designed to:
- Extract structured information in JSON format.
- Handle inconsistencies or missing data with placeholders.
- Focus on key candidate details (e.g., name, email, experience, skills).

### Interview Assistant Prompt
The prompt adheres to the following:
- Simulates a friendly yet professional technical interviewer.
- Adapts questions based on candidate information and responses.
- Combines conversational and technical assessments.
- Includes fallback mechanisms for unclear inputs.


## Challenges & Solutions

### Challenges
1. **Parsing Incomplete Data**: Resumes often have missing or inconsistent fields.
2. **Dynamic Question Generation**: Ensuring questions remain contextually relevant and engaging.
3. **Handling Large PDFs**: Managing file size limits and optimizing text extraction.

### Solutions
1. **Graceful Handling of Missing Fields**: Introduced placeholders and defaults for missing data.
2. **Context-Aware Prompts**: Designed robust prompts to dynamically adapt to candidate profiles.
3. **File Size Validation**: Set a 10MB file size limit to ensure efficient processing.

## Future implmentation 
1. **Text to Speech (TTS) Integration** **& Speech to Text (STT) Integration**
2. **Code Editor for Technical Questions**
3. **AI Proctoring for Monitoring Interview Integrity**

# Deployed on streamlit 
[talentscout-ai-interviewer](https://talentscout-ai-interviewer.streamlit.app/)

