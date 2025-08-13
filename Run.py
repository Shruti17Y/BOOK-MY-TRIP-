import Authenticate
import home
import Hotel
import Payment
import transport
Authenticate.main()
home.main()
try:
    transport.insert_transport(Authenticate.id,home.t_id)
    Hotel.main()
    Payment.insert_payment()
except Exception as e:
    print("Thanks.Have a nice day!")