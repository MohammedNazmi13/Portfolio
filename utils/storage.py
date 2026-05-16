import os
import cloudinary
import cloudinary.uploader
from flask import current_app
from werkzeug.utils import secure_filename
import time

def upload_file(file, folder):
    """
    Uploads a file to Cloudinary if configured, otherwise saves locally.
    Returns the URL of the uploaded file.
    """
    if not file or file.filename == '':
        return None

    # Check if Cloudinary is configured
    cloud_name = current_app.config.get('CLOUDINARY_CLOUD_NAME')
    api_key = current_app.config.get('CLOUDINARY_API_KEY')
    api_secret = current_app.config.get('CLOUDINARY_API_SECRET')

    if cloud_name and api_key and api_secret:
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        try:
            # Upload to Cloudinary
            # resource_type="auto" allows PDFs, videos, etc.
            result = cloudinary.uploader.upload(
                file, 
                folder=f"portfolio/{folder}",
                resource_type="auto"
            )
            return result.get('secure_url')
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            # Fallback to local if Cloudinary fails (though it will likely fail on Vercel too)
    
    # Fallback: Local storage (may fail on serverless environments like Vercel)
    try:
        filename = secure_filename(file.filename)
        unique_filename = f"{int(time.time())}_{filename}"
        
        # Determine upload path
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads', folder)
        
        # Try to save locally, but catch ANY errors to fallback to Base64
        try:
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            
            file_path = os.path.join(upload_path, unique_filename)
            file.save(file_path)
            return f"/static/uploads/{folder}/{unique_filename}"
        except (OSError, Exception) as e:
            # If we are on Vercel or any read-only filesystem, fallback to Base64
            import base64
            # Reset file pointer to beginning
            file.seek(0)
            file_data = file.read()
            # If file is empty, return None
            if not file_data:
                return None
            base64_data = base64.b64encode(file_data).decode('utf-8')
            mime_type = file.content_type or 'application/octet-stream'
            return f"data:{mime_type};base64,{base64_data}"
            
    except Exception as e:
        print(f"Final upload fallback error: {e}")
        return None
