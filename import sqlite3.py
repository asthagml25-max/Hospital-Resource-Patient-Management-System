import sqlite3
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("hospital.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                contact TEXT NOT NULL,
                disease TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                schedule TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                room_no INTEGER PRIMARY KEY,
                room_type TEXT NOT NULL,
                available INTEGER NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)

        self.conn.commit()

    def close(self):
        self.conn.close()


class Patient:
    def __init__(self, db):
        self.db = db

    def exists(self, patient_id):
        self.db.cursor.execute(
            "SELECT patient_id FROM patients WHERE patient_id = ?",
            (patient_id,)
        )
        return self.db.cursor.fetchone() is not None

    def add(self):
        patient_id = input("Enter patient ID: ").strip()

        if self.exists(patient_id):
            print("Patient ID already exists.")
            return

        name = input("Enter patient name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        try:
            age = int(input("Enter age: "))

            if age <= 0 or age > 120:
                print("Invalid age.")
                return

        except ValueError:
            print("Age must be a number.")
            return

        gender = input("Enter gender: ").strip()
        contact = input("Enter contact number: ").strip()
        disease = input("Enter disease/condition: ").strip()

        if not contact.isdigit() or len(contact) != 10:
            print("Contact number must contain 10 digits.")
            return

        self.db.cursor.execute("""
            INSERT INTO patients
            VALUES (?, ?, ?, ?, ?, ?)
        """, (patient_id, name, age, gender, contact, disease))

        self.db.conn.commit()

        print("Patient added successfully.")

    def view(self):
        self.db.cursor.execute("SELECT * FROM patients")
        patients = self.db.cursor.fetchall()

        if not patients:
            print("No patient records found.")
            return

        print("\n========== PATIENT RECORDS ==========")

        for patient in patients:
            print("Patient ID :", patient[0])
            print("Name       :", patient[1])
            print("Age        :", patient[2])
            print("Gender     :", patient[3])
            print("Contact    :", patient[4])
            print("Disease    :", patient[5])
            print("-------------------------------------")

    def search(self):
        patient_id = input("Enter patient ID: ").strip()

        self.db.cursor.execute(
            "SELECT * FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        patient = self.db.cursor.fetchone()

        if not patient:
            print("Patient not found.")
            return

        print("\nPatient Details")
        print("----------------")
        print("Patient ID :", patient[0])
        print("Name       :", patient[1])
        print("Age        :", patient[2])
        print("Gender     :", patient[3])
        print("Contact    :", patient[4])
        print("Disease    :", patient[5])

    def update(self):
        patient_id = input("Enter patient ID: ").strip()

        if not self.exists(patient_id):
            print("Patient not found.")
            return

        name = input("Enter new name: ").strip()

        try:
            age = int(input("Enter new age: "))

            if age <= 0 or age > 120:
                print("Invalid age.")
                return

        except ValueError:
            print("Invalid age.")
            return

        gender = input("Enter new gender: ").strip()
        contact = input("Enter new contact: ").strip()
        disease = input("Enter new disease/condition: ").strip()

        if not contact.isdigit() or len(contact) != 10:
            print("Invalid contact number.")
            return

        self.db.cursor.execute("""
            UPDATE patients
            SET name = ?, age = ?, gender = ?, contact = ?, disease = ?
            WHERE patient_id = ?
        """, (name, age, gender, contact, disease, patient_id))

        self.db.conn.commit()

        print("Patient information updated successfully.")

    def menu(self):
        while True:
            print("\n========== PATIENT MANAGEMENT ==========")
            print("1. Add Patient")
            print("2. View Patients")
            print("3. Search Patient")
            print("4. Update Patient")
            print("5. Back")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add()
            elif choice == "2":
                self.view()
            elif choice == "3":
                self.search()
            elif choice == "4":
                self.update()
            elif choice == "5":
                break
            else:
                print("Invalid choice.")


class Doctor:
    def __init__(self, db):
        self.db = db

    def exists(self, doctor_id):
        self.db.cursor.execute(
            "SELECT doctor_id FROM doctors WHERE doctor_id = ?",
            (doctor_id,)
        )
        return self.db.cursor.fetchone() is not None

    def add(self):
        doctor_id = input("Enter doctor ID: ").strip()

        if self.exists(doctor_id):
            print("Doctor ID already exists.")
            return

        name = input("Enter doctor name: ").strip()
        specialization = input("Enter specialization: ").strip()
        schedule = input("Enter schedule: ").strip()

        if not name or not specialization or not schedule:
            print("All fields are required.")
            return

        self.db.cursor.execute("""
            INSERT INTO doctors
            VALUES (?, ?, ?, ?)
        """, (doctor_id, name, specialization, schedule))

        self.db.conn.commit()

        print("Doctor added successfully.")

    def view(self):
        self.db.cursor.execute("SELECT * FROM doctors")
        doctors = self.db.cursor.fetchall()

        if not doctors:
            print("No doctor records found.")
            return

        print("\n========== DOCTOR RECORDS ==========")

        for doctor in doctors:
            print("Doctor ID      :", doctor[0])
            print("Name           :", doctor[1])
            print("Specialization :", doctor[2])
            print("Schedule       :", doctor[3])
            print("------------------------------------")

    def menu(self):
        while True:
            print("\n========== DOCTOR MANAGEMENT ==========")
            print("1. Add Doctor")
            print("2. View Doctors")
            print("3. Back")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add()
            elif choice == "2":
                self.view()
            elif choice == "3":
                break
            else:
                print("Invalid choice.")


class Appointment:
    def __init__(self, db):
        self.db = db

    def patient_exists(self, patient_id):
        self.db.cursor.execute(
            "SELECT patient_id FROM patients WHERE patient_id = ?",
            (patient_id,)
        )
        return self.db.cursor.fetchone() is not None

    def doctor_exists(self, doctor_id):
        self.db.cursor.execute(
            "SELECT doctor_id FROM doctors WHERE doctor_id = ?",
            (doctor_id,)
        )
        return self.db.cursor.fetchone() is not None

    def book(self):
        patient_id = input("Enter patient ID: ").strip()

        if not self.patient_exists(patient_id):
            print("Patient does not exist.")
            return

        doctor_id = input("Enter doctor ID: ").strip()

        if not self.doctor_exists(doctor_id):
            print("Doctor does not exist.")
            return

        date = input("Enter date (DD-MM-YYYY): ").strip()
        time = input("Enter time (HH:MM): ").strip()

        try:
            datetime.strptime(date, "%d-%m-%Y")
            datetime.strptime(time, "%H:%M")
        except ValueError:
            print("Invalid date or time format.")
            return

        self.db.cursor.execute("""
            SELECT appointment_id
            FROM appointments
            WHERE doctor_id = ?
            AND date = ?
            AND time = ?
        """, (doctor_id, date, time))

        if self.db.cursor.fetchone():
            print("Doctor is already booked at this time.")
            return

        self.db.cursor.execute("""
            INSERT INTO appointments
            (patient_id, doctor_id, date, time)
            VALUES (?, ?, ?, ?)
        """, (patient_id, doctor_id, date, time))

        self.db.conn.commit()

        print("Appointment booked successfully.")

    def view(self):
        self.db.cursor.execute("""
            SELECT
                a.appointment_id,
                p.name,
                d.name,
                a.date,
                a.time
            FROM appointments a
            JOIN patients p
            ON a.patient_id = p.patient_id
            JOIN doctors d
            ON a.doctor_id = d.doctor_id
            ORDER BY a.date, a.time
        """)

        appointments = self.db.cursor.fetchall()

        if not appointments:
            print("No appointments found.")
            return

        print("\n========== APPOINTMENTS ==========")

        for appointment in appointments:
            print("Appointment ID :", appointment[0])
            print("Patient        :", appointment[1])
            print("Doctor         :", appointment[2])
            print("Date           :", appointment[3])
            print("Time           :", appointment[4])
            print("----------------------------------")

    def cancel(self):
        try:
            appointment_id = int(
                input("Enter appointment ID: ")
            )
        except ValueError:
            print("Invalid appointment ID.")
            return

        self.db.cursor.execute(
            "SELECT appointment_id FROM appointments WHERE appointment_id = ?",
            (appointment_id,)
        )

        if not self.db.cursor.fetchone():
            print("Appointment not found.")
            return

        self.db.cursor.execute(
            "DELETE FROM appointments WHERE appointment_id = ?",
            (appointment_id,)
        )

        self.db.conn.commit()

        print("Appointment cancelled successfully.")

    def menu(self):
        while True:
            print("\n======= APPOINTMENT MANAGEMENT =======")
            print("1. Book Appointment")
            print("2. View Appointments")
            print("3. Cancel Appointment")
            print("4. Back")

            choice = input("Enter choice: ")

            if choice == "1":
                self.book()
            elif choice == "2":
                self.view()
            elif choice == "3":
                self.cancel()
            elif choice == "4":
                break
            else:
                print("Invalid choice.")


class Room:
    def __init__(self, db):
        self.db = db

    def add(self):
        try:
            room_no = int(input("Enter room number: "))
        except ValueError:
            print("Invalid room number.")
            return

        room_type = input("Enter room type: ").strip()

        self.db.cursor.execute(
            "SELECT room_no FROM rooms WHERE room_no = ?",
            (room_no,)
        )

        if self.db.cursor.fetchone():
            print("Room already exists.")
            return

        self.db.cursor.execute("""
            INSERT INTO rooms
            VALUES (?, ?, ?)
        """, (room_no, room_type, 1))

        self.db.conn.commit()

        print("Room added successfully.")

    def view(self):
        self.db.cursor.execute("SELECT * FROM rooms")
        rooms = self.db.cursor.fetchall()

        if not rooms:
            print("No rooms found.")
            return

        print("\n========== ROOM DETAILS ==========")

        for room in rooms:
            status = "Available" if room[2] else "Occupied"

            print("Room Number :", room[0])
            print("Room Type   :", room[1])
            print("Status      :", status)
            print("----------------------------------")

    def allocate(self):
        try:
            room_no = int(input("Enter room number: "))
        except ValueError:
            print("Invalid room number.")
            return

        self.db.cursor.execute(
            "SELECT available FROM rooms WHERE room_no = ?",
            (room_no,)
        )

        room = self.db.cursor.fetchone()

        if not room:
            print("Room not found.")
            return

        if room[0] == 0:
            print("Room is already occupied.")
            return

        self.db.cursor.execute("""
            UPDATE rooms
            SET available = 0
            WHERE room_no = ?
        """, (room_no,))

        self.db.conn.commit()

        print("Room allocated successfully.")

    def release(self):
        try:
            room_no = int(input("Enter room number: "))
        except ValueError:
            print("Invalid room number.")
            return

        self.db.cursor.execute(
            "SELECT available FROM rooms WHERE room_no = ?",
            (room_no,)
        )

        room = self.db.cursor.fetchone()

        if not room:
            print("Room not found.")
            return

        if room[0] == 1:
            print("Room is already available.")
            return

        self.db.cursor.execute("""
            UPDATE rooms
            SET available = 1
            WHERE room_no = ?
        """, (room_no,))

        self.db.conn.commit()

        print("Room released successfully.")

    def menu(self):
        while True:
            print("\n========== ROOM MANAGEMENT ==========")
            print("1. Add Room")
            print("2. View Rooms")
            print("3. Allocate Room")
            print("4. Release Room")
            print("5. Back")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add()
            elif choice == "2":
                self.view()
            elif choice == "3":
                self.allocate()
            elif choice == "4":
                self.release()
            elif choice == "5":
                break
            else:
                print("Invalid choice.")


class Resource:
    def __init__(self, db):
        self.db = db

    def add(self):
        name = input("Enter resource name: ").strip()

        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Quantity must be a number.")
            return

        if quantity < 0:
            print("Quantity cannot be negative.")
            return

        self.db.cursor.execute(
            "SELECT quantity FROM resources WHERE name = ?",
            (name,)
        )

        resource = self.db.cursor.fetchone()

        if resource:
            new_quantity = resource[0] + quantity

            self.db.cursor.execute("""
                UPDATE resources
                SET quantity = ?
                WHERE name = ?
            """, (new_quantity, name))

            print("Resource quantity updated.")

        else:
            self.db.cursor.execute("""
                INSERT INTO resources
                (name, quantity)
                VALUES (?, ?)
            """, (name, quantity))

            print("Resource added successfully.")

        self.db.conn.commit()

    def view(self):
        self.db.cursor.execute("SELECT * FROM resources")
        resources = self.db.cursor.fetchall()

        if not resources:
            print("No resources found.")
            return

        print("\n========== MEDICAL RESOURCES ==========")

        for resource in resources:
            print("Resource ID :", resource[0])
            print("Name        :", resource[1])
            print("Quantity    :", resource[2])
            print("---------------------------------------")

    def issue(self):
        name = input("Enter resource name: ").strip()

        try:
            quantity = int(input("Enter quantity to issue: "))
        except ValueError:
            print("Invalid quantity.")
            return

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

        self.db.cursor.execute(
            "SELECT quantity FROM resources WHERE name = ?",
            (name,)
        )

        resource = self.db.cursor.fetchone()

        if not resource:
            print("Resource not found.")
            return

        if resource[0] < quantity:
            print("Insufficient resource quantity.")
            return

        new_quantity = resource[0] - quantity

        self.db.cursor.execute("""
            UPDATE resources
            SET quantity = ?
            WHERE name = ?
        """, (new_quantity, name))

        self.db.conn.commit()

        print("Resource issued successfully.")
        print("Remaining quantity:", new_quantity)

    def menu(self):
        while True:
            print("\n======= RESOURCE MANAGEMENT =======")
            print("1. Add Resource")
            print("2. View Resources")
            print("3. Issue Resource")
            print("4. Back")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add()
            elif choice == "2":
                self.view()
            elif choice == "3":
                self.issue()
            elif choice == "4":
                break
            else:
                print("Invalid choice.")


class HospitalManagementSystem:
    def __init__(self):
        self.db = Database()

        self.patient = Patient(self.db)
        self.doctor = Doctor(self.db)
        self.appointment = Appointment(self.db)
        self.room = Room(self.db)
        self.resource = Resource(self.db)

    def run(self):
        while True:
            print("\n============================================")
            print("       HOSPITAL MANAGEMENT SYSTEM")
            print("============================================")
            print("1. Patient Management")
            print("2. Doctor Management")
            print("3. Appointment Management")
            print("4. Room Management")
            print("5. Medical Resource Management")
            print("6. Exit")
            print("============================================")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.patient.menu()

            elif choice == "2":
                self.doctor.menu()

            elif choice == "3":
                self.appointment.menu()

            elif choice == "4":
                self.room.menu()

            elif choice == "5":
                self.resource.menu()

            elif choice == "6":
                print("Thank you for using Hospital Management System.")
                self.db.close()
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    hospital = HospitalManagementSystem()
    hospital.run()