import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class StorageHandler:
    def __init__(self, base_dir="data"):
        self.base_dir = Path(base_dir)
        self.backup_dir = self.base_dir / "backups"
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.base_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
    def save_data(self, data, filename):
        """Save data to a JSON file with automatic backup."""
        file_path = self.base_dir / filename
        
        # Create backup of existing file if it exists
        if file_path.exists():
            backup_name = f"{filename}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
            backup_path = self.backup_dir / backup_name
            shutil.copy2(file_path, backup_path)
            
        # Save new data
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
    def load_data(self, filename):
        """Load data from JSON file."""
        file_path = self.base_dir / filename
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
        
    def delete_data(self, filename):
        """Delete data file with backup."""
        file_path = self.base_dir / filename
        if file_path.exists():
            # Create backup before deletion
            backup_name = f"{filename}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.del.bak"
            backup_path = self.backup_dir / backup_name
            shutil.copy2(file_path, backup_path)
            file_path.unlink()
            
    def list_files(self):
        """List all data files."""
        return [f.name for f in self.base_dir.glob("*.json") if f.is_file()]
        
    def cleanup_old_backups(self, days=30):
        """Remove backups older than specified days."""
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        for backup_file in self.backup_dir.glob("*.bak"):
            if backup_file.stat().st_mtime < cutoff:
                backup_file.unlink() 