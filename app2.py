"""
Weight Tracker Application
=========================

A Streamlit-based web application for tracking personal weight progress.
This application allows users to:
- Create and manage user accounts
- Track daily weight measurements
- Set and monitor weight goals
- Visualize weight progress
- Manage weight data entries

Author: [Archiev]
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import requests
from PIL import Image
from io import BytesIO
import time
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Custom CSS ---
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #00B4D8;
        --secondary-color: #0077B6;
        --background-color: #0A192F;
        --secondary-bg: #112240;
        --text-color: #E6F1FF;
        --border-color: #233554;
        --input-bg: #1D3461;
        --hover-color: #0096C7;
        --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        --gradient: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    }
    
    /* Custom styling for the entire app */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
        width: 100%;
        max-width: 100%;
        margin: 0;
        padding: 0;
    }
    
    /* Main content container */
    .main .block-container {
        padding: 1rem 2rem;
        max-width: 100%;
    }
    
    /* Sidebar container */
    .css-1d391kg {
        background-color: var(--secondary-bg);
        padding: 1.5rem;
        border-right: 1px solid var(--border-color);
        width: 100%;
        box-shadow: var(--box-shadow);
    }
    
    /* Content columns */
    .row-widget.stHorizontal {
        gap: 2rem;
    }
    
    /* Weight input section styling */
    .section-container {
        background-color: var(--secondary-bg);
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin: 0.8rem 0;
        box-shadow: var(--box-shadow);
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .section-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Section headers */
    .section-container h2 {
        color: var(--text-color);
        font-size: 1.3rem;
        margin: 0 0 0.8rem 0;
        padding-bottom: 0.4rem;
        font-weight: 600;
        text-align: center;
        border-bottom: 2px solid var(--border-color);
        letter-spacing: 0.5px;
    }
    
    /* Date container */
    .date-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin: 0.4rem 0;
        width: 100%;
        padding: 0;
    }
    
    /* Date navigation buttons */
    .date-container .stButton button {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 2.5rem !important;
        min-width: 2.5rem !important;
        padding: 0 !important;
        font-size: 1.2rem !important;
        border-radius: 50% !important;
        background: var(--gradient) !important;
        color: var(--text-color) !important;
        border: none !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
        box-shadow: var(--box-shadow) !important;
    }

    /* Date input styling */
    .date-input {
        text-align: center;
        width: 100%;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Hide the default date input label */
    .date-input .stDateInput > label {
        display: none !important;
    }
    
    /* Style the date input */
    .date-input .stDateInput > div > div {
        display: flex;
        justify-content: center;
    }
    
    /* Style the formatted date display */
    .date-input h3 {
        text-align: center;
        margin: 0 !important;
        padding: 0.2rem 0 !important;
        font-size: 1.1rem !important;
        color: var(--text-color);
    }
    
    /* Weight input styling */
    .weight-input {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding: 0;
        margin: 0.4rem 0;
        background: none;
    }
    
    .weight-input label,
    .stNumberInput > label {
        text-align: center !important;
        width: 100% !important;
        margin: 0 0 0.4rem 0 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: var(--text-color) !important;
        display: block !important;
        letter-spacing: 0.5px !important;
    }
    
    .weight-input input,
    .stNumberInput > div > div > input {
        text-align: center !important;
        font-size: 1.2rem !important;
        padding: 0.6rem !important;
        background-color: var(--input-bg) !important;
        color: var(--text-color) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 8px !important;
        width: 100% !important;
        max-width: 200px !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
    }
    
    /* Add Entry button styling */
    .stButton > button[data-testid="baseButton-secondary"] {
        margin-top: 0.8rem !important;
        background: var(--gradient) !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 0.8rem !important;
        border-radius: 8px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        max-width: 200px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* Weight input container */
    .weight-input > div {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding: 0;
        background: none;
    }
    
    .weight-input input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(0, 180, 216, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Quote styling */
    .quote-container {
        background: var(--gradient);
        padding: 1.2rem 1.8rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        color: var(--text-color);
        font-size: 1.2rem;
        text-align: center;
        box-shadow: var(--box-shadow);
        border: none;
    }
    
    /* Dataframe styling */
    .dataframe {
        background-color: var(--secondary-bg);
        color: var(--text-color);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid var(--border-color);
        margin: 1rem 0;
        font-size: 1rem;
        box-shadow: var(--box-shadow);
    }
    
    /* Progress graph styling */
    .stPlot {
        background-color: var(--secondary-bg);
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: var(--box-shadow);
        margin: 1rem 0;
    }
    
    /* Login form styling */
    .login-form {
        background-color: var(--secondary-bg);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        margin: 1rem auto;
        box-shadow: var(--box-shadow);
        transition: all 0.3s ease;
        max-width: 600px;
    }
    
    .login-form:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    
    /* Login input fields */
    .login-form .stTextInput > div > div > input,
    .login-form .stTextInput[type="password"] > div > div > input {
        background-color: var(--input-bg) !important;
        color: var(--text-color) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 0.8rem 1rem !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
        margin-bottom: 0.8rem !important;
        text-align: left !important;
    }
    
    /* Login form labels */
    .login-form .stTextInput > label {
        color: var(--text-color) !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 0.5px !important;
    }

    /* Remove extra padding from form elements */
    .login-form .stForm > div:first-child {
        padding-top: 0 !important;
    }

    .login-form .stForm {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Adjust spacing for the entire login container */
    .login-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }

    .login-container .title {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .login-container .subtitle {
        text-align: center;
        margin-bottom: 1rem;
        color: var(--text-color);
        opacity: 0.8;
    }

    /* Adjust form field containers */
    .stTextInput > div {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Style for form field wrapper */
    .stTextInput {
        margin-bottom: 1rem !important;
    }

    /* Remove extra margins from streamlit elements */
    .element-container, .stMarkdown {
        margin-bottom: 0.5rem !important;
    }
    
    /* Login button */
    .login-form .stButton > button {
        background: var(--gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        margin-top: 1rem !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: var(--box-shadow) !important;
    }
    
    .login-form .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    .login-form .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Create account button */
    .stButton > button[key="create_account_btn"],
    .stButton > button[key="back_to_login_btn"] {
        background: transparent !important;
        border: 2px solid var(--primary-color) !important;
        color: var(--primary-color) !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button[key="create_account_btn"]:hover,
    .stButton > button[key="back_to_login_btn"]:hover {
        background: var(--primary-color) !important;
        color: white !important;
        transform: translateY(-2px);
    }
    
    /* Quote container */
    .quote-container {
        background: var(--gradient);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        color: var(--text-color);
        text-align: center;
        box-shadow: var(--box-shadow);
        border: none;
    }
    
    /* Help text */
    .stTextInput .help-text {
        color: var(--text-color) !important;
        opacity: 0.8;
        font-size: 0.9rem !important;
        margin-top: 0.4rem !important;
    }
    
    /* Success/Error messages in login form */
    .login-form .stSuccess,
    .login-form .stError,
    .login-form .stWarning {
        margin: 1rem 0 !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        text-align: center !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .login-form {
            padding: 1.5rem;
        }
        
        .login-form .stTextInput > div > div > input,
        .login-form .stTextInput[type="password"] > div > div > input {
            padding: 0.8rem 1rem !important;
            font-size: 1rem !important;
        }
        
        .login-form .stButton > button {
            padding: 0.8rem 1.5rem !important;
            font-size: 1.1rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- Constants ---
USERS_FILE = "users.csv"  # File to store user credentials
LEADERBOARD_FILE = "leaderboard.csv"  # File for future leaderboard feature

# --- Helper Functions ---
def load_users():
    """
    Load user credentials from CSV file.
    
    Returns:
        pd.DataFrame: DataFrame containing username and password columns.
                     Returns empty DataFrame if file doesn't exist.
    """
    try:
        if os.path.exists(USERS_FILE):
            df = pd.read_csv(USERS_FILE)
            # Clean the data
            df["Username"] = df["Username"].astype(str).str.strip()
            df["Password"] = df["Password"].astype(str).str.strip()
            return df
        return pd.DataFrame(columns=["Username", "Password"])
    except Exception as e:
        st.error(f"Error loading users: {str(e)}")
        return pd.DataFrame(columns=["Username", "Password"])

def save_users(users_df):
    """
    Save user credentials to CSV file with error handling.
    """
    try:
        # Clean the data before saving
        users_df["Username"] = users_df["Username"].astype(str).str.strip()
        users_df["Password"] = users_df["Password"].astype(str).str.strip()
        users_df.to_csv(USERS_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving user data: {str(e)}")
        return False

def delete_user(username):
    """
    Delete a user account and associated data.
    
    Args:
        username (str): Username of the account to delete
    """
    users_df = load_users()
    if username in users_df["Username"].values:
        users_df = users_df[users_df["Username"] != username]
        save_users(users_df)

        # Delete user's weight data file
        user_file = f"weight_data_{username}.csv"
        if os.path.exists(user_file):
            os.remove(user_file)

        st.success("✅ Your account has been deleted successfully.")
        
        # Clear session and prevent re-login
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        st.rerun()

def get_user_file(username):
    """
    Get the filename for a user's weight data.
    
    Args:
        username (str): Username
        
    Returns:
        str: Filename for the user's weight data
    """
    return f"weight_data_{username}.csv"

def get_goal_weight_file(username):
    """
    Get the filename for a user's goal weight.
    
    Args:
        username (str): Username
        
    Returns:
        str: Filename for the user's goal weight
    """
    return f"goal_weight_{username}.txt"

def load_goal_weight(username):
    """
    Load user's goal weight from file.
    
    Args:
        username (str): Username
        
    Returns:
        float or None: Goal weight if set, None otherwise
    """
    try:
        goal_file = get_goal_weight_file(username)
        if os.path.exists(goal_file):
            with open(goal_file, "r") as f:
                return float(f.read().strip())
        return None
    except Exception as e:
        st.error(f"Error loading goal weight: {str(e)}")
        return None

def save_goal_weight(username, goal_weight):
    """
    Save user's goal weight to file.
    
    Args:
        username (str): Username
        goal_weight (float): Goal weight to save
    """
    try:
        goal_file = get_goal_weight_file(username)
        with open(goal_file, "w") as f:
            f.write(str(round(goal_weight, 2)))
    except Exception as e:
        st.error(f"Error saving goal weight: {str(e)}")

def estimate_time_to_goal(username, goal_weight, df):
    """
    Estimate time to reach goal weight based on past data.
    
    Args:
        username (str): Username
        goal_weight (float): Target goal weight
        df (pd.DataFrame): User's weight history
        
    Returns:
        str: Estimated time message or error message
    """
    try:
        if len(df) < 2:
            return "Not enough data to estimate time."

        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        weight_change_per_day = (df["Weight"].iloc[0] - df["Weight"].iloc[-1]) / (df["Date"].iloc[-1] - df["Date"].iloc[0]).days

        if weight_change_per_day <= 0:
            return "No weight loss trend detected."

        days_needed = abs((goal_weight - df["Weight"].iloc[-1]) / weight_change_per_day)
        
        # Convert days to months and remaining days
        months = int(days_needed // 30.44)  # Average days in a month
        remaining_days = int(days_needed % 30.44)
        
        if months == 0:
            return f"📅 Estimated time to reach goal weight: {remaining_days} days"
        elif remaining_days == 0:
            return f"📅 Estimated time to reach goal weight: {months} months"
        else:
            return f"📅 Estimated time to reach goal weight: {months} months {remaining_days} days"
    except Exception as e:
        return f"Error calculating time estimate: {str(e)}"

def load_goggins_image(is_login=True):
    """
    Load and return the David Goggins motivational image from local file.
    
    Args:
        is_login (bool): If True, loads goggins1.jpg for login page, else goggins2.jpg
    
    Returns:
        PIL.Image: The loaded image, or None if the image cannot be loaded
    """
    try:
        # Load the appropriate image based on the page
        filename = "goggins1.jpg" if is_login else "goggins2.jpg"
        img = Image.open(filename)
        return img
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None

# --- Authentication Pages ---
def signup_page():
    """
    Display and handle user signup functionality.
    """
    # Add container for better centering
    st.markdown("""
        <div style="max-width: 800px; margin: 0 auto; padding: 2rem;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">
                    📝 Create Your Account
                </h1>
            </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="quote-container" style="margin-bottom: 2rem;">
            <strong style="font-size: 1.4rem;">Your journey to a healthier you starts here!</strong>
        </div>
    """, unsafe_allow_html=True)
    
    users_df = load_users()
    
    # Create a form for signup with improved styling
    st.markdown("""
        <div class="login-form" style="max-width: 600px; margin: 0 auto;">
    """, unsafe_allow_html=True)
    
    with st.form("signup_form", clear_on_submit=False):
        new_username = st.text_input("Choose a Username", 
                                   placeholder="Enter your username",
                                   help="Username must be at least 3 characters long")
        
        new_password = st.text_input("Choose a Password", 
                                   type="password",
                                   placeholder="Enter your password",
                                   help="Password must be at least 4 characters long")

        # Center the register button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("Create Account", use_container_width=True)
        
        if submitted:
            if len(new_username) < 3 or len(new_password) < 4:
                st.error("Username must be at least 3 characters and password at least 4 characters long!")
            elif new_username in users_df["Username"].values:
                st.error("Username already exists! Choose another.")
            else:
                new_user = pd.DataFrame([[new_username, new_password]], columns=["Username", "Password"])
                users_df = pd.concat([users_df, new_user], ignore_index=True)
                if save_users(users_df):
                    st.success("✅ Account created successfully! Redirecting to login...")
                    st.session_state["show_signup"] = False
                    time.sleep(2)
                    st.rerun()
    
    # Back to login button with improved spacing
    st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to Login", key="back_to_login_btn", use_container_width=True):
            st.session_state["show_signup"] = False
            st.rerun()
    st.markdown('</div></div></div>', unsafe_allow_html=True)

def login_page():
    """
    Display and handle user login functionality.
    """
    # Use a wider ratio for the main content
    col_main, col_img = st.columns([5, 2])
    
    with col_main:
        # Add container with improved styling
        st.markdown("""
            <div class="login-container">
                <div class="title">
                    <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">
                        🏋️ Welcome to Fitness Tracker!
                    </h1>
                </div>
                <div class="quote-container" style="margin-bottom: 1.5rem;">
                    <strong style="font-size: 1.4rem;">Track your progress, achieve your goals!</strong>
                </div>
                <div class="subtitle">
                    <p style="font-size: 1.2rem;">Your personal weight tracking companion</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        users_df = load_users()
        
        # Create a form for login with improved styling
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", 
                                   key="username_input", 
                                   placeholder="Enter your username",
                                   help="Enter your registered username")
            
            password = st.text_input("Password", 
                                   type="password", 
                                   key="password_input", 
                                   placeholder="Enter your password",
                                   help="Enter your password")
            
            # Center the login button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.warning("Please enter both username and password.")
                else:
                    # Clean input
                    username = str(username).strip()
                    password = str(password).strip()
                    
                    # Load users
                    users_df = load_users()
                    
                    # Check credentials
                    user_match = users_df[users_df["Username"] == username]
                    
                    if not user_match.empty:
                        stored_password = user_match["Password"].iloc[0]
                        if stored_password == password:
                            st.success("✅ Login successful! Redirecting...")
                            st.session_state["logged_in"] = True
                            st.session_state["username"] = username
                            st.session_state["just_logged_in"] = True
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Invalid password.")
                    else:
                        st.error(f"Username '{username}' not found.")
        
        # Create Account button with improved spacing
        st.markdown('<div style="text-align: center; margin-top: 1rem;">', unsafe_allow_html=True)
        if st.button("Create a New Account", key="create_account_btn", use_container_width=True):
            st.session_state["show_signup"] = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_img:
        # Adjust image container styling
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; margin-top: 2rem;">
        """, unsafe_allow_html=True)
        
        goggins_img = load_goggins_image(is_login=True)
        if goggins_img:
            st.image(goggins_img, width=250, caption="GET AFTER IT!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- Main Application ---
def fitness_tracker(username):
    """
    Main fitness tracking interface.
    
    Args:
        username (str): Current user's username
    """
    # Initialize navigation state if not exists
    if "nav_target" not in st.session_state:
        st.session_state.nav_target = None
    
    # Sidebar
    with st.sidebar:
        # User greeting with improved styling
        st.markdown(f"""
            <div style="text-align: center; padding: 1rem 0;">
                <h1 style="font-size: 1.8rem; margin-bottom: 0.5rem;">👋 Hello</h1>
                <h2 style="font-size: 1.4rem; color: var(--primary-color); margin-top: 0;">{username}</h2>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        # Add the three functional dashboards first
        st.markdown("""
            <div style="margin: 1rem 0;">
                <h2 style="font-size: 1.4rem; margin-bottom: 1rem;">📊 Dashboards</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Add Health Dashboard button
        if st.button("🏥 Health Dashboard", key="health_dashboard_btn", use_container_width=True):
            st.session_state["show_health_dashboard"] = True
            st.rerun()
        
        # Add Running Assistant button
        if st.button("🏃🏽 Running Assistant", key="running_assistant_btn", use_container_width=True):
            st.session_state["show_running_assistant"] = True
            st.rerun()
        
        # Add Calorie Calculator button
        if st.button("🍽️ Fat Calc", key="calorie_calculator_btn", use_container_width=True):
            st.session_state["show_calorie_calculator"] = True
            st.rerun()

        # Add Data for Nerds button
        if st.button("🤓 Data for Nerds", key="data_nerds_btn", use_container_width=True):
            st.session_state["show_data_nerds"] = True
            st.rerun()
            
        st.markdown("---")
        
        # Add Refresh Button with improved styling
        st.markdown("""
            <div style="margin: 1rem 0;">
                <p style="font-size: 1rem; color: var(--text-color); opacity: 0.8; margin-bottom: 0.5rem;">
                    Refresh to see the latest updates
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Refresh Data", key="refresh_btn", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        
        # Account Settings with improved spacing
        st.markdown("""
            <div style="margin: 1rem 0;">
                <h2 style="font-size: 1.4rem; margin-bottom: 1rem;">⚙️ Account Settings</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Password Change Section with improved styling
        with st.expander("🔑 Change Password"):
            st.markdown('<div style="padding: 0.5rem 0;">', unsafe_allow_html=True)
            current_password = st.text_input("Current Password", type="password", key="current_pwd")
            new_password = st.text_input("New Password", type="password", key="new_pwd")
            confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pwd")
            
            if st.button("Update Password", key="update_pwd_btn", use_container_width=True):
                if not current_password or not new_password or not confirm_password:
                    st.error("Please fill in all password fields.")
                elif new_password != confirm_password:
                    st.error("New passwords do not match.")
                elif len(new_password) < 4:
                    st.error("New password must be at least 4 characters long.")
                else:
                    users_df = load_users()
                    user_row = users_df[users_df["Username"] == username]
                    
                    if not user_row.empty and user_row["Password"].iloc[0] == current_password:
                        # Update the password in the DataFrame
                        users_df.loc[users_df["Username"] == username, "Password"] = new_password
                        
                        # Save the updated DataFrame
                        success = save_users(users_df)
                        
                        if success:
                            st.success("✅ Password updated successfully! Please login again with your new password.")
                            # Add a small delay to show the success message
                            time.sleep(2)
                            # Clear all session state to force a complete logout
                            for key in list(st.session_state.keys()):
                                del st.session_state[key]
                            # Ensure we're completely logged out
                            st.session_state["logged_in"] = False
                            st.session_state["show_signup"] = False
                            st.rerun()
                    else:
                        st.error("Current password is incorrect.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Delete Account Section with improved styling
        with st.expander("❌ Delete Account"):
            st.markdown('<div style="padding: 0.5rem 0;">', unsafe_allow_html=True)
            st.warning("⚠️ This action cannot be undone!")
            
            if "confirm_delete_account" not in st.session_state:
                st.session_state.confirm_delete_account = False
                
            if not st.session_state.confirm_delete_account:
                if st.button("Delete Account", key="delete_account_btn", use_container_width=True):
                    st.session_state.confirm_delete_account = True
                    st.rerun()
            else:
                st.error("Are you sure you want to delete your account? This cannot be undone!")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes, Delete", key="confirm_delete_btn", use_container_width=True):
                        users_df = load_users()
                        if username in users_df["Username"].values:
                            # Remove user from users DataFrame
                            users_df = users_df[users_df["Username"] != username]
                            save_users(users_df)
                            
                            # Delete user's weight data file
                            user_file = f"weight_data_{username}.csv"
                            if os.path.exists(user_file):
                                os.remove(user_file)
                                
                            # Delete user's goal weight file if it exists
                            goal_file = f"goal_weight_{username}.txt"
                            if os.path.exists(goal_file):
                                os.remove(goal_file)
                            
                            st.success("✅ Account deleted successfully!")
                            time.sleep(2)
                            
                            # Clear all session state
                            for key in list(st.session_state.keys()):
                                del st.session_state[key]
                                
                            # Set logged_in to False explicitly
                            st.session_state["logged_in"] = False
                            st.rerun()
                with col2:
                    if st.button("No, Cancel", key="cancel_delete_btn", use_container_width=True):
                        st.session_state.confirm_delete_account = False
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Logout button with improved styling
        st.markdown('<div style="padding: 1rem 0;">', unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state.pop("username")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Main Content
    col_main, col_img = st.columns([4, 1])
    
    with col_main:
        st.title("🏋️ Your Fitness Journey")
        
        # Handle navigation
        if "nav_target" in st.session_state and st.session_state.nav_target:
            target = st.session_state.nav_target
            st.session_state.nav_target = None  # Reset navigation state
            
            # Create anchor targets
            if target == "add_weight":
                st.markdown('<a name="add_weight"></a>', unsafe_allow_html=True)
            elif target == "progress":
                st.markdown('<a name="progress"></a>', unsafe_allow_html=True)
            elif target == "view_data":
                st.markdown('<a name="view_data"></a>', unsafe_allow_html=True)
            elif target == "goal":
                st.markdown('<a name="goal"></a>', unsafe_allow_html=True)
            
            # Add JavaScript for smooth scrolling
            st.markdown(f"""
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        const element = document.querySelector('a[name="{target}"]');
                        if (element) {{
                            element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                        }}
                    }});
                </script>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="quote-container">
                <strong>Every day is a new opportunity to improve!</strong>
            </div>
        """, unsafe_allow_html=True)

        # Load and prepare user data
        data_file = get_user_file(username)
        try:
            df = pd.read_csv(data_file)
            df["Date"] = pd.to_datetime(df["Date"])
            df["Weight"] = df["Weight"].round(2)
            df = df.drop_duplicates(subset=["Date"], keep="last")
            df = df.sort_values("Date")
            try:
                df.to_csv(data_file, index=False)
            except Exception as e:
                st.error(f"Error saving data: {str(e)}")
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Date", "Weight"])
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            df = pd.DataFrame(columns=["Date", "Weight"])

        # Quick Stats
        if not df.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Starting Weight", f"{df['Weight'].iloc[0]:.1f} kg")
            with col2:
                st.metric("Current Weight", f"{df['Weight'].iloc[-1]:.1f} kg")
            with col3:
                weight_change = df['Weight'].iloc[-1] - df['Weight'].iloc[0]
                st.metric("Total Change", f"{weight_change:+.1f} kg")
        
        # Weight Entry Section
        st.markdown('<div id="add_weight"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="section-container">
                <h2>➕ Add Your Weight Entry</h2>
                <div style="max-width: 500px; margin: 0 auto;">
        """, unsafe_allow_html=True)
        
        # Reset selected_date to current date on page load/refresh
        if "selected_date" not in st.session_state or st.session_state.get("just_logged_in", False):
            st.session_state.selected_date = datetime.now().date()
            st.session_state.just_logged_in = False

        # Date Selection with improved layout
        st.markdown('<div class="date-container">', unsafe_allow_html=True)
        date_col1, date_col2, date_col3 = st.columns([0.2, 2, 0.2])
        with date_col1:
            if st.button("◀", key="prev_day_btn", help="Previous Day", use_container_width=True):
                st.session_state.selected_date = st.session_state.selected_date - timedelta(days=1)
                st.rerun()
        with date_col2:
            st.markdown('<div class="date-input">', unsafe_allow_html=True)
            try:
                selected_date = st.date_input("Select Date", 
                                            value=st.session_state.selected_date,
                                            min_value=None,
                                            max_value=None,
                                            label_visibility="collapsed",
                                            key="date_selector")
                st.session_state.selected_date = selected_date
                formatted_date = selected_date.strftime("%d %B %Y")
                st.markdown(f'<h3 style="text-align: center;">{formatted_date}</h3>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Invalid date format: {str(e)}")
                selected_date = datetime.now().date()
        with date_col3:
            if st.button("▶", key="next_day_btn", help="Next Day", use_container_width=True):
                next_date = st.session_state.selected_date + timedelta(days=1)
                st.session_state.selected_date = next_date
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Weight Input with improved layout
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="weight-input">', unsafe_allow_html=True)
            try:
                new_weight = st.number_input("Weight (kg)", 
                                           min_value=30.0,
                                           max_value=200.0, 
                                           step=0.05,
                                           format="%.2f",
                                           value=70.0,
                                           label_visibility="visible")
            except Exception as e:
                st.error(f"Invalid weight value: {str(e)}")
                new_weight = 70.0
            st.markdown('</div>', unsafe_allow_html=True)

            if st.button("Add Entry", key="add_entry_btn", use_container_width=True):
                try:
                    # Format the date
                    selected_date_str = selected_date.strftime("%Y-%m-%d")
                    
                    # Create or load the DataFrame
                    if df.empty:
                        df = pd.DataFrame(columns=["Date", "Weight"])
                    
                    # Convert existing dates to string format for comparison
                    existing_dates = df["Date"].dt.strftime("%Y-%m-%d").values if not df.empty else []
                    
                    # Update or add new entry
                    if selected_date_str in existing_dates:
                        st.warning("Entry exists for this date. It will be updated.")
                        df.loc[df["Date"].dt.strftime("%Y-%m-%d") == selected_date_str, "Weight"] = round(new_weight, 2)
                    else:
                        new_entry = pd.DataFrame({
                            "Date": [pd.to_datetime(selected_date_str)],
                            "Weight": [round(new_weight, 2)]
                        })
                        df = pd.concat([df, new_entry], ignore_index=True)
                    
                    # Save the entry
                    if save_weight_entry(username, df, data_file):
                        st.success("✅ Weight entry added!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Failed to save weight entry. Please try again.")
                except Exception as e:
                    st.error(f"Error adding entry: {str(e)}")
        
        st.markdown("</div></div>", unsafe_allow_html=True)

        # Data Display Section
        st.markdown('<div id="view_data"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="section-container">
                <h2>📊 Your Weight Data</h2>
        """, unsafe_allow_html=True)
        
        if not df.empty:
            try:
                df["Date"] = pd.to_datetime(df["Date"]).dt.strftime('%d %B %Y')
                df["Weight"] = df["Weight"].round(2)
                df["Weight Difference"] = df["Weight"].diff().fillna(0).round(2)
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error displaying data: {str(e)}")
        else:
            st.info("No weight entries yet. Add your first entry above!")
        
        st.markdown("</div>", unsafe_allow_html=True)

        # Progress Graph Section
        st.markdown('<div id="progress"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="section-container">
                <h2>📈 Weight Progress Over Time</h2>
        """, unsafe_allow_html=True)
        
        if not df.empty:
            try:
                # Create interactive plot using plotly
                fig = make_subplots(specs=[[{"secondary_y": False}]])
                
                # Add actual weight data
                fig.add_trace(
                    go.Scatter(
                        x=df["Date"],
                        y=df["Weight"],
                        mode='markers+lines',
                        name='Weight',
                        line=dict(color='#00B4D8', width=2),
                        marker=dict(size=8),
                        hovertemplate="Date: %{x}<br>Weight: %{y:.2f} kg<extra></extra>"
                    )
                )
                
                # Add goal weight line if set
                goal_weight = load_goal_weight(username)
                if goal_weight:
                    fig.add_trace(
                        go.Scatter(
                            x=df["Date"],
                            y=[goal_weight] * len(df["Date"]),
                            mode='lines',
                            name='Goal Weight',
                            line=dict(color='#FFB700', width=2, dash='dash'),
                            hovertemplate="Goal Weight: %{y:.2f} kg<extra></extra>"
                        )
                    )
                
                # Update layout
                fig.update_layout(
                    title={
                        'text': "Weight Progress Over Time",
                        'y':0.95,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    plot_bgcolor='rgba(10,25,47,0.1)',
                    paper_bgcolor='rgba(10,25,47,0)',
                    font=dict(color='#E6F1FF'),
                    xaxis=dict(
                        title="Date",
                        gridcolor='rgba(35,53,84,0.5)',
                        showgrid=True
                    ),
                    yaxis=dict(
                        title="Weight (kg)",
                        gridcolor='rgba(35,53,84,0.5)',
                        showgrid=True
                    ),
                    hovermode='x unified',
                    showlegend=True,
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    )
                )
                
                # Display the plot
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error creating graph: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)

        # Goal Weight Section
        st.markdown('<div id="goal"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="section-container">
                <h2>🎯 Set Your Goal Weight</h2>
        """, unsafe_allow_html=True)
        
        current_goal = load_goal_weight(username)
        goal_weight = st.number_input("Enter your goal weight (kg)", 
                                    min_value=30.0, 
                                    max_value=200.0, 
                                    step=0.1, 
                                    value=current_goal or 70.0)

        if st.button("Save Goal Weight", key="save_goal_btn", use_container_width=True):
            try:
                save_goal_weight(username, goal_weight)
                st.success("✅ Goal weight saved successfully!")
                time.sleep(1)  # Brief pause for user feedback
                st.rerun()
            except Exception as e:
                st.error(f"Error saving goal weight: {str(e)}")

        if current_goal and not df.empty:
            with st.expander("View Weight Loss Progress"):
                # Calculate progress
                current_weight = df["Weight"].iloc[-1]
                starting_weight = df["Weight"].iloc[0]
                total_to_lose = starting_weight - current_goal
                current_progress = starting_weight - current_weight
                progress_percentage = min(100, max(0, (current_progress / total_to_lose) * 100))
                
                # Calculate milestones
                milestones = {
                    25: ("Bronze", "🥉"),
                    50: ("Silver", "🥈"),
                    75: ("Gold", "🥇"),
                    100: ("Champion", "🏆")
                }
                
                # Determine current level and next milestone
                current_level = None
                next_milestone = None
                for threshold, (level, icon) in sorted(milestones.items()):
                    if progress_percentage >= threshold:
                        current_level = level
                    else:
                        next_milestone = (threshold, level, icon)
                        break
                
                # Display progress bar with gamification elements
                st.markdown("""
                    <div style="text-align: center; margin: 1.5rem 0;">
                        <h3>Your Weight Loss Journey</h3>
                """, unsafe_allow_html=True)
                
                # Progress bar container with custom styling
                st.markdown(f"""
                    <div style="
                        background: var(--secondary-bg);
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin: 1rem 0;
                        border: 2px solid var(--border-color);
                    ">
                        <div style="
                            background: var(--background-color);
                            height: 30px;
                            border-radius: 15px;
                            overflow: hidden;
                            position: relative;
                            margin: 1rem 0;
                        ">
                            <div style="
                                background: var(--gradient);
                                height: 100%;
                                width: {progress_percentage}%;
                                transition: width 0.5s ease;
                                position: relative;
                                overflow: hidden;
                            ">
                                <div style="
                                    position: absolute;
                                    top: 0;
                                    left: 0;
                                    right: 0;
                                    bottom: 0;
                                    background: linear-gradient(90deg, 
                                        rgba(255,255,255,0) 0%,
                                        rgba(255,255,255,0.2) 50%,
                                        rgba(255,255,255,0) 100%);
                                    animation: shine 2s infinite;
                                "></div>
                            </div>
                        </div>
                        <div style="
                            display: flex;
                            justify-content: space-between;
                            margin: 0.5rem 0;
                            font-size: 0.9rem;
                            color: var(--text-color);
                            opacity: 0.8;
                        ">
                            <span>Start: {starting_weight:.1f} kg</span>
                            <span>Current: {current_weight:.1f} kg</span>
                            <span>Goal: {current_goal:.1f} kg</span>
                        </div>
                        <div style="
                            font-size: 1.2rem;
                            margin: 1rem 0;
                            color: var(--primary-color);
                            font-weight: bold;
                        ">
                            {progress_percentage:.1f}% Complete
                        </div>
                """, unsafe_allow_html=True)
                
                # Display current level and next milestone
                if current_level:
                    st.markdown(f"""
                        <div style="
                            font-size: 1.4rem;
                            margin: 1rem 0;
                            color: var(--primary-color);
                            font-weight: bold;
                        ">
                            Current Level: {current_level}
                        </div>
                    """, unsafe_allow_html=True)
                
                if next_milestone:
                    threshold, level, icon = next_milestone
                    remaining_percentage = threshold - progress_percentage
                    st.markdown(f"""
                        <div style="
                            font-size: 1.1rem;
                            margin: 0.5rem 0;
                            color: var(--text-color);
                            opacity: 0.8;
                        ">
                            Next Level: {level} {icon} ({remaining_percentage:.1f}% remaining)
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                estimated_time = estimate_time_to_goal(username, current_goal, df)
                st.write(estimated_time)

        # Data Management Section
        st.markdown("""
            <div class="section-container">
                <h2>⚙️ Data Management</h2>
        """, unsafe_allow_html=True)

        # Delete Weight Entry Section
        st.markdown("""
            <div style="margin-bottom: 2rem;">
                <h3>🗑️ Delete Weight Entry</h3>
        """, unsafe_allow_html=True)
        
        delete_date = st.date_input("Select date to delete entry", key="delete_date")
        
        if "confirm_delete_entry_state" not in st.session_state:
            st.session_state.confirm_delete_entry_state = False
            
        if st.button("Delete Selected Entry", key="delete_entry_btn", use_container_width=True):
            try:
                # Convert delete_date to string format
                delete_date_str = delete_date.strftime("%Y-%m-%d")
                
                # Convert df dates to datetime if they aren't already
                if not df.empty:
                    df["Date"] = pd.to_datetime(df["Date"])
                    # Check if the date exists
                    if any(df["Date"].dt.strftime("%Y-%m-%d") == delete_date_str):
                        st.session_state.confirm_delete_entry_state = True
                        st.warning(f"Are you sure you want to delete the entry for {delete_date.strftime('%d %B %Y')}?")
                    else:
                        st.warning("No entry found for the selected date.")
                else:
                    st.warning("No entries exist in your data.")
            except Exception as e:
                st.error(f"Error checking date: {str(e)}")
                
        if st.session_state.confirm_delete_entry_state:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Yes, Delete", key="confirm_delete_entry", use_container_width=True):
                    try:
                        delete_date_str = delete_date.strftime("%Y-%m-%d")
                        # Convert dates to datetime for comparison
                        df["Date"] = pd.to_datetime(df["Date"])
                        # Filter out the selected date
                        df = df[df["Date"].dt.strftime("%Y-%m-%d") != delete_date_str]
                        if save_weight_entry(username, df, data_file):
                            st.success(f"Entry for {delete_date.strftime('%d %B %Y')} deleted!")
                            st.session_state.confirm_delete_entry_state = False
                            time.sleep(1)
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting entry: {str(e)}")
                        st.session_state.confirm_delete_entry_state = False
            with col2:
                if st.button("Cancel", key="cancel_delete_entry", use_container_width=True):
                    st.session_state.confirm_delete_entry_state = False
                    st.rerun()

        # Delete All Data Section
        st.markdown("""
            <div>
                <h3>❌ Delete All Data</h3>
            </div>
        """, unsafe_allow_html=True)

        if "confirm_delete_all" not in st.session_state:
            st.session_state.confirm_delete_all = False

        if not st.session_state.confirm_delete_all:
            if st.button("Delete All Data", key="delete_all_btn", use_container_width=True):
                st.session_state.confirm_delete_all = True
                st.rerun()
        else:
            st.warning("⚠️ Are you sure you want to delete all data? This action cannot be undone.")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Yes, Delete All", key="confirm_delete_all_btn", use_container_width=True):
                    try:
                        # Create empty DataFrame
                        empty_df = pd.DataFrame(columns=["Date", "Weight"])
                        
                        # Ensure the data file exists and is writable
                        data_file = get_user_file(username)
                        empty_df.to_csv(data_file, index=False)
                        
                        # Also delete goal weight file if it exists
                        goal_file = get_goal_weight_file(username)
                        if os.path.exists(goal_file):
                            os.remove(goal_file)
                            
                        st.success("✅ All data has been deleted successfully!")
                        st.session_state.confirm_delete_all = False
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting data: {str(e)}")
                        st.session_state.confirm_delete_all = False
            with col2:
                if st.button("No, Cancel", key="cancel_delete_all_btn", use_container_width=True):
                    st.session_state.confirm_delete_all = False
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_img:
        goggins_img = load_goggins_image(is_login=False)
        if goggins_img:
            st.image(goggins_img, width=300, caption="STAY HARD!")

def save_weight_entry(username, df, data_file):
    """
    Save weight entry with proper error handling.
    """
    try:
        # Ensure the DataFrame has the correct columns
        if "Date" not in df.columns or "Weight" not in df.columns:
            st.error("Invalid data format")
            return False
            
        # Convert Date column to datetime if it's not already
        df["Date"] = pd.to_datetime(df["Date"])
        
        # Sort by date
        df = df.sort_values("Date")
        
        # Round weight to 2 decimal places
        df["Weight"] = df["Weight"].round(2)
        
        # Save to CSV
        df.to_csv(data_file, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving weight data: {str(e)}")
        return False

def health_dashboard_page(username):
    """
    Display and handle the health dashboard functionality.
    """
    # Add container for better centering
    st.markdown("""
        <div style="max-width: 1000px; margin: 0 auto; padding: 2rem;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">
                    🏥 Health Dashboard
                </h1>
            </div>
    """, unsafe_allow_html=True)
    
    # Back button at the top
    if st.button("← Back to Main Page", key="back_to_main_btn", use_container_width=True):
        st.session_state["show_health_dashboard"] = False
        st.rerun()
    
    # Load user data
    data_file = get_user_file(username)
    try:
        df = pd.read_csv(data_file)
        current_weight = df["Weight"].iloc[-1] if not df.empty else None
    except:
        current_weight = None
    
    # Load or get height
    height_file = f"height_{username}.txt"
    try:
        if os.path.exists(height_file):
            with open(height_file, "r") as f:
                height = float(f.read().strip())
        else:
            height = None
    except:
        height = None
    
    # Height input section
    st.markdown("""
        <div class="section-container">
            <h2>📏 Your Height</h2>
    """, unsafe_allow_html=True)
    
    if height is None:
        st.info("Please enter your height to calculate BMI and other health metrics.")
        col1, col2 = st.columns([3, 1])
        with col1:
            height_input = st.number_input("Height (cm)", 
                                         min_value=100, 
                                         max_value=250, 
                                         value=170,
                                         step=1,
                                         format="%d",
                                         key="initial_height")
        with col2:
            if st.button("Save Height", key="save_height_btn", use_container_width=True):
                with open(height_file, "w") as f:
                    f.write(str(int(height_input)))
                st.success("✅ Height saved successfully!")
                time.sleep(1)
                st.rerun()
    else:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown(f"<h3 style='text-align: center;'>Current Height: {int(height)} cm</h3>", unsafe_allow_html=True)
        with col2:
            new_height = st.number_input("New Height (cm)", 
                                       min_value=100, 
                                       max_value=250, 
                                       value=int(height), 
                                       step=1,
                                       format="%d",
                                       key="update_height")
        with col3:
            if st.button("Update", key="update_height_btn", use_container_width=True):
                with open(height_file, "w") as f:
                    f.write(str(int(new_height)))
                st.success("✅ Height updated successfully!")
                time.sleep(1)
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # BMI Calculator Section
    if height is not None and current_weight is not None:
        bmi = current_weight / ((height/100) ** 2)
        bmi_category = ""
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif 18.5 <= bmi < 25:
            bmi_category = "Normal weight"
        elif 25 <= bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"
        
        healthy_weight_min = 18.5 * ((height/100) ** 2)
        healthy_weight_max = 24.9 * ((height/100) ** 2)
        
        st.markdown("""
            <div class="section-container">
                <h2>⚖️ BMI Analysis</h2>
                <div style="padding: 1rem 0;">
        """, unsafe_allow_html=True)
        
        # First row with BMI and Category
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div style="text-align: center; margin-bottom: 1.5rem;">
                    <p style="font-size: 1rem; color: var(--text-color); opacity: 0.8; margin-bottom: 0.5rem;">Current BMI</p>
                    <h2 style="font-size: 2.5rem; margin: 0; color: var(--primary-color);">{bmi:.1f}</h2>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="text-align: center; margin-bottom: 1.5rem;">
                    <p style="font-size: 1rem; color: var(--text-color); opacity: 0.8; margin-bottom: 0.5rem;">Category</p>
                    <h2 style="font-size: 2rem; margin: 0; color: var(--text-color);">{bmi_category}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        # Divider
        st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
        
        # Healthy Weight Range Section
        st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem 0;">
                <p style="font-size: 1.1rem; color: var(--text-color); opacity: 0.8; margin-bottom: 1rem;">
                    Healthy Weight Range for Your Height
                </p>
                <div style="display: flex; justify-content: center; align-items: center; gap: 1rem;">
                    <h3 style="font-size: 1.8rem; margin: 0; color: var(--text-color);">
                        {healthy_weight_min:.1f} kg - {healthy_weight_max:.1f} kg
                    </h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Body Fat Calculator Section
    st.markdown("""
        <div class="section-container">
            <h2>📊 Body Fat Calculator</h2>
            <p style="text-align: center; margin-bottom: 1rem;">Using the US Navy Method</p>
    """, unsafe_allow_html=True)
    
    if "show_bodyfat_calc" not in st.session_state:
        st.session_state.show_bodyfat_calc = False
    
    if not st.session_state.show_bodyfat_calc:
        if st.button("Calculate My Body Fat %", key="calc_bodyfat_btn", use_container_width=True):
            st.session_state.show_bodyfat_calc = True
            st.rerun()
    else:
        with st.form("bodyfat_form"):
            gender = st.radio("Gender", ["Male", "Female"])
            height_cm = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
            neck_cm = st.number_input("Neck Circumference (cm)", min_value=20.0, max_value=60.0, value=40.0, step=0.1)
            waist_cm = st.number_input("Waist Circumference (cm)", min_value=50.0, max_value=200.0, value=80.0, step=0.1)
            if gender == "Female":
                hip_cm = st.number_input("Hip Circumference (cm)", min_value=50.0, max_value=200.0, value=90.0, step=0.1)
            
            submitted = st.form_submit_button("Calculate Body Fat %")
            
            if submitted:
                if gender == "Male":
                    body_fat = 495 / (1.0324 - 0.19077 * math.log10(waist_cm - neck_cm) + 0.15456 * math.log10(height_cm)) - 450
                else:
                    body_fat = 495 / (1.29579 - 0.35004 * math.log10(waist_cm + hip_cm - neck_cm) + 0.22100 * math.log10(height_cm)) - 450
                
                body_fat = round(body_fat, 1)
                
                # Determine body fat category
                if gender == "Male":
                    if body_fat < 6:
                        category = "Essential Fat"
                    elif 6 <= body_fat < 13:
                        category = "Athletes"
                    elif 13 <= body_fat < 17:
                        category = "Fitness"
                    elif 17 <= body_fat < 25:
                        category = "Average"
                    else:
                        category = "Obese"
                else:
                    if body_fat < 14:
                        category = "Essential Fat"
                    elif 14 <= body_fat < 21:
                        category = "Athletes"
                    elif 21 <= body_fat < 25:
                        category = "Fitness"
                    elif 25 <= body_fat < 32:
                        category = "Average"
                    else:
                        category = "Obese"
                
                st.markdown(f"""
                    <div style="text-align: center; margin-top: 1rem;">
                        <h3>Your Body Fat Percentage</h3>
                        <p style="font-size: 2rem; color: var(--primary-color);">{body_fat}%</p>
                        <p style="font-size: 1.2rem;">Category: {category}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        if st.button("Close Calculator", key="close_calc_btn", use_container_width=True):
            st.session_state.show_bodyfat_calc = False
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def running_assistant_page(username):
    """
    Display and handle the running assistant functionality.
    """
    # Add container for better centering
    st.markdown("""
        <div style="max-width: 1000px; margin: 0 auto; padding: 2rem;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">
                    🏃🏽 Running Assistant
                </h1>
            </div>
    """, unsafe_allow_html=True)
    
    # Back button at the top
    if st.button("← Back to Main Page", key="back_to_main_btn", use_container_width=True):
        st.session_state["show_running_assistant"] = False
        st.rerun()

    # Personal Records Section
    st.markdown("""
        <div class="section-container">
            <h2>🏆 Personal Records</h2>
    """, unsafe_allow_html=True)

    with st.expander("📊 Enter Your Personal Records"):
        # Create columns for different distances
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distance")
            has_5k = st.checkbox("5K")
            has_10k = st.checkbox("10K")
            has_hm = st.checkbox("Half Marathon")
            has_fm = st.checkbox("Full Marathon")
            has_ultra = st.checkbox("Ultra (50K+)")
            
        with col2:
            st.subheader("Best Time (hh:mm:ss)")
            if has_5k:
                time_5k = st.text_input("5K Time", placeholder="00:25:00")
            if has_10k:
                time_10k = st.text_input("10K Time", placeholder="00:50:00")
            if has_hm:
                time_hm = st.text_input("Half Marathon Time", placeholder="01:45:00")
            if has_fm:
                time_fm = st.text_input("Full Marathon Time", placeholder="03:45:00")
            if has_ultra:
                time_ultra = st.text_input("Ultra Time", placeholder="06:00:00")

    # Training Pace Calculator
    st.markdown("""
        <div class="section-container" style="margin-top: 2rem;">
            <h2>⚡ Training Pace Calculator</h2>
    """, unsafe_allow_html=True)

    with st.expander("Calculate Your Training Paces"):
        st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <p>Enter your recent race time to calculate your training paces</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            race_distance = st.selectbox("Select Race Distance", ["5K", "10K", "Half Marathon", "Full Marathon"])
            race_time = st.text_input("Race Time (hh:mm:ss)", placeholder="00:25:00")
        
        if race_time and len(race_time.split(":")) == 3:
            try:
                h, m, s = map(int, race_time.split(":"))
                total_seconds = h * 3600 + m * 60 + s
                
                # Calculate paces based on race time
                if race_distance == "5K":
                    base_distance = 5
                elif race_distance == "10K":
                    base_distance = 10
                elif race_distance == "Half Marathon":
                    base_distance = 21.1
                else:
                    base_distance = 42.2

                # Calculate paces
                race_pace = total_seconds / base_distance
                easy_pace = race_pace * 1.3  # 30% slower than race pace
                tempo_pace = race_pace * 1.1  # 10% slower than race pace
                interval_pace = race_pace * 0.9  # 10% faster than race pace
                recovery_pace = race_pace * 1.4  # 40% slower than race pace

                # Display paces
                st.markdown("""
                    <div style="text-align: center; margin-top: 1rem;">
                        <h3>Your Training Paces (per km)</h3>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1rem;">
                            <div style="background: var(--secondary-bg); padding: 1rem; border-radius: 8px;">
                                <p style="color: var(--primary-color); font-weight: bold;">Easy Pace</p>
                                <p>{:.1f} min/km</p>
                            </div>
                            <div style="background: var(--secondary-bg); padding: 1rem; border-radius: 8px;">
                                <p style="color: var(--primary-color); font-weight: bold;">Tempo Pace</p>
                                <p>{:.1f} min/km</p>
                            </div>
                            <div style="background: var(--secondary-bg); padding: 1rem; border-radius: 8px;">
                                <p style="color: var(--primary-color); font-weight: bold;">Interval Pace</p>
                                <p>{:.1f} min/km</p>
                            </div>
                            <div style="background: var(--secondary-bg); padding: 1rem; border-radius: 8px;">
                                <p style="color: var(--primary-color); font-weight: bold;">Recovery Pace</p>
                                <p>{:.1f} min/km</p>
                            </div>
                        </div>
                    </div>
                """.format(
                    easy_pace/60,
                    tempo_pace/60,
                    interval_pace/60,
                    recovery_pace/60
                ), unsafe_allow_html=True)

            except:
                st.error("Please enter time in format HH:MM:SS")

    # Running Form Guide
    st.markdown("""
        <div class="section-container" style="margin-top: 2rem;">
            <h2>🎯 Running Form Guide</h2>
    """, unsafe_allow_html=True)

    with st.expander("Learn Proper Running Form"):
        st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h3>Key Elements of Good Running Form</h3>
            </div>
        """, unsafe_allow_html=True)

        # Create tabs for different aspects of running form
        tab1, tab2, tab3 = st.tabs(["Posture", "Foot Strike", "Arm Movement"])
        
        with tab1:
            st.markdown("""
                <div style="text-align: center;">
                    <h4>Proper Running Posture</h4>
                    <p>• Keep your head up and eyes forward</p>
                    <p>• Maintain a straight back</p>
                    <p>• Lean slightly forward from ankles</p>
                    <p>• Keep shoulders relaxed</p>
                    <p>• Engage core muscles</p>
                </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
                <div style="text-align: center;">
                    <h4>Foot Strike</h4>
                    <p>• Land mid-foot, not on heel</p>
                    <p>• Keep feet under your body</p>
                    <p>• Quick, light steps</p>
                    <p>• Avoid overstriding</p>
                    <p>• Maintain cadence of 170-180 steps/minute</p>
                </div>
            """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
                <div style="text-align: center;">
                    <h4>Arm Movement</h4>
                    <p>• Keep arms at 90-degree angle</p>
                    <p>• Swing arms forward and back</p>
                    <p>• Don't cross arms over body</p>
                    <p>• Keep hands relaxed</p>
                    <p>• Maintain shoulder stability</p>
                </div>
            """, unsafe_allow_html=True)

    # Nutrition Guide for North Indian Weather
    st.markdown("""
        <div class="section-container" style="margin-top: 2rem;">
            <h2>🍎 Nutrition Guide</h2>
    """, unsafe_allow_html=True)

    with st.expander("Nutrition Tips for North Indian Weather"):
        st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h3>Seasonal Nutrition Guide</h3>
            </div>
        """, unsafe_allow_html=True)

        # Create tabs for different seasons
        tab1, tab2, tab3 = st.tabs(["Summer", "Monsoon", "Winter"])
        
        with tab1:
            st.markdown("""
                <div style="text-align: center;">
                    <h4>Summer Running Nutrition</h4>
                    <p>• Hydrate well before, during, and after runs</p>
                    <p>• Electrolyte-rich drinks (nimbu pani, coconut water)</p>
                    <p>• Light, easily digestible pre-run meals</p>
                    <p>• Fruits high in water content (watermelon, muskmelon)</p>
                    <p>• Avoid heavy, spicy foods</p>
                    <p>• Early morning or evening runs recommended</p>
                </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
                <div style="text-align: center;">
                    <h4>Monsoon Running Nutrition</h4>
                    <p>• Warm, light meals before running</p>
                    <p>• Ginger tea for immunity</p>
                    <p>• Vitamin C rich foods</p>
                    <p>• Stay hydrated despite humidity</p>
                    <p>• Avoid street food</p>
                    <p>• Post-run warm beverages</p>
                </div>
            """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
                <div style="text-align: center;">
                    <h4>Winter Running Nutrition</h4>
                    <p>• Warm pre-run meals</p>
                    <p>• Hot beverages (green tea, coffee)</p>
                    <p>• Energy-rich foods (nuts, seeds)</p>
                    <p>• Vitamin D rich foods</p>
                    <p>• Stay hydrated despite cold weather</p>
                    <p>• Post-run warm meals</p>
                </div>
            """, unsafe_allow_html=True)

    # Target Pace/Goal Setting
    st.markdown("""
        <div class="section-container" style="margin-top: 2rem;">
            <h2>🎯 Set Your Running Goals</h2>
    """, unsafe_allow_html=True)

    with st.expander("Set and Track Your Goals"):
        st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h3>Set Your Target Pace and Goals</h3>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            target_distance = st.selectbox("Target Distance", ["5K", "10K", "Half Marathon", "Full Marathon"])
            target_time = st.text_input("Target Time (hh:mm:ss)", placeholder="00:25:00")
            target_date = st.date_input("Target Date")
        
        if target_time and len(target_time.split(":")) == 3:
            try:
                h, m, s = map(int, target_time.split(":"))
                total_seconds = h * 3600 + m * 60 + s
                
                # Calculate target pace
                if target_distance == "5K":
                    distance = 5
                elif target_distance == "10K":
                    distance = 10
                elif target_distance == "Half Marathon":
                    distance = 21.1
                else:
                    distance = 42.2
                
                target_pace = total_seconds / distance
                
                # Calculate days until target
                days_until = (target_date - datetime.now().date()).days
                
                st.markdown(f"""
                    <div style="text-align: center; margin-top: 1rem;">
                        <h3>Your Goal Details</h3>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1rem;">
                            <div style="background: var(--secondary-bg); padding: 1rem; border-radius: 8px;">
                                <p style="color: var(--primary-color); font-weight: bold;">Target Pace</p>
                                <p>{target_pace/60:.1f} min/km</p>
                            </div>
                            <div style="background: var(--secondary-bg); padding: 1rem; border-radius: 8px;">
                                <p style="color: var(--primary-color); font-weight: bold;">Days Until Goal</p>
                                <p>{days_until} days</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Training recommendations based on days until target
                if days_until > 0:
                    st.markdown("""
                        <div style="text-align: center; margin-top: 1rem;">
                            <h4>Training Recommendations</h4>
                            <p>• Run 3-4 times per week</p>
                            <p>• Include one long run weekly</p>
                            <p>• Add interval training sessions</p>
                            <p>• Rest days are important</p>
                            <p>• Stay consistent with training</p>
                        </div>
                    """, unsafe_allow_html=True)

            except:
                st.error("Please enter time in format HH:MM:SS")

    # Race Time Predictor
    st.markdown("""
        <div class="section-container" style="margin-top: 2rem;">
            <h2>⏱️ Race Time Predictor</h2>
    """, unsafe_allow_html=True)

    with st.expander("Predict Your Race Times"):
        st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <p>Enter your recent race time to predict your performance at other distances</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Enter Your Recent Race")
            race_distance = st.selectbox("Distance", ["5K", "10K", "Half Marathon", "Full Marathon"])
            race_time = st.text_input("Time (hh:mm:ss)", placeholder="00:25:00")
        
        with col2:
            st.subheader("Predicted Times")
            if race_time and len(race_time.split(":")) == 3:
                try:
                    # Convert time to seconds for calculations
                    h, m, s = map(int, race_time.split(":"))
                    total_seconds = h * 3600 + m * 60 + s
                    
                    # Calculate predicted times using common race time prediction formulas
                    if race_distance == "5K":
                        base_seconds = total_seconds
                        base_distance = 5
                    elif race_distance == "10K":
                        base_seconds = total_seconds
                        base_distance = 10
                    elif race_distance == "Half Marathon":
                        base_seconds = total_seconds
                        base_distance = 21.1
                    else:
                        base_seconds = total_seconds
                        base_distance = 42.2

                    # Calculate predictions using a common race prediction formula
                    def predict_time(target_distance):
                        return base_seconds * (target_distance/base_distance) ** 1.06

                    # Display predictions
                    distances = [5, 10, 21.1, 42.2]
                    names = ["5K", "10K", "Half Marathon", "Full Marathon"]
                    
                    for d, n in zip(distances, names):
                        if d != base_distance:  # Don't predict the input distance
                            predicted_seconds = predict_time(d)
                            hours = int(predicted_seconds // 3600)
                            minutes = int((predicted_seconds % 3600) // 60)
                            seconds = int(predicted_seconds % 60)
                            st.write(f"{n}: {hours:02d}:{minutes:02d}:{seconds:02d}")
                except:
                    st.error("Please enter time in format HH:MM:SS")
            else:
                st.info("Enter your recent race time to see predictions")

    # Training Plans Section
    st.markdown("""
        <div class="section-container" style="margin-top: 2rem;">
            <h2>📋 Free Training Plans</h2>
            <p style="text-align: center; margin-bottom: 1rem;">Click on the links below to access free training plans</p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="text-align: center;">
                <h3>10K Plans</h3>
                <ul style="list-style-type: none; padding: 0;">
                    <li><a href="https://www.halhigdon.com/training-programs/10k-training/novice-10k/" target="_blank">Hal Higdon's Novice 10K</a></li>
                    <li><a href="https://www.nike.com/pdf/Nike-Run-Club-10K-Training-Plan.pdf" target="_blank">Nike 10K Plan (PDF)</a></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <h3>Half Marathon Plans</h3>
                <ul style="list-style-type: none; padding: 0;">
                    <li><a href="https://www.halhigdon.com/training-programs/half-marathon-training/novice-1-half-marathon/" target="_blank">Hal Higdon's Novice HM</a></li>
                    <li><a href="https://www.nike.com/pdf/Nike-Run-Club-Half-Marathon-Training-Plan-Audio-Guided-Runs.pdf" target="_blank">Nike Half Marathon Plan (PDF)</a></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="text-align: center;">
                <h3>Marathon Plans</h3>
                <ul style="list-style-type: none; padding: 0;">
                    <li><a href="https://www.halhigdon.com/training-programs/marathon-training/novice-1-marathon/" target="_blank">Hal Higdon's Novice Marathon</a></li>
                    <li><a href="https://www.nike.com/pdf/Nike-Run-Club-Marathon-Training-Plan.pdf" target="_blank">Nike Marathon Plan (PDF)</a></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

def calorie_calculator_page(username):
    """
    Display and handle the calorie calculator functionality.
    """
    # Add container for better centering
    st.markdown("""
        <div style="max-width: 1000px; margin: 0 auto; padding: 2rem;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">
                    🍽️ Fat Calc
                </h1>
            </div>
    """, unsafe_allow_html=True)
    
    # Back button at the top
    if st.button("← Back to Main Page", key="back_to_main_btn", use_container_width=True):
        st.session_state["show_calorie_calculator"] = False
        st.rerun()
    
    # Load user data
    data_file = get_user_file(username)
    try:
        df = pd.read_csv(data_file)
        current_weight = df["Weight"].iloc[-1] if not df.empty else None
    except:
        current_weight = None
    
    # Load or get height
    height_file = f"height_{username}.txt"
    try:
        if os.path.exists(height_file):
            with open(height_file, "r") as f:
                height = float(f.read().strip())
        else:
            height = None
    except:
        height = None
    
    # BMR Calculator Section
    st.markdown("""
        <div class="section-container">
            <h2>⚖️ Your Basal Metabolic Rate (BMR)</h2>
    """, unsafe_allow_html=True)
    
    if height is None or current_weight is None:
        st.warning("⚠️ Please complete your profile in the Health Dashboard to calculate your BMR.")
    else:
        # Initialize session state for user inputs if not exists
        if "user_age" not in st.session_state:
            st.session_state.user_age = 30
        if "user_gender" not in st.session_state:
            st.session_state.user_gender = "Male"
        if "user_activity_level" not in st.session_state:
            st.session_state.user_activity_level = "Moderately active (moderate exercise/sports 3-5 days/week)"
        if "user_target_weight" not in st.session_state:
            st.session_state.user_target_weight = current_weight - 5.0
        if "user_fat_loss_rate" not in st.session_state:
            st.session_state.user_fat_loss_rate = "Moderate (0.5 kg/week)"
        
        # Get age from user with session state
        age = st.number_input("Enter your age", 
                            min_value=15, 
                            max_value=100, 
                            value=st.session_state.user_age,
                            key="age_input")
        st.session_state.user_age = age
        
        gender = st.radio("Select your gender", 
                         ["Male", "Female"], 
                         index=0 if st.session_state.user_gender == "Male" else 1,
                         key="gender_input")
        st.session_state.user_gender = gender
        
        if gender == "Male":
            bmr = (10 * current_weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * current_weight) + (6.25 * height) - (5 * age) - 161
        
        # Display BMR with nice formatting
        st.markdown(f"""
            <div style="text-align: center; margin: 1.5rem 0;">
                <p style="font-size: 1.2rem; color: var(--text-color); opacity: 0.8; margin-bottom: 0.5rem;">Your BMR</p>
                <h2 style="font-size: 2.5rem; margin: 0; color: var(--primary-color);">{int(bmr)}</h2>
                <p style="font-size: 1.1rem; color: var(--text-color); opacity: 0.8;">calories per day</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Activity Level Multiplier with session state
        activity_level = st.selectbox(
            "Select your activity level",
            ["Sedentary (little or no exercise)",
             "Lightly active (light exercise/sports 1-3 days/week)",
             "Moderately active (moderate exercise/sports 3-5 days/week)",
             "Very active (hard exercise/sports 6-7 days/week)",
             "Extra active (very hard exercise/sports & physical job or 2x training)"],
            index=["Sedentary (little or no exercise)",
                   "Lightly active (light exercise/sports 1-3 days/week)",
                   "Moderately active (moderate exercise/sports 3-5 days/week)",
                   "Very active (hard exercise/sports 6-7 days/week)",
                   "Extra active (very hard exercise/sports & physical job or 2x training)"].index(st.session_state.user_activity_level)
        )
        st.session_state.user_activity_level = activity_level
        
        activity_multipliers = {
            "Sedentary (little or no exercise)": 1.2,
            "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
            "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
            "Very active (hard exercise/sports 6-7 days/week)": 1.725,
            "Extra active (very hard exercise/sports & physical job or 2x training)": 1.9
        }
        
        tdee = bmr * activity_multipliers[activity_level]
        
        st.markdown(f"""
            <div style="text-align: center; margin: 1.5rem 0;">
                <p style="font-size: 1.2rem; color: var(--text-color); opacity: 0.8; margin-bottom: 0.5rem;">Your Total Daily Energy Expenditure (TDEE)</p>
                <h2 style="font-size: 2.5rem; margin: 0; color: var(--primary-color);">{int(tdee)}</h2>
                <p style="font-size: 1.1rem; color: var(--text-color); opacity: 0.8;">calories per day</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Calorie Requirements for Fat Loss Section
    st.markdown("""
        <div class="section-container">
            <h2>🎯 Calorie Requirements for Fat Loss</h2>
    """, unsafe_allow_html=True)
    
    with st.expander("Calculate Your Fat Loss Calories"):
        st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <p>Select your desired rate of fat loss</p>
            </div>
        """, unsafe_allow_html=True)
        
        fat_loss_rate = st.select_slider(
            "Rate of Fat Loss",
            options=["Slow (0.25 kg/week)", "Moderate (0.5 kg/week)", "Aggressive (1 kg/week)"],
            value=st.session_state.user_fat_loss_rate
        )
        st.session_state.user_fat_loss_rate = fat_loss_rate
        
        if fat_loss_rate == "Slow (0.25 kg/week)":
            calorie_deficit = 275  # 0.25 kg = 275 calories per day
        elif fat_loss_rate == "Moderate (0.5 kg/week)":
            calorie_deficit = 550  # 0.5 kg = 550 calories per day
        else:  # Aggressive
            calorie_deficit = 1100  # 1 kg = 1100 calories per day
        
        if 'tdee' in locals():
            target_calories = tdee - calorie_deficit
            
            st.markdown(f"""
                <div style="text-align: center; margin: 1.5rem 0;">
                    <p style="font-size: 1.2rem; color: var(--text-color); opacity: 0.8; margin-bottom: 0.5rem;">Recommended Daily Calories for {fat_loss_rate}</p>
                    <h2 style="font-size: 2.5rem; margin: 0; color: var(--primary-color);">{int(target_calories)}</h2>
                    <p style="font-size: 1.1rem; color: var(--text-color); opacity: 0.8;">calories per day</p>
                    <p style="font-size: 1rem; color: var(--text-color); opacity: 0.8; margin-top: 0.5rem;">(Deficit: {calorie_deficit} calories)</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Please complete your profile in the Health Dashboard to calculate your calorie requirements.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Fat Loss Timeline Calculator
    st.markdown("""
        <div class="section-container">
            <h2>📅 Fat Loss Timeline Calculator</h2>
    """, unsafe_allow_html=True)
    
    with st.expander("Calculate Your Fat Loss Timeline"):
        if current_weight is not None:
            target_weight = st.number_input(
                "Enter your target weight (kg)",
                min_value=30.0,
                max_value=200.0,
                value=st.session_state.user_target_weight,
                step=0.1
            )
            st.session_state.user_target_weight = target_weight
            
            if 'tdee' in locals():
                daily_calories = st.number_input(
                    "Enter your target daily calories",
                    min_value=1000,
                    max_value=5000,
                    value=int(target_calories) if 'target_calories' in locals() else int(tdee - 500),
                    step=50
                )
            
            if 'tdee' in locals():
                daily_deficit = tdee - daily_calories
                kg_to_lose = current_weight - target_weight
                
                if kg_to_lose > 0:
                    # Calculate time to reach goal
                    # 1 kg of fat = 7700 calories
                    days_to_goal = int((kg_to_lose * 7700) / daily_deficit)
                    target_date = datetime.now() + timedelta(days=days_to_goal)
                    
                    st.markdown(f"""
                        <div style="text-align: center; margin: 1.5rem 0;">
                            <h3>Estimated Timeline</h3>
                            <p style="font-size: 1.2rem; margin: 0.5rem 0;">Weight to lose: {kg_to_lose:.1f} kg</p>
                            <p style="font-size: 1.2rem; margin: 0.5rem 0;">Daily deficit: {daily_deficit} calories</p>
                            <p style="font-size: 1.2rem; margin: 0.5rem 0;">Estimated days to goal: {days_to_goal}</p>
                            <p style="font-size: 1.2rem; margin: 0.5rem 0;">Target date: {target_date.strftime('%d %B %Y')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Add progress visualization
                    fig, ax = plt.subplots(figsize=(10, 6))
                    plt.style.use('dark_background')
                    
                    # Create date range
                    dates = pd.date_range(start=datetime.now(), periods=days_to_goal + 1, freq='D')
                    weights = [current_weight - (daily_deficit * i / 7700) for i in range(len(dates))]
                    
                    # Plot the line
                    ax.plot(dates, weights, color='#00B4D8', linewidth=2.5, label='Projected Weight')
                    
                    # Add current and target weight markers
                    ax.scatter(datetime.now(), current_weight, color='#00B4D8', s=100, label='Current Weight')
                    ax.scatter(target_date, target_weight, color='#FFB700', s=100, label='Target Weight')
                    
                    # Customize the plot
                    ax.set_title('Projected Weight Loss Timeline', fontsize=14, pad=20)
                    ax.set_xlabel('Date', fontsize=12)
                    ax.set_ylabel('Weight (kg)', fontsize=12)
                    ax.grid(True, linestyle='--', alpha=0.3)
                    ax.legend()
                    
                    # Rotate x-axis labels for better readability
                    plt.xticks(rotation=45)
                    
                    # Adjust layout
                    plt.tight_layout()
                    
                    # Display the plot
                    st.pyplot(fig)
                else:
                    st.warning("Your target weight is higher than or equal to your current weight.")
        else:
            st.warning("Please complete your profile in the Health Dashboard to calculate your timeline.")
    
    # Tips section moved outside the timeline calculator expander
    st.markdown("""
        <div style="margin-top: 2rem;">
            <h3 style="text-align: center;">💡 Tips for Success</h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("View Tips and Guidelines"):
        st.markdown("""
            #### 📊 Tracking Tips
            1. **Consistent Calorie Tracking**
               - Use a food diary or app
               - Weigh and measure portions
               - Log everything, even small snacks
            
            2. **Meal Planning**
               - Plan meals in advance
               - Prepare healthy snacks
               - Keep healthy options readily available
            
            3. **Mindful Eating**
               - Eat slowly and savor each bite
               - Listen to hunger cues
               - Avoid emotional eating
            
            4. **Exercise Integration**
               - Combine cardio and strength training
               - Stay active throughout the day
               - Track non-exercise activity
            
            5. **Progress Monitoring**
               - Take progress photos
               - Measure body circumferences
               - Track strength gains
            
            #### ⚠️ Important Notes
            - This is an estimate based on mathematical calculations
            - Individual results may vary
            - Consult healthcare providers before starting any diet
            - Focus on sustainable habits over quick fixes
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add Methodology Explanation Section
    st.markdown("""
        <div class="section-container">
            <h2>🧮 How We Calculate Everything</h2>
    """, unsafe_allow_html=True)
    
    with st.expander("Learn about the calculations"):
        st.markdown("""
            #### 1. BMR (Basal Metabolic Rate)
            We use the **Mifflin-St Jeor Equation** because it's considered the most accurate for most people:
            - For Men: BMR = (10 × weight) + (6.25 × height) - (5 × age) + 5
            - For Women: BMR = (10 × weight) + (6.25 × height) - (5 × age) - 161
            
            Example: A 30-year-old woman who is 165cm tall and weighs 70kg
            - BMR = (10 × 70) + (6.25 × 165) - (5 × 30) - 161
            - BMR = 700 + 1031.25 - 150 - 161
            - BMR ≈ 1420 calories/day
            
            #### 2. TDEE (Total Daily Energy Expenditure)
            We multiply your BMR by an activity factor:
            - Sedentary: BMR × 1.2
            - Lightly active: BMR × 1.375
            - Moderately active: BMR × 1.55
            - Very active: BMR × 1.725
            - Extra active: BMR × 1.9
            
            #### 3. Fat Loss Calories
            We create different calorie deficits based on your goals:
            - Slow (0.25 kg/week): 275 calorie deficit
            - Moderate (0.5 kg/week): 550 calorie deficit
            - Aggressive (1 kg/week): 1100 calorie deficit
            
            #### 4. Timeline Calculations
            To estimate how long it will take to reach your goal:
            1. Calculate total kg to lose = Current weight - Target weight
            2. Convert kg to calories (1 kg of fat = 7700 calories)
            3. Divide by your daily calorie deficit
            
            Example: To lose 5kg with a 550 calorie daily deficit
            - Total calories to burn = 5kg × 7700 = 38,500 calories
            - Days needed = 38,500 ÷ 550 = 70 days
            
            #### Important Notes
            - These are estimates based on averages
            - Individual results can vary based on:
              - Genetics
              - Sleep quality
              - Stress levels
              - Medical conditions
              - Medications
            - Always consult with healthcare providers for personalized advice
        """)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def get_weekly_averages(username):
    """
    Calculate weekly averages for the user's weight data.
    Weeks start on Monday and end on Sunday.
    Current week average is calculated dynamically based on entries up to current day.
    
    Args:
        username (str): Username to get data for
        
    Returns:
        dict: Dictionary containing current and previous week's averages
    """
    try:
        # Load data from CSV
        data_file = get_user_file(username)
        if not os.path.exists(data_file):
            return {"current_week_avg": None, "previous_week_avg": None}
        
        # Read the CSV file and ensure it's not empty
        df = pd.read_csv(data_file)
        if df.empty:
            return {"current_week_avg": None, "previous_week_avg": None}
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Get today's date and calculate week boundaries
        today = pd.Timestamp.now().normalize()  # Get today's date without time
        current_week_start = today - pd.Timedelta(days=today.weekday())  # Monday of current week
        previous_week_start = current_week_start - pd.Timedelta(weeks=1)  # Monday of previous week
        previous_week_end = current_week_start - pd.Timedelta(days=1)  # Sunday of previous week
        
        # Debug prints
        print(f"Today: {today}")
        print(f"Current week start: {current_week_start}")
        print(f"Previous week start: {previous_week_start}")
        print(f"Previous week end: {previous_week_end}")
        
        # Get current week's data (from Monday to today)
        current_week_data = df[
            (df['Date'] >= current_week_start) & 
            (df['Date'] <= today)
        ]
        
        # Get previous week's data (from Monday to Sunday)
        previous_week_data = df[
            (df['Date'] >= previous_week_start) & 
            (df['Date'] <= previous_week_end)
        ]
        
        # Debug prints
        print(f"Current week data:\n{current_week_data}")
        print(f"Previous week data:\n{previous_week_data}")
        
        # Calculate averages
        current_week_avg = None if current_week_data.empty else current_week_data['Weight'].mean()
        previous_week_avg = None if previous_week_data.empty else previous_week_data['Weight'].mean()
        
        # Round averages to 2 decimal places if they exist
        return {
            "current_week_avg": round(current_week_avg, 2) if current_week_avg is not None else None,
            "previous_week_avg": round(previous_week_avg, 2) if previous_week_avg is not None else None
        }
        
    except Exception as e:
        print(f"Error in get_weekly_averages: {str(e)}")
        return {"current_week_avg": None, "previous_week_avg": None}

def calculate_trend_analysis(username):
    """
    Calculate trend analysis including regression line for weight data.
    
    Args:
        username (str): Username to analyze data for
        
    Returns:
        dict: Dictionary containing trend analysis data and regression parameters
    """
    try:
        # Load data from CSV
        data_file = get_user_file(username)
        if not os.path.exists(data_file):
            return None
        
        df = pd.read_csv(data_file)
        if df.empty:
            return None
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Create numeric X values (days since start)
        df['Days'] = (df['Date'] - df['Date'].min()).dt.days
        
        # Calculate regression line
        X = df['Days'].values.reshape(-1, 1)
        y = df['Weight'].values
        
        from sklearn.linear_model import LinearRegression
        reg = LinearRegression().fit(X, y)
        
        # Generate trend line points
        trend_line = reg.predict(X)
        
        # Calculate R-squared
        r_squared = reg.score(X, y)
        
        # Calculate daily weight change rate
        daily_change = reg.coef_[0]
        
        return {
            'dates': df['Date'],
            'weights': df['Weight'],
            'trend_line': trend_line,
            'r_squared': r_squared,
            'daily_change': daily_change
        }
    except Exception as e:
        print(f"Error in trend analysis: {str(e)}")
        return None

def data_nerds_page(username):
    """
    Display the Data for Nerds dashboard with advanced analytics.
    """
    # Page header
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤓 Data for Nerds</h1>
            <p style="font-size: 1.2rem;">Deep dive into your weight loss journey</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get weekly averages
    weekly_stats = get_weekly_averages(username)
    
    # Weekly comparison section
    with st.expander("📊 Weekly Average Comparison", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        # Previous Week Average
        with col1:
            prev_week_value = weekly_stats['previous_week_avg']
            st.metric(
                label="Previous Week Avg",
                value=f"{prev_week_value:.2f} kg" if prev_week_value is not None else "No data"
            )
        
        # Current Week Average (without delta)
        with col2:
            curr_week_value = weekly_stats['current_week_avg']
            st.metric(
                label="Current Week Avg",
                value=f"{curr_week_value:.2f} kg" if curr_week_value is not None else "No data"
            )
        
        # Net Weekly Change
        with col3:
            if curr_week_value is not None and prev_week_value is not None:
                change = curr_week_value - prev_week_value
                arrow_color = "green" if change < 0 else "red"
                arrow_symbol = "↓" if change < 0 else "↑"
                
                st.markdown(f"""
                    <div style="text-align: center;">
                        <p style="font-size: 1rem; margin-bottom: 0.5rem;">Net Weekly Change</p>
                        <p style="font-size: 1.8rem; font-weight: bold; color: {arrow_color}; margin: 0;">
                            {arrow_symbol} {abs(change):.2f} kg
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="text-align: center;">
                        <p style="font-size: 1rem; margin-bottom: 0.5rem;">Net Weekly Change</p>
                        <p style="font-size: 1.5rem; margin: 0;">No data</p>
                    </div>
                """, unsafe_allow_html=True)
    
    # Trend Analysis Section
    with st.expander("📈 Trend Analysis", expanded=True):
        trend_data = calculate_trend_analysis(username)
        
        if trend_data is not None:
            # Create interactive plot using plotly
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            fig = make_subplots(specs=[[{"secondary_y": False}]])
            
            # Add actual weight data
            fig.add_trace(
                go.Scatter(
                    x=trend_data['dates'],
                    y=trend_data['weights'],
                    mode='markers+lines',
                    name='Weight',
                    line=dict(color='#00B4D8', width=2),
                    marker=dict(size=8),
                    hovertemplate="Date: %{x}<br>Weight: %{y:.2f} kg<extra></extra>"
                )
            )
            
            # Add trend line
            fig.add_trace(
                go.Scatter(
                    x=trend_data['dates'],
                    y=trend_data['trend_line'],
                    mode='lines',
                    name='Trend',
                    line=dict(color='#FFB700', width=2, dash='dash'),
                    hovertemplate="Date: %{x}<br>Trend: %{y:.2f} kg<extra></extra>"
                )
            )
            
            # Update layout
            fig.update_layout(
                title={
                    'text': "Weight Trend Analysis",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                plot_bgcolor='rgba(10,25,47,0.1)',
                paper_bgcolor='rgba(10,25,47,0)',
                font=dict(color='#E6F1FF'),
                xaxis=dict(
                    title="Date",
                    gridcolor='rgba(35,53,84,0.5)',
                    showgrid=True
                ),
                yaxis=dict(
                    title="Weight (kg)",
                    gridcolor='rgba(35,53,84,0.5)',
                    showgrid=True
                ),
                hovermode='x unified',
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            
            # Display the plot
            st.plotly_chart(fig, use_container_width=True)
            
            # Display trend statistics
            col1, col2 = st.columns(2)
            
            with col1:
                daily_change = trend_data['daily_change']
                change_color = "green" if daily_change < 0 else "red"
                st.markdown(f"""
                    <div style="text-align: center;">
                        <p style="font-size: 1rem; margin-bottom: 0.5rem;">Average Daily Change</p>
                        <p style="font-size: 1.4rem; color: {change_color}; margin: 0;">
                            {daily_change:.3f} kg/day
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                r_squared = trend_data['r_squared']
                st.markdown(f"""
                    <div style="text-align: center;">
                        <p style="font-size: 1rem; margin-bottom: 0.5rem;">Trend Reliability (R²)</p>
                        <p style="font-size: 1.4rem; color: var(--primary-color); margin: 0;">
                            {r_squared:.3f}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Add interpretation
            st.markdown("""
                <div style="margin-top: 1rem; padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                    <p style="font-size: 1rem; margin-bottom: 0.5rem;">📊 Trend Interpretation</p>
                    <ul style="margin: 0; padding-left: 1.2rem;">
                        <li>The blue line shows your actual weight measurements</li>
                        <li>The yellow dashed line shows the overall trend</li>
                        <li>R² value closer to 1.0 indicates a more reliable trend</li>
                        <li>Hover over the graph to see detailed values</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Not enough data for trend analysis. Add more weight entries to see trends.")
    
    # Add Methodology Explanation Section (add this before the back button)
    with st.expander("🔬 Methodology & Technical Details"):
        st.markdown("""
            ### Understanding the Trend Analysis

            #### 1. Linear Regression 📐
            We use a statistical method called "Linear Regression" to find the best-fitting straight line through your weight measurements. Think of it like drawing a line that tries to get as close as possible to all your data points.

            **Technical Details:**  
            The equation used is: Weight = β₀ + β₁(Days) + ε  
            *Where:*
            - β₀ is the y-intercept (starting point)
            - β₁ is the slope (daily weight change)
            - ε is the error term
            
            #### 2. R-squared (R²) Value 📊
            R² measures how well the trend line fits your actual data. It ranges from 0 to 1:
            - R² = 1.0: Perfect fit (rare in real data)
            - R² = 0.7: Strong trend
            - R² = 0.5: Moderate trend
            - R² < 0.3: Weak trend

            **Technical Formula:**  
            R² = 1 - (SSres / SStot)
            - SSres: Sum of squared residuals (differences between actual and predicted values)
            - SStot: Total sum of squares (total variance in your weight)
            
            #### 3. Daily Weight Change Rate 📈
            This is the slope (β₁) of the regression line, showing how much weight changes per day on average.
            - Negative value: You're losing weight
            - Positive value: You're gaining weight
            - Example: -0.1 kg/day means you're losing 0.1 kg per day on average
            
            #### 4. Data Processing Steps 🔄
            1. Convert dates to numeric values (days since first measurement)
            2. Apply scikit-learn's LinearRegression model to calculate trend
            3. Generate trend line points for visualization
            4. Calculate confidence metrics (R²)
            
            #### 5. Visualization Details 🎨
            The graph uses Plotly for interactive visualization with:
            - Actual measurements: Blue dots with connecting lines
            - Trend line: Yellow dashed line showing the overall direction
            - Interactive hover: Shows exact values when you move your mouse over the graph
            - Unified hover mode: Aligns vertical hover line across all data points
            
            ---
            
            ##### 💡 Why This Matters
            This analysis helps you:
            - See your true progress beyond daily fluctuations
            - Understand if your weight loss/gain is statistically significant
            - Predict future trends if you maintain current habits
            - Make data-driven decisions about your fitness journey
            
            ##### ⚠️ Limitations
            Keep in mind:
            - Past trends don't guarantee future results
            - Weight naturally fluctuates day-to-day
            - Linear trends are simplified models of complex biological processes
            - More data points generally lead to more reliable trends
        """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Main Dashboard", key="back_btn"):
        st.session_state["show_data_nerds"] = False
        st.rerun()

def get_weight_entries(username):
    """
    Load weight entries for a given username from their data file.
    
    Args:
        username (str): Username to get entries for
        
    Returns:
        list: List of dictionaries containing date and weight entries
    """
    try:
        data_file = get_user_file(username)
        if os.path.exists(data_file):
            df = pd.read_csv(data_file)
            df["Date"] = pd.to_datetime(df["Date"])
            entries = [{"date": row["Date"], "weight": row["Weight"]} 
                      for _, row in df.iterrows()]
            return entries
        return []
    except Exception as e:
        st.error(f"Error loading weight entries: {str(e)}")
        return []

# --- Application Entry Point ---
if __name__ == "__main__":
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "show_signup" not in st.session_state:
        st.session_state["show_signup"] = False
    if "show_health_dashboard" not in st.session_state:
        st.session_state["show_health_dashboard"] = False
    if "show_running_assistant" not in st.session_state:
        st.session_state["show_running_assistant"] = False
    if "show_calorie_calculator" not in st.session_state:
        st.session_state["show_calorie_calculator"] = False
    if "show_data_nerds" not in st.session_state:
        st.session_state["show_data_nerds"] = False

    # Route to appropriate page
    if st.session_state["show_signup"]:
        signup_page()
    elif st.session_state["show_health_dashboard"]:
        health_dashboard_page(st.session_state["username"])
    elif st.session_state["show_running_assistant"]:
        running_assistant_page(st.session_state["username"])
    elif st.session_state["show_calorie_calculator"]:
        calorie_calculator_page(st.session_state["username"])
    elif st.session_state["show_data_nerds"]:
        data_nerds_page(st.session_state["username"])
    elif st.session_state["logged_in"]:
        fitness_tracker(st.session_state["username"])
    else:
        login_page()
