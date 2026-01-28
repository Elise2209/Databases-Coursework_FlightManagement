import sqlite3
conn = sqlite3.connect('store')
conn.execute("PRAGMA foreign_keys = ON;")

#conn.execute("DROP TABLE 'Pilot'")
#conn.commit()

#conn.execute("DROP TABLE 'Flight'")
#conn.commit()

conn.execute("CREATE TABLE IF NOT EXISTS 'Pilot' (PilotID INTEGER PRIMARY KEY, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, LicenceNumber TEXT NOT NULL UNIQUE, Rank TEXT, HireDate DATE, Phone TEXT, Email TEXT)")

conn.execute("CREATE TABLE IF NOT EXISTS 'Location' (LocationID INTEGER PRIMARY KEY, AirportCode TEXT NOT NULL UNIQUE, AirportName TEXT NOT NULL, Country TEXT, City TEXT, TimeZone TEXT, TimeZoneUKadjt TEXT)")

conn.execute("CREATE TABLE IF NOT EXISTS 'Aircraft'(AircraftID INTEGER PRIMARY KEY, TailNumber TEXT NOT NULL UNIQUE, Model TEXT NOT NULL, Capacity INTEGER NOT NULL CHECK (Capacity >0))")

conn.execute("CREATE TABLE IF NOT EXISTS 'Flight'(FlightID INTEGER PRIMARY KEY, FlightNumber TEXT NOT NULL, Status TEXT NOT NULL DEFAULT 'Scheduled', DepartureDateTime TEXT NOT NULL, ArrivalDateTime TEXT NOT NULL, Gate TEXT, AircraftID INTEGER NOT NULL, OriginLocationID INTEGER NOT NULL, ArrivalLocationID INTEGER NOT NULL, FOREIGN KEY (AircraftID) REFERENCES Aircraft(AircraftID), FOREIGN KEY (OriginLocationID) REFERENCES Location(LocationID), FOREIGN KEY (ArrivalLocationID) REFERENCES Location(LocationID), CHECK (OriginLocationID <> ArrivalLocationID), CHECK (ArrivalDateTime > DepartureDateTime))")

conn.execute("CREATE TABLE IF NOT EXISTS 'FlightAssignment'(FlightID INTEGER NOT NULL, PilotID INTEGER NOT NULL, Role TEXT NOT NULL, AssignedAt TEXT DEFAULT (datetime('now')), PRIMARY KEY (FlightID, PilotID), FOREIGN KEY (FlightID) REFERENCES Flight(FlightID) ON DELETE CASCADE, FOREIGN KEY (PilotID) REFERENCES Pilot(PilotID) ON DELETE CASCADE)")

conn.execute("CREATE TABLE IF NOT EXISTS 'PilotQualification'(PilotID INTEGER NOT NULL, AircraftID INTEGER NOT NULL, CertificationDate TEXT, PRIMARY KEY (PilotID, AircraftID), FOREIGN KEY (PilotID) REFERENCES Pilot(PilotID) ON DELETE CASCADE,  FOREIGN KEY (AircraftID) REFERENCES Aircraft(AircraftID) ON DELETE CASCADE)")
conn.commit()


conn.execute("DELETE FROM FlightAssignment;")
conn.execute("DELETE FROM PilotQualification;")
conn.execute("DELETE FROM Flight;")
conn.execute("DELETE FROM Pilot;")
conn.execute("DELETE FROM Aircraft;")
conn.execute("DELETE FROM Location;")

