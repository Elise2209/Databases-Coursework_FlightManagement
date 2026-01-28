-- Query 1: Flight Retrieval: Retrieve flights based on multiple criteria, such as destination, status, or departure date.
-- This gives information on a flight depending on the AirportCode of the destination 
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
    WHERE a.AirportCode = 'JFK'
    ORDER BY f.DepartureDateTime;

-- This gives information on a flight where the status is 'scheduled' 

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
    WHERE f.Status = 'Scheduled'
    ORDER BY f.DepartureDateTime;

-- This gives information on a flight on a certain departure data' 

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
    WHERE f.DepartureDateTime BETWEEN '2026-02-01 00:00:00'
                                  AND '2026-02-01 23:59:59'
    ORDER BY f.DepartureDateTime;

    
-- Query 2: Schedule Modification: Update flight schedules (e.g., change departure time or status).

--Update the depature date - need to ensure this is before arrival date 

SELECT FlightID, FlightNumber, DepartureDateTime, Status
FROM Flight
WHERE FlightID = 1;

UPDATE Flight
SET DepartureDateTime = '2026-01-05 09:30:00'
WHERE FlightID = 1;

SELECT FlightID, FlightNumber, DepartureDateTime, Status
FROM Flight
WHERE FlightID = 1;

--Update the status  

SELECT FlightID, FlightNumber, DepartureDateTime, Status
FROM Flight
WHERE FlightID = 1;

UPDATE Flight
SET Status = 'Delayed'
WHERE FlightID = 1;

SELECT FlightID, FlightNumber, DepartureDateTime, Status
FROM Flight
WHERE FlightID = 1;

--Query 3: Pilot Assignment: Assign pilots to flights and retrieve information about pilot schedules.
-- Assign a pilot to a flight (with checks) 

SELECT PilotID, FirstName, LastName, Rank
FROM Pilot
WHERE PilotID = 3;

SELECT FlightID, FlightNumber, DepartureDateTime, Status
FROM Flight
WHERE FlightID = 1;

SELECT FlightID, PilotID, Role, AssignedAt
FROM FlightAssignment
WHERE FlightID = 1 AND PilotID = 3;

INSERT OR IGNORE INTO FlightAssignment (FlightID, PilotID, Role)
VALUES (1, 3, 'First Officer');

SELECT FlightID, PilotID, Role, AssignedAt
FROM FlightAssignment
WHERE FlightID = 1 AND PilotID = 3;

-- Retrieve a Pilot's schedule 
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
WHERE p.PilotID = 1
ORDER BY f.DepartureDateTime;

--Query 4: Destination Management: View and update destination information as required.
-- View all destination locations: 
SELECT LocationID, AirportCode, AirportName, City, Country, TimeZone, TimeZoneUKadjt
FROM Location
ORDER BY AirportCode;

-- View one destination 

SELECT LocationID, AirportCode, AirportName, City, Country, TimeZone, TimeZoneUKadjt
FROM Location
WHERE AirportCode = 'LHR';

-- Update airport name 

SELECT LocationID, AirportCode, AirportName
FROM Location
WHERE AirportCode = 'JFK';

UPDATE Location
SET AirportName = 'John F. Kennedy International Airport1'
WHERE AirportCode = 'JFK';

SELECT LocationID, AirportCode, AirportName
FROM Location
WHERE AirportCode = 'JFK';

-- Update City and TimeZone

SELECT AirportCode, City, TimeZone
FROM Location
WHERE AirportCode = 'DXB';

UPDATE Location
SET City = 'Dubai1',
    TimeZone = 'MiddleEast/Dubai1'
WHERE AirportCode = 'DXB';

SELECT AirportCode, City, TimeZone
FROM Location
WHERE AirportCode = 'DXB';

-- Update Flight status

UPDATE Flight 
SET Status = 'Delayed' 
WHERE FlightID = 1;

UPDATE Flight 
SET OriginLocationID = (SELECT LocationID from Location where AirportCode = 'JFK') 
WHERE FlightID = 1;

Select * from Flight
WHERE FlightID = 1;

-- View all destinations 

SELECT LocationID, AirportCode, AirportName, City, Country, TimeZone, TimeZoneUKadjt
FROM Location
ORDER BY AirportCode;

-- View number of flights to each destination (arrivals)  

SELECT
    a.AirportCode AS Destination,
    a.City,
    a.Country,
    COUNT(*) AS NumFlightsArriving
FROM Flight f
JOIN Location a ON a.LocationID = f.ArrivalLocationID
GROUP BY a.LocationID, a.AirportCode, a.City, a.Country
ORDER BY NumFlightsArriving DESC, a.AirportCode;

-- view number of flights from each origin (departures) 

SELECT
    o.AirportCode AS Origin,
    o.City,
    o.Country,
    COUNT(*) AS NumFlightsDeparting
FROM Flight f
JOIN Location o ON o.LocationID = f.OriginLocationID
GROUP BY o.LocationID, o.AirportCode, o.City, o.Country
ORDER BY NumFlightsDeparting DESC, o.AirportCode;

-- check the number of flights assigned to each pilot
-- left join was used so pilots with zero assignments appeared

SELECT
    p.PilotID,
    p.FirstName || ' ' || p.LastName AS PilotName,
    COUNT(fa.FlightID) AS NumAssignedFlights
FROM Pilot p
LEFT JOIN FlightAssignment fa ON fa.PilotID = p.PilotID
GROUP BY p.PilotID, p.FirstName, p.LastName
ORDER BY NumAssignedFlights DESC, p.PilotID;

-- flights by status 

SELECT
    Status,
    COUNT(*) AS NumFlights
FROM Flight
GROUP BY Status
ORDER BY NumFlights DESC;

