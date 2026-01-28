import sqlite3

    # 1) Flight retrieval queries (destination/status/date)
    # 2) Schedule modification (UPDATE flight schedules - e.g. change departure time or status)
    # 3) Pilot assignment (INSERT) + pilot schedule (SELECT)
    # 4) Destination management (SELECT/ and UPDATE)
    # 5) Summary queries (such as the number of flights to each destination or the number of flights assigned to a pilot'

# Converting SQL to Python 
conn = sqlite3.connect('store')

# Query 1: Flight Retrieval: Retrieve flights based on multiple criteria, such as destination, status, or departure date.
# This gives information on a flight depending on the AirportCode of the destination 
def view_flights(column_name: str, user_input: str):     
    cursor = conn.cursor()
    cursor.execute(f"""    
        SELECT
            f.FlightID,
            f.FlightNumber,
            f.Status,
            f.DepartureDateTime,
            f.ArrivalDateTime,
            o.AirportCode AS Origin,
            a.AirportCode AS Destination,
            f.Gate
        FROM Flight f
        JOIN Location o ON o.LocationID = f.OriginLocationID
        JOIN Location a ON a.LocationID = f.ArrivalLocationID
        WHERE {column_name} = ?
        ORDER BY f.DepartureDateTime;
    """, [user_input])
    return cursor.fetchall()


#Updating a flight's status by putting in flight number (update status, origin and arrival)

def update_flight():
    flight_number = input("Flight Number: ")
    flights = view_flights("f.FlightNumber", flight_number)
    if len(flights) != 1:
        print("Incorrect Flight Number")
        return
    else: 
        pretty_print_flights(flights)
    attribute_change = input("Enter attribute to change (status/origin/destination): ")
    change = input("What do you want to change this value to: ")
    if attribute_change.lower() == "status":
        update_flight_status(flights[0][0], change)
    elif attribute_change.lower() == "origin":
        update_flight_origin(flights[0][0], change)
    elif attribute_change.lower() in ["dest", "destination"]:
        update_flight_arrival(flights[0][0], change)
    else:
        print("Unknown property")
        return
    flights = view_flights("f.FlightNumber", flight_number)
    pretty_print_flights(flights)


def update_flight_status(flight_id, new_status):
    data = conn.execute(f"""    
        UPDATE Flight
        SET Status = ?
        WHERE FlightID = ?;
    """, [new_status, flight_id])
    print(f"{data.rowcount} row(s) effected")

def update_flight_origin(flight_id, new_origin): 
    data = conn.execute(f"""
        UPDATE Flight 
        SET OriginLocationID = (SELECT LocationID from Location where AirportCode = ?)
        WHERE FlightID = ?;
    """, [new_origin, flight_id])
    print(f"{data.rowcount} row(s) effected")   

def update_flight_arrival(flight_id, new_arrival):
    data = conn.execute(f""" 
        UPDATE FLIGHT 
        SET ArrivalLocationID = (SELECT LocationID from Location where AirportCode = ?)
        WHERE FlightID = ?; 
        """, [new_arrival, flight_id])
    print(f"{data.rowcount} row(s) effected")     


#Adding a new flight 
def add_flight():
    flight_number = input("New Flight Number: ")
    status = input("Status: ")
    departuredate = input("Depature Date/Time: ")
    arrivaldate = input("Arrival Date/Time: ")
    originlocationid = input("Origin: ")
    arrivallocationid = input("Destination: ")
    gate = input("Gate: ")
    aircraftid = input("Aircraft Tail Number: ")
    data = conn.execute(f"""    
        INSERT INTO Flight (FlightNumber, Status, DepartureDateTime, ArrivalDateTime, OriginLocationID, ArrivalLocationID, Gate, AircraftID) 
        VALUES (
                ?,?,?,?,
                (SELECT LocationID FROM Location WHERE AirportCode = ?),
                (SELECT LocationID FROM Location WHERE AirportCode = ?),
                ?,
                (SELECT AircraftID FROM Aircraft WHERE TailNumber = ?)
        )
    """, [flight_number, status, departuredate, arrivaldate, originlocationid, arrivallocationid, gate, aircraftid] )
    print(data)

