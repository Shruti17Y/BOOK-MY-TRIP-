from database import Connection
conn = Connection.create_connection()
import random,string,Authenticate,home

def generate_bus_number():
    return f"{random.choice(['KA', 'MH', 'DL', 'TN'])} {random.randint(10, 99)} {random.choice(string.ascii_uppercase)} {random.randint(1000, 9999)}"

def generate_flight_number():
    return f"{random.choice(['AI', 'BA', 'QR', 'EK'])}{random.randint(100, 9999)}"

def generate_pnr_number():
    return f"{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"

def insert_transport(u_id, t_id):
    global tr_id
    try:
        with conn.cursor() as cursor:
            # Fetch source and destination from Trip table
            cursor.execute("SELECT source, destination FROM Trip WHERE t_id = %s", (t_id,))
            trip = cursor.fetchone()
            
            if not trip:
                print("Trip ID not found.")
                return
            
            source, destination = trip
            
            # Get user input for transport mode
            transport_modes = ["Bus", "Train", "Flight"]
            print("Choose a transport mode: 1. Bus  2. Train  3. Flight")
            choice = int(input("Enter your choice (1/2/3): "))
            
            if choice not in [1, 2, 3]:
                print("Invalid choice.")
                return
            
            transport_mode = transport_modes[choice - 1]
            price = random.randint(100, 4000)
            
            if transport_mode == "Bus":
                tr_no = generate_bus_number()
            elif transport_mode == "Train":
                tr_no = generate_pnr_number()
            else:
                tr_no = generate_flight_number()
            
            # Insert into Transport table
            cursor.execute(
                """
                INSERT INTO Transport (u_id, t_id, transport_mode, price, source, destination, tr_no)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING tr_id
                """,
                (u_id, t_id, transport_mode, price, source, destination, tr_no)
            )
            tr_id = cursor.fetchone()[0]
            conn.commit()
            print("Transport entry added successfully.")
    except Exception as e:
        if conn:
            conn.rollback()
        print("Error inserting transport entry:", e)
    finally:
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    insert_transport(Authenticate.id, home.t_id)