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
    
    /* Period separator */
    .period-separator {
        background: #e0e0e0;
        padding: 10px;
        border-radius: 6px;
        text-align: center;
        margin: 20px 0;
        font-weight: 600;
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

# Calculate time difference and format as HH:MM
def calculate_time_duration(start_time, end_time):
    """Calculate duration between two times and return as 'HH:MM' format"""
    if start_time and end_time:
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        
        # If end time is before start time, assume next day
        if end_dt < start_dt:
            end_dt += timedelta(days=1)
        
        duration = end_dt - start_dt
        total_minutes = int(duration.total_seconds() / 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        return f"{hours}:{minutes:02d}", total_minutes
    return "0:00", 0

# Convert time string to minutes
def time_to_minutes(time_str):
    """Convert 'HH:MM' format to total minutes"""
    if ':' in time_str:
        parts = time_str.split(':')
        return int(parts[0]) * 60 + int(parts[1])
    return 0

# Convert minutes to time string
def minutes_to_time(minutes):
    """Convert total minutes to 'HH:MM' format"""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}:{mins:02d}"

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
    
    st.markdown("---")
    
    # Morning/First Period
    st.markdown("### ☀️ Morning Period (Before Break)")
    col1, col2 = st.columns(2)
    
    with col1:
        morning_start = st.time_input(
            "Start Work",
            value=datetime.now().replace(hour=7, minute=56, second=0, microsecond=0),
            help="When did you start working in the morning?",
            step=60,
            key="morning_start"
        )
    
    with col2:
        morning_end = st.time_input(
            "Finish (Before Break)",
            value=datetime.now().replace(hour=11, minute=23, second=0, microsecond=0),
            help="When did you stop for break?",
            step=60,
            key="morning_end"
        )
    
    # Calculate morning duration
    morning_duration, morning_minutes = calculate_time_duration(morning_start, morning_end)
    
    st.markdown('<div class="period-separator">☕ BREAK TIME</div>', unsafe_allow_html=True)
    
    # Afternoon/Second Period
    st.markdown("### 🌤️ Afternoon Period (After Break)")
    col3, col4 = st.columns(2)
    
    with col3:
        afternoon_start = st.time_input(
            "Start Work (After Break)",
            value=datetime.now().replace(hour=12, minute=20, second=0, microsecond=0),
            help="When did you return from break?",
            step=60,
            key="afternoon_start"
        )
    
    with col4:
        afternoon_end = st.time_input(
            "Finish Work",
            value=datetime.now().replace(hour=17, minute=45, second=0, microsecond=0),
            help="When did you finish working?",
            step=60,
            key="afternoon_end"
        )
    
    # Calculate afternoon duration
    afternoon_duration, afternoon_minutes = calculate_time_duration(afternoon_start, afternoon_end)
    
    # Calculate break duration
    break_duration_str, break_minutes = calculate_time_duration(morning_end, afternoon_start)
    
    # Calculate total work time
    total_work_minutes = morning_minutes + afternoon_minutes
    total_work_time = minutes_to_time(total_work_minutes)
    
    st.markdown("---")
    
    # Display summary
    st.markdown("### 📊 Work Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Morning Period", morning_duration)
    with col2:
        st.metric("Afternoon Period", afternoon_duration)
    with col3:
        st.metric("Break Time", break_duration_str)
    with col4:
        st.metric("Total Work Time", total_work_time)
    
    # Submit button
    st.markdown("---")
    if st.button("✅ Submit Work Log", type="primary", use_container_width=True):
        if not employee_name or employee_name.strip() == "":
            st.error("⚠️ Please enter your name")
        else:
            record = {
                "date": work_date.strftime("%Y-%m-%d"),
                "employee_name": employee_name.strip(),
                "morning_start": morning_start.strftime("%H:%M"),
                "morning_end": morning_end.strftime("%H:%M"),
                "afternoon_start": afternoon_start.strftime("%H:%M"),
                "afternoon_end": afternoon_end.strftime("%H:%M"),
                "morning_duration": morning_duration,
                "afternoon_duration": afternoon_duration,
                "break_duration": break_duration_str,
                "total_work_time": total_work_time,
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
        
        # Filter and action buttons at the top
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.info(f"📊 Showing records for **{TEAM_NAME}** team under manager **{MANAGER_NAME}**")
        
        with col2:
            # Search/Filter by name
            search_name = st.text_input("🔍 Search by name", placeholder="Type name to filter...", key="search_filter")
        
        with col3:
            if st.button("🗑️ Clear All Records", type="secondary", use_container_width=True):
                if st.session_state.get('confirm_delete_all', False):
                    st.session_state.records = []
                    save_records([])
                    st.session_state.confirm_delete_all = False
                    st.rerun()
                else:
                    st.session_state.confirm_delete_all = True
                    st.warning("⚠️ Click again to confirm deletion")
        
        # Filter records if search is active
        display_records = st.session_state.records.copy()
        if search_name:
            display_records = [r for r in display_records if search_name.lower() in r.get('employee_name', '').lower()]
        
        st.markdown("---")
        
        # Check if we have records to display
        if len(display_records) == 0:
            st.warning("No records found matching your search.")
        else:
            # Create table header
            st.markdown("""
                <style>
                .record-table {
                    width: 100%;
                    margin: 10px 0;
                }
                .record-row {
                    display: grid;
                    grid-template-columns: 1.5fr 1fr 1fr 1fr 1fr 1fr 1fr 0.5fr;
                    gap: 10px;
                    padding: 15px;
                    border-bottom: 1px solid #e0e0e0;
                    align-items: center;
                    background: white;
                }
                .record-row:hover {
                    background: #f5f5f5;
                }
                .record-header {
                    display: grid;
                    grid-template-columns: 1.5fr 1fr 1fr 1fr 1fr 1fr 1fr 0.5fr;
                    gap: 10px;
                    padding: 15px;
                    background: #000000;
                    color: white;
                    font-weight: 600;
                }
                .record-cell {
                    font-size: 14px;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Table header
            st.markdown("""
                <div class="record-header">
                    <div>Employee Name</div>
                    <div>Date</div>
                    <div>Morning Start</div>
                    <div>Morning End</div>
                    <div>Afternoon Start</div>
                    <div>Afternoon End</div>
                    <div>Total Work</div>
                    <div>Action</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Display each record with delete button
            for idx, record in enumerate(display_records):
                cols = st.columns([1.5, 1, 1, 1, 1, 1, 1, 0.5])
                
                with cols[0]:
                    st.write(record.get('employee_name', 'N/A'))
                with cols[1]:
                    st.write(record.get('date', 'N/A'))
                with cols[2]:
                    st.write(record.get('morning_start', 'N/A'))
                with cols[3]:
                    st.write(record.get('morning_end', 'N/A'))
                with cols[4]:
                    st.write(record.get('afternoon_start', 'N/A'))
                with cols[5]:
                    st.write(record.get('afternoon_end', 'N/A'))
                with cols[6]:
                    st.write(f"**{record.get('total_work_time', 'N/A')}**")
                with cols[7]:
                    if st.button("🗑️", key=f"del_{idx}", help="Delete this record"):
                        # Find and remove the record
                        original_idx = st.session_state.records.index(record)
                        deleted_name = st.session_state.records[original_idx].get('employee_name', 'Record')
                        st.session_state.records.pop(original_idx)
                        save_records(st.session_state.records)
                        st.success(f"✅ Deleted record for {deleted_name}")
                        st.rerun()
        
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
    "<p style='text-align: center; color: #666666;'>Created by Digital Engineering Team for Digital Engineering Team - Schmalz V 1.5 | 2025</p>",
    unsafe_allow_html=True
)
