# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import os
from optimizer import simulate_demand, simulate_supply, calculate_financials

st.set_page_config(page_title="E-Commerce Strategic Price Optimizer", layout="wide", page_icon="💹")

# ----------------------------------------------------------------------------------
# THEME / ANIMATION LAYER (presentation only — no business logic lives here)
# ----------------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
  --ink: #0A0E1A;
  --panel: #121830;
  --panel-hover: #1A2240;
  --border-subtle: rgba(255,255,255,0.09);
  --gold: #F0B429;
  --green: #00D9A3;
  --red: #FF5C7A;
  --cyan: #5CC8FF;
  --paper: #E8ECF4;
  --mist: #8A93AC;
}

[data-testid="stAppViewContainer"] { background: var(--ink) !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 1.6rem; max-width: 1400px; }

h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.01em; color: var(--paper); }
body, p, span, label, div { font-family: 'Inter', sans-serif; }

/* ---------- Hero ---------- */
.hero-title { font-family:'Space Grotesk',sans-serif; font-size:2.05rem; font-weight:700; line-height:1.18; color:var(--paper); margin-bottom:0.15rem; }
.hero-title .accent { background: linear-gradient(90deg, var(--gold), var(--green)); -webkit-background-clip:text; background-clip:text; color:transparent; }
.hero-caption { font-family:'IBM Plex Mono', monospace; font-size:0.76rem; color:var(--mist); letter-spacing:0.03em; text-transform:uppercase; margin-top:-0.1rem; }

.live-dot { display:inline-block; width:9px; height:9px; border-radius:50%; background:var(--green); margin-right:9px; box-shadow:0 0 0 0 rgba(0,217,163,0.6); animation:pulseDot 1.8s infinite; vertical-align:middle; }
@keyframes pulseDot { 0%{box-shadow:0 0 0 0 rgba(0,217,163,0.55);} 70%{box-shadow:0 0 0 9px rgba(0,217,163,0);} 100%{box-shadow:0 0 0 0 rgba(0,217,163,0);} }

/* ---------- Alerts ---------- */
[data-testid="stAlert"] { background: var(--panel) !important; border:1px solid var(--border-subtle) !important; border-radius:12px !important; }
[data-testid="stAlert"] p { color: var(--paper) !important; font-family:'Inter', sans-serif; }

/* ---------- Form panel ---------- */
[data-testid="stForm"] {
  background: var(--panel);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 1.5rem 1.35rem 1.1rem;
  transition: box-shadow 0.3s ease;
}
[data-testid="stForm"]:hover { box-shadow: 0 0 0 1px rgba(240,180,41,0.18); }
[data-testid="stForm"] label { color: var(--mist) !important; font-size:0.82rem !important; font-weight:500 !important; }

/* ---------- Native bordered containers (cards) ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--panel) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 16px !important;
  transition: border-color 0.25s ease;
  animation: fadeInUp 0.45s ease-out both;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: rgba(240,180,41,0.32) !important; }

/* ---------- Tabs ---------- */
[data-testid="stTabs"] button[role="tab"] { font-family:'Space Grotesk',sans-serif; color:var(--mist); font-size:0.92rem; }
[data-testid="stTabs"] button[aria-selected="true"] { color: var(--paper) !important; border-bottom-color: var(--gold) !important; }
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background-color: var(--gold) !important; }