#View Pilot's schedule - based on name or through Pilot ID
def view_pilot(column_name: str, user_input: str):     
    cursor = conn.cursor()
    cursor.execute(f"""    
        SELECT
        p.PilotID,
        p.FirstName || ' ' || p.LastName AS PilotName,
        f.FlightID,
        f.FlightNumber,
        f.Status,
        f.DepartureDateTime,
        f.ArrivalDateTime,
        o.AirportCode AS Origin,
        a.AirportCode AS Destination,
        fa.Role
    FROM FlightAssignment fa
    JOIN Pilot p    ON p.PilotID = fa.PilotID
    JOIN Flight f   ON f.FlightID = fa.FlightID
    JOIN Location o ON o.LocationID = f.OriginLocationID
    JOIN Location a ON a.LocationID = f.ArrivalLocationID
    WHERE {column_name} = ?
ORDER BY f.DepartureDateTime;
    """, [user_input])
    return cursor.fetchall()


#Assigning a pilot to a flight.  
def assign_pilot():
    pilot_id = input("PilotID: ").strip()
    flight_number = input("Flight Number: ").strip()
    role = input("Role (e.g. Captain/FO): ").strip()
    cur = conn.cursor()

    #finding the flight
    cur.execute("""
        SELECT FlightID, DepartureDateTime, ArrivalDateTime
        FROM Flight
        WHERE FlightNumber = ?;
    """, [flight_number])
    flight = cur.fetchone()
    #returns none if cannot find the flight
    if flight is None:
        print("Flight not found.")
        return None

    flight_id, new_dep, new_arr = flight

    #conflict check with the pilot 
    cur.execute("""
        SELECT f.FlightNumber, f.DepartureDateTime, f.ArrivalDateTime
        FROM FlightAssignment fa
        JOIN Flight f ON f.FlightID = fa.FlightID
        WHERE fa.PilotID = ?
          AND fa.FlightID != ?
          AND (? < f.ArrivalDateTime AND ? > f.DepartureDateTime);
    """, [pilot_id, flight_id, new_dep, new_arr])

    conflicts = cur.fetchall()
    if conflicts:
        print("Pilot has a conflict with:")
        for c in conflicts:
            print(f"  {c[0]} [{c[1]} -> {c[2]}]")
        return None

    #need to check if pilot already in this role 
    cur.execute("""
        SELECT 1
        FROM FlightAssignment
        WHERE PilotID = ? AND FlightID = ?;
    """, [pilot_id, flight_id])

    if cur.fetchone():
        cur.execute("""
            UPDATE FlightAssignment
            SET Role = ?
            WHERE PilotID = ? AND FlightID = ?;
        """, [role, pilot_id, flight_id])
        print("Role updated successfully!")
    else:
        cur.execute("""
            INSERT INTO FlightAssignment (PilotID, FlightID, Role)
            VALUES (?, ?, ?);
        """, [pilot_id, flight_id, role])
        print("Pilot assigned successfully!")

    conn.commit()
    return pilot_id

#Show location information 
def view_location():
    print("""
1. View all locations
2. View one location by Airport Code
""")
    choice = input("Choose option: ").strip()

    cur = conn.cursor()

    if choice == "1":
        cur.execute("""
            SELECT LocationID, AirportCode, AirportName, City, Country, TimeZone, TimeZoneUKadjt
            FROM Location
            ORDER BY AirportCode;
        """)
        rows = cur.fetchall()

        for r in rows:
            print(f"{r[1]} | {r[2]} | {r[3]}, {r[4]} | TZ: {r[5]} | UK Adj: {r[6]}")

    elif choice == "2":
        airport_code = input("Enter Airport Code (e.g. LHR or MAN): ").strip().upper()
        cur.execute("""
            SELECT LocationID, AirportCode, AirportName, City, Country, TimeZone, TimeZoneUKadjt
            FROM Location
            WHERE AirportCode = ?;
        """, [airport_code])

        row = cur.fetchone()
        if not row:
            print("Location not found.")
            return

        print(f"""
LocationID: {row[0]}
AirportCode: {row[1]}
AirportName: {row[2]}
City: {row[3]}
Country: {row[4]}
TimeZone: {row[5]}
TimeZoneUKadjt: {row[6]}
""")
    else:
        print("Invalid option.")


