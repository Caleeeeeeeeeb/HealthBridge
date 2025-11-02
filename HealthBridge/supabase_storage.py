"""
Custom Django storage backend for Supabase Storage
"""
import os
from io import BytesIO
from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client
from urllib.parse import urljoin


class SupabaseStorage(Storage):
    """
    Custom storage backend for Supabase Storage.
    Handles file uploads, downloads, and URL generation.
    """
    
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.bucket_name = settings.SUPABASE_BUCKET_NAME
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        
    def _open(self, name, mode='rb'):
        """
        Open a file from Supabase Storage.
        """
        try:
            # Download file from Supabase
            file_data = self.client.storage.from_(self.bucket_name).download(name)
            return BytesIO(file_data)
        except Exception as e:
            raise IOError(f"Error opening file {name}: {str(e)}")
    
    def _save(self, name, content):
        """
        Save a file to Supabase Storage.
        """
        print(f"🔵 SupabaseStorage._save() called for: {name}")
        try:
            # Read file content
            file_content = content.read()
            print(f"🔵 File size: {len(file_content)} bytes")
            
            # Upload to Supabase Storage
            print(f"🔵 Uploading to bucket: {self.bucket_name}")
            self.client.storage.from_(self.bucket_name).upload(
                path=name,
                file=file_content,
                file_options={"content-type": content.content_type if hasattr(content, 'content_type') else "application/octet-stream"}
            )
            
            print(f"✅ Successfully uploaded to Supabase: {name}")
            return name
        except Exception as e:
            print(f"❌ Error uploading to Supabase: {str(e)}")
            # If file exists, try to update it
            try:
                print(f"🔄 Attempting to update existing file...")
                self.client.storage.from_(self.bucket_name).update(
                    path=name,
                    file=file_content,
                    file_options={"content-type": content.content_type if hasattr(content, 'content_type') else "application/octet-stream"}
                )
                print(f"✅ Successfully updated file in Supabase: {name}")
                return name
            except Exception as update_error:
                print(f"❌ Update also failed: {str(update_error)}")
                raise IOError(f"Error saving file {name}: {str(e)} | Update attempt: {str(update_error)}")
    
    def delete(self, name):
        """
        Delete a file from Supabase Storage.
        """
        try:
            self.client.storage.from_(self.bucket_name).remove([name])
        except Exception as e:
            raise IOError(f"Error deleting file {name}: {str(e)}")
    
    def exists(self, name):
        """
        Check if a file exists in Supabase Storage.
        """
        try:
            # Try to list the file
            files = self.client.storage.from_(self.bucket_name).list(path=os.path.dirname(name))
            filename = os.path.basename(name)
            return any(file['name'] == filename for file in files)
        except Exception:
            return False
    
    def url(self, name):
        """
        Return the public URL for the file.
        """
        try:
            # Get public URL from Supabase
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(name)
            return public_url
        except Exception as e:
            # Fallback: construct URL manually
            return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{name}"
    
    def size(self, name):
        """
        Return the size of a file in bytes.
        """
        try:
            files = self.client.storage.from_(self.bucket_name).list(path=os.path.dirname(name))
            filename = os.path.basename(name)
            for file in files:
                if file['name'] == filename:
                    return file.get('metadata', {}).get('size', 0)
            return 0
        except Exception:
            return 0
    
    def listdir(self, path):
        """
        List the contents of a directory.
        """
        try:
            files = self.client.storage.from_(self.bucket_name).list(path=path)
            directories = [f['name'] for f in files if f.get('id') is None]
            files_list = [f['name'] for f in files if f.get('id') is not None]
            return directories, files_list
        except Exception:
            return [], []
