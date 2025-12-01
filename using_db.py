from db_utils import DatabaseConnection

def main():
    print("Testing database connection with context manager...")
    
    # Using context manager (recommended)
    try:
        with DatabaseConnection() as db:
            # Perform database operations here
            print("connection established inside context manager.")
            pass
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
        
if __name__ == "__main__":
    main()
    print("\nTesting manual connection...")