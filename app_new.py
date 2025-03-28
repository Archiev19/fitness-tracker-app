"""
Weight Tracker Application
=========================

A Streamlit-based web application for tracking personal fitness progress.
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
import json
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from storage_handler import StorageHandler

# Initialize storage handler
storage = StorageHandler()

# Configure Streamlit page
st.set_page_config(
    page_title="Fitness Tracker",
    page_icon="💪",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
    }
    .reportview-container {
        background: #FAFAFA;
    }
    </style>
""", unsafe_allow_html=True)

def load_users():
    """Load users from storage"""
    users_data = storage.load_data("users.json")
    if not users_data:
        return pd.DataFrame(columns=['username', 'email', 'password_hash'])
    return pd.DataFrame(users_data)

def save_users(users_df):
    """Save users to storage"""
    users_data = users_df.to_dict('records')
    storage.save_data(users_data, "users.json")

def get_user_data(username):
    """Get user's weight data"""
    data = storage.load_data(f"weights_{username}.json")
    if not data:
        return pd.DataFrame(columns=['date', 'weight'])
    return pd.DataFrame(data)

def save_user_data(username, df):
    """Save user's weight data"""
    storage.save_data(df.to_dict('records'), f"weights_{username}.json")

def get_goal_data(username):
    """Get user's goal data"""
    data = storage.load_data(f"goals_{username}.json")
    if not data:
        return None
    return data

def save_goal_data(username, goal_weight, target_date):
    """Save user's goal data"""
    data = {
        'goal_weight': goal_weight,
        'target_date': target_date.strftime('%Y-%m-%d')
    }
    storage.save_data(data, f"goals_{username}.json")

def login_page():
    """Display login page"""
    st.title("Welcome to Fitness Tracker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                users_df = load_users()
                user = users_df[
                    (users_df['email'] == email) & 
                    (users_df['password_hash'] == password)
                ]
                if not user.empty:
                    st.session_state.username = user.iloc[0]['username']
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    with col2:
        st.header("Sign Up")
        with st.form("signup_form"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Sign Up")
            
            if submit:
                if new_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    users_df = load_users()
                    if new_username in users_df['username'].values:
                        st.error("Username already exists!")
                    else:
                        new_user = pd.DataFrame({
                            'username': [new_username],
                            'email': [new_email],
                            'password_hash': [new_password]
                        })
                        users_df = pd.concat([users_df, new_user], ignore_index=True)
                        save_users(users_df)
                        st.success("Account created successfully!")
                        st.session_state.username = new_username
                        st.rerun()

def weight_tracker():
    """Display weight tracker page"""
    st.title("Weight Tracker")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Weight input form
        with st.form("weight_form"):
            weight = st.number_input("Enter your weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
            date = st.date_input("Date", datetime.now())
            submit = st.form_submit_button("Save Weight")
            
            if submit:
                df = get_user_data(st.session_state.username)
                new_entry = pd.DataFrame({
                    'date': [date.strftime('%Y-%m-%d')],
                    'weight': [weight]
                })
                df = pd.concat([df, new_entry], ignore_index=True)
                save_user_data(st.session_state.username, df)
                st.success("Weight saved successfully!")
                st.rerun()
        
        # Weight history chart
        df = get_user_data(st.session_state.username)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['weight'],
                mode='lines+markers',
                name='Weight'
            ))
            
            goal_data = get_goal_data(st.session_state.username)
            if goal_data:
                goal_weight = goal_data['goal_weight']
                fig.add_hline(
                    y=goal_weight,
                    line_dash="dash",
                    annotation_text=f"Goal: {goal_weight}kg"
                )
            
            fig.update_layout(
                title="Weight History",
                xaxis_title="Date",
                yaxis_title="Weight (kg)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Goal Setting")
        with st.form("goal_form"):
            goal_weight = st.number_input("Goal Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
            target_date = st.date_input("Target Date", min_value=datetime.now())
            submit = st.form_submit_button("Set Goal")
            
            if submit:
                save_goal_data(st.session_state.username, goal_weight, target_date)
                st.success("Goal set successfully!")
                st.rerun()

def main():
    """Main app logic"""
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if st.session_state.username is None:
        login_page()
    else:
        st.sidebar.title(f"Welcome, {st.session_state.username}!")
        if st.sidebar.button("Sign Out"):
            st.session_state.clear()
            st.rerun()
        
        weight_tracker()

if __name__ == "__main__":
    main() 