conn.executemany("""
INSERT OR IGNORE INTO Pilot
(PilotID, FirstName, LastName, LicenceNumber, Rank, HireDate, Phone, Email)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", [
(1,  "Amelia", "Reed",    "LIC10001", "Captain",       "2015-03-12", "+44 7700 900101", "amelia.reed@airdemo.com"),
(2,  "James",  "Khan",    "LIC10002", "Captain",       "2012-09-01", "+44 7700 900102", "james.khan@airdemo.com"),
(3,  "Sofia",  "Patel",   "LIC10003", "First Officer", "2019-06-20", "+44 7700 900103", "sofia.patel@airdemo.com"),
(4,  "Oliver", "Nguyen",  "LIC10004", "First Officer", "2020-01-15", "+44 7700 900104", "oliver.nguyen@airdemo.com"),
(5,  "Maya",   "Turner",  "LIC10005", "Captain",       "2014-11-05", "+44 7700 900105", "maya.turner@airdemo.com"),
(6,  "Ethan",  "Brooks",  "LIC10006", "First Officer", "2021-04-09", "+44 7700 900106", "ethan.brooks@airdemo.com"),
(7,  "Aisha",  "Hassan",  "LIC10007", "Captain",       "2013-07-27", "+44 7700 900107", "aisha.hassan@airdemo.com"),
(8,  "Noah",   "Murphy",  "LIC10008", "First Officer", "2018-02-18", "+44 7700 900108", "noah.murphy@airdemo.com"),
(9,  "Chloe",  "Evans",   "LIC10009", "Captain",       "2016-05-30", "+44 7700 900109", "chloe.evans@airdemo.com"),
(10, "Liam",   "Olsen",   "LIC10010", "First Officer", "2022-08-12", "+44 7700 900110", "liam.olsen@airdemo.com"),
(11, "Isla",   "Morgan",  "LIC10011", "Captain",       "2011-12-03", "+44 7700 900111", "isla.morgan@airdemo.com"),
(12, "Kai",    "Sato",    "LIC10012", "First Officer", "2017-10-22", "+44 7700 900112", "kai.sato@airdemo.com"),
])

conn.executemany("""
INSERT OR IGNORE INTO Location
(LocationID, AirportCode, AirportName, Country, City, TimeZone, TimeZoneUKadjt)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", [
(1,  "LHR", "Heathrow Airport",           "UK",          "London",     "Europe/London",      "UK"),
(2,  "MAN", "Manchester Airport",         "UK",          "Manchester", "Europe/London",      "UK"),
(3,  "CDG", "Charles de Gaulle Airport",  "France",      "Paris",      "Europe/Paris",       "+1"),
(4,  "AMS", "Amsterdam Schiphol Airport", "Netherlands", "Amsterdam",  "Europe/Amsterdam",   "+1"),
(5,  "FRA", "Frankfurt Airport",          "Germany",     "Frankfurt",  "Europe/Berlin",      "+1"),
(6,  "MAD", "Adolfo Suárez Madrid Barajas","Spain",      "Madrid",     "Europe/Madrid",      "+1"),
(7,  "DUB", "Dublin Airport",             "Ireland",     "Dublin",     "Europe/Dublin",      "UK"),
(8,  "JFK", "John F. Kennedy Intl",       "USA",         "New York",   "America/New_York",   "-5"),
(9,  "DXB", "Dubai International",        "UAE",         "Dubai",      "Asia/Dubai",         "+4"),
(10, "HND", "Haneda Airport",             "Japan",       "Tokyo",      "Asia/Tokyo",         "+9"),
(11, "SIN", "Changi Airport",             "Singapore",   "Singapore",  "Asia/Singapore",     "+8"),
(12, "YYZ", "Toronto Pearson Intl",       "Canada",      "Toronto",    "America/Toronto",    "-5"),
])


conn.executemany("""
INSERT OR IGNORE INTO Aircraft
(AircraftID, TailNumber, Model, Capacity)
VALUES (?, ?, ?, ?)
""", [
(1,  "G-ABCD", "Airbus A320", 180),
(2,  "G-ABCE", "Airbus A321", 220),
(3,  "G-ABCF", "Boeing 737-800", 189),
(4,  "G-ABCG", "Boeing 787-9", 290),
(5,  "G-ABCH", "Airbus A350-900", 315),
(6,  "G-ABCI", "Embraer E190", 100),
(7,  "G-ABCJ", "Airbus A330-300", 300),
(8,  "G-ABCK", "Boeing 777-300ER", 360),
(9,  "G-ABCL", "Boeing 737 MAX 8", 178),
(10, "G-ABCM", "Airbus A220-300", 145),
])

