from app import ai_client
from app.lead_analyzer import analyze_lead
from app.conversation_coach import get_next_step
import streamlit as st
from app.ui.dashboard import (
    render_score_card,
    render_sales_coach,
    render_profile,
)
from app.business_modes import get_system_prompt
import app.ai_client as ai_client
from app.lead_qualifier import extract_lead_info, lead_score
from app.pdf_export import create_proposal_pdf
from app.csv_export import profile_to_csv
# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="Ignition AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------
# Session State
# ---------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []
if "profile" not in st.session_state:
    st.session_state.profile = {}

if "analysis" not in st.session_state:
    st.session_state.analysis = analyze_lead({})

if "next_step" not in st.session_state:
    st.session_state.next_step = {
        "next_question": None,
        "reason": "",
        "next_action": "",
    }

# ---------------------------------
# Current Conversation State
# ---------------------------------

profile = st.session_state.profile
analysis = st.session_state.analysis
next_step = st.session_state.next_step

score = analysis["score"]

# ---------------------------------
# Sidebar
# ---------------------------------

with st.sidebar:

    st.title("🚀 Ignition AI")

    st.caption(
        "AI Business Automation Platform"
    )

    mode = st.selectbox(
        "Business Mode",
        [
            "Lead Qualification",
            "Customer Support",
            "Appointment Booking",
        ],
    )

    st.markdown("---")

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.7,
    )

    st.markdown("---")

    if st.button("🗑️ New Conversation"):

        st.session_state.messages = []
        st.session_state.profile = {}
        st.session_state.analysis = analyze_lead({})
        st.session_state.next_step = {
            "next_question": None,
            "reason": "",
            "next_action": "",
        }

        st.session_state["generated_proposal"] = None
        st.session_state["solution_text"] = ""

        st.rerun()

    st.divider()

    st.subheader("System")

    st.success("🟢 Online")

    st.write("Version", "v0.3")

    st.write("Model", "GPT-4.1 Mini")

    st.write("Provider", "OpenRouter")
    st.divider()

    render_score_card(analysis)

# ---------------------------------
# Main Layout
# ---------------------------------

chat_section = st.container()

st.write("")

left_col, right_col = st.columns([5, 1])

with left_col:
    
# ---------------------------------
# Chat History
# ---------------------------------

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if not st.session_state.messages:

        st.title("🤖 AI Lead Assistant")

        st.caption(
            "Qualify leads, answer questions, and help businesses automate customer conversations."
        )

        st.info(
            """
            ## Try asking something like:

            • Hi, I own a real estate agency with 12 employees.

            • I need an AI assistant for my website.

            • We want to automate lead qualification.

            • I run a law firm and need appointment booking.

            The assistant will automatically build a lead profile while guiding the conversation.
            """
        )

        st.divider()

# ---------------------------------
# Chat Input
# ---------------------------------

prompt = st.chat_input(
    "Describe your business or ask me anything..."
)

if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    conversation = st.session_state.messages.copy()

    system_prompt = get_system_prompt(mode)

    # Extract only the newly found information
    profile = extract_lead_info(conversation)

    # Merge with existing CRM profile
    existing_profile = st.session_state.profile.copy()

    for key, value in profile.items():
        if value is not None:
            existing_profile[key] = value

    st.session_state.profile = existing_profile
    profile = existing_profile

    # Analyze the complete merged profile
    analysis = analyze_lead(profile)

    closing_stage = (
        analysis["quality"] == "High"
        and len(analysis["missing"]) <= 1
    )

    with st.chat_message("assistant"):

        placeholder = st.empty()

        response = ""

        for chunk in ai_client.generate_response(
            system_prompt=system_prompt,
            conversation=conversation,
            temperature=temperature,
            closing_stage=closing_stage,
        ):
            response += chunk
            placeholder.markdown(response)

        placeholder.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    conversation = st.session_state.messages

    next_step = get_next_step(analysis)

    st.session_state.analysis = analysis
    st.session_state.next_step = next_step

    st.rerun()

