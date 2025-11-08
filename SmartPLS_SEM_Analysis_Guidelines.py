import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SmartPLS Research Assistant Guide by Mahbub Hassan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS FOR "GOOD LOOKING" DESIGN ---
# (This is the magic for making it colorful and professional)
custom_css = """
<style>
    /* --- Main App Colors --- */
    :root {
        --primary-color: #004e92;       /* Deep Blue for headers */
        --secondary-color: #f4f7f6;     /* Light Gray background */
        --accent-color: #00c1d4;        /* Bright Teal for buttons/accents */
        --pass-color: #28a745;          /* Green for Pass */
        --warn-color: #ffc107;          /* Yellow for Warning */
        --fail-color: #dc3545;          /* Red for Fail */
    }

    /* --- General App Background --- */
    .stApp {
        background-color: var(--secondary-color);
    }

    /* --- Sidebar --- */
    [data-testid="stSidebar"] {
        background-color: var(--primary-color);
        color: white;
    }
    [data-testid="stSidebar"] .stRadio > label {
        color: white; /* Make radio labels white */
        font-size: 1.1em;
    }
    [data-testid="stSidebar"] h1 {
        color: white;
        font-weight: 700;
    }

    /* --- Main Content --- */
    h1 {
        color: var(--primary-color);
        font-weight: 700;
    }
    h2, h3 {
        color: var(--primary-color);
    }

    /* --- Buttons --- */
    .stButton > button {
        background-color: var(--accent-color);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #00a1b3; /* Darker teal on hover */
        color: white;
    }

    /* --- Tabs --- */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #e0e0e0;
        border-radius: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
    }

    /* --- Result Text Classes --- */
    .pass-text {
        color: var(--pass-color);
        font-weight: bold;
    }
    .warn-text {
        color: var(--warn-color);
        font-weight: bold;
    }
    .fail-text {
        color: var(--fail-color);
        font-weight: bold;
    }
    
    /* --- Metric Styling --- */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 15px;
    }
    [data-testid="stMetric"] > div[data-testid="stMetricLabel"] {
        font-size: 1.1em;
        font-weight: 600;
    }

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🔬 SEM Analysis Workflow")
st.sidebar.markdown("Follow these steps in order for a valid analysis.")

page = st.sidebar.radio("Select Your Analysis Step:", [
    "🏠 Home: Introduction",
    "🧪 Step 1: Measurement Model",
    "📈 Step 2: Structural Model",
    "🧬 Step 3: Advanced Analyses"
])

# --- 4. HELPER FUNCTION TO DISPLAY METRICS ---
# This reusable function creates the nice "PASS/FAIL" metric boxes
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
    else:
        st.metric(label=label, value=value)
        st.info(explanation)


# --- ---------------------- ---
# --- PAGE 1: HOME ---
# --- ---------------------- ---
if page == "🏠 Home: Introduction":
    st.title("📊 Welcome to the SmartPLS Results Assistant by Mahbub Hassan!")
    st.markdown("### Your Step-by-Step Guide to PLS-SEM Analysis")
    st.markdown("""
    This app is a step-by-step guide to help you interpret the results from your SmartPLS analysis. 
    It's designed to follow the standard reporting procedure for a PLS-SEM paper.

    **Follow the steps in the sidebar in order:**
    1.  **Measurement Model:** First, you MUST validate your constructs (variables).
    2.  **Structural Model:** Second, you test the relationships *between* your constructs (your hypotheses).
    3.  **Advanced Analyses:** Finally, you can explore more complex relationships like mediation, moderation, etc.

    Use the navigation menu on the left to begin.
    """)
    
    st.warning("""
    **Disclaimer:** This tool is an educational guide, not a substitute for a deep understanding of statistics. 
    The thresholds provided are common 'rules of thumb' (e.g., from Hair et al.), but you should always 
    consult your supervisor, journal guidelines, and relevant methodological literature.
    """)

# --- ---------------------- ---
# --- PAGE 2: MEASUREMENT MODEL ---
# --- ---------------------- ---
elif page == "🧪 Step 1: Measurement Model":
    st.title("🧪 Step 1: Measurement Model Assessment")
    st.markdown("First, you must prove that your constructs are valid and reliable. **Run the 'PLS Algorithm' in SmartPLS.**")

    tabs = st.tabs([
        "✅ 1. Indicator Reliability (Outer Loadings)",
        "✅ 2. Internal Consistency Reliability",
        "✅ 3. Convergent Validity (AVE)",
        "✅ 4. Discriminant Validity"
    ])

    # --- Tab 1: Outer Loadings ---
    with tabs[0]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** Checks if each *item* (question) is a good measure of its *construct* (variable).
            - **Where to find it:** "Outer Loadings" table.
            - **Thresholds:**
                - **> 0.708:** Ideal.
                - **0.4 - 0.7:** Acceptable, *if* deleting it doesn't improve Composite Reliability or AVE.
                - **< 0.4:** Must be deleted.
            """)
        
        with col2:
            st.subheader("Interactive Checker")
            with st.form("ol_checker"):
                ol_val = st.number_input("Enter your Outer Loading Value", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
                ol_submitted = st.form_submit_button("Check Loading")

            if ol_submitted:
                if ol_val >= 0.708:
                    display_metric(f"Loading: {ol_val:.3f}", "PASS", "This loading is ideal. Keep it.", "pass")
                elif ol_val >= 0.4:
                    display_metric(f"Loading: {ol_val:.3f}", "ACCEPTABLE", "Weak loading. Only keep if reliability (rho_c, AVE) is high.", "warn")
                else:
                    display_metric(f"Loading: {ol_val:.3f}", "FAIL", "Loading is too low. You must delete this item.", "fail")
    
    # --- Tab 2: Internal Consistency ---
    with tabs[1]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** Checks if all items for a construct are measuring the same thing.
            - **Where to find it:** "Construct Reliability" table.
            - **Thresholds:**
                - **Composite Reliability (rho_c):** **> 0.70** (This is the modern standard).
                - **Cronbach's Alpha (α):** **> 0.70** (Traditional standard).
            """)
        
        with col2:
            st.subheader("Interactive Checker")
            with st.form("cr_checker"):
                cr_val = st.number_input("Enter your Composite Reliability (rho_c)", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
                cr_submitted = st.form_submit_button("Check Reliability")

            if cr_submitted:
                if cr_val >= 0.7:
                    display_metric(f"rho_c: {cr_val:.3f}", "PASS", "This construct is reliable.", "pass")
                elif cr_val >= 0.6:
                    display_metric(f"rho_c: {cr_val:.3f}", "ACCEPTABLE", "Only acceptable for exploratory research. Try to improve it.", "warn")
                else:
                    display_metric(f"rho_c: {cr_val:.3f}", "FAIL", "Construct is not reliable. You must fix this (e.g., delete low-loading items).", "fail")

    # --- Tab 3: Convergent Validity (AVE) ---
    with tabs[2]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** Checks if your construct explains a significant amount of variance in its items.
            - **Where to find it:** "Construct Reliability" table.
            - **Threshold:**
                - **Average Variance Extracted (AVE):** Must be **> 0.50**.
            """)
        
        with col2:
            st.subheader("Interactive Checker")
            with st.form("ave_checker"):
                ave_val = st.number_input("Enter your AVE Value", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
                ave_submitted = st.form_submit_button("Check AVE")

            if ave_submitted:
                if ave_val >= 0.5:
                    display_metric(f"AVE: {ave_val:.3f}", "PASS", "This construct has convergent validity.", "pass")
                else:
                    display_metric(f"AVE: {ave_val:.3f}", "FAIL", "Lacks convergent validity. You must fix this by deleting items with low loadings.", "fail")

    # --- Tab 4: Discriminant Validity ---
    with tabs[3]:
        st.subheader("What to Check")
        st.markdown("Checks that your constructs are truly distinct from each other. The **HTMT** is the modern 'gold standard'.")
        
        dv_tabs = st.tabs(["HTMT (Modern Method)", "Fornell-Larcker (Traditional Method)"])
        
        with dv_tabs[0]:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("""
                - **What it is:** Heterotrait-Monotrait Ratio.
                - **Where to find it:** "Discriminant Validity" -> "HTMT" table.
                - **Thresholds:**
                    - **< 0.85:** Ideal (for conceptually distinct constructs).
                    - **< 0.90:** Acceptable (for conceptually similar constructs).
                    - **> 0.90:** Fail.
                """)
            with col2:
                st.subheader("Interactive Checker")
                with st.form("htmt_checker"):
                    htmt_val = st.number_input("Enter your HTMT Value", min_value=0.0, max_value=1.2, value=0.8, step=0.01)
                    htmt_submitted = st.form_submit_button("Check HTMT")
                
                if htmt_submitted:
                    if htmt_val >= 0.9:
                        display_metric(f"HTMT: {htmt_val:.3f}", "FAIL", "Lacks discriminant validity. Your constructs are not distinct.", "fail")
                    elif htmt_val >= 0.85:
                        display_metric(f"HTMT: {htmt_val:.3f}", "ACCEPTABLE", "This is acceptable, but only if constructs are very similar.", "warn")
                    else:
                        display_metric(f"HTMT: {htmt_val:.3f}", "PASS", "This construct has discriminant validity.", "pass")
        
        with dv_tabs[1]:
            st.info("The Fornell-Larcker criterion is a traditional method. Most reviewers now prefer HTMT.")
            st.markdown("""
            - **Where to find it:** "Discriminant Validity" -> "Fornell-Larcker" table.
            - **Threshold:** The value at the top of each column (the **square root of the AVE**, in bold) must be **larger** than all the values *below it* in that column.
            """)

    st.success("**Proceed to the Structural Model ONLY IF your Measurement Model is valid!**")

# --- ---------------------- ---
# --- PAGE 3: STRUCTURAL MODEL ---
# --- ---------------------- ---
elif page == "📈 Step 2: Structural Model":
    st.title("📈 Step 2: Structural Model Assessment")
    st.markdown("Now you test your hypotheses. **Run 'Bootstrapping' (e.g., 5,000 subsamples) in SmartPLS.**")

    tabs = st.tabs([
        "✅ 1. Collinearity (VIF)",
        "✅ 2. Hypothesis Testing (Paths)",
        "✅ 3. Explanatory Power (R²)",
        "✅ 4. Effect Size (f²)",
        "✅ 5. Predictive Relevance (Q²)"
    ])

    # --- Tab 1: VIF ---
    with tabs[0]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** Checks if your *predictor* constructs (IVs) are too similar to each other.
            - **Where to find it:** "Collinearity Statistics (VIF)" table (from **PLS Algorithm** report). Look at the *inner model* values.
            - **Thresholds:**
                - **< 3.0:** Ideal.
                - **< 5.0:** Acceptable.
                - **> 5.0:** Fail (High collinearity).
            """)
        with col2:
            st.subheader("Interactive Checker")
            with st.form("vif_checker"):
                vif_val = st.number_input("Enter your VIF Value", min_value=0.0, max_value=20.0, value=2.5, step=0.1)
                vif_submitted = st.form_submit_button("Check VIF")
            
            if vif_submitted:
                if vif_val > 5.0:
                    display_metric(f"VIF: {vif_val:.2f}", "FAIL", "Multicollinearity is a problem. Consider merging or deleting a predictor.", "fail")
                elif vif_val > 3.0:
                    display_metric(f"VIF: {vif_val:.2f}", "ACCEPTABLE", "No major collinearity issue, but not ideal.", "warn")
                else:
                    display_metric(f"VIF: {vif_val:.2f}", "PASS", "No multicollinearity issue detected.", "pass")

    # --- Tab 2: Hypothesis Testing ---
    with tabs[1]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** Tests your hypotheses (e.g., "H1: IV -> DV is supported").
            - **Where to find it:** "Path Coefficients" table (from **Bootstrapping** report).
            - **Thresholds:**
                - **P-Value:** **< 0.05** = Hypothesis is **supported** (significant).
                - **Original Sample (β):** Shows the *direction* (positive or negative) and *strength* of the effect.
            """)
        with col2:
            st.subheader("Interactive Checker")
            with st.form("hyp_checker"):
                path = st.text_input("Path (e.g., 'IV -> DV')", "IV -> DV")
                beta_val = st.number_input("Enter Original Sample (β) Value", value=0.0, step=0.01)
                p_val = st.number_input("Enter P-Value", min_value=0.0, max_value=1.0, value=0.05, step=0.001, format="%.3f")
                hyp_submitted = st.form_submit_button("Check Hypothesis")

            if hyp_submitted:
                direction = "positive" if beta_val > 0 else "negative"
                if p_val < 0.05:
                    display_metric(f"{path}", f"p = {p_val:.3f}", f"SUPPORTED. The relationship is significant and {direction}. (β = {beta_val:.3f})", "pass")
                else:
                    display_metric(f"{path}", f"p = {p_val:.3f}", f"NOT SUPPORTED. The relationship is not significant.", "fail")

    # --- Tab 3: R-squared ---
    with tabs[2]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** Explanatory power. How much of the variance in your DV is explained by your IV(s).
            - **Where to find it:** "R-squared" table (from **PLS Algorithm** report).
            - **Thresholds (Rules of Thumb):**
                - **≈ 0.75:** Substantial
                - **≈ 0.50:** Moderate
                - **≈ 0.25:** Weak
            """)
        with col2:
            st.subheader("Interactive Checker")
            with st.form("r2_checker"):
                r2_val = st.number_input("Enter your R² Value", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
                r2_submitted = st.form_submit_button("Check R²")

            if r2_submitted:
                if r2_val >= 0.75:
                    status, text = "pass", "Substantial explanatory power."
                elif r2_val >= 0.50:
                    status, text = "pass", "Moderate explanatory power."
                elif r2_val >= 0.25:
                    status, text = "warn", "Weak explanatory power."
                else:
                    status, text = "fail", "Very weak explanatory power."
                display_metric(f"R² = {r2_val:.2f}", text, f"The model explains {r2_val*100:.0f}% of the variance.", status)

    # --- Tab 4: f-squared ---
    with tabs[3]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** Effect size. The individual contribution of an IV in explaining a DV.
            - **Where to find it:** "f-squared" table (from **PLS Algorithm** report).
            - **Thresholds:**
                - **≥ 0.35:** Large effect
                - **≥ 0.15:** Medium effect
                - **≥ 0.02:** Small effect
            """)
        with col2:
            st.subheader("Interactive Checker")
            with st.form("f2_checker"):
                f2_val = st.number_input("Enter your f² Value", min_value=0.0, max_value=2.0, value=0.15, step=0.01)
                f2_submitted = st.form_submit_button("Check f²")

            if f2_submitted:
                if f2_val >= 0.35:
                    status, text = "pass", "Large effect size."
                elif f2_val >= 0.15:
                    status, text = "pass", "Medium effect size."
                elif f2_val >= 0.02:
                    status, text = "warn", "Small effect size."
                else:
                    status, text = "fail", "No effect size (or negligible)."
                display_metric(f"f² = {f2_val:.3f}", text, f"This predictor has a {text.lower()}", status)

    # --- Tab 5: Q-squared ---
    with tabs[4]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** Predictive Relevance. Checks if your model has predictive power.
            - **How to get it:** Run the **'Blindfolding'** algorithm.
            - **Where to find it:** 'Construct Cross-validated Redundancy' report.
            - **Threshold:**
                - **Q² > 0:** The model HAS predictive relevance.
                - **Q² < 0:** The model LACKS predictive relevance.
            """)
        with col2:
            st.subheader("Interactive Checker")
            with st.form("q2_checker"):
                q2_val = st.number_input("Enter your Q² Value (for a DV)", value=0.3, step=0.01)
                q2_submitted = st.form_submit_button("Check Q²")

            if q2_submitted:
                if q2_val > 0:
                    display_metric(f"Q² = {q2_val:.3f}", "PASS", "The model has predictive relevance.", "pass")
                else:
                    display_metric(f"Q² = {q2_val:.3f}", "FAIL", "The model lacks predictive relevance.", "fail")


# --- ---------------------- ---
# --- PAGE 4: ADVANCED ANALYSES ---
# --- ---------------------- ---
elif page == "🧬 Step 3: Advanced Analyses":
    st.title("🧬 Step 3: Advanced Analyses")
    st.markdown("Explore complex relationships once your main model is validated.")
    
    tabs = st.tabs([
        "🤝 Mediation", 
        "⚖️ Moderation", 
        "👨‍👩‍👧‍👦 Multigroup Analysis (MGA)", 
        "🎯 IPMA",
        "🧩 fsQCA"
    ])
    
    # --- Tab 1: Mediation ---
    with tabs[0]:
        st.header("Mediation Analysis")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** Tests if an IV affects a DV *through* a Mediator variable (IV -> MED -> DV).
            - **Where to find it:** "Specific Indirect Effects" table (from **Bootstrapping** report).
            - **Threshold:**
                - **P-Value < 0.05:** You have a significant mediation effect.
            - **Types:**
                - **Full Mediation:** Indirect effect is significant, but *direct* effect (IV -> DV) is not.
                - **Partial Mediation:** *Both* indirect and direct effects are significant.
            """)
        with col2:
            st.subheader("Interactive Checker")
            with st.form("med_checker"):
                st.markdown("**Indirect Effect (IV -> MED -> DV)**")
                indirect_p = st.number_input("Enter P-Value for Indirect Effect", min_value=0.0, max_value=1.0, value=0.05, step=0.001, format="%.3f")
                st.markdown("**Direct Effect (IV -> DV)**")
                direct_p = st.number_input("Enter P-Value for Direct Effect", min_value=0.0, max_value=1.0, value=0.05, step=0.001, format="%.3f")
                med_submitted = st.form_submit_button("Check Mediation")
            
            if med_submitted:
                if indirect_p < 0.05:
                    if direct_p < 0.05:
                        display_metric(f"p = {indirect_p:.3f}", "PARTIAL MEDIATION", "Both direct and indirect effects are significant.", "pass")
                    else:
                        display_metric(f"p = {indirect_p:.3f}", "FULL MEDIATION", "The indirect effect is significant, but the direct effect is not.", "pass")
                else:
                    display_metric(f"p = {indirect_p:.3f}", "NO MEDIATION", "The indirect effect is not significant.", "fail")

    # --- Tab 2: Moderation ---
    with tabs[1]:
        st.header("Moderation Analysis")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** Tests if a *third variable* (Moderator) changes the strength of a relationship.
            - **How to run:** Add a "Moderating Effect" in SmartPLS and run **Bootstrapping**.
            - **Where to find it:** "Path Coefficients" table. Look for the **interaction term** (e.g., `Moderator * IV -> DV`).
            - **Threshold:**
                - **P-Value < 0.05:** You have a significant moderation effect.
            """)
        with col2:
            st.subheader("Interactive Checker")
            with st.form("mod_checker"):
                p_val = st.number_input("Enter P-Value for the Interaction Term", min_value=0.0, max_value=1.0, value=0.05, step=0.001, format="%.3f")
                mod_submitted = st.form_submit_button("Check Moderation")
            
            if mod_submitted:
                if p_val < 0.05:
                    display_metric(f"p = {p_val:.3f}", "SUPPORTED", "You have a significant moderation effect. Run a 'Simple Slope Analysis' to interpret it.", "pass")
                else:
                    display_metric(f"p = {p_val:.3f}", "NOT SUPPORTED", "There is no significant moderation effect.", "fail")

    # --- Tab 3: MGA ---
    with tabs[2]:
        st.header("Multigroup Analysis (MGA)")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** Compares path coefficients between two groups (e.g., Men vs. Women).
            - **How to run:** Run the **"MGA"** algorithm.
            - **Where to find it:** "MGA" report. Look at the `p-value (Permutation)`.
            - **Threshold:**
                - **P-Value < 0.05:** There is a **significant difference** between the groups.
            """)
        with col2:
            st.subheader("Interactive Checker")
            with st.form("mga_checker"):
                path = st.text_input("Path to Compare (e.g., 'IV -> DV')", "IV -> DV")
                p_val = st.number_input("Enter P-Value (Permutation)", min_value=0.0, max_value=1.0, value=0.05, step=0.001, format="%.3f")
                mga_submitted = st.form_submit_button("Check MGA")
            
            if mga_submitted:
                if p_val < 0.05:
                    display_metric(f"p = {p_val:.3f}", "DIFFERENCE FOUND", f"The effect of '{path}' is significantly different between your groups.", "pass")
                else:
                    display_metric(f"p = {p_val:.3f}", "NO DIFFERENCE", f"There is no significant difference for '{path}' between your groups.", "fail")

    # --- Tab 4: IPMA ---
    with tabs[3]:
        st.header("Importance-Performance Map Analysis (IPMA)")
        st.subheader("Visual Interpretation Guide")
        st.markdown("The IPMA is a visual chart, not a single 'pass/fail' number. It's for making managerial recommendations. Run the **'IPMA'** algorithm and find the chart.")
        st.markdown("Here is how to interpret the four quadrants:")

        # Create a 2x2 grid to represent the IPMA chart
        col1, col2 = st.columns(2)
        with col1:
            st.info("#### Q2: Low Importance / High Performance")
            st.markdown("""- **Action:** Low Priority
- **Meaning:** You are doing great, but it doesn't matter much to your DV.""")
        
        with col2:
            st.success("#### Q1: High Importance / High Performance")
            st.markdown("""- **Action:** Keep Up the Good Work
- **Meaning:** These are your star drivers. They are critical and you perform well in them.""")

        col3, col4 = st.columns(2)
        with col3:
            st.warning("#### Q3: Low Importance / Low Performance")
            st.markdown("""- **Action:** Lowest Priority
- **Meaning:** Don't waste resources here. It doesn't matter and you aren't good at it.""")
        
        with col4:
            st.error("#### Q4: High Importance / Low Performance")
            st.markdown("""- **Action:** **HIGH PRIORITY TO FIX**
- **Meaning:** These are your key weaknesses. They are critical for your DV, but you are performing poorly.""")


    # --- Tab 5: fsQCA ---
    with tabs[4]:
        st.header("Fuzzy-Set Qualitative Comparative Analysis (fsQCA)")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("What to Check")
            st.markdown("""
            - **What it is:** A completely different method from SEM. It finds *recipes* (configurations) of factors that lead to an outcome.
            - **Where to find it:** "fsQCA" report.
            - **Thresholds:**
                - **Consistency:** The "rule" for the recipe. Must be **> 0.80**.
                - **Coverage:** How much of the outcome is *explained* by this one recipe.
            """)
        with col2:
            st.subheader("Interactive Checker")
            with st.form("fsqca_checker"):
                consistency = st.number_input("Enter Consistency Value", min_value=0.0, max_value=1.0, value=0.8, step=0.01)
                coverage = st.number_input("Enter Coverage Value", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
                fsqca_submitted = st.form_submit_button("Check fsQCA Recipe")
            
            if fsqca_submitted:
                if consistency > 0.80:
                    display_metric(f"Consistency: {consistency:.3f}", "VALID RECIPE", f"This 'recipe' is a valid path to the outcome, explaining {coverage*100:.0f}% of it.", "pass")
                else:
                    display_metric(f"Consistency: {consistency:.3f}", "NOT VALID", "This 'recipe' is not a reliable path to the outcome.", "fail")
