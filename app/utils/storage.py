import os
import shutil
from fastapi import UploadFile
from datetime import datetime
from app.config.settings import get_settings

settings = get_settings()

class Storage:
    def __init__(self, disk='local'):
        self.disk = disk
        self.base_path = os.path.join('app', 'storage')
        os.makedirs(self.base_path, exist_ok=True)
    
    async def store(self, file: UploadFile, path=''):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        
        destination_path = os.path.join(self.base_path, path)
        os.makedirs(destination_path, exist_ok=True)
        
        file_path = os.path.join(destination_path, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return os.path.join(path, filename)
    
    def get(self, path):
        return os.path.join(self.base_path, path)
    
    def delete(self, path):
        file_path = os.path.join(self.base_path, path)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False