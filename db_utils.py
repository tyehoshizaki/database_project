"""
Database Utility Module
Provides secure database connections using environment variables.
"""

import mariadb # type: ignore
import os
from dotenv import load_dotenv # type: ignore
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class DatabaseConnection:
    """
    A context manager for MariaDB database connections.
    Automatically handles connection opening and closing.
    """
    
    def __init__(self):
        self.connection: Optional[mariadb.Connection] = None
        
    def __enter__(self):
        """Establish database connection."""
        try:
            self.connection = mariadb.connect(
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_DATABASE')
            )
            print("✅ Database connection established!")
            return self.connection
            
        except mariadb.Error as e:
            print(f"❌ Error connecting to MariaDB: {e}")
            raise
        except (ValueError, TypeError) as e:
            print(f"❌ Environment variable error: {e}")
            print("Please check your .env file and ensure all required variables are set.")
            raise
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            print("🔒 Database connection closed.")

def connect_to_mariadb() -> Optional[mariadb.Connection]:
    """
    Create a database connection using environment variables.
    
    Returns:
        mariadb.Connection or None: Database connection object or None if failed
    """
    try:
        conn = mariadb.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )
        print("✅ Database connection successful!")
        return conn
        
    except mariadb.Error as e:
        print(f"❌ Error connecting to MariaDB: {e}")
        return None
    except (ValueError, TypeError) as e:
        print(f"❌ Environment variable error: {e}")
        print("Please check your .env file and ensure all required variables are set.")
        return None

def disconnect_from_mariadb(conn: Optional[mariadb.Connection]) -> None:
    """
    Close a database connection safely.
    
    Args:
        conn: The database connection to close
    """
    if conn:
        conn.close()
        print("🔒 Database connection closed.")

def test_connection() -> bool:
    """
    Test the database connection and return success status.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    conn = connect_to_mariadb()
    if conn:
        disconnect_from_mariadb(conn)
        return True
    return False

# Example usage with context manager
if __name__ == "__main__":
    print("Testing database connection with context manager...")
    
    # Using context manager (recommended)
    try:
        with DatabaseConnection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 MariaDB Version: {version[0]}")
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
    
    # Using manual connection
    print("\nTesting manual connection...")
    if test_connection():
        print("🎉 All connection tests passed!")
    else:
        print("💥 Connection test failed!")