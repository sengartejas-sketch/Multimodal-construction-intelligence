import json
import streamlit as st
from ai_analyzer import analyze_construction_image

st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Multimodal Construction Intelligence Platform")
st.caption("AI-assisted construction safety, crack diagnostics, planning, and site advisory.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "Gemini API key (optional for demo mode)",
        type="password",
        help="Your key is used for AI analysis. Never share it or commit it to GitHub."
    )
    st.divider()
    st.write("**Project status:** Prototype")
    st.caption("AI analysis requires a valid Gemini API key. Demo mode is illustrative only.")

safety_tab, crack_tab, planning_tab, assistant_tab = st.tabs([
    "🦺 Site Safety",
    "🧱 Crack Diagnostics",
    "📐 Planning & Valuation",
    "🌦️ Site Assistant"
])

def run_image_analysis(uploaded_file, analysis_type, button_label):
    if uploaded_file is None:
        st.info("Upload a JPG or PNG image to begin.")
        return
    st.image(uploaded_file, caption="Uploaded image", use_container_width=True)
    if st.button(button_label, key=f"analyze_{analysis_type}"):
        if not api_key:
            st.warning("No API key entered. Add a Gemini API key in the sidebar to run AI analysis.")
            st.info("You can still explore the planning and weather advisory tabs without a key.")
            return
        try:
            with st.spinner("Analyzing image..."):
                result = analyze_construction_image(
                    image_bytes=uploaded_file.getvalue(),
                    mime_type=uploaded_file.type,
                    api_key=api_key,
                    analysis_type=analysis_type,
                )
            st.subheader("Analysis result")
            st.json(result)
            st.download_button(
                "Download JSON report",
                data=json.dumps(result, indent=2),
                file_name=f"{analysis_type}_report.json",
                mime="application/json",
                key=f"download_{analysis_type}",
            )
            st.warning(
                "This is an AI-generated estimate, not a certified inspection. "
                "Ask a qualified construction or structural professional to verify important findings."
            )
        except Exception as exc:
            st.error(f"Analysis could not be completed: {exc}")
            st.caption("Check your internet connection, API key, model availability, and API quota.")

with safety_tab:
    st.subheader("Site Safety & PPE Audit")
    st.write("Upload a construction-site photo to review visible personal protective equipment (PPE) and potential hazards.")
    safety_image = st.file_uploader(
        "Choose a construction-site image",
        type=["jpg", "jpeg", "png"],
        key="safety_upload",
    )
    run_image_analysis(safety_image, "safety", "Analyze site safety")

with crack_tab:
    st.subheader("Crack Diagnostics & Structural Integrity")
    st.write("Upload a concrete or wall photo to get a preliminary visual review of possible defects.")
    crack_image = st.file_uploader(
        "Choose a wall or concrete image",
        type=["jpg", "jpeg", "png"],
        key="crack_upload",
    )
    run_image_analysis(crack_image, "cracks", "Analyze visible cracks")

with planning_tab:
    st.subheader("Construction Planning & Valuation")
    st.write("These calculations are illustrative and are not a professional quotation or valuation.")
    col1, col2 = st.columns(2)
    with col1:
        structure = st.selectbox("Structure type", ["Residential", "Commercial", "Industrial", "Other"])
        area = st.number_input("Built-up area (sq. ft.)", min_value=0, value=1000, step=100)
        rate = st.number_input("Estimated construction cost per sq. ft. (₹)", min_value=0, value=2000, step=100)
    with col2:
        location_tier = st.selectbox("Location category", ["Tier 1", "Tier 2", "Tier 3"])
        completion = st.slider("Construction completion (%)", 0, 100, 0)
        valuation_rate = st.number_input("Estimated market value per sq. ft. (₹)", min_value=0, value=2500, step=100)
    budget = area * rate
    spent = budget * completion / 100
    valuation = area * valuation_rate
    m1, m2, m3 = st.columns(3)
    m1.metric("Illustrative project budget", f"₹{budget:,.0f}")
    m2.metric("Budget proportion by completion", f"₹{spent:,.0f}")
    m3.metric("Illustrative market value", f"₹{valuation:,.0f}")
    st.progress(completion / 100)
    st.write(f"**Project:** {structure} · **Location category:** {location_tier}")
    st.caption("Actual budgets, market values, steel, and cement quantities require local rates, drawings, and professional estimates.")

with assistant_tab:
    st.subheader("Daily Site Assistant & Weather Advisory")
    weather = st.selectbox(
        "Current or expected site condition",
        ["Normal", "High Wind", "Heavy Rain", "Extreme Heat"],
    )
    advice = {
        "Normal": [
            "Continue routine site inspections and housekeeping.",
            "Check PPE, access routes, equipment condition, and first-aid supplies."
        ],
        "High Wind": [
            "Check official weather alerts and equipment manufacturer wind limits.",
            "Pause crane, lifting, or work-at-height activities when site procedures or competent supervisors require it."
        ],
        "Heavy Rain": [
            "Inspect drainage, slippery surfaces, excavation stability, and water ingress.",
            "Keep people away from wet electrical equipment and have a competent person assess hazards."
        ],
        "Extreme Heat": [
            "Provide drinking water, shade, rest breaks, and heat-stress monitoring.",
            "Adjust work schedules and follow local heat-safety procedures."
        ],
    }
    for item in advice[weather]:
        st.write(f"- {item}")

    st.divider()
    st.write("Ask a general construction-planning question:")
    question = st.text_area("Your question", placeholder="Example: What should be checked before concrete is poured?")
    if st.button("Get guidance"):
        if not question.strip():
            st.warning("Enter a question first.")
        elif not api_key:
            st.info("Add a Gemini API key in the sidebar to ask the AI assistant.")
        else:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                with st.spinner("Preparing guidance..."):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=(
                            "You are a cautious construction information assistant. "
                            "Give general educational guidance, state uncertainties, and "
                            "do not certify structural safety or replace qualified professionals.\n\n"
                            + question
                        ),
                    )
                st.markdown(response.text or "No response returned.")
            except Exception as exc:
                st.error(f"Could not get guidance: {exc}")

st.divider()
st.caption("Educational prototype. AI outputs and cost calculations must be independently verified.")
