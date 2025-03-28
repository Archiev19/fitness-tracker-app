import sqlite3
import pandas as pd
from datetime import datetime
import os
import shutil

class Database:
    def __init__(self):
        self.db_file = 'fitness_tracker.db'
        self.backup_dir = 'backups'
        self.init_db()
        self.ensure_backup_dir()

    def ensure_backup_dir(self):
        """Ensure backup directory exists"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_backup(self):
        """Create a backup of the database file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(self.backup_dir, f'fitness_tracker_{timestamp}.db')
            shutil.copy2(self.db_file, backup_file)
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

    def restore_backup(self, backup_file):
        """Restore database from a backup file"""
        try:
            # Create backup of current state before restoring
            self.create_backup()
            
            # Verify backup file is valid before restoring
            test_conn = sqlite3.connect(backup_file)
            test_conn.close()
            
            shutil.copy2(backup_file, self.db_file)
            return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False

    def get_backup_files(self):
        """Get list of available backup files"""
        if not os.path.exists(self.backup_dir):
            return []
        return sorted([f for f in os.listdir(self.backup_dir) if f.endswith('.db')], reverse=True)

    def cleanup_old_backups(self, max_backups=5):
        """Keep only the most recent backups"""
        backup_files = self.get_backup_files()
        if len(backup_files) > max_backups:
            for old_file in backup_files[max_backups:]:
                try:
                    os.remove(os.path.join(self.backup_dir, old_file))
                except Exception as e:
                    print(f"Error cleaning up old backup: {e}")

    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Create weight_entries table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS weight_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date DATE,
            weight REAL,
            FOREIGN KEY (username) REFERENCES users(username),
            UNIQUE(username, date)
        )
        ''')

        # Create goals table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            username TEXT PRIMARY KEY,
            target_weight REAL,
            target_date DATE,
            FOREIGN KEY (username) REFERENCES users(username)
        )
        ''')

        # Create running_entries table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS running_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date DATE,
            distance REAL,
            duration INTEGER,
            heart_rate INTEGER,
            FOREIGN KEY (username) REFERENCES users(username)
        )
        ''')

        conn.commit()
        conn.close()

    def add_user(self, username, password):
        """Add a new user to the database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def verify_user(self, username, password):
        """Verify user credentials"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        return result and result[0] == password

    def add_weight_entry(self, username, date, weight):
        """Add a new weight entry"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            # Create backup before modification
            self.create_backup()
            
            cursor.execute('''
            INSERT OR REPLACE INTO weight_entries (username, date, weight)
            VALUES (?, ?, ?)
            ''', (username, date, weight))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding weight entry: {e}")
            return False
        finally:
            conn.close()

    def get_weight_history(self, username):
        """Get weight history for a user"""
        conn = sqlite3.connect(self.db_file)
        query = '''
        SELECT date, weight 
        FROM weight_entries 
        WHERE username = ? 
        ORDER BY date
        '''
        df = pd.read_sql_query(query, conn, params=(username,))
        conn.close()
        return df

    def set_goal(self, username, target_weight, target_date):
        """Set or update user's goal"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT OR REPLACE INTO goals (username, target_weight, target_date)
            VALUES (?, ?, ?)
            ''', (username, target_weight, target_date))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error setting goal: {e}")
            return False
        finally:
            conn.close()

    def get_goal(self, username):
        """Get user's goal"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT target_weight, target_date 
        FROM goals 
        WHERE username = ?
        ''', (username,))
        result = cursor.fetchone()
        conn.close()
        return result if result else None

    def add_running_entry(self, username, date, distance, duration, heart_rate):
        """Add a new running entry"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO running_entries (username, date, distance, duration, heart_rate)
            VALUES (?, ?, ?, ?, ?)
            ''', (username, date, distance, duration, heart_rate))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding running entry: {e}")
            return False
        finally:
            conn.close()

    def get_running_history(self, username):
        """Get running history for a user"""
        conn = sqlite3.connect(self.db_file)
        query = '''
        SELECT date, distance, duration, heart_rate 
        FROM running_entries 
        WHERE username = ? 
        ORDER BY date
        '''
        df = pd.read_sql_query(query, conn, params=(username,))
        conn.close()
        return df

    def delete_weight_entry(self, username, date):
        """Delete a specific weight entry"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute('''
            DELETE FROM weight_entries 
            WHERE username = ? AND date = ?
            ''', (username, date))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting weight entry: {e}")
            return False
        finally:
            conn.close()

    def clear_user_data(self, username):
        """Clear all data for a user"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            # Create backup before deletion
            self.create_backup()
            
            cursor.execute('DELETE FROM weight_entries WHERE username = ?', (username,))
            cursor.execute('DELETE FROM goals WHERE username = ?', (username,))
            cursor.execute('DELETE FROM running_entries WHERE username = ?', (username,))
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error clearing user data: {e}")
            return False
        finally:
            conn.close() 