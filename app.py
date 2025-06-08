import streamlit as st
from prompts import generate_greeting, generate_questions
from utils import validate_email, validate_phone, save_candidate_data

st.set_page_config(page_title="TalentScout - Hiring Assistant", page_icon="🤖", layout="centered")
st.title("🤖 TalentScout Hiring Assistant")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = "greet"
    st.session_state.data = {}

def next_step(step_name):
    st.session_state.step = step_name

# Step 1: Greeting
if st.session_state.step == "greet":
    with st.chat_message("assistant"):
        st.markdown(generate_greeting())
    next_step("name")

# Step 2: Name
if st.session_state.step == "name":
    with st.form("name_form"):
        name = st.text_input("Enter your full name:")
        submitted = st.form_submit_button("Next")
        if submitted:
            if name.strip() == "":
                st.warning("Please enter your name.")
            else:
                st.session_state.data["name"] = name.strip()
                next_step("email")

# Step 3: Email
if st.session_state.step == "email":
    with st.form("email_form"):
        email = st.text_input("Enter your email address:")
        submitted = st.form_submit_button("Next")
        if submitted:
            if not validate_email(email.strip()):
                st.warning("Please enter a valid email address.")
            else:
                st.session_state.data["email"] = email.strip()
                next_step("phone")

# Step 4: Phone Number
if st.session_state.step == "phone":
    with st.form("phone_form"):
        phone = st.text_input("Enter your 10-digit phone number:")
        submitted = st.form_submit_button("Next")
        if submitted:
            if not validate_phone(phone.strip()):
                st.warning("Please enter a valid 10-digit phone number.")
            else:
                st.session_state.data["phone"] = phone.strip()
                next_step("experience")

# Step 5: Years of Experience
if st.session_state.step == "experience":
    with st.form("experience_form"):
        experience = st.number_input("Enter your years of experience:", min_value=0, step=1)
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.data["experience"] = int(experience)
            next_step("position")

# Step 6: Desired Position(s)
if st.session_state.step == "position":
    with st.form("position_form"):
        position = st.text_input("Enter your desired position(s):")
        submitted = st.form_submit_button("Next")
        if submitted:
            if position.strip() == "":
                st.warning("Please enter a position.")
            else:
                st.session_state.data["position"] = position.strip()
                next_step("location")

# Step 7: Current Location
if st.session_state.step == "location":
    with st.form("location_form"):
        location = st.text_input("Enter your current location:")
        submitted = st.form_submit_button("Next")
        if submitted:
            if location.strip() == "":
                st.warning("Please enter your location.")
            else:
                st.session_state.data["location"] = location.strip()
                next_step("tech_stack")

# Step 8: Tech Stack
if st.session_state.step == "tech_stack":
    with st.form("stack_form"):
        tech_stack = st.text_area("List the programming languages, frameworks, databases, and tools you're proficient in:")
        submitted = st.form_submit_button("Generate Questions")
        if submitted:
            if tech_stack.strip() == "":
                st.warning("Please describe your tech stack.")
            else:
                st.session_state.data["tech_stack"] = tech_stack.strip()
                next_step("questions")

# Step 9: Generate Technical Questions
# Replace your Step 9 and Final Step with this:

# Step 9: Generate Technical Questions
if st.session_state.step == "questions":
    with st.chat_message("assistant"):
        st.markdown("Generating questions based on your tech stack...")
        try:
            questions = generate_questions(st.session_state.data["tech_stack"])
            st.session_state.data["questions"] = questions
            
            # Display questions with instructions
            st.markdown("### 📝 Technical Assessment Questions")
            st.markdown(f"**Based on your tech stack: {st.session_state.data['tech_stack']}**")
            st.markdown("---")
            st.markdown(questions)
            st.markdown("---")
            
            # Instructions
            st.info("""
            📋 **Instructions:**
            
            1. **Solve these questions in your local compiler/IDE**
            2. **Create separate files for each question** (e.g., question1.py, question2.java, etc.)
            3. **Include comments explaining your approach**
            4. **Test your solutions with sample inputs**
            5. **Submit all code files to:** `talentscout.tech.assessment@gmail.com`
            
            📧 **Email Subject:** `Technical Assessment - [Your Name] - [Position]`
            
            ⏰ **Submission Deadline:** Within 48 hours
            
            After evaluating your code, we will schedule your interview within 5-7 business days.
            """)
            
            if st.button("✅ I Understand - Proceed to Summary", type="primary"):
                next_step("summary")
                
        except Exception as e:
            st.error("⚠️ Failed to generate questions. Please try again.")
            st.stop()

# Step 10: Detailed Summary
if st.session_state.step == "summary":
    st.markdown("## 📋 Assessment Summary")
    
    # Candidate Details
    st.markdown("### 👤 Candidate Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Name:** {st.session_state.data['name']}")
        st.write(f"**Email:** {st.session_state.data['email']}")
        st.write(f"**Phone:** {st.session_state.data['phone']}")
    
    with col2:
        st.write(f"**Experience:** {st.session_state.data['experience']} years")
        st.write(f"**Position:** {st.session_state.data['position']}")
        st.write(f"**Location:** {st.session_state.data['location']}")
    
    # Tech Stack
    st.markdown("### 💻 Tech Stack")
    st.write(st.session_state.data['tech_stack'])
    
    # Questions Summary
    st.markdown("### 📝 Questions Assigned")
    with st.expander("View All Questions"):
        st.markdown(st.session_state.data['questions'])
    
    # Next Steps
    st.markdown("### 🚀 Next Steps")
    st.success("""
    **What happens next:**
    
    1. **Complete the coding assessment** in your local environment
    2. **Submit code files** to: talentscout.tech.assessment@gmail.com
    3. **Wait for evaluation** (5-7 business days)
    4. **Interview scheduling** if shortlisted
    
    **Remember:** Email subject should be `Technical Assessment - [Your Name] - [Position]`
    """)
    
    # Save data
    save_candidate_data(st.session_state.data)
    
    if st.button("🎯 Complete Assessment", type="primary"):
        next_step("end")

# Final Step: Graceful Conclusion
if st.session_state.step == "end":
    st.markdown("---")
    st.markdown("### 🎯 Thank You!")
    
    st.balloons()  # Fun animation
    
    st.success("""
    🙏 **Thank you for completing the initial screening with TalentScout!**
    
    📧 **Important Reminders:**
    - Submit your code files to: `talentscout.tech.assessment@gmail.com`
    - Use email subject: `Technical Assessment - [Your Name] - [Position]`
    - Deadline: 48 hours from now
    
    🤝 **We're excited to review your work and potentially welcome you to our client's team!**
    
    📞 **Questions?** Feel free to contact us at careers@talentscout.com
    
    Good luck with your assessment! 🚀
    """)
    
    st.info("**TalentScout Recruitment Agency** | Connecting Top Tech Talent")
    
    # Option to start new assessment
    if st.button("🔄 Start New Assessment"):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()