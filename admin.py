import streamlit as st
from utils import load_candidate_data, get_latest_candidates

st.set_page_config(
    page_title="TalentScout Admin", 
    page_icon="📊", 
    layout="wide"
)

st.title("📊 TalentScout Admin Dashboard")
st.markdown("---")

# Load all candidates
candidates = load_candidate_data()

if not candidates:
    st.info("No candidates found.")
    st.stop()

st.write(f"**Total Candidates:** {len(candidates)}")

# Show recent candidates
recent_candidates = get_latest_candidates(10)

for idx, candidate in enumerate(recent_candidates):
    with st.expander(f"📋 {candidate['name']} - {candidate['position']} ({candidate.get('timestamp', 'No date')[:10]})"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Personal Info:**")
            st.write(f"• Name: {candidate['name']}")
            st.write(f"• Email: {candidate['email']}")
            st.write(f"• Phone: {candidate['phone']}")
            st.write(f"• Experience: {candidate['experience']} years")
            st.write(f"• Location: {candidate['location']}")
        
        with col2:
            st.write("**Assessment Info:**")
            st.write(f"• Position: {candidate['position']}")
            st.write(f"• Status: {candidate.get('status', 'N/A')}")
            st.write(f"• Submitted: {candidate.get('timestamp', 'N/A')[:19]}")
            st.write(f"• Deadline: {candidate.get('submission_deadline', 'N/A')[:19]}")
        
        st.write("**Tech Stack:**")
        st.code(candidate['tech_stack'])
        
        if 'questions' in candidate:
            st.write("**Questions Assigned:**")
            st.code(candidate['questions'])

# Summary statistics
st.markdown("---")
st.subheader("📈 Quick Stats")

col1, col2, col3 = st.columns(3)

with col1:
    avg_exp = sum(c.get('experience', 0) for c in candidates) / len(candidates)
    st.metric("Average Experience", f"{avg_exp:.1f} years")

with col2:
    positions = [c.get('position', '').lower() for c in candidates]
    common_position = max(set(positions), key=positions.count) if positions else "N/A"
    st.metric("Most Common Position", common_position.title())

with col3:
    recent_count = len([c for c in candidates if c.get('timestamp', '')])
    st.metric("Recent Assessments", recent_count)