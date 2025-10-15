import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="Work Hours Tracker",
    page_icon="⏰",
    layout="wide"
)

# Professional Black & White CSS
st.markdown("""
    <style>
    /* Global styling */
    .main {
        background-color: #ffffff;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: white;
        padding: 30px;
        text-align: center;
        border-radius: 0px;
        margin: -60px -60px 20px -60px;
        border-bottom: 3px solid #000000;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 10px 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: #f5f5f5;
        border-bottom: 2px solid #cccccc;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: #f5f5f5;
        border-radius: 0px;
        padding: 0px 30px;
        font-size: 16px;
        font-weight: 500;
        color: #333333;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        border-bottom: 3px solid #000000;
        color: #000000;
    }
    
    /* Metric cards styling */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        color: #000000;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #666666;
        font-size: 14px;
        font-weight: 500;
    }
    
    [data-testid="metric-container"] {
        background: #f9f9f9;
        padding: 20px;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Form inputs styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTimeInput > div > div > input,
    .stDateInput > div > div > input {
        border: 2px solid #cccccc;
        border-radius: 6px;
        padding: 12px;
        font-size: 14px;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #000000;
        box-shadow: 0 0 0 1px #000000;
    }
    
    /* Disabled input styling */
    .stTextInput > div > div > input:disabled {
        background-color: #f5f5f5;
        color: #666666;
        cursor: not-allowed;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: #000000;
        color: white;
        border: none;
        padding: 15px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 6px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: #333333;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Section headers */
    h2 {
        color: #000000;
        font-weight: 700;
        margin-bottom: 30px;
    }
    
    h3 {
        color: #000000;
        font-weight: 600;
        margin: 30px 0 20px 0;
    }
    
    /* Divider */
    hr {
        margin: 30px 0;
        border: none;
        height: 1px;
        background: #e0e0e0;
    }
    
    /* Table styling */
    .dataframe {
        font-size: 14px;
    }
    
    .dataframe th {
        background-color: #000000 !important;
        color: white !important;
        font-weight: 600;
        padding: 15px !important;
    }
    
    .dataframe td {
        padding: 15px !important;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .dataframe tbody tr:hover {
        background-color: #f5f5f5;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #f0f0f0;
        color: #000000;
        border-left: 4px solid #000000;
        padding: 15px;
        border-radius: 6px;
    }
    
    /* Overview stat cards */
    .stat-card {
        background: #f9f9f9;
        color: #000000;
        padding: 25px;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stat-card h4 {
        font-size: 14px;
        margin-bottom: 10px;
        color: #666666;
        font-weight: 500;
    }
    
    .stat-card .number {
        font-size: 32px;
        font-weight: 700;
        color: #000000;
    }
    
    /* Date display styling */
    .current-date-display {
        background: #f5f5f5;
        padding: 15px;
        border-radius: 6px;
        border: 2px solid #e0e0e0;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .current-date-display h3 {
        margin: 0;
        color: #000000;
        font-size: 18px;
    }
    
    .current-date-display p {
        margin: 5px 0 0 0;
        color: #666666;
        font-size: 14px;
    }
    
    /* Info box styling */
    .info-box {
        background: #f5f5f5;
        padding: 12px;
        border-radius: 6px;
        border-left: 4px solid #666666;
        margin-bottom: 15px;
        color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

# PERMANENT SETTINGS - DO NOT CHANGE
TEAM_NAME = "Digital Engineering"
MANAGER_NAME = "H.Patricia"

# Initialize session state for storing records
if 'records' not in st.session_state:
    st.session_state.records = []

# Load existing records from file if available
def load_records():
    if os.path.exists('work_records.json'):
        with open('work_records.json', 'r') as f:
            return json.load(f)
    return []

# Save records to file
def save_records(records):
    with open('work_records.json', 'w') as f:
        json.dump(records, f, indent=2)

# Calculate work duration considering breaks
def calculate_work_hours(start_time, end_time, break_minutes):
    if start_time and end_time:
        duration = end_time - start_time
        total_minutes = duration.total_seconds() / 60
        work_minutes = total_minutes - break_minutes
        return max(0, work_minutes / 60)  # Return hours
    return 0

# Custom header
st.markdown('''
    <div class="main-header">
        <h1>⏰ Work Hours Tracking System</h1>
        <p>Digital Engineering Team - Manager: H.Patricia</p>
    </div>
''', unsafe_allow_html=True)

# Create tabs
tab1, tab2 = st.tabs(["📝 Log Work Hours", "📊 View Records"])

# Tab 1: Input Form
with tab1:
    st.markdown("## Log Your Work Hours")
    
    # Auto-filled current date display
    today = datetime.now()
    st.markdown(f"""
        <div class="current-date-display">
            <h3>📅 Today's Date: {today.strftime('%B %d, %Y')}</h3>
            <p>{today.strftime('%A')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Use today's date automatically
    work_date = today.date()
    
    # Display permanent team and manager info
    st.markdown(f"""
        <div class="info-box">
            <strong>Team:</strong> {TEAM_NAME} | <strong>Manager:</strong> {MANAGER_NAME}
        </div>
    """, unsafe_allow_html=True)
    
    # Employee name input
    employee_name = st.text_input(
        "👤 Your Name",
        placeholder="Enter your full name",
        help="Type your name to track your work hours"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Start time
        start_time = st.time_input(
            "Start Working ⏰",
            value=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
            help="When did you start working? (You can type the exact time)",
            step=60  # 1 minute steps
        )
        
        # Break duration
        break_duration = st.number_input(
            "Break Duration (minutes) ☕",
            min_value=0,
            max_value=240,
            value=30,
            step=1,
            help="Total break time in minutes (enter any number)"
        )
    
    with col2:
        # End time
        end_time = st.time_input(
            "Finish Working 🏁",
            value=datetime.now().replace(hour=17, minute=0, second=0, microsecond=0),
            help="When did you finish working? (You can type the exact time)",
            step=60  # 1 minute steps
        )
    
    # Combine date and time for calculation
    start_datetime = datetime.combine(work_date, start_time)
    end_datetime = datetime.combine(work_date, end_time)
    
    # If end time is before start time, assume it's the next day
    if end_datetime < start_datetime:
        end_datetime += timedelta(days=1)
    
    # Calculate work hours
    work_hours = calculate_work_hours(start_datetime, end_datetime, break_duration)
    
    # Submit button
    st.markdown("---")
    if st.button("✅ Submit Work Log", type="primary", use_container_width=True):
        if not employee_name or employee_name.strip() == "":
            st.error("⚠️ Please enter your name")
        else:
            record = {
                "date": work_date.strftime("%Y-%m-%d"),
                "employee_name": employee_name.strip(),
                "start_time": start_time.strftime("%H:%M"),
                "end_time": end_time.strftime("%H:%M"),
                "break_minutes": break_duration,
                "work_hours": round(work_hours, 2),
                "team": TEAM_NAME,
                "manager": MANAGER_NAME,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.session_state.records.append(record)
            save_records(st.session_state.records)
            
            st.success(f"✅ Work hours logged successfully for {employee_name}!")
            st.balloons()

# Tab 2: View Records
with tab2:
    st.markdown("## Work Records")
    
    # Load records
    if not st.session_state.records:
        st.session_state.records = load_records()
    
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        
        # Handle old records that don't have employee_name field
        if 'employee_name' not in df.columns:
            df['employee_name'] = 'Unknown'
        
        # Filter options
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info(f"📊 Showing records for **{TEAM_NAME}** team under manager **{MANAGER_NAME}**")
        
        with col2:
            if st.button("🗑️ Clear All Records", type="secondary"):
                if st.session_state.get('confirm_delete', False):
                    st.session_state.records = []
                    save_records([])
                    st.session_state.confirm_delete = False
                    st.rerun()
                else:
                    st.session_state.confirm_delete = True
                    st.warning("⚠️ Click again to confirm deletion")
        
        # Display table
        st.dataframe(
            df[['date', 'employee_name', 'start_time', 'end_time', 'break_minutes', 'work_hours']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "date": "Date",
                "employee_name": "Employee Name",
                "start_time": "Start Time",
                "end_time": "End Time",
                "break_minutes": "Break (min)",
                "work_hours": "Work Hours"
            }
        )
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Records as CSV",
            data=csv,
            file_name=f"work_records_digital_engineering_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("📝 No records yet. Start logging your work hours in the 'Log Work Hours' tab!")

# Footer
st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: #666666;'>Work Hours Tracking System v1.0 | "
    f"Digital Engineering Team | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>",
    unsafe_allow_html=True
)