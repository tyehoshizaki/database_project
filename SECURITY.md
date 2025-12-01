# Database Security Setup 🔒

This project uses environment variables to keep database credentials secure and separate from your source code.

## Files Created

### Core Files
- **`.env`** - Contains your actual database credentials (🚨 NEVER commit this file!)
- **`.env.example`** - Template file showing required environment variables
- **`db_utils.py`** - Secure database connection utilities
- **`test_secure.py`** - Test script using secure connections

### Updated Files
- **`connection_to_db.py`** - Updated to use environment variables
- **`environment/requirements.txt`** - Added `python-dotenv` dependency
- **`.gitignore`** - Already includes `.env` files (✅ Good!)

## Environment Variables

Your `.env` file contains these variables:

```bash
DB_HOST=192.168.1.72      # Database server address
DB_PORT=3306              # Database port
DB_USER=tye               # Database username  
DB_PASSWORD=1234          # Database password
DB_DATABASE=mydata        # Database name
```

## Usage Examples

### Method 1: Using the Context Manager (Recommended)
```python
from db_utils import DatabaseConnection

with DatabaseConnection() as db:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM your_table")
    results = cursor.fetchall()
```

### Method 2: Manual Connection
```python
from db_utils import connect_to_mariadb, disconnect_from_mariadb

conn = connect_to_mariadb()
if conn:
    # Do your database work here
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    print(cursor.fetchone())
    
    disconnect_from_mariadb(conn)
```

### Method 3: Direct Usage
```python
import mariadb
import os
from dotenv import load_dotenv

load_dotenv()

conn = mariadb.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT', 3306)),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_DATABASE')
)
```

## Security Best Practices ✅

1. **✅ Environment Variables**: Credentials are stored in `.env`, not in code
2. **✅ Git Ignore**: `.env` file is excluded from version control
3. **✅ Example Template**: `.env.example` shows required variables without exposing real data
4. **✅ Error Handling**: Proper exception handling for connection failures
5. **✅ Context Managers**: Automatic connection cleanup

## Setup for New Developers

1. Copy the example file: `cp .env.example .env`
2. Edit `.env` with your actual database credentials
3. Install dependencies: `pip install -r environment/requirements.txt`
4. Test connection: `python3 test_secure.py`

## Testing

Run any of these to test your secure connection:

```bash
python3 test_secure.py      # Simple connection test
python3 db_utils.py         # Comprehensive connection test
```

## Important Notes ⚠️

- **NEVER commit the `.env` file** to version control
- Keep your database credentials private
- Use different `.env` files for development, staging, and production
- Consider using more secure authentication methods (SSL certificates, IAM, etc.) for production

## Troubleshooting

If you get "ModuleNotFoundError", make sure your virtual environment is active and run:
```bash
pip install python-dotenv mariadb
```

If you get connection errors, verify your `.env` file has the correct database credentials.