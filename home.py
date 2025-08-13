from datetime import datetime
from database import Connection
import Authenticate
c = Connection.create_connection()

def new_trip(u_id):
    global t_id 
    today = datetime.now()
    
    while True:
        source = input("Enter your city: ")
        destination = input("Which city do you wish to go to?: ")
        
        if any(char.isdigit() for char in source) or any(char.isdigit() for char in destination):
            print("Source or destination cannot have an integer.")
            continue
        else:
            break
    
    while True:
        try:
            temp_date = input("Enter start date and time (YYYY-MM-DD HH:MM:SS): ")
            str_td = datetime.strptime(temp_date, "%Y-%m-%d %H:%M:%S")
            
            if str_td <= today:
                print("Start date and time cannot be in the past.")
                continue
            
            temp_date = input("Enter end date and time (YYYY-MM-DD HH:MM:SS): ")
            end_td = datetime.strptime(temp_date, "%Y-%m-%d %H:%M:%S")
            
            if end_td <= str_td:
                print("End date and time cannot be before start date.")
                continue
            else:
                break
        except ValueError as e:
            print(f"Please provide the date and time in the specified format. Error: {e}")
            continue
    
    t_id = None
    while True: 
        try:
            query = "INSERT INTO trip (u_id, source, destination, str_td, end_td) VALUES (%s, %s, %s, %s, %s) RETURNING t_id"
            values = (u_id, source, destination, str_td, end_td)
            cursor = c.cursor()
            cursor.execute(query, values)
            t_id = cursor.fetchone()[0]
            c.commit()
            cursor.close()
            print("Trip successfully added!")
            break
            
        except Exception as e:
            print(f"Error adding trip to database: {e}")
            continue
    
    return t_id

def get_trips(u_id):
    try:
        query = """
            SELECT source, destination, str_td, end_td 
            FROM trip 
            WHERE u_id = %s 
            ORDER BY end_td DESC
        """
        
        cursor = c.cursor()
        cursor.execute(query, (u_id,))
        trips = cursor.fetchall()
        cursor.close()
        
        if trips:
            print("Past Trips:")
            for trip in trips:
                print(f"From {trip[0]} to {trip[1]}, Start: {trip[2]}, End: {trip[3]}")
        else:
            print("No past trips found.")
    except Exception as e:
        print(f"Error retrieving past trips: {e}")

def get_recommended_destination():
    try:
        query = """
            SELECT destination, COUNT(*) as trip_count 
            FROM trip
            GROUP BY destination 
            ORDER BY trip_count DESC 
            LIMIT 1
        """
        
        cursor = c.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            print(f"Recommended place to visit: {result[0]} with {result[1]} trips")
        else:
            print("No trip data available to recommend a place.")
    except Exception as e:
        print(f"Error retrieving most frequent destination: {e}")

def get_user_details(u_id):
    try:
        query = """
            SELECT u_id, username, email 
            FROM "User" 
            WHERE u_id = %s
        """
        
        cursor = c.cursor()
        cursor.execute(query, (u_id,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            print(f"User ID: {user[0]}\nUsername: {user[1]}\nEmail: {user[2]}")
            choice = input("Do you want to update your details? (yes/no): ").strip().lower()
            if choice == "yes":
                update_details(u_id)
                return True
            else:
                return False
        else:
            print("User not found.")
    except Exception as e:
        print(f"Error retrieving user details: {e}")

def update_details(u_id):
    attempts = 3
    while attempts > 0:
        try:
            password = input("Enter your password: ")
            
            query = 'SELECT password FROM "User" WHERE u_id = %s'
            cursor = c.cursor()
            cursor.execute(query, (u_id,))
            stored_password = cursor.fetchone()
            cursor.close()
            
            if stored_password and stored_password[0] == password:
                new_username = input("Enter new username (leave blank to keep current): ")
                new_email = input("Enter new email (leave blank to keep current): ")
                
                update_query = 'UPDATE "User" SET '
                update_values = []
                
                if new_username:
                    update_query += "username = %s, "
                    update_values.append(new_username)
                if new_email:
                    update_query += "email = %s, "
                    update_values.append(new_email)
                
                if update_values:
                    update_query = update_query.rstrip(", ") + " WHERE u_id = %s"
                    update_values.append(u_id)
                    
                    cursor = c.cursor()
                    cursor.execute(update_query, tuple(update_values))
                    c.commit()
                    cursor.close()
                    print("User details updated successfully.")
                else:
                    print("No changes made.")
                return
            else:
                attempts -= 1
                print(f"Incorrect password. {attempts} attempts remaining.")
        except Exception as e:
            print(f"Error while updating details: {e}")
    
    print("Too many incorrect attempts. Update cancelled.")

def admin_method(u_id):
    try:
        cursor = c.cursor()
        cursor.execute("SELECT role FROM \"User\" WHERE u_id = %s", (u_id,))
        role = cursor.fetchone()
        
        if role and role[0].lower() == "admin":
            cursor.execute("SELECT u_id, username, email FROM \"User\" WHERE role = 'customer'")
            users = cursor.fetchall()
            cursor.close()
            
            print("Current Users:")
            for user in users:
                print(f"User ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
        else:
            print("Access denied. You are not an admin.")
    except Exception as e:
        print(f"Error checking admin role or retrieving user data: {e}")

def main():
    while True:
        print("\nSelect an option:")
        print("1. Create a new trip")
        print("2. View past trips")
        print("3. Get recommended destination")
        print("4. View/update user details")
        print("5. Admin actions")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            new_trip(Authenticate.id)
            break
        elif choice == '2':
            get_trips(Authenticate.id)
        elif choice == '3':
            get_recommended_destination()
        elif choice == '4':
            get_user_details(Authenticate.id)
        elif choice == '5':
            admin_method(Authenticate.id)
        elif choice == '6':
            print("Exiting the trip interface.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()