with right_col:

    render_sales_coach(next_step)

    st.divider()

    render_profile(profile)
    st.divider()

    st.subheader("📝 Conversation Summary")

    if any(profile.values()):

        summary = f"""
    **Company:** {profile.get('company') or 'Unknown'}

    **Decision Maker:** {profile.get('decision_maker') or 'Unknown'}

    **Industry:** {profile.get('industry') or 'Unknown'}

    **Business Goal:** {profile.get('goal') or 'Not provided'}

    **Budget:** {profile.get('budget') or 'Not discussed'}

    **Timeline:** {profile.get('timeline') or 'Not discussed'}
    """

        st.markdown(summary)

    else:

        st.info(
            "Start a conversation to generate a business summary."
        )
    
    st.divider()

    st.subheader("📄 Proposal Generator")
    
    if analysis["score"] < 40:
        st.caption(
            "Complete a little more of the conversation to unlock proposal generation."
        )
    
    if "generated_proposal" not in st.session_state:
        st.session_state["generated_proposal"] = None

    if "solution_text" not in st.session_state:
        st.session_state["solution_text"] = ""

    if st.button(
        "Generate Proposal",
        use_container_width=True,
        disabled=analysis["score"] < 40,
    ):
        goal = (profile.get("goal") or "").lower()

        solution = [
            "• Capturing lead information",
            "• Improving response times",
        ]

        if "lead" in goal:
            solution.append("• Intelligent lead qualification")

        if "website" in goal:
            solution.append("• AI assistant for your website")

        if "whatsapp" in goal:
            solution.append("• WhatsApp customer assistant")

        if "appointment" in goal or "booking" in goal:
            solution.append("• Automated appointment booking")

        if "customer" in goal:
            solution.append("• 24/7 customer support")

        if "staff" in goal or "reception" in goal:
            solution.append("• Reduce staff workload through automation")

        if "social" in goal:
            solution.append("• Social media enquiry management")

        solution.append("• Business analytics and reporting")

        solution_text = "\n".join(solution)
        st.session_state["solution_text"] = solution_text
        st.write(solution_text)

        proposal = f"""
    # AI Automation Proposal

    ## Client

    Company: {profile.get("company") or "Prospective Client"}

    ---

    ## Contact

    Decision Maker:
    {profile.get("decision_maker") or "To Be Confirmed"}

    Industry:
    {profile.get("industry") or "General Business"}

    ---

    ## Business Need

    {profile.get("goal") or "Business automation solution tailored to client requirements."}

    ---

    ## Proposed Solution

    We propose implementing a customized AI solution designed specifically for this business.

    {solution_text}

    ---

    ## Estimated Project Scope

    Budget:
    {profile.get("budget") or "To Be Discussed"}

    Timeline:
    {profile.get("timeline") or "To Be Discussed"}

    ---

    Thank you for considering Project Ignition.
    """

        st.session_state["generated_proposal"] = proposal
        
if st.session_state["generated_proposal"]:

    st.divider()

    st.header("📄 AI Automation Proposal")

    with st.container(border=True):
        st.markdown(st.session_state["generated_proposal"])
    pdf_bytes = create_proposal_pdf(
        st.session_state.profile,
        st.session_state["solution_text"],
    )
    csv_data = profile_to_csv(
        st.session_state.profile,
        st.session_state.analysis,
    )

    st.download_button(
        "📥 Download Proposal PDF",
        data=pdf_bytes,
        file_name="AI_Proposal.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
    st.download_button(
        "📊 Download Lead CSV",
        data=csv_data,
        file_name="Lead_Profile.csv",
        mime="text/csv",
        use_container_width=True,
    )

# ---------------------------------
# Footer
# ---------------------------------

st.markdown("---")

st.caption(
    "Project Ignition • AI Lead Assistant • Built with Streamlit + OpenRouter"
)