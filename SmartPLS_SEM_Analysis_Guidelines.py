# ============================================================
# SmartPLS Research Assistant v1.5
# Developed by Mahbub Hassan
# Department of Civil Engineering, Chulalongkorn University
# ============================================================

import streamlit as st
import pandas as pd
import io

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SmartPLS Research Assistant | Mahbub Hassan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CHULALONGKORN THEME CSS ---
custom_css = """
<style>
    :root {
        --primary-color: #C5007B;       /* CU Pink */
        --secondary-color: #F6F2F7;     /* Soft Lavender Gray */
        --accent-color: #7A1E6C;        /* Deep Purple for buttons */
        --pass-color: #28a745;
        --warn-color: #ffc107;
        --fail-color: #dc3545;
    }

    .stApp {
        background-color: var(--secondary-color);
        font-family: 'Segoe UI', sans-serif;
    }

    /* --- Sidebar --- */
    [data-testid="stSidebar"] {
        background-color: var(--primary-color);
        color: white;
    }
    [data-testid="stSidebar"] h1 {
        color: white;
        font-weight: 700;
    }
    [data-testid="stSidebar"] .stRadio > label {
        color: white;
        font-size: 1.05em;
    }

    /* --- Main Headings --- */
    h1, h2, h3 {
        color: var(--accent-color);
        font-weight: 700;
    }

    /* --- Buttons --- */
    .stButton > button {
        background-color: var(--accent-color);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #9c2d85;
        color: white;
    }

    /* --- Tabs --- */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f0d9e8;
        border-radius: 5px;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
        font-weight: 600;
    }

    /* --- Metric Cards --- */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 14px;
    }
    .pass-text { color: var(--pass-color); font-weight: bold; }
    .warn-text { color: var(--warn-color); font-weight: bold; }
    .fail-text { color: var(--fail-color); font-weight: bold; }

    /* --- Footer --- */
    .footer {
        text-align: center;
        color: gray;
        font-size: 14px;
        padding-top: 15px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 3. BRANDING HEADER ---
st.markdown(
    """
    <div style="background: linear-gradient(90deg, #C5007B, #7A1E6C); 
                padding:18px; border-radius:10px; color:white; text-align:center;">
        <h2 style="margin:0;">SmartPLS Research Assistant</h2>
        <p style="margin:4px 0 0;">Developed by <b>Mahbub Hassan</b> | 
        Department of Civil Engineering, Chulalongkorn University |
        <a href="https://www.bdeshi-lab.org/" target="_blank" style="color:#FFDDEE; text-decoration:none; font-weight:600;">
        B'Deshi Emerging Research Lab
        </a></p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🔬 SEM Analysis Workflow")
st.sidebar.markdown("Follow these steps sequentially for valid analysis.")
page = st.sidebar.radio(
    "Select Step:",
    ["🏠 Home: Introduction",
     "🧪 Step 1: Measurement Model",
     "📈 Step 2: Structural Model",
     "🧬 Step 3: Advanced Analyses"]
)

# --- 5. DISPLAY FUNCTION ---
def display_metric(label, value, explanation, status):
    if status == "pass":
        st.metric(label=label, value=value, delta="PASS")
        st.markdown(f"<p class='pass-text'>✅ {explanation}</p>", unsafe_allow_html=True)
    elif status == "warn":
        st.metric(label=label, value=value, delta="ACCEPTABLE", delta_color="off")
        st.markdown(f"<p class='warn-text'>⚠️ {explanation}</p>", unsafe_allow_html=True)
    elif status == "fail":
        st.metric(label=label, value=value, delta="FAIL", delta_color="inverse")
        st.markdown(f"<p class='fail-text'>❌ {explanation}</p>", unsafe_allow_html=True)

# --- 6. DATA EXPORT UTILITY ---
def export_summary(data_dict):
    if not data_dict: return
    df = pd.DataFrame(data_dict)
    csv = df.to_csv(index=False)
    st.download_button(
        label="💾 Download Your Summary (CSV)",
        data=csv,
        file_name="SmartPLS_Results_Summary.csv",
        mime="text/csv"
    )

