import streamlit as st


def render_score_card(analysis):
    score = analysis["score"]
    quality = analysis["quality"]
    st.subheader("📈 Lead Score")

    st.metric(
        label="Lead Score",
        value=score,
        delta=f"{quality} Quality",
    )

    if score >= 80:
        st.success("🔥 HOT LEAD")

    elif score >= 60:
        st.warning("🟡 WARM LEAD")

    else:
        st.info("🟢 EARLY STAGE")

    if analysis["missing"]:
        st.markdown("### 📋 Remaining Information")

        for field in analysis["missing"]:
            st.write(f"• {field.replace('_', ' ').title()}")

    else:
        st.success("All key information collected.")

    st.write("")
    
    
def render_sales_coach(next_step):
    
    st.subheader("🧠 AI Sales Coach")

    st.markdown("#### 💬 Next Question")

    if next_step["next_question"]:
        st.info(next_step["next_question"])
    else:
        st.success("Lead qualification is complete.")

    st.markdown("#### 💡 Why")
    st.write(next_step["reason"])

    st.markdown("#### ✅ Recommended Action")
    st.success(next_step["next_action"])
    
    
def render_profile(profile):
            
    st.subheader("👤 Lead Profile")

    fields = [
        ("🏢 Company", "company"),
        ("🏭 Industry", "industry"),
        ("💰 Budget", "budget"),
        ("📅 Timeline", "timeline"),
        ("👥 Employees", "employees"),
        ("👤 Decision Maker", "decision_maker"),
        ("🎯 Goal", "goal"),
        
        # Contact Information
        ("📧 Email", "email"),
        ("📱 Phone", "phone"),
        ("💬 WhatsApp", "whatsapp"),
        ("☎️ Preferred Contact", "preferred_contact"),
    ]

    completed = 0

    for label, key in fields:

        value = profile.get(key)

        st.markdown(f"**{label}**")

        if value:
            completed += 1
            st.write(value)
        else:
            st.caption("— Not provided")

        st.write("")
    progress = completed / len(fields)

    st.progress(progress)

    percent = int(progress * 100)

    st.caption(
        f"{completed}/{len(fields)} fields collected • {percent}% Complete"
    )

    st.write("")
    
def render_dashboard(profile, analysis, next_step):

    render_score_card(analysis)

    st.divider()

    render_sales_coach(next_step)

    st.divider()

    render_profile(profile)
    st.divider()

    st.subheader("📝 Conversation Summary")

    st.info(
        "No summary available yet. Complete a conversation to generate an AI business summary."
    )