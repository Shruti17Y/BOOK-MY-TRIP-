from database import Connection
import Authenticate
import home

conn = Connection.create_connection()
cur = conn.cursor()

def view_hotels():
    try:
        # Retrieve the destination from the Trip table
        cur.execute("SELECT destination FROM Trip WHERE t_id = %s", (home.t_id,))
        destination = cur.fetchone()[0]
        
        # Fetch hotels with vacancy = TRUE and state = destination
        cur.execute("""
            SELECT hotel_id, hotel_name, hotel_address, hotel_price
            FROM Hotel
            WHERE vacancy = TRUE AND state = %s
        """, (destination,))
        hotels = cur.fetchall()
        if hotels:
            for hotel in hotels:
                print(f"Hotel ID: {hotel[0]}, Name: {hotel[1]}, Address: {hotel[2]}, Price: {hotel[3]}")
        else:
            print("No hotels found.")
            return False
    except Exception as e:
        print(f"Error occurred while viewing hotels: {e}")

def book_hotel(hotel_id, user_id):
    while(True):
        try:
            # Check if the hotel has vacancy
            cur.execute("SELECT vacancy FROM Hotel WHERE hotel_id = %s", (hotel_id,))
            result = cur.fetchone()
            
            # Check if the hotel_id exists
            if result is None:
                print(f"Hotel {hotel_id} does not exist.")
                temp = view_hotels()
                if(temp==False):
                    return False
                hotel_id = int(input("Enter the hotel ID you want to book: "))
                hotel_id = book_hotel(hotel_id, user_id)
                return hotel_id
            
            vacancy = result[0]
            if vacancy:
                # Log the booking 
                conn.commit()
                print(f"Hotel {hotel_id} booked successfully!")
                return hotel_id
            else:
                print(f"Hotel {hotel_id} is not available.")
        except Exception as e:
            print(f"Error occurred while booking hotel: {e}")
            continue

def main():
    global hotel_id
    if Authenticate.role == 'customer':
        while True:
            try:
                temp = view_hotels()
                if(temp==False):
                    hotel_id = -1
                    return 
                print("\n1. Book Hotels")
                print("2. Exit")
                choice = input("Enter your choice: ")
                if choice == '1':
                    hotel_id = int(input("Enter the hotel ID you want to book: "))
                    hotel_id = book_hotel(hotel_id, Authenticate.id)
                    if(hotel_id==False):
                        return
                    break
                elif choice == '2':
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid choice.")
            except Exception as e:
                print(f"Error: {e}")
    else:
        while True:
            try:
                print("\n1. View Hotels")
                print("2. Add Hotel")
                print("3. To edit the vacancy")
                print("4. Exit")
                choice = input("Enter your choice: ")
                if choice == '1':
                    cur.execute("SELECT * FROM Hotel")
                    hotels = cur.fetchall()
                    for hotel in hotels:
                        print(f"Hotel ID: {hotel[0]}, Name: {hotel[1]}, Address: {hotel[2]}, Price: {hotel[3]}, State: {hotel[4]}, Vacancy: {hotel[5]}")
                elif choice == '2':
                    hotel_name = input("Enter hotel name: ")
                    hotel_address = input("Enter hotel address: ")
                    hotel_price = float(input("Enter hotel price: "))
                    hotel_state = input("Enter hotel state: ")
                    vacancy = input("Enter vacancy (TRUE/FALSE): ").upper() == 'TRUE'
                    cur.execute(
                        "INSERT INTO Hotel (hotel_name, hotel_address, hotel_price, hotel_state, vacancy) VALUES (%s, %s, %s, %s, %s)",
                        (hotel_name, hotel_address, hotel_price, hotel_state, vacancy)
                    )
                    conn.commit()
                    print("Hotel added successfully!")
                elif choice == '3':
                    cur.execute("SELECT hotel_id FROM Hotel")
                    hotels = cur.fetchall()
                    hotel_ids = [hotel[0] for hotel in hotels]
                    hotel_id = int(input("Enter the hotel ID for which you want to edit the vacancy: "))
                    if hotel_id in hotel_ids:
                        new_vacancy = input("Enter new vacancy status (TRUE/FALSE): ").upper()
                        cur.execute("UPDATE Hotel SET vacancy = %s WHERE hotel_id = %s", (new_vacancy, hotel_id))
                        conn.commit()
                        print("Hotel vacancy status updated successfully!")
                    else:
                        print(f"Hotel id : {hotel_id} is not present.")
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter valid values.")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")