
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.db import init_db
from app.scraper import run_scraper
from app.rag import RAG
from app.agents import DataExtractorAgent, ReviewAgent



# PAGE CONFIG



st.set_page_config(page_title="Samsung Smart Assistant", layout="wide")

st.title("📱 Samsung Smartphone Smart Assistant")
st.write("Your personal assistant for all Samsung smartphone information.")



# THINKING / LOADER HTML

def loader_html():
    return """
    <style>
    .loader {
      border: 6px solid #f3f3f3;
      border-top: 6px solid #3498db;
      border-radius: 50%;
      width: 40px;
      height: 40px;
      animation: spin 0.9s linear infinite;
      margin: auto;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    .center-loader {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 16px 0;
    }
    </style>

    <div class="center-loader">
        <div class="loader"></div>
    </div>
    """



# INITIALIZE DATABASE + DATA (AUTO)


init_db()

st.subheader("📦 Data Status")

if "data_initialized" not in st.session_state:
    with st.spinner("Initializing Samsung phone data (scraping + seed fallback)…"):
        try:
            # Try scraping; scraper will auto-fallback to SEED_DATA if scraping fails
            count = run_scraper(use_backup=False)
            st.session_state["data_initialized"] = True
            st.session_state["data_count"] = count
            if count > 0:
                st.success(f"Loaded {count} Samsung phone models in the background.")
            else:
                st.warning("⚠ No new phones loaded. Using existing database / seed data.")
        except Exception:
            st.session_state["data_initialized"] = True
            st.session_state["data_count"] = 0
            st.warning("⚠ Could not refresh data from GSMArena. Using existing database / seed data.")
else:
    count = st.session_state.get("data_count", 0)
    if count > 0:
        st.caption(f"📂 {count} phone models available from previous load.")
    else:
        st.caption("📂 Using existing database / seed data.")


st.divider()



# QUESTION INPUT

st.subheader("🤖 Ask a Question")

query = st.text_input("Ask about any Samsung phone (specs, comparison, best battery, etc.):")
submit = st.button("Ask AI")



# HANDLE QUERY


if submit and query.strip():
    # Initialize RAG + Agents
    rag = RAG()
    extractor = DataExtractorAgent(rag)
    reviewer = ReviewAgent()

    # Show loader while extracting / searching
    loader_placeholder = st.empty()
    loader_placeholder.markdown(loader_html(), unsafe_allow_html=True)

    extracted = extractor.extract(query)

    # Remove loader after extraction
    loader_placeholder.empty()

    query_type = extracted.get("type")

    
    # SINGLE PHONE QUERY
    
    if query_type == "single":
        phone = extracted.get("data")

        if phone is None:
            st.error("❌ I couldn't find a relevant Samsung phone for that query in the local database.")
        else:
            st.success(f"📱 Found: {phone['model_name']}")

            # st.json(phone)

            # Loader while AI generates explanation
            gen_loader = st.empty()
            gen_loader.markdown(loader_html(), unsafe_allow_html=True)

            answer = reviewer.generate(
                f"Explain full specs and strengths of {phone['model_name']} based on this info: {phone}"
            )

            gen_loader.empty()

            st.markdown("### 🧠 AI Summary")
            st.write(answer)


    # COMPARISON QUERY
   
    elif query_type == "compare":
        p1, p2 = extracted.get("data", (None, None))

        if p1 is None or p2 is None:
            st.error("❌ One or both Samsung models were not found in the local database.")
        else:
            st.success("📊 Comparison Data Found")

            col1, col2 = st.columns(2)
            # with col1:
            #     st.markdown("#### 📱 Phone 1")
            #     # st.json(p1)
            # with col2:
            #     st.markdown("#### 📱 Phone 2")
            #     # st.json(p2)

            gen_loader = st.empty()
            gen_loader.markdown(loader_html(), unsafe_allow_html=True)

            answer = reviewer.generate(
                f"Compare these two Samsung phones and give a user-friendly verdict:\nPhone A: {p1}\nPhone B: {p2}"
            )

            gen_loader.empty()

            st.markdown("### 🧠 AI Comparison Summary")
            st.write(answer)


    # BEST BATTERY QUERY

    elif query_type == "best_battery":
        phone = extracted.get("data")

        if phone is None:
            st.error("❌ I couldn't find any Samsung phone under this budget in the local database.")
        else:
            st.success(f"🔋 Best Battery Phone Under Budget: {phone['model_name']}")

            # st.json(phone)

            gen_loader = st.empty()
            gen_loader.markdown(loader_html(), unsafe_allow_html=True)

            answer = reviewer.generate(
                f"Recommend {phone['model_name']} as the best Samsung phone for battery life under this budget. "
                f"Base your reasoning on this info: {phone}"
            )

            gen_loader.empty()

            st.markdown("### 🧠 AI Recommendation")
            st.write(answer)

    else:
        st.error("⚠ Something went wrong understanding your question. Please try rephrasing.")

else:
    st.info(
        "💡 Try questions like:\n"
        "- 'Specs of Samsung Galaxy S23 Ultra'\n"
        "- 'Compare S23 Ultra and S22 Ultra'\n"
        "- 'Best Samsung battery phone under $800'\n"
    )
