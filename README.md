APPLICATION FLOW & PROJECT STRUCTURE

------------------------------------------------------------
FLOW:
------------------------------------------------------------
LOGIN PAGE
 ├── SIGN UP (Admin / Customer)
 └── LOGIN (Admin / Customer)
       |
       v
HOME PAGE
 ├── NEW TRIP
 │     ├── ADD TRIP DETAILS
 │     ├── BOOK TRANSPORT
 │     └── BOOK HOTELS
 │            |
 │            v
 │         PAYMENT PAGE
 │          ├── Net Banking
 │          └── UPI
 │                |
 │                v
 │            TRIP SUMMARY
 │              ├── Back to Home
 │              └── Make Another Trip
 │
 ├── HISTORY
 └── UPDATE PROFILE DETAILS

------------------------------------------------------------
FOLDER & FILE STRUCTURE:
------------------------------------------------------------
GP_SEM-3/
│
├── run.py               # Main entry point; starts app and routes between pages
│
├── Authenticate.py       # Handles user/admin signup & login logic
│
├── home.py               # Displays home page options:
│                         # - New Trip
│                         # - History
│                         # - Update Profile
│
├── trip.py               # Manages new trip creation:
│                         # - Add trip details
│                         # - Calls transport.py & hotels.py
│
├── transport.py          # Handles transport booking:
│                         # - Mode of transport
│                         # - Booking confirmation
│
├── hotels.py             # Handles hotel booking:
│                         # - Hotel search
│                         # - Booking confirmation
│
├── payment.py            # Payment processing:
│                         # - Net Banking
│                         # - UPI
│
├── summary.py            # Trip summary page:
│                         # - Display booked trip details
│                         # - Option to return home or make another trip
│
├── database.py           # Database connection and queries
│
├── flow.txt              # Project flow documentation
│
└── __pycache__/          # Auto-generated Python cache files
------------------------------------------------------------