# ==============================================================
# --- PAGE 1: HOME ---
# ==============================================================
if page == "🏠 Home: Introduction":
    st.title("📊 Welcome to the SmartPLS Research Assistant")
    st.markdown("""
    This interactive tool supports researchers and students in interpreting and reporting 
    **Partial Least Squares Structural Equation Modeling (PLS-SEM)** results derived from **SmartPLS**.  

    **Workflow Overview**
    1. **Measurement Model:** Validate constructs (reliability & validity).  
    2. **Structural Model:** Test hypotheses and model strength.  
    3. **Advanced Analyses:** Explore mediation, moderation, MGA, and fsQCA.
    """)
    with st.expander("📘 Glossary of Key Terms"):
        st.markdown("""
        - **AVE** — Average Variance Extracted  
        - **CR (rho_c)** — Composite Reliability  
        - **HTMT** — Heterotrait–Monotrait Ratio  
        - **VIF** — Variance Inflation Factor  
        - **Q²** — Predictive Relevance  
        """)
    with st.expander("📚 Cite This Tool"):
        st.markdown("""
        **Hassan, M. (2025). SmartPLS Research Assistant: Interactive Guide for PLS-SEM Analysis and Reporting. Streamlit App.**  
        Department of Civil Engineering, Chulalongkorn University.  
        """)

    st.warning("**Disclaimer:** This educational resource complements, not replaces, methodological training. Always verify against journal standards and theoretical models.")

