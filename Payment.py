from database import Connection
import psycopg2
from psycopg2 import sql
import datetime as dt
import Authenticate
import Hotel
from decimal import Decimal
import home
import transport

def insert_payment():
    try:
        conn = Connection.create_connection()
        cur = conn.cursor()

        # Define the INSERT query
        amnt1 = (0,)
        if(not Hotel.hotel_id==-1):
            cur.execute("SELECT hotel_price FROM Hotel WHERE hotel_id = %s", (Hotel.hotel_id,))
            amnt1 = cur.fetchone()
        else:
            amnt1 = (0,)
        cur.execute("SELECT price FROM transport WHERE tr_id = %s", (transport.tr_id,))
        amnt2 = cur.fetchone()
        amount = ((((amnt1[0]) * Decimal(0.15)) + amnt1[0]) + (amnt2[0] * Decimal(0.15)) + amnt2[0])
        print(amount)

        temp = -1
        while not temp >= 0:
            temp = int(input("Enter the choice of the payment:\n1: Google Pay\n2: Credit Card\n3: Debit Card\nEnter here: "))
            if temp == 1:
                payment_method = "Google Pay"
            elif temp == 2:
                payment_method = "Credit Card"
            elif temp == 3:
                payment_method = "Debit Card"
            else:
                temp = -1
                print("Enter a valid input between 1 and 3.")
        
        pay_td = dt.datetime.now()
        insert_query = sql.SQL("""
            INSERT INTO Payment (u_id, t_id, hotel_id, amount, payment_method, pay_td)
            VALUES (%s, %s, %s, %s, %s, %s)
        """)

        # Execute the query with the provided data
        cur.execute(insert_query, (Authenticate.id, home.t_id, Hotel.hotel_id, amount, payment_method, pay_td))

        # Commit the transaction
        conn.commit()
        print("Payment inserted successfully\nThanks.Have a nice day!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error inserting payment: {error}")

# Example usage
if __name__ == "__main__":
    insert_payment()
