import re,sys
from database import Connection
conn = Connection.create_connection()
cur = conn.cursor()
from psycopg2 import sql
def validate_credentials(username, password):
    try:
        cursor = conn.cursor()
        query = sql.SQL('SELECT * FROM "User" WHERE username = %s AND password = %s')
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        if user is not None:
            global id
            id = user[0]
            global role
            role = user[4]
            return True
        else:
            print("No user found, try again.")
            return None
    except Exception as e:
        print(f"Error validating credentials: {e}")
        return False

def login():
    if not conn:
        print("Database connection is not established.")
        return

    attempts = 3
    while attempts > 0:
        try:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            obj = validate_credentials(username, password) 
            if obj:
                print("Login successful!")
                return
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"Invalid credentials. {attempts} attempts remaining, try again.")
                else:
                    print("No attempts remaining. Access denied.")
                    return
        except Exception as e:
            print(f"Error during login process: {e}")
            return

def is_valid_email(email: str) -> bool:
    """Validate an email address using regex."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def signup():
    if not conn:
        print("Database connection is not established.")
        return
    try:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        role = input("Enter your role: ")
        while True:
            email = input("Enter your email: ")
            if is_valid_email(email):
                break
            else:
                print("Please enter a valid email.")
                continue
        
        # PostgreSQL query to add the new user
        cur.execute("""
            INSERT INTO "User" (username, password, email, role)
            VALUES (%s, %s, %s, %s)
        """, (username, password, email, role))
        conn.commit()
        
        print("Registered Successfully.")
    except Exception as e:
        print(f"Particular email already exists, please login: {e}")
        login()

def main():
    if not conn:
        print("Database connection is not established.")
        return

    while True:
        print("Welcome to Travel Management System\nMenu:")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        try:
            choice = input("Enter your choice (1/2/3): ")
            
            if choice == '1':
                login()
                break
            elif choice == '2':
                signup()
            elif choice == '3':
                print("Exiting the program.")
                sys.exit(0)
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error processing choice: {e}")

if __name__ == "__main__":
    main()
