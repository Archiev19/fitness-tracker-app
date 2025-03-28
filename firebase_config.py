import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import streamlit as st
import json

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Check if Firebase is already initialized
        firebase_admin.get_app()
    except ValueError:
        # Initialize Firebase Admin SDK
        # Check if running on Streamlit Cloud (using secrets)
        if 'firebase' in st.secrets:
            # Use Streamlit secrets
            service_account_info = st.secrets['firebase']
            cred = credentials.Certificate(service_account_info)
        else:
            # Use local credentials file
            cred = credentials.Certificate('firebase-credentials.json')
        
        firebase_admin.initialize_app(cred)
    
    # Get Firestore client
    db = firestore.client()
    return db

def get_user_data(user_id):
    """Get user data from Firestore"""
    db = initialize_firebase()
    user_doc = db.collection('users').document(user_id).get()
    return user_doc.to_dict() if user_doc.exists else None

def save_user_data(user_id, data):
    """Save user data to Firestore"""
    db = initialize_firebase()
    db.collection('users').document(user_id).set(data)

def update_user_data(user_id, data):
    """Update user data in Firestore"""
    db = initialize_firebase()
    db.collection('users').document(user_id).update(data)

def delete_user_data(user_id):
    """Delete user data from Firestore"""
    db = initialize_firebase()
    db.collection('users').document(user_id).delete()

def get_all_users():
    """Get all users from Firestore"""
    db = initialize_firebase()
    users = db.collection('users').stream()
    return [user.to_dict() for user in users]

def verify_firebase_token(token):
    """Verify Firebase ID token"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        return None 