# ==============================================================
# --- PAGE 2: MEASUREMENT MODEL ---
# ==============================================================
elif page == "🧪 Step 1: Measurement Model":
    st.title("🧪 Step 1: Measurement Model Assessment")
    st.markdown("Run the **PLS Algorithm** in SmartPLS and check these values.")
    tabs = st.tabs(["Outer Loadings", "Reliability", "Convergent Validity", "Discriminant Validity"])
    summary = {}

    # Outer Loadings
    with tabs[0]:
        ol = st.number_input("Enter Outer Loading", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
        if st.button("Check Loading"):
            if ol >= 0.708:
                display_metric("Outer Loading", ol, "Ideal indicator reliability.", "pass")
            elif ol >= 0.4:
                display_metric("Outer Loading", ol, "Acceptable for exploratory research.", "warn")
            else:
                display_metric("Outer Loading", ol, "Too low. Delete this item.", "fail")
            summary["Outer Loading"] = [ol]

    # Reliability
    with tabs[1]:
        cr = st.number_input("Enter Composite Reliability (rho_c)", 0.0, 1.0, 0.8, 0.01)
        if st.button("Check Reliability"):
            if cr >= 0.7:
                display_metric("Composite Reliability", cr, "Construct is reliable.", "pass")
            elif cr >= 0.6:
                display_metric("Composite Reliability", cr, "Acceptable for early-stage models.", "warn")
            else:
                display_metric("Composite Reliability", cr, "Not reliable.", "fail")
            summary["Composite Reliability"] = [cr]

    # AVE
    with tabs[2]:
        ave = st.number_input("Enter AVE", 0.0, 1.0, 0.5, 0.01)
        if st.button("Check AVE"):
            if ave >= 0.5:
                display_metric("AVE", ave, "Convergent validity achieved.", "pass")
            else:
                display_metric("AVE", ave, "Convergent validity not achieved.", "fail")
            summary["AVE"] = [ave]

    # Discriminant Validity
    with tabs[3]:
        htmt = st.number_input("Enter HTMT", 0.0, 1.0, 0.85, 0.01)
        if st.button("Check HTMT"):
            if htmt < 0.85:
                display_metric("HTMT", htmt, "Good discriminant validity.", "pass")
            elif htmt < 0.9:
                display_metric("HTMT", htmt, "Acceptable discriminant validity.", "warn")
            else:
                display_metric("HTMT", htmt, "Constructs not distinct.", "fail")
            summary["HTMT"] = [htmt]

    export_summary(summary)

# ==============================================================
# --- PAGE 3: STRUCTURAL MODEL ---
# ==============================================================
elif page == "📈 Step 2: Structural Model":
    st.title("📈 Step 2: Structural Model Assessment")
    st.markdown("Run **Bootstrapping (5,000 subsamples)** in SmartPLS to interpret relationships.")
    tabs = st.tabs(["VIF", "Path Coefficients", "R²", "f²", "Q²"])

    with tabs[0]:
        vif = st.number_input("Enter VIF", 0.0, 20.0, 2.5, 0.1)
        if st.button("Check VIF"):
            if vif < 3:
                display_metric("VIF", vif, "No multicollinearity issue.", "pass")
            elif vif < 5:
                display_metric("VIF", vif, "Acceptable but improve model parsimony.", "warn")
            else:
                display_metric("VIF", vif, "High collinearity problem.", "fail")

    with tabs[1]:
        path = st.text_input("Path (e.g., PE → ATT)")
        beta = st.number_input("Path Coefficient (β)", -1.0, 1.0, 0.25, 0.01)
        pval = st.number_input("P-value", 0.0, 1.0, 0.05, 0.001)
        if st.button("Check Hypothesis"):
            if pval < 0.05:
                display_metric(path, f"β={beta:.2f}, p={pval:.3f}", "Significant relationship supported.", "pass")
            else:
                display_metric(path, f"β={beta:.2f}, p={pval:.3f}", "Not statistically significant.", "fail")

    with tabs[2]:
        r2 = st.number_input("R² Value", 0.0, 1.0, 0.5, 0.01)
        if st.button("Check R²"):
            if r2 >= 0.75:
                display_metric("R²", r2, "Substantial explanatory power.", "pass")
            elif r2 >= 0.5:
                display_metric("R²", r2, "Moderate explanatory power.", "warn")
            else:
                display_metric("R²", r2, "Weak explanatory power.", "fail")

    with tabs[3]:
        f2 = st.number_input("Effect Size (f²)", 0.0, 1.0, 0.15, 0.01)
        if st.button("Check f²"):
            if f2 >= 0.35:
                display_metric("f²", f2, "Large effect size.", "pass")
            elif f2 >= 0.15:
                display_metric("f²", f2, "Medium effect size.", "warn")
            elif f2 >= 0.02:
                display_metric("f²", f2, "Small effect size.", "warn")
            else:
                display_metric("f²", f2, "No meaningful effect.", "fail")

    with tabs[4]:
        q2 = st.number_input("Q² Value", -1.0, 1.0, 0.2, 0.01)
        if st.button("Check Q²"):
            if q2 > 0:
                display_metric("Q²", q2, "Model has predictive relevance.", "pass")
            else:
                display_metric("Q²", q2, "No predictive relevance.", "fail")

# ==============================================================
# --- PAGE 4: ADVANCED ANALYSES ---
# ==============================================================
elif page == "🧬 Step 3: Advanced Analyses":
    st.title("🧬 Step 3: Advanced Analyses")
    st.info("Perform these analyses only after validating Measurement and Structural Models.")
    st.markdown("""
    **Supported advanced evaluations:**
    - Mediation (Indirect Effects)
    - Moderation (Interaction Terms)
    - Multigroup Analysis (MGA)
    - Importance–Performance Map (IPMA)
    - fsQCA
    """)

# ==============================================================
# --- FOOTER ---
# ==============================================================
st.markdown(
    """
    <hr>
    <div class="footer">
        © 2025 Mahbub Hassan | Department of Civil Engineering, Chulalongkorn University |
        <a href="https://www.bdeshi-lab.org/" target="_blank" style="color:gray; text-decoration:none; font-weight:600;">
        B'Deshi Emerging Research Lab
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
