# 🧠 TalentScout Hiring Assistant

An intelligent AI-powered Hiring Assistant chatbot built using Streamlit and a large language model (LLM) to streamline the candidate screening process. This project demonstrates effective prompt engineering, conversational AI design, and real-world data handling for recruitment scenarios.

---

## 🚀 Project Overview

**TalentScout Hiring Assistant** is a smart chatbot that simulates the initial technical screening of candidates. It interacts with users via a web UI (built using Streamlit), collects essential candidate details, and generates customized technical questions based on their declared tech stack using the `HuggingFaceH4/zephyr-7b-beta` LLM.

The chatbot gracefully concludes the conversation and stores candidate data securely in a structured JSON file. An `admin` panel is also provided for recruiters to view submissions.

---

## 💡 Key Features

- ✅ Gathers essential candidate information (name, experience, tech stack, etc.)
- 🧠 Uses `zephyr-7b-beta` from Hugging Face to generate tailored technical questions
- 📂 Saves candidate responses in `candidate.json`
- 🧾 Separate admin interface (`admin.py`) to view all candidate data
- 🌐 Fully interactive and intuitive UI via **Streamlit**
- 👋 Graceful conversation end with follow-up instructions

---

## 🛠️ Technologies & Tools

- **Python 3.9+**
- **Streamlit** – for frontend interaction
- **Hugging Face Transformers** – for question generation via `zephyr-7b-beta`
- **Requests** – for API handling
- **JSON** – for candidate data storage

---

## 🖥️ Installation Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/talentscout-hiring-assistant.git
   cd talentscout-hiring-assistant

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt

3. **Run the Assistant (User View):**

   ```bash
    streamlit run app.py

4. **Run the Admin Panel (Recruiter View):**

   ```bash
    streamlit run admin.py


# Usage Guide

## For Candidates

1. Open the assistant by running:
   ```bash
   streamlit run app.py
2. Fill in your details:

- Full Name  
- Email  
- Phone Number  
- Years of Experience  
- Desired Role  
- Current Location  
- Tech Stack  

Based on your tech stack, the assistant will:

- Generate 3–5 tailored technical interview questions using the Zephyr-7B model from Hugging Face.
- Display the questions in a clean interface.

At the end of the conversation:

- Your details and questions will be saved in a `candidates.json` file.
- You'll receive a thank-you message and information about the next steps.

---

## 👨‍💻 For Recruiters (Admin Panel)

Launch the admin dashboard by running:

```bash
streamlit run admin.py


The admin panel will:

-Display a list of all candidate entries stored in candidates.json.

-Show the collected information such as name, contact, tech stack, and generated questions.

-Use this data for screening and further recruitment steps.

## 📄 License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software for personal or commercial purposes. See the [LICENSE](LICENSE) file for full license details.

