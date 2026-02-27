import streamlit as st
import pandas as pd
import sys
import os

# Add the current directory to sys.path to find the engine
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from reputex_engine import ReputeXEngine

st.set_page_config(
    page_title="ReputeX - Clinical Enterprise",
    page_icon="medical_services",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS to match the clinical theme
st.markdown("""
<style>
    :root {
        --primary-color: #0F4C75;
        --secondary-color: #0D9488;
        --background-light: #F8F9FA;
        --text-main: #1A202C;
        --border-color: #E2E8F0;
    }
    
    .main {
        background-color: var(--background-light);
    }
    
    [data-testid="stSidebar"] {
        background-color: var(--primary-color);
        color: white;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        background-color: #0a3655;
        color: white;
    }
    
    .kpi-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid var(--border-color);
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    .kpi-title {
        color: #64748B;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .kpi-value {
        color: var(--text-main);
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }
    
    .glass-panel {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-color);
        border-radius: 1rem;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("### ReputeX")
    st.markdown("Clinical Enterprise")
    st.divider()
    page = st.radio("Navigation", ["Network Command Center", "Crisis Modeler", "Clinic Intelligence"])
    
    st.divider()
    st.markdown("### System Status")
    st.success("Core Engine: Online")
    st.info("API Latency: 42ms")

if page == "Network Command Center":
    st.subheader("Network Command Center")
    
    tab1, tab2 = st.tabs(["Overview", "Target Simulation"])
    
    with tab1:
        cols = st.columns(6)
        kpis = [
            ("Net Avg", "4.8", "+0.2%"),
            ("Vol", "1,240", "+5.4%"),
            ("MoM Growth", "+12%", "+12%"),
            ("Risk Score", "Low", "-2pts"),
            ("Loc < 4.2", "3", "0"),
            ("Target %", "92%", "+1.5%")
        ]
        
        for col, (title, value, delta) in zip(cols, kpis):
            with col:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">{title}</div>
                    <div class="kpi-value">{value}</div>
                    <div style="color: #0D9488; font-size: 0.7rem; font-weight: 500; margin-top: 0.2rem;">{delta}</div>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("---")
        
        # Charts Section
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("### Network Reputation Trend (12 Mo)")
            # Mock trend data
            st.line_chart([4.5, 4.4, 4.6, 4.5, 4.7, 4.8, 4.7, 4.9, 4.8, 4.8, 4.9, 4.8])
            
        with c2:
            st.markdown("### Review Velocity by Region")
            # Create a dataframe for the bar chart
            velocity_data = pd.DataFrame({
                "Region": ["East", "West", "North", "South", "Metro"],
                "Volume": [60, 45, 70, 30, 55]
            })
            st.bar_chart(velocity_data.set_index("Region"))

        st.markdown("---")
        
        # Location Performance Table
        st.markdown("### Location Performance")
        data = [
            ["Northwell Valley Stream", "Valley Stream, NY", 4.9, 342, "+8.2%", "Healthy"],
            ["Downtown Urgent Care", "New York, NY", 3.6, 89, "-12.4%", "Risk"],
            ["Sinai Pediatric Center", "Brooklyn, NY", 4.2, 156, "0.0%", "Warning"],
            ["Queens Surgical Unit", "Queens, NY", 4.7, 512, "+1.2%", "Healthy"],
            ["Manhasset Cardiology", "Manhasset, NY", 4.5, 203, "+3.4%", "Healthy"]
        ]
        df = pd.DataFrame(data, columns=["Location Name", "City", "Rating", "Vol", "MoM %", "Status"])
        st.table(df)
    
    with tab2:
        st.markdown("### Target Rating Strategy")
        st.write("Calculate what it takes to reach your reputation goals.")
        
        t_total = st.number_input("Current Total Reviews (T)", min_value=1, value=320, key="t_total")
        r_avg = st.number_input("Current Avg Rating (R)", min_value=1.0, max_value=5.0, value=4.4, step=0.1, key="r_avg")
        d_target = st.number_input("Desired Rating (D)", min_value=1.0, max_value=5.0, value=4.9, step=0.1, key="d_target")
        
        strategy_mode = st.toggle("Enable Manual Star Strategy Mix", value=False)
        
        star_mix_val = 5.0
        if strategy_mode:
            st.write("Configure Target Star Mix:")
            p5 = st.slider("5★ Percentage", 0, 100, 80)
            p4 = st.slider("4★ Percentage", 0, 100 - p5, 15)
            p3 = 100 - p5 - p4
            st.info(f"Mix: {p5}% 5★, {p4}% 4★, {p3}% 3★")
            star_mix_val = ReputeXEngine.calculate_weighted_star_value({5: p5/100, 4: p4/100, 3: p3/100})
            st.write(f"Weighted Star Value (WSV): {star_mix_val:.2f}")

        if st.button("Calculate Requirements"):
            req_x = ReputeXEngine.solve_for_additional_reviews(t_total, r_avg, d_target, star_value=star_mix_val)
            
            if req_x == float('inf'):
                st.error("Target rating is impossible with current star mix.")
            else:
                st.success(f"Required New Reviews: {req_x}")
                st.metric("New Total Volume", f"{int(t_total + req_x)}")
                
                # Module 3 integration
                velocity = st.number_input("Avg Reviews per Month", min_value=0.1, value=13.3)
                months = ReputeXEngine.predict_time(req_x, velocity)
                st.write(f"Estimated Time: **{months:.1f} months** ({months/12:.1f} years)")
                
                # Module 6 & 7
                age = st.number_input("Business Age (Months)", min_value=1, value=24)
                difficulty = ReputeXEngine.calculate_difficulty_score(req_x, age)
                st.write(f"Difficulty Score: {int(difficulty)}")
                
                rec = ReputeXEngine.get_strategy_recommendation(req_x, months, d_target)
                st.info(f"ORM Advisor: {rec}")

elif page == "Crisis Modeler":
    st.subheader("Crisis Modeler")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Scenario Builder")
        event_type = st.selectbox("Impact Event", [
            "Viral Social Media Incident",
            "Policy Change Backlash",
            "Hygiene/Safety Report",
            "Staff Misconduct",
            "Competitor Smear Campaign"
        ])
        
        neg_influx = st.number_input("Projected Negative Influx (1-star reviews)", min_value=1, value=50)
        duration = st.slider("Impact Duration (Hours)", 24, 168, 48)
        
        st.markdown("---")
        st.markdown("### Current Health")
        curr_reviews = st.number_input("Current Total Reviews", min_value=1, value=320)
        curr_rating = st.number_input("Current Average Rating", min_value=1.0, max_value=5.0, value=4.5, step=0.1)
        
        if st.button("Run Simulation"):
            # Simulation Logic
            new_rating = ReputeXEngine.simulate_negative_impact(curr_reviews, curr_rating, neg_influx, 1.0)
            st.session_state['new_rating'] = new_rating
            st.session_state['simulation_run'] = True
            
    with col2:
        if st.session_state.get('simulation_run', False):
            nr = st.session_state['new_rating']
            drop = curr_rating - nr
            
            st.markdown(f"""
            <div style="background-color: white; border: 1px solid #E2E8F0; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 24px rgba(46, 139, 133, 0.08);">
                <div style="color: #E68A8A; font-weight: bold; margin-bottom: 0.5rem;">Projected Impact</div>
                <div style="display: flex; align-items: baseline; gap: 1rem;">
                    <span style="font-size: 3.5rem; font-weight: bold; color: #1A2F2D;">{nr:.1f}</span>
                    <span style="background-color: rgba(230, 138, 138, 0.1); color: #E68A8A; padding: 0.25rem 0.5rem; rounded-full; font-size: 0.8rem; font-weight: bold;">-{drop:.1f} Drop</span>
                </div>
                <div style="color: #E68A8A; font-size: 0.8rem; margin-top: 1rem;">Warning: falls below critical threshold.</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Impact Trajectory")
            # Mock recovery chart
            st.line_chart([curr_rating, nr, nr + 0.1, nr + 0.2, nr + 0.3, curr_rating])
            
            # Recovery Insight
            req_5_star = ReputeXEngine.solve_for_additional_reviews(curr_reviews + neg_influx, nr, curr_rating)
            st.info(f"Recovery Timeline: It will take {req_5_star} consistent 5-star reviews to recover to {curr_rating} rating.")
        else:
            st.info("Configure the scenario and click 'Run Simulation' to see projected impact.")

elif page == "Clinic Intelligence":
    st.subheader("Clinic Intelligence Unit /// TERMINAL v2.4")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("""
        <div style="background-color: #1E293B; color: white; padding: 1.5rem; border-radius: 4px; border-left: 4px solid #F43F5E;">
            <div style="font-size: 0.7rem; font-family: monospace; color: #94A3B8;">REPUTATION DIFFICULTY</div>
            <div style="font-size: 1.2rem; font-weight: bold; color: #F43F5E; margin-top: 0.2rem;">HARD (82/100)</div>
            <div style="font-size: 0.7rem; color: #94A3B8; margin-top: 0.5rem;">High volume saturation. Requires 2.4x velocity to impact rating.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Deep Telemetry")
        st.metric("Aggregate Score", "4.7", "Composite")
        
        st.markdown("### Command Matrix")
        st.button("Simulate Growth", key="sim_growth")
        st.button("Simulate Crisis", key="sim_crisis")
        st.button("Set Target", key="set_target")
        
    with c2:
        st.markdown("### Live Sentiment Stream")
        reviews = [
            {"user": "Sarah Jenkins", "star": 5, "text": "I came in for a sprained ankle. The wait time was surprisingly short and Dr. Smith was extremely thorough."},
            {"user": "Mike T.", "star": 2, "text": "Normally I like this place, but today the front desk staff was incredibly rude. The billing process is confusing."},
            {"user": "Elena R.", "star": 5, "text": "Quick and efficient. The nurse was very kind to my son."}
        ]
        
        for rev in reviews:
            with st.container():
                st.markdown(f"**{rev['user']}** {'⭐' * rev['star']}")
                st.write(rev['text'])
                st.divider()