# Updating location information: 
def update_location():
    airport_code = input("Enter Airport Code to update: ").strip().upper()

    cur = conn.cursor()
    cur.execute("""
        SELECT LocationID, AirportCode, AirportName
        FROM Location
        WHERE AirportCode = ?;
    """, [airport_code])

    row = cur.fetchone()
    if not row:
        print("Location not found.")
        return

    print(f"Current Airport Name: {row[2]}")
    new_name = input("Enter new Airport Name: ").strip()

    cur.execute("""
        UPDATE Location
        SET AirportName = ?
        WHERE AirportCode = ?;
    """, [new_name, airport_code])

    conn.commit()
    print("Airport name updated.")

    cur.execute("""
        SELECT LocationID, AirportCode, AirportName
        FROM Location
        WHERE AirportCode = ?;
    """, [airport_code])

    updated = cur.fetchone()
    print(f"Updated: {updated[1]} | {updated[2]}")



#Printing flight out in a user friendly manner 
def pretty_print_flights(flight_data):
    for d in flight_data:
        print(f"{d[1]} {d[5]}->{d[6]} ({d[2]}) [{d[3]} -> {d[4]}]")

#Printing out pilot flight assignment: 
def print_pilot_assignment_flights(flight_assignment):
    if not flight_assignment: 
        print("No flights found for that pilot.")
        return
    for r in flight_assignment: 
        print(f"{r[1]} (ID {r[0]}) | {r[3]} {r[7]}->{r[8]} "
        f"({r[4]}) [{r[5]} -> {r[6]}] Role: {r[9]}")

def numeric_input(prompt):
    # helper function to get a numeric choice from teh user
    user_input_str = input(prompt)
    if user_input_str.isdigit():
        return int(user_input_str)
    return None

def search():
    print("""
    Search By
        1. By Origination Airport Code
        2. By Destination Airport Code
        3. By Status
        4. By Flight Number
    """)
    choice = numeric_input("Enter option: ")
    if choice == 1:
        user_input = input("Enter Origin Airport Code: ")
        flights = view_flights("o.AirportCode", user_input.upper())
        pretty_print_flights(flights)
    elif choice == 2: 
        user_input = input("Enter Destination Airport Code: ")
        flights = view_flights("a.AirportCode", user_input.upper())     
        pretty_print_flights(flights)
    elif choice == 3:        
        user_input = input("Enter Status: ")
        flights = view_flights("f.Status", user_input)
        pretty_print_flights(flights)
    elif choice == 4:                
        user_input = input("Enter Flight Number: ")
        flights = view_flights("f.FlightNumber", user_input)
        pretty_print_flights(flights)


#User menu
while True:
    print("""
    Menu
        1. Search by ...
        2. Add Flight
        3. Update Flight
        4. View Pilot Schedule
        5. Assign a Pilot to a Flight
        6. View Location Information
        7. Update Location Information
        """)
    
    choice = numeric_input("Enter option: ")
    if choice == None:
        print("Invalid Input.")
    elif choice == 1:
        search()
    elif choice == 2:
        add_flight()
    elif choice == 3:
        update_flight()
    elif choice == 4:
        user_input = input("Enter Pilot ID or full name: ").strip()
        if user_input.isdigit():
            rows = view_pilot("p.PilotID", user_input)
        else:
            #handles situation when 2+ spaces are added 
            name = " ".join(user_input.split()).lower()
            # match against combined pilot name
            rows = view_pilot("LOWER(TRIM(p.FirstName || ' ' || p.LastName))", name)
        print_pilot_assignment_flights(rows)
    elif choice == 5:
        pilot_id = assign_pilot()
        if pilot_id:  # we only get pilot id back if assignment wokred
            rows = view_pilot("p.PilotID", pilot_id)
            print_pilot_assignment_flights(rows)
    elif choice == 6:
        view_location()
    elif choice == 7:
        update_location()
    