conn.executemany("""
INSERT OR IGNORE INTO Flight
(FlightID, FlightNumber, Status, DepartureDateTime, ArrivalDateTime, Gate,
 AircraftID, OriginLocationID, ArrivalLocationID)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
(1,  "AD101", "Scheduled", "2026-02-01 08:10:00", "2026-02-01 09:25:00", "A12",  1, 1, 2),  # LHR->MAN
(2,  "AD102", "Scheduled", "2026-02-01 10:00:00", "2026-02-01 12:20:00", "B03",  3, 1, 3),  # LHR->CDG
(3,  "AD103", "Delayed",   "2026-02-02 14:30:00", "2026-02-02 16:40:00", "C07",  2, 2, 4),  # MAN->AMS
(4,  "AD104", "Scheduled", "2026-02-03 07:15:00", "2026-02-03 09:55:00", "A02",  6, 2, 5),  # MAN->FRA
(5,  "AD105", "Cancelled", "2026-02-03 18:00:00", "2026-02-03 20:10:00", "D01",  6, 3, 1),  # CDG->LHR
(6,  "AD106", "Scheduled", "2026-02-04 09:45:00", "2026-02-04 11:00:00", "A18", 10, 7, 1),  # DUB->LHR
(7,  "AD107", "Scheduled", "2026-02-05 12:30:00", "2026-02-05 15:10:00", "B14",  7, 1, 6),  # LHR->MAD
(8,  "AD108", "Scheduled", "2026-02-06 11:00:00", "2026-02-06 19:15:00", "E22",  4, 1, 8),  # LHR->JFK
(9,  "AD109", "Scheduled", "2026-02-07 21:00:00", "2026-02-08 06:05:00", "F05",  5, 1, 9),  # LHR->DXB
(10, "AD110", "Scheduled", "2026-02-08 13:20:00", "2026-02-09 09:10:00", "G09",  8, 1, 10), # LHR->HND
(11, "AD111", "Scheduled", "2026-02-10 20:40:00", "2026-02-11 16:20:00", "H01",  5, 1, 11), # LHR->SIN
(12, "AD112", "Scheduled", "2026-02-12 15:05:00", "2026-02-12 23:20:00", "E03",  4, 1, 12), # LHR->YYZ
])

conn.executemany("""
INSERT OR IGNORE INTO FlightAssignment
(FlightID, PilotID, Role, AssignedAt)
VALUES (?, ?, ?, ?)
""", [
(1,  1,  "Captain",       "2026-01-10 09:00:00"),
(1,  3,  "First Officer", "2026-01-10 09:05:00"),
(2,  2,  "Captain",       "2026-01-10 10:00:00"),
(2,  4,  "First Officer", "2026-01-10 10:05:00"),
(3,  5,  "Captain",       "2026-01-11 08:30:00"),
(3,  6,  "First Officer", "2026-01-11 08:35:00"),
(4,  7,  "Captain",       "2026-01-11 09:10:00"),
(4,  8,  "First Officer", "2026-01-11 09:12:00"),
(5,  9,  "Captain",       "2026-01-12 12:00:00"),
(6,  11, "Captain",       "2026-01-12 15:00:00"),
(6,  10, "First Officer", "2026-01-12 15:05:00"),
(7,  1,  "Captain",       "2026-01-13 11:00:00"),
(8,  2,  "Captain",       "2026-01-13 13:00:00"),
(8,  12, "First Officer", "2026-01-13 13:05:00"),
(9,  7,  "Captain",       "2026-01-14 10:00:00"),
])


conn.executemany("""
INSERT OR IGNORE INTO PilotQualification
(PilotID, AircraftID, CertificationDate)
VALUES (?, ?, ?)
""", [
(1,  1,  "2016-01-10"),
(1,  2,  "2017-05-22"),
(2,  3,  "2013-03-14"),
(2,  4,  "2018-09-02"),
(3,  1,  "2020-02-01"),
(3,  6,  "2021-11-19"),
(4,  3,  "2020-07-07"),
(5,  2,  "2015-06-30"),
(5,  7,  "2019-04-18"),
(6,  6,  "2022-01-12"),
(7,  5,  "2014-12-01"),
(7,  8,  "2020-10-05"),
(8,  9,  "2018-03-03"),
(9,  10, "2017-08-21"),
(11, 4,  "2012-02-14"),
])

conn.commit()
print("Sample data inserted successfully.")