/* ---------- Metrics ---------- */
[data-testid="stMetric"] {
  background: var(--panel-hover);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 0.85rem 1rem 0.7rem;
  animation: fadeInUp 0.5s ease-out both;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
[data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 10px 26px rgba(0,0,0,0.4); border-color: rgba(240,180,41,0.3); }
[data-testid="stMetricLabel"] { color: var(--mist) !important; font-size:0.72rem !important; text-transform:uppercase; letter-spacing:0.05em; }
[data-testid="stMetricValue"] { font-family:'IBM Plex Mono', monospace !important; color: var(--paper) !important; text-shadow: 0 0 16px rgba(240,180,41,0.16); }
[data-testid="stMetricDelta"] { font-family:'IBM Plex Mono', monospace !important; }

[data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(1) [data-testid="stMetric"] { animation-delay: 0s; }
[data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stMetric"] { animation-delay: 0.08s; }
[data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(3) [data-testid="stMetric"] { animation-delay: 0.16s; }

@keyframes fadeInUp { from { opacity:0; transform: translateY(14px); } to { opacity:1; transform: translateY(0); } }

/* ---------- Buttons ---------- */
[data-testid="stFormSubmitButton"] button,
[data-testid="stBaseButton-secondaryFormSubmit"] button,
.stButton button {
  background: linear-gradient(90deg, var(--gold), #ffce5c) !important;
  color: #1A1404 !important;
  font-weight:600 !important;
  border: none !important;
  border-radius: 10px !important;
  transition: transform 0.15s ease, box-shadow 0.2s ease !important;
}
[data-testid="stFormSubmitButton"] button:hover,
[data-testid="stBaseButton-secondaryFormSubmit"] button:hover,
.stButton button:hover {
  transform: translateY(-2px) scale(1.01);
  box-shadow: 0 12px 26px rgba(240,180,41,0.35) !important;
}

/* ---------- Price Position Spectrum (signature element) ---------- */
.gauge-panel { margin-top: 0.4rem; padding: 0.2rem 0.1rem 0.1rem; }
.gauge-title { font-family:'Space Grotesk',sans-serif; font-size:1rem; font-weight:600; color:var(--paper); margin-bottom:0.7rem; }
.gauge-sub { font-family:'IBM Plex Mono', monospace; font-size:0.7rem; color:var(--mist); font-weight:400; margin-left:6px; }
.gauge-row { display:flex; align-items:center; gap:0.7rem; margin:0.55rem 0; opacity:0; animation: fadeInUp 0.5s ease-out forwards; }
.gauge-row-label { width:88px; flex-shrink:0; font-family:'IBM Plex Mono', monospace; font-size:0.72rem; color:var(--mist); text-align:right; }
.gauge-track-mini { position:relative; flex:1; height:8px; border-radius:4px; background: rgba(255,255,255,0.07); }
.gauge-marker-mini { position:absolute; top:50%; width:15px; height:15px; border-radius:50%; transform:translate(-50%,-50%) scale(0.4); border:2px solid var(--ink); animation: markerPop 0.5s ease-out 0.1s forwards; opacity:0; }
@keyframes markerPop { from { opacity:0; transform: translate(-50%,-50%) scale(0.3); } to { opacity:1; transform: translate(-50%,-50%) scale(1); } }
.gauge-marker-mini.gold { background: var(--gold); box-shadow:0 0 12px rgba(240,180,41,0.65); }
.gauge-marker-mini.green { background: var(--green); box-shadow:0 0 12px rgba(0,217,163,0.65); }
.gauge-marker-mini.red { background: var(--red); box-shadow:0 0 12px rgba(255,92,122,0.65); }
.gauge-value { width:78px; flex-shrink:0; font-family:'IBM Plex Mono', monospace; font-size:0.78rem; font-weight:500; }
.gauge-value.gold { color: var(--gold); }
.gauge-value.green { color: var(--green); }
.gauge-value.red { color: var(--red); }

hr { border-color: var(--border-subtle) !important; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="hero-title">AI-Powered E-Commerce <span class="accent">Price Prediction</span> '
    '&amp; Strategic Market Simulation</div>'
    '<div class="hero-caption">Course Project for Simulation and Modelling (IT3016) '
    '&middot; Advanced Optimization Sandbox</div>',
    unsafe_allow_html=True
)
st.markdown("---")

encoder_path = 'models/label_encoder.pkl'

ui_categories = [
    "Electronics & Gadgets",
    "Clothing, Shoes & Fashion",
    "Home, Kitchen & Furniture",
    "Beauty & Personal Care",
    "Automotive & Industrial",
    "Sports, Fitness & Outdoors",
    "Books, Music & Entertainment",
    "Office Supplies & Stationary",
    "Toys, Kids & Baby",
    "Other Miscellaneous"
]

def map_ui_to_raw_category(selected_ui_cat, dataset_classes):
    keyword_map = {
        "Electronics & Gadgets": ["electr", "audio", "video", "camera", "phone", "tv", "comp", "access"],
        "Clothing, Shoes & Fashion": ["apparel", "cloth", "shoe", "watch", "jewel", "fash", "bag"],
        "Home, Kitchen & Furniture": ["home", "kitchen", "furnit", "appliances", "decor", "bed"],
        "Beauty & Personal Care": ["beaut", "care", "health", "groom", "makeup"],
        "Automotive & Industrial": ["auto", "car", "motor", "indust", "tool"],
        "Sports, Fitness & Outdoors": ["sport", "fit", "out", "camp", "cycl"],
        "Books, Music & Entertainment": ["book", "music", "movie", "game", "toy"],
        "Office Supplies & Stationary": ["off", "suppl", "station", "pen", "paper"],
        "Toys, Kids & Baby": ["toy", "kid", "baby", "child"]
    }
    keywords = keyword_map.get(selected_ui_cat, [])
    for raw_cat in dataset_classes:
        for kw in keywords:
            if kw in raw_cat.lower():
                return raw_cat
    return dataset_classes[0]

def render_price_spectrum(min_price, max_price, baseline_price, optimal_price, your_price, is_profitable):
    """Purely presentational: positions three already-computed prices on a visual scale."""
    rng = max(max_price - min_price, 1e-6)

    def pct(v):
        return max(0.0, min(100.0, (v - min_price) / rng * 100))

    pct_baseline, pct_optimal, pct_your = pct(baseline_price), pct(optimal_price), pct(your_price)
    your_class = "green" if is_profitable else "red"

    html = f"""
    <div class="gauge-panel">
        <div class="gauge-title">🎯 Price Position Spectrum
            <span class="gauge-sub">range ${min_price:.2f} – ${max_price:.2f}</span>
        </div>
        <div class="gauge-row" style="animation-delay:0s;">
            <span class="gauge-row-label">ML Baseline</span>
            <div class="gauge-track-mini">
                <div class="gauge-marker-mini gold" style="left:{pct_baseline:.2f}%;" title="ML Recommended Price: ${baseline_price:.2f}"></div>
            </div>
            <span class="gauge-value gold">${baseline_price:.2f}</span>
        </div>
        <div class="gauge-row" style="animation-delay:0.12s;">
            <span class="gauge-row-label">Optimal Peak</span>
            <div class="gauge-track-mini">
                <div class="gauge-marker-mini green" style="left:{pct_optimal:.2f}%;" title="Theoretical Optimal Price: ${optimal_price:.2f}"></div>
            </div>
            <span class="gauge-value green">${optimal_price:.2f}</span>
        </div>
        <div class="gauge-row" style="animation-delay:0.24s;">
            <span class="gauge-row-label">Your Price</span>
            <div class="gauge-track-mini">
                <div class="gauge-marker-mini {your_class}" style="left:{pct_your:.2f}%;" title="Your Selected Price: ${your_price:.2f}"></div>
            </div>
            <span class="gauge-value {your_class}">${your_price:.2f}</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

if os.path.exists(encoder_path):
    label_encoder = joblib.load(encoder_path)
    dataset_classes = list(label_encoder.classes_)
else:
    st.error("❌ Model artifacts missing! Please run 'python model.py' in your terminal first.")
    dataset_classes = ["Electronics"]

# App Column Splits
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📋 Simulation Parameters")

    with st.form("simulation_form"):
        selected_ui_category = st.selectbox("Product Category", ui_categories)
        category = map_ui_to_raw_category(selected_ui_category, dataset_classes)

        unit_cost = st.number_input("Wholesale Unit Cost Price ($)", min_value=1.0, value=50.0, step=5.0)

        selected_model_name = st.selectbox(
            "Predictive Machine Learning Engine",
            ["XGBoost Regressor", "Random Forest", "Linear Regression"]
        )

        market_mode = st.selectbox(
            "Amazon Competitive Climate",
            ["Balanced Market", "High Demand (Sellers' Market)", "High Competition (Buyers' Market)"]
        )

        elasticity = st.slider("Price Elasticity of Demand (ε)", 0.5, 3.0, 1.05)
        sim_price_input = st.number_input("Your Custom Target Selling Price ($)", min_value=float(unit_cost), value=float(unit_cost * 1.5), step=5.0)

        st.markdown(" ")
        submit_button = st.form_submit_button(label="Run Market Simulation 🚀", use_container_width=True)

base_demand = 400

with col2:
    if submit_button or 'initialized' not in st.session_state:
        st.session_state['initialized'] = True

        if os.path.exists(encoder_path):
            category_encoded = label_encoder.transform([category])[0]
        else:
            category_encoded = 0

        input_features = pd.DataFrame([[category_encoded, unit_cost]], columns=['category_encoded', 'wholesale_cost'])

        model_file_map = {
            "XGBoost Regressor": "xgboost_market_model.pkl",
            "Random Forest": "random_forest_model.pkl",
            "Linear Regression": "linear_regression_model.pkl"
        }

        model_path = f"models/{model_file_map[selected_model_name]}"
        if os.path.exists(model_path):
            active_model = joblib.load(model_path)
            predicted_baseline_price = max(unit_cost * 1.1, float(active_model.predict(input_features)[0]))
        else:
            predicted_baseline_price = unit_cost * 1.5

        sim_demand = simulate_demand(base_demand, predicted_baseline_price, sim_price_input, elasticity, market_mode)
        revenue, profit = calculate_financials(sim_price_input, sim_demand, unit_cost)

        price_range = np.linspace(unit_cost + 1, max(predicted_baseline_price * 2.5, sim_price_input * 1.5), 100)

        demand_series = []
        profit_series = []
        for p in price_range:
            d = simulate_demand(base_demand, predicted_baseline_price, p, elasticity, market_mode)
            _, pr = calculate_financials(p, d, unit_cost)
            demand_series.append(d)
            profit_series.append(pr)

        max_profit_idx = np.argmax(profit_series)
        optimal_price = price_range[max_profit_idx]
        optimal_profit = profit_series[max_profit_idx]

        st.toast(f"Simulation complete — {sim_demand} units projected", icon="📡")

        tab_results, tab_profit, tab_demand = st.tabs(["📊 Results & Price Position", "📈 Profit Curve", "📦 Demand Curve"])

        with tab_results:
            with st.container(border=True):
                st.markdown(
                    '<h3><span class="live-dot"></span>Optimization Inference Evaluation Results</h3>',
                    unsafe_allow_html=True
                )

                r_col1, r_col2 = st.columns(2)
                r_col1.metric("ML Recommended Market Price", f"${predicted_baseline_price:.2f}")
                r_col2.metric("Your Selected Test Price", f"${sim_price_input:.2f}", delta=f"${sim_price_input - predicted_baseline_price:.2f} vs Base")

                st.markdown("---")

                m1, m2, m3 = st.columns(3)
                m1.metric("Projected Orders Volume", f"{sim_demand} units")
                m2.metric("Estimated Gross Revenue", f"${revenue:,.2f}")

                if profit >= 0:
                    m3.metric("Projected Net Profit Flow", f"${profit:,.2f}", delta="Profitable State")
                else:
                    m3.metric("Projected Net Profit Flow", f"${profit:,.2f}", delta="Net Loss Zone", delta_color="inverse")

                st.markdown("---")

                render_price_spectrum(
                    min_price=float(price_range.min()),
                    max_price=float(price_range.max()),
                    baseline_price=predicted_baseline_price,
                    optimal_price=float(optimal_price),
                    your_price=sim_price_input,
                    is_profitable=(profit >= 0)
                )

        with tab_profit:
            with st.container(border=True):
                st.markdown("#### 📊 User-Friendly Financial Optimization Curves")

                fig_profit = go.Figure()

                fig_profit.add_trace(go.Scatter(
                    x=price_range, y=profit_series,
                    name="Net Profit Expectation Floor",
                    line=dict(color="#00D9A3", width=4, shape="spline"),
                    fill='tozeroy', fillcolor='rgba(0, 217, 163, 0.12)'
                ))

                fig_profit.add_trace(go.Scatter(
                    x=[optimal_price], y=[optimal_profit],
                    mode="markers+text",
                    name="Theoretical Optimal Peak Price",
                    text=[f"Optimal Max: ${optimal_profit:,.0f} at ${optimal_price:.2f}"],
                    textposition="top center",
                    textfont=dict(color="#F0B429", family="IBM Plex Mono, monospace"),
                    marker=dict(color="#F0B429", size=15, symbol="star", line=dict(color="#0A0E1A", width=1))
                ))

                fig_profit.add_vline(
                    x=sim_price_input,
                    line_width=2,
                    line_dash="dash",
                    line_color="#5CC8FF"
                )

                fig_profit.add_trace(go.Scatter(
                    x=[sim_price_input], y=[profit],
                    mode="markers",
                    name="Your Selected Price State",
                    marker=dict(color="#5CC8FF", size=14, symbol="circle", line=dict(color="#0A0E1A", width=1))
                ))

                fig_profit.update_layout(
                    title="Strategic Financial Yield Curve Optimization Envelope",
                    xaxis_title="Simulated Selling Price Configuration ($)",
                    yaxis_title="Expected Project Net Profit ($)",
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(255,255,255,0.02)",
                    font=dict(family="IBM Plex Mono, monospace", color="#E8ECF4", size=12),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    hovermode="x unified",
                    transition=dict(duration=600, easing="cubic-in-out"),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.07)", rangeslider=dict(visible=True, thickness=0.06, bgcolor="rgba(255,255,255,0.04)")),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.07)")
                )

                st.plotly_chart(fig_profit, use_container_width=True)

        with tab_demand:
            with st.container(border=True):
                st.markdown("#### 📦 Projected Demand Response Curve")

                fig_demand = go.Figure()

                fig_demand.add_trace(go.Scatter(
                    x=price_range, y=demand_series,
                    name="Projected Demand",
                    line=dict(color="#5CC8FF", width=4, shape="spline"),
                    fill='tozeroy', fillcolor='rgba(92, 200, 255, 0.12)'
                ))

                fig_demand.add_vline(
                    x=sim_price_input,
                    line_width=2,
                    line_dash="dash",
                    line_color="#F0B429"
                )

                fig_demand.add_trace(go.Scatter(
                    x=[sim_price_input], y=[sim_demand],
                    mode="markers",
                    name="Your Selected Price State",
                    marker=dict(color="#F0B429", size=14, symbol="circle", line=dict(color="#0A0E1A", width=1))
                ))

                fig_demand.update_layout(
                    title="Price Sensitivity → Order Volume Response",
                    xaxis_title="Simulated Selling Price Configuration ($)",
                    yaxis_title="Projected Demand (units)",
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(255,255,255,0.02)",
                    font=dict(family="IBM Plex Mono, monospace", color="#E8ECF4", size=12),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    hovermode="x unified",
                    transition=dict(duration=600, easing="cubic-in-out"),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.07)")
                )

                st.plotly_chart(fig_demand, use_container_width=True)

    else:
        st.info("💡 Adjust your product features, select your predictive engine algorithm in the left panel, and click 'Run Market Simulation 🚀' to render your dashboard.")
