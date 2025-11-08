# ============================================================
# SmartPLS Research Assistant v2.0 (Single-file, Pro UI)
# Author: Mahbub Hassan | Department of Civil Engineering, Chulalongkorn University
# Branding: B'Deshi Emerging Research Lab (www.bdeshi-lab.org)
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO
import datetime

# -------------------------------
# 1) PAGE CONFIG + SESSION STATE
# -------------------------------
st.set_page_config(
    page_title="SmartPLS Research Assistant | Mahbub Hassan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"  # "light" or "dark"

# -------------------------------
# 2) THEME (DARK/LIGHT) + CSS
#    Contemporary neutral palette
# -------------------------------
LIGHT = {
    "bg": "#F8FAFC",      # slate-50
    "panel": "#FFFFFF",   # white
    "primary": "#0F172A", # slate-900
    "accent": "#06B6D4",  # cyan-500
    "accent2": "#2563EB", # blue-600
    "muted": "#64748B",   # slate-500
    "border": "#E5E7EB",  # gray-200
    "good": "#16A34A",    # green-600
    "warn": "#F59E0B",    # amber-500
    "bad":  "#DC2626",    # red-600
}
DARK = {
    "bg": "#0B1220",      # near-slate-950
    "panel": "#0F172A",   # slate-900
    "primary": "#E5E7EB", # gray-200
    "accent": "#22D3EE",  # cyan-400
    "accent2": "#60A5FA", # blue-400
    "muted": "#94A3B8",   # slate-400
    "border": "#1F2937",  # gray-800
    "good": "#22C55E",    # green-500
    "warn": "#FBBF24",    # amber-400
    "bad":  "#F87171",    # red-400
}
P = DARK if st.session_state.theme_mode == "dark" else LIGHT

custom_css = f"""
<style>
    .stApp {{
        background-color: {P["bg"]};
        color: {P["primary"]};
        font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', Arial, sans-serif;
    }}
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {P["panel"]} 0%, {P["bg"]} 120%);
        color: {P["primary"]};
        border-right: 1px solid {P["border"]};
    }}
    /* Cards / panels (metrics look) */
    .card {{
        background: {P["panel"]};
        border: 1px solid {P["border"]};
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}
    /* Buttons */
    .stButton > button {{
        background-color: {P["accent2"]};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
    }}
    .stButton > button:hover {{ filter: brightness(1.05); }}
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: {P["panel"]};
        border: 1px solid {P["border"]};
        border-radius: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {P["muted"]};
        font-weight: 600;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background: {P["accent"]};
        color: #001016;
        border-radius: 10px;
    }}
    .good-text {{ color: {P["good"]}; font-weight: 700; }}
    .warn-text {{ color: {P["warn"]}; font-weight: 700; }}
    .bad-text  {{ color: {P["bad"]};  font-weight: 700; }}
    .footer {{
        text-align: center; color: {P["muted"]}; font-size: 13px; padding-top: 10px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------------
# 3) BRANDING HEADER + THEME TOGGLE
# -------------------------------
colA, colB = st.columns([0.8, 0.2])
with colA:
    st.markdown(
        f"""
        <div class="card" style="display:flex; align-items:center; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:14px;">
                <div style="width:46px; height:46px; background:{P["accent"]}; border-radius:10px;"></div>
                <div>
                    <div style="font-size:22px; font-weight:800;">SmartPLS Research Assistant</div>
                    <div style="font-size:14px; color:{P["muted"]};">
                        Developed by <b>Mahbub Hassan</b> · Department of Civil Engineering, Chulalongkorn University · 
                        <a href="https://www.bdeshi-lab.org/" target="_blank" style="color:{P["accent2"]}; text-decoration:none;">B'Deshi Emerging Research Lab</a>
                    </div>
                </div>
            </div>
            <div style="font-size:12px; color:{P["muted"]};">
                {datetime.datetime.now().strftime("%b %d, %Y")}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with colB:
    st.write("")
    mode = st.toggle("🌙 Dark Mode", value=(st.session_state.theme_mode == "dark"))
    st.session_state.theme_mode = "dark" if mode else "light"

# -------------------------------
# 4) SIDEBAR NAVIGATION + HELP
# -------------------------------
st.sidebar.title("🔬 SEM Analysis Workflow")
st.sidebar.caption("Follow sequentially for correct reporting.")
page = st.sidebar.radio(
    "Select Section:",
    ["🏠 Home",
     "🧪 Measurement Model",
     "📈 Structural Model",
     "🧬 Advanced Analyses",
     "📦 Upload & Parse (Optional)"]
)

with st.sidebar.expander("🆘 Quick Help"):
    st.markdown(
        "- **Enter values** from SmartPLS reports (PLS Algorithm / Bootstrapping / Blindfolding).\n"
        "- Use **Download Summary** to keep a CSV record for your appendix.\n"
        "- Check the **Glossary** and **Citations** when drafting the methods section."
    )

# -------------------------------
# 5) UTILITIES
# -------------------------------
def gauge(title:str, value:float, threshold:float, max_val:float=1.0, good_when_higher:bool=True):
    """
    Plotly donut gauge: shows how far a metric is from its threshold.
    good_when_higher=True means value>=threshold is good; otherwise reverse.
    """
    v = max(0.0, min(value, max_val))
    frac = v / max_val if max_val else 0.0
    # status
    ok = v >= threshold if good_when_higher else v <= threshold
    color = P["good"] if ok else (P["warn"] if abs(v-threshold) < 0.05*max_val else P["bad"])
    fig = go.Figure(data=[
        go.Pie(
            values=[v, max_val - v],
            labels=[f"{title}: {v:.2f}", ""],
            hole=0.7,
            direction="clockwise",
            sort=False,
            textinfo="label",
            marker=dict(colors=[color, P["border"]]),
            showlegend=False
        )
    ])
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        annotations=[dict(text=f"{v:.2f}", x=0.5, y=0.5, font_size=18, showarrow=False, font_color=P["primary"])],
        paper_bgcolor=P["panel"],
        plot_bgcolor=P["panel"]
    )
    return fig

def radar_construct(construct_name:str, metrics:dict):
    """
    Radar chart for CR, AVE, and (1-HTMT) as 'distinctness score'
    metrics = {'CR':x, 'AVE':y, 'HTMT':z}
    """
    CR = metrics.get("CR", 0.0)
    AVE = metrics.get("AVE", 0.0)
    HTMT = metrics.get("HTMT", 0.0)
    distinct = max(0.0, 1.0 - HTMT)  # higher better
    cats = ["Composite Reliability", "AVE", "Distinctness (1-HTMT)"]
    vals = [CR, AVE, distinct]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals, theta=cats, fill='toself', name=construct_name,
                                  line=dict(color=P["accent2"])))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        paper_bgcolor=P["panel"],
        font_color=P["primary"],
        margin=dict(l=10, r=10, t=10, b=10)
    )
    return fig

def effect_bar(paths_df: pd.DataFrame):
    """
    Bar chart for effect sizes (f²) or betas by path.
    paths_df columns: ['Path', 'Beta', 'f2', 'p']
    """
    if paths_df.empty:
        return go.Figure()
    fig = px.bar(
        paths_df, x="Path", y="f2", text="f2",
        color="f2", color_continuous_scale="Blues" if st.session_state.theme_mode=="light" else "Cividis"
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside', cliponaxis=False)
    fig.update_layout(
        paper_bgcolor=P["panel"], plot_bgcolor=P["panel"],
        font_color=P["primary"], margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="Effect Size (f²)"
    )
    return fig

def status_text(msg:str, level:str):
    css = {"pass": "good-text", "warn": "warn-text", "fail": "bad-text"}.get(level, "good-text")
    st.markdown(f"<div class='{css}'>{msg}</div>", unsafe_allow_html=True)

def export_summary_csv(rows:list[dict]):
    if not rows:
        return
    df = pd.DataFrame(rows)
    st.download_button(
        "💾 Download Summary (CSV)",
        df.to_csv(index=False).encode("utf-8"),
        file_name="SmartPLS_Results_Summary.csv",
        mime="text/csv"
    )

# ============================================================
# 6) PAGES
# ============================================================

# ----------------- HOME -----------------
if page == "🏠 Home":
    st.subheader("Welcome")
    st.markdown(
        f"""
        <div class="card">
            <p>This assistant helps interpret and report <b>PLS-SEM</b> results obtained from <b>SmartPLS</b>.</p>
            <ul>
                <li><b>Measurement Model</b>: Indicator reliability, CR (rho_c), AVE, HTMT.</li>
                <li><b>Structural Model</b>: VIF, path significance, R², f², Q² (blindfolding).</li>
                <li><b>Advanced</b>: Mediation, Moderation, MGA, IPMA, fsQCA (guidance).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        with st.expander("📘 Glossary"):
            st.markdown(
                "- **CR (rho_c)**: Composite Reliability (≥ 0.70 good)\n"
                "- **AVE**: Average Variance Extracted (≥ 0.50)\n"
                "- **HTMT**: Heterotrait–Monotrait Ratio (< 0.85 ideal; < 0.90 acceptable)\n"
                "- **VIF**: Variance Inflation Factor (< 3 ideal, < 5 acceptable)\n"
                "- **Q²**: Predictive relevance (> 0)\n"
                "- **f²**: Effect size (≥ 0.35 large; ≥ 0.15 medium; ≥ 0.02 small)"
            )
    with c2:
        with st.expander("📚 Citations / References"):
            st.markdown(
                "- Hair, J. F., Hult, G. T. M., Ringle, C. M., & Sarstedt, M. (2019). *A Primer on Partial Least Squares Structural Equation Modeling (PLS-SEM)*. Sage.\n"
                "- Sarstedt, M., Ringle, C. M., & Hair, J. F. (2022). Partial least squares structural equation modeling. *Handbook of Market Research*.\n"
                "- Henseler, J., Ringle, C. M., & Sarstedt, M. (2015). A new criterion for assessing discriminant validity in variance-based SEM. *Journal of the Academy of Marketing Science*."
            )

# ------------- MEASUREMENT MODEL -------------
elif page == "🧪 Measurement Model":
    st.subheader("Measurement Model Assessment")

    # Inputs card
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            ol = st.number_input("Outer Loading (example item)", 0.0, 1.0, 0.72, 0.01)
        with c2:
            cr = st.number_input("Composite Reliability (CR / rho_c)", 0.0, 1.0, 0.82, 0.01)
        with c3:
            ave = st.number_input("AVE", 0.0, 1.0, 0.56, 0.01)
        d1, d2 = st.columns(2)
        with d1:
            htmt = st.number_input("HTMT (pairwise)", 0.0, 1.2, 0.78, 0.01)
        with d2:
            construct = st.text_input("Construct Name (for Radar)", value="ATT")
        st.markdown("</div>", unsafe_allow_html=True)

    # Gauges
    st.markdown("#### Visual Diagnostics")
    g1, g2, g3, g4 = st.columns(4)
    with g1:
        st.plotly_chart(gauge("Outer Loading", ol, threshold=0.708, max_val=1.0, good_when_higher=True), use_container_width=True)
        status_text("≥ 0.708 ideal; 0.4–0.7 keep if CR/AVE okay; < 0.4 delete.", "pass" if ol>=0.708 else ("warn" if ol>=0.4 else "fail"))
    with g2:
        st.plotly_chart(gauge("CR (rho_c)", cr, threshold=0.70), use_container_width=True)
        status_text("≥ 0.70 indicates internal consistency.", "pass" if cr>=0.7 else ("warn" if cr>=0.6 else "fail"))
    with g3:
        st.plotly_chart(gauge("AVE", ave, threshold=0.50), use_container_width=True)
        status_text("≥ 0.50 indicates convergent validity.", "pass" if ave>=0.5 else "fail")
    with g4:
        st.plotly_chart(gauge("HTMT", htmt, threshold=0.85, max_val=1.0, good_when_higher=False), use_container_width=True)
        status_text("< 0.85 ideal; < 0.90 acceptable.", "pass" if htmt<0.85 else ("warn" if htmt<0.90 else "fail"))

    # Radar summary
    st.markdown("#### Construct Summary (Radar)")
    st.plotly_chart(radar_construct(construct, {"CR": cr, "AVE": ave, "HTMT": htmt}), use_container_width=True)

    # Export
    export_summary_csv([
        {"Metric": "Outer Loading", "Value": ol},
        {"Metric": "Composite Reliability (CR)", "Value": cr},
        {"Metric": "AVE", "Value": ave},
        {"Metric": "HTMT", "Value": htmt},
        {"Metric": "Construct", "Value": construct},
    ])

# ------------- STRUCTURAL MODEL -------------
elif page == "📈 Structural Model":
    st.subheader("Structural Model Assessment")

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        a1, a2, a3 = st.columns(3)
        with a1:
            vif = st.number_input("VIF", 0.0, 20.0, 2.4, 0.1)
        with a2:
            r2 = st.number_input("R²", 0.0, 1.0, 0.52, 0.01)
        with a3:
            q2 = st.number_input("Q²", -1.0, 1.0, 0.21, 0.01)
        st.markdown("</div>", unsafe_allow_html=True)

    # Gauges for model-level metrics
    st.markdown("#### Model-Level Diagnostics")
    h1, h2, h3 = st.columns(3)
    with h1:
        st.plotly_chart(gauge("VIF", vif, threshold=3.0, max_val=10.0, good_when_higher=False), use_container_width=True)
        status_text("< 3.0 ideal; < 5.0 acceptable.", "pass" if vif<3 else ("warn" if vif<5 else "fail"))
    with h2:
        # R² threshold is contextual; provide rule-of-thumb annotation
        st.plotly_chart(gauge("R²", r2, threshold=0.50), use_container_width=True)
        status_text("≈0.75 substantial; ≈0.50 moderate; ≈0.25 weak.", "pass" if r2>=0.5 else ("warn" if r2>=0.25 else "fail"))
    with h3:
        st.plotly_chart(gauge("Q²", q2, threshold=0.0, max_val=1.0, good_when_higher=True), use_container_width=True)
        status_text("> 0 indicates predictive relevance.", "pass" if q2>0 else "fail")

    st.markdown("#### Paths & Effect Sizes")
    st.caption("Enter a few paths (IV → DV) to visualize f² and track significance.")
    path_entries = st.text_area("Paths (CSV format: Path,Beta,f2,p)", value="PE→ATT,0.28,0.16,0.004\nEC→ATT,0.22,0.09,0.031\nTR→ATT,0.05,0.01,0.210")
    try:
        df_paths = pd.read_csv(StringIO(path_entries), header=None, names=["Path","Beta","f2","p"])
    except Exception:
        df_paths = pd.DataFrame(columns=["Path","Beta","f2","p"])

    cA, cB = st.columns([0.5, 0.5])
    with cA:
        st.plotly_chart(effect_bar(df_paths), use_container_width=True)
    with cB:
        if not df_paths.empty:
            # simple table with style cues
            styled = df_paths.copy()
            styled["Supported?"] = styled["p"].apply(lambda x: "✅ Yes" if x<0.05 else "❌ No")
            st.dataframe(styled, use_container_width=True, height=220)

    export_summary_csv(
        [{"Metric":"VIF","Value":vif},{"Metric":"R²","Value":r2},{"Metric":"Q²","Value":q2}] +
        df_paths.to_dict(orient="records")
    )

# ------------- ADVANCED -------------
elif page == "🧬 Advanced Analyses":
    st.subheader("Advanced Analyses (Guided)")

    tabs = st.tabs(["Mediation", "Moderation", "MGA", "IPMA", "fsQCA"])
    with tabs[0]:
        st.markdown("**Mediation:** Enter p-values of indirect and direct effects.")
        c1, c2 = st.columns(2)
        with c1:
            p_ind = st.number_input("p (Indirect: IV→MED→DV)", 0.0, 1.0, 0.012, 0.001, format="%.3f")
        with c2:
            p_dir = st.number_input("p (Direct: IV→DV)", 0.0, 1.0, 0.08, 0.001, format="%.3f")
        if p_ind < 0.05 and p_dir >= 0.05:
            status_text("Full mediation supported (indirect significant; direct not).", "pass")
        elif p_ind < 0.05 and p_dir < 0.05:
            status_text("Partial mediation supported (both significant).", "pass")
        else:
            status_text("No mediation (indirect effect not significant).", "fail")

    with tabs[1]:
        st.markdown("**Moderation:** Enter the p-value of the interaction term (e.g., MOD*IV→DV).")
        p_mod = st.number_input("p (Interaction term)", 0.0, 1.0, 0.041, 0.001, format="%.3f")
        status_text("Moderation supported." if p_mod<0.05 else "No moderation.", "pass" if p_mod<0.05 else "fail")

    with tabs[2]:
        st.markdown("**MGA:** Enter permutation p-value for group difference in a specific path.")
        c1, c2 = st.columns([0.6, 0.4])
        with c1:
            path_name = st.text_input("Path (e.g., PE→ATT)", "PE→ATT")
        with c2:
            p_mga = st.number_input("p (Permutation)", 0.0, 1.0, 0.033, 0.001, format="%.3f")
        status_text(f"MGA difference on {path_name} is significant." if p_mga<0.05 else f"No significant MGA difference on {path_name}.",
                    "pass" if p_mga<0.05 else "fail")

    with tabs[3]:
        st.markdown("**IPMA:** Interpret quadrants: Q1 (High Importance/High Performance) – maintain; Q4 (High/Low) – prioritize improvement.")
        grid = pd.DataFrame({
            "Quadrant":["Q1","Q2","Q3","Q4"],
            "Importance":["High","Low","Low","High"],
            "Performance":["High","High","Low","Low"],
            "Action":["Keep up","Low priority","Lowest priority","Fix urgently"]
        })
        st.dataframe(grid, use_container_width=True, height=200)

    with tabs[4]:
        st.markdown("**fsQCA:** Enter Consistency and Coverage of a solution recipe.")
        c1, c2 = st.columns(2)
        with c1:
            cons = st.number_input("Consistency", 0.0, 1.0, 0.86, 0.01)
        with c2:
            covg = st.number_input("Coverage", 0.0, 1.0, 0.48, 0.01)
        if cons >= 0.80:
            status_text(f"Valid recipe (Consistency {cons:.2f}; Coverage {covg:.2f}).", "pass")
        else:
            status_text(f"Insufficient consistency ({cons:.2f}); not reliable.", "fail")

# ------------- OPTIONAL UPLOAD/PARSE -------------
elif page == "📦 Upload & Parse (Optional)":
    st.subheader("Upload SmartPLS Outputs (CSV) to Pre-Fill Checks")
    st.caption("If you export tables from SmartPLS as CSV (e.g., Outer Loadings, Reliability, HTMT), upload and we will preview them here.")

    uploaded = st.file_uploader("Upload one or more CSV files", type=["csv"], accept_multiple_files=True)
    if uploaded:
        for file in uploaded:
            st.markdown(f"**{file.name}**")
            try:
                df = pd.read_csv(file)
                st.dataframe(df, use_container_width=True, height=220)
            except Exception as e:
                st.error(f"Could not parse {file.name}: {e}")

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    f"""
    <hr>
    <div class="footer">
        © {datetime.datetime.now().year} Mahbub Hassan · Department of Civil Engineering, Chulalongkorn University ·
        <a href="https://www.bdeshi-lab.org/" target="_blank" style="color:{P["muted"]}; text-decoration:none; font-weight:600;">
            B'Deshi Emerging Research Lab
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
