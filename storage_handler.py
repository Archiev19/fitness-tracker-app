import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime
import streamlit as st

# Configure Cloudinary
def init_cloudinary():
    # Check if running on Streamlit Cloud (using secrets)
    if 'cloudinary' in st.secrets:
        # Use Streamlit secrets
        cloudinary.config(
            cloud_name = st.secrets['cloudinary']['cloud_name'],
            api_key = st.secrets['cloudinary']['api_key'],
            api_secret = st.secrets['cloudinary']['api_secret']
        )
    else:
        # Use hardcoded credentials (not recommended for production)
        cloudinary.config(
            cloud_name = "your_cloud_name",  # You'll get this after signing up
            api_key = "your_api_key",        # You'll get this after signing up
            api_secret = "your_api_secret"   # You'll get this after signing up
        )

def upload_file(file, user_id):
    """Upload a file to Cloudinary"""
    try:
        # Initialize Cloudinary
        init_cloudinary()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        public_id = f"fitness_tracker/{user_id}/{timestamp}"
        
        # Upload file to Cloudinary
        result = cloudinary.uploader.upload(
            file,
            public_id=public_id,
            folder="fitness_tracker",
            resource_type="auto"
        )
        
        return {
            'success': True,
            'url': result['secure_url'],
            'public_id': result['public_id']
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def delete_file(public_id):
    """Delete a file from Cloudinary"""
    try:
        # Initialize Cloudinary
        init_cloudinary()
        
        result = cloudinary.uploader.destroy(public_id)
        return {
            'success': True,
            'result': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_user_files(user_id):
    """Get all files for a specific user"""
    try:
        # Initialize Cloudinary
        init_cloudinary()
        
        result = cloudinary.api.resources(
            type="upload",
            prefix=f"fitness_tracker/{user_id}/"
        )
        return {
            'success': True,
            'files': result['resources']
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        } 