
import sqlite3
from datetime import datetime


class HospitalManagementSystem:
    def __init__(self):
        self.conn = sqlite3.connect("hospital.db")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    def create_tables(self):
        queries = [
            """CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY, name TEXT NOT NULL,
                age INTEGER NOT NULL, gender TEXT, contact TEXT,
                disease TEXT)""",
            """CREATE TABLE IF NOT EXISTS doctors (
                doctor_id TEXT PRIMARY KEY, name TEXT NOT NULL,
                specialization TEXT NOT NULL, schedule TEXT)""",
            """CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL, doctor_id TEXT NOT NULL,
                date TEXT NOT NULL, time TEXT NOT NULL)""",
            """CREATE TABLE IF NOT EXISTS rooms (
                room_no INTEGER PRIMARY KEY, room_type TEXT NOT NULL,
                available INTEGER NOT NULL DEFAULT 1)""",
            """CREATE TABLE IF NOT EXISTS resources (
                resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL, quantity INTEGER NOT NULL)""",
            """CREATE TABLE IF NOT EXISTS medical_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL, diagnosis TEXT NOT NULL,
                treatment TEXT, notes TEXT)""",
            """CREATE TABLE IF NOT EXISTS prescriptions (
                prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL, doctor_id TEXT NOT NULL,
                medicine TEXT NOT NULL, dosage TEXT NOT NULL,
                duration TEXT NOT NULL, instructions TEXT)""",
            """CREATE TABLE IF NOT EXISTS bills (
                bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL, consultation REAL NOT NULL,
                room_charge REAL NOT NULL, medicine_charge REAL NOT NULL,
                other_charge REAL NOT NULL, total REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending')"""
        ]

        for query in queries:
            self.conn.execute(query)

        self.conn.commit()

    def get_text(self, message):
        value = input(message).strip()
        if not value:
            raise ValueError("Input cannot be empty.")
        return value

    def get_number(self, message, minimum=0):
        value = float(input(message))
        if value < minimum:
            raise ValueError(f"Value must be at least {minimum}.")
        return value

    def exists(self, table, column, value):
        query = f"SELECT 1 FROM {table} WHERE {column} = ?"
        return self.conn.execute(query, (value,)).fetchone() is not None

    def show_rows(self, query, heading):
        rows = self.conn.execute(query).fetchall()
        print(f"\n--- {heading} ---")
        if not rows:
            print("No records found.")
        else:
            for row in rows:
                print(" | ".join(str(item) for item in row))

    def add_patient(self):
        patient_id = self.get_text("Patient ID: ")
        name = self.get_text("Name: ")
        age = int(self.get_number("Age: ", 1))

        if age > 120:
            raise ValueError("Age cannot exceed 120.")

        gender = self.get_text("Gender: ")
        contact = self.get_text("10-digit contact number: ")

        if not contact.isdigit() or len(contact) != 10:
            raise ValueError("Contact must contain exactly 10 digits.")

        disease = input("Disease/condition: ").strip()

        self.conn.execute(
            "INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?)",
            (patient_id, name, age, gender, contact, disease)
        )
        self.conn.commit()
        print("Patient added successfully.")

    def patient_menu(self):
        while True:
            print("\n1. Add Patient  2. View Patients")
            print("3. Search Patient  4. Update Patient  5. Back")
            choice = input("Choice: ")

            if choice == "1":
                self.add_patient()

            elif choice == "2":
                self.show_rows("SELECT * FROM patients", "Patients")

            elif choice == "3":
                pid = self.get_text("Patient ID: ")
                self.show_rows(
                    "SELECT * FROM patients WHERE patient_id = ?"
                    .replace("?", "?"),
                    "Patient Search"
                ) if False else None
                row = self.conn.execute(
                    "SELECT * FROM patients WHERE patient_id = ?", (pid,)
                ).fetchone()
                print(row if row else "Patient not found.")

            elif choice == "4":
                pid = self.get_text("Patient ID to update: ")
                if not self.exists("patients", "patient_id", pid):
                    print("Patient not found.")
                    continue

                name = self.get_text("New name: ")
                age = int(self.get_number("New age: ", 1))
                if age > 120:
                    raise ValueError("Age cannot exceed 120.")
                gender = self.get_text("New gender: ")
                contact = self.get_text("New 10-digit contact: ")

                if not contact.isdigit() or len(contact) != 10:
                    raise ValueError("Invalid contact number.")

                disease = input("New disease/condition: ").strip()

                self.conn.execute("""
                    UPDATE patients SET name=?, age=?, gender=?,
                    contact=?, disease=? WHERE patient_id=?
                """, (name, age, gender, contact, disease, pid))
                self.conn.commit()
                print("Patient updated.")

            elif choice == "5":
                break
            else:
                print("Invalid choice.")

    def doctor_menu(self):
        while True:
            print("\n1. Add Doctor  2. View Doctors  3. Back")
            choice = input("Choice: ")

            if choice == "1":
                did = self.get_text("Doctor ID: ")
                name = self.get_text("Doctor name: ")
                specialization = self.get_text("Specialization: ")
                schedule = self.get_text("Schedule: ")

                self.conn.execute(
                    "INSERT INTO doctors VALUES (?, ?, ?, ?)",
                    (did, name, specialization, schedule)
                )
                self.conn.commit()
                print("Doctor added.")

            elif choice == "2":
                self.show_rows("SELECT * FROM doctors", "Doctors")

            elif choice == "3":
                break
            else:
                print("Invalid choice.")

    def appointment_menu(self):
        while True:
            print("\n1. Book  2. View  3. Cancel  4. Back")
            choice = input("Choice: ")

            if choice == "1":
                pid = self.get_text("Patient ID: ")
                did = self.get_text("Doctor ID: ")

                if not self.exists("patients", "patient_id", pid):
                    print("Patient not found.")
                    continue
                if not self.exists("doctors", "doctor_id", did):
                    print("Doctor not found.")
                    continue

                date = self.get_text("Date (DD-MM-YYYY): ")
                time = self.get_text("Time (HH:MM): ")
                datetime.strptime(date, "%d-%m-%Y")
                datetime.strptime(time, "%H:%M")

                conflict = self.conn.execute("""
                    SELECT 1 FROM appointments
                    WHERE doctor_id=? AND date=? AND time=?
                """, (did, date, time)).fetchone()

                if conflict:
                    print("Doctor already has an appointment at that time.")
                    continue

                self.conn.execute("""
                    INSERT INTO appointments (patient_id, doctor_id, date, time)
                    VALUES (?, ?, ?, ?)
                """, (pid, did, date, time))
                self.conn.commit()
                print("Appointment booked.")

            elif choice == "2":
                self.show_rows("""
                    SELECT a.appointment_id, p.name, d.name, a.date, a.time
                    FROM appointments a
                    JOIN patients p ON p.patient_id=a.patient_id
                    JOIN doctors d ON d.doctor_id=a.doctor_id
                    ORDER BY a.date, a.time
                """, "Appointments")

            elif choice == "3":
                aid = int(self.get_number("Appointment ID: ", 1))
                cursor = self.conn.execute(
                    "DELETE FROM appointments WHERE appointment_id=?", (aid,)
                )
                self.conn.commit()
                print("Appointment cancelled." if cursor.rowcount else
                      "Appointment not found.")

            elif choice == "4":
                break
            else:
                print("Invalid choice.")

    def room_menu(self):
        while True:
            print("\n1. Add Room  2. View Rooms")
            print("3. Allocate Room  4. Release Room  5. Back")
            choice = input("Choice: ")

            if choice == "1":
                room_no = int(self.get_number("Room number: ", 1))
                room_type = self.get_text("Room type: ")
                self.conn.execute(
                    "INSERT INTO rooms VALUES (?, ?, 1)",
                    (room_no, room_type)
                )
                self.conn.commit()
                print("Room added.")

            elif choice == "2":
                self.show_rows("""
                    SELECT room_no, room_type,
                    CASE WHEN available=1 THEN 'Available'
                    ELSE 'Occupied' END FROM rooms
                """, "Rooms")

            elif choice in ("3", "4"):
                room_no = int(self.get_number("Room number: ", 1))
                room = self.conn.execute(
                    "SELECT available FROM rooms WHERE room_no=?",
                    (room_no,)
                ).fetchone()

                if not room:
                    print("Room not found.")
                    continue

                if choice == "3" and room[0] == 1:
                    self.conn.execute(
                        "UPDATE rooms SET available=0 WHERE room_no=?",
                        (room_no,)
                    )
                    print("Room allocated.")
                elif choice == "4" and room[0] == 0:
                    self.conn.execute(
                        "UPDATE rooms SET available=1 WHERE room_no=?",
                        (room_no,)
                    )
                    print("Room released.")
                else:
                    print("Room status does not allow this operation.")

                self.conn.commit()

            elif choice == "5":
                break
            else:
                print("Invalid choice.")

    def resource_menu(self):
        while True:
            print("\n1. Add Stock  2. View Stock")
            print("3. Issue Resource  4. Back")
            choice = input("Choice: ")

            if choice == "1":
                name = self.get_text("Resource name: ")
                quantity = int(self.get_number("Quantity to add: ", 0))

                self.conn.execute("""
                    INSERT INTO resources (name, quantity) VALUES (?, ?)
                    ON CONFLICT(name) DO UPDATE
                    SET quantity = quantity + excluded.quantity
                """, (name, quantity))
                self.conn.commit()
                print("Stock updated.")

            elif choice == "2":
                self.show_rows("SELECT * FROM resources", "Resources")

            elif choice == "3":
                name = self.get_text("Resource name: ")
                quantity = int(self.get_number("Quantity to issue: ", 1))
                row = self.conn.execute(
                    "SELECT quantity FROM resources WHERE name=?", (name,)
                ).fetchone()

                if not row:
                    print("Resource not found.")
                elif row[0] < quantity:
                    print("Insufficient stock.")
                else:
                    self.conn.execute(
                        "UPDATE resources SET quantity=quantity-? WHERE name=?",
                        (quantity, name)
                    )
                    self.conn.commit()
                    print("Resource issued. Remaining:", row[0] - quantity)

            elif choice == "4":
                break
            else:
                print("Invalid choice.")

    def history_menu(self):
        while True:
            print("\n1. Add Medical History  2. View History  3. Back")
            choice = input("Choice: ")

            if choice == "1":
                pid = self.get_text("Patient ID: ")
                if not self.exists("patients", "patient_id", pid):
                    print("Patient not found.")
                    continue

                diagnosis = self.get_text("Diagnosis: ")
                treatment = input("Treatment: ").strip()
                notes = input("Notes: ").strip()

                self.conn.execute("""
                    INSERT INTO medical_history
                    (patient_id, diagnosis, treatment, notes)
                    VALUES (?, ?, ?, ?)
                """, (pid, diagnosis, treatment, notes))
                self.conn.commit()
                print("Medical history saved.")

            elif choice == "2":
                self.show_rows("""
                    SELECT h.history_id, p.name, h.diagnosis,
                    h.treatment, h.notes
                    FROM medical_history h
                    JOIN patients p ON p.patient_id=h.patient_id
                """, "Medical History")

            elif choice == "3":
                break
            else:
                print("Invalid choice.")

    def prescription_menu(self):
        while True:
            print("\n1. Add Prescription  2. View Prescriptions  3. Back")
            choice = input("Choice: ")

            if choice == "1":
                pid = self.get_text("Patient ID: ")
                did = self.get_text("Doctor ID: ")

                if not self.exists("patients", "patient_id", pid):
                    print("Patient not found.")
                    continue
                if not self.exists("doctors", "doctor_id", did):
                    print("Doctor not found.")
                    continue

                medicine = self.get_text("Medicine: ")
                dosage = self.get_text("Dosage: ")
                duration = self.get_text("Duration: ")
                instructions = input("Instructions: ").strip()

                self.conn.execute("""
                    INSERT INTO prescriptions
                    (patient_id, doctor_id, medicine, dosage, duration, instructions)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (pid, did, medicine, dosage, duration, instructions))
                self.conn.commit()
                print("Prescription saved.")

            elif choice == "2":
                self.show_rows("""
                    SELECT pr.prescription_id, p.name, d.name, pr.medicine,
                    pr.dosage, pr.duration, pr.instructions
                    FROM prescriptions pr
                    JOIN patients p ON p.patient_id=pr.patient_id
                    JOIN doctors d ON d.doctor_id=pr.doctor_id
                """, "Prescriptions")

            elif choice == "3":
                break
            else:
                print("Invalid choice.")

    def billing_menu(self):
        while True:
            print("\n1. Create Bill  2. View Bills")
            print("3. Mark Bill Paid  4. Back")
            choice = input("Choice: ")

            if choice == "1":
                pid = self.get_text("Patient ID: ")
                if not self.exists("patients", "patient_id", pid):
                    print("Patient not found.")
                    continue

                consultation = self.get_number("Consultation charge: ")
                room_charge = self.get_number("Room charge: ")
                medicine_charge = self.get_number("Medicine charge: ")
                other_charge = self.get_number("Other charges: ")
                total = consultation + room_charge + medicine_charge + other_charge

                self.conn.execute("""
                    INSERT INTO bills
                    (patient_id, consultation, room_charge, medicine_charge,
                     other_charge, total, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'Pending')
                """, (pid, consultation, room_charge, medicine_charge,
                      other_charge, total))
                self.conn.commit()
                print(f"Bill created. Total: Rs. {total:.2f}")

            elif choice == "2":
                self.show_rows("""
                    SELECT b.bill_id, p.name, b.total, b.status
                    FROM bills b JOIN patients p
                    ON p.patient_id=b.patient_id
                """, "Bills")

            elif choice == "3":
                bill_id = int(self.get_number("Bill ID: ", 1))
                cursor = self.conn.execute(
                    "UPDATE bills SET status='Paid' WHERE bill_id=?",
                    (bill_id,)
                )
                self.conn.commit()
                print("Bill marked paid." if cursor.rowcount else
                      "Bill not found.")

            elif choice == "4":
                break
            else:
                print("Invalid choice.")

    def dashboard(self):
        print("\n========== HOSPITAL DASHBOARD ==========")
        tables = ["patients", "doctors", "appointments", "rooms", "resources"]

        for table in tables:
            count = self.conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            print(f"Total {table.title()}: {count}")

        available = self.conn.execute(
            "SELECT COUNT(*) FROM rooms WHERE available=1"
        ).fetchone()[0]
        occupied = self.conn.execute(
            "SELECT COUNT(*) FROM rooms WHERE available=0"
        ).fetchone()[0]
        revenue = self.conn.execute(
            "SELECT COALESCE(SUM(total), 0) FROM bills WHERE status='Paid'"
        ).fetchone()[0]
        pending = self.conn.execute(
            "SELECT COALESCE(SUM(total), 0) FROM bills WHERE status='Pending'"
        ).fetchone()[0]

        print("Available rooms:", available)
        print("Occupied rooms:", occupied)
        print(f"Paid bills total: Rs. {revenue:.2f}")
        print(f"Pending bills total: Rs. {pending:.2f}")

    def run(self):
        menus = {
            "1": ("Patient Management", self.patient_menu),
            "2": ("Doctor Management", self.doctor_menu),
            "3": ("Appointment Management", self.appointment_menu),
            "4": ("Room Management", self.room_menu),
            "5": ("Resource Management", self.resource_menu),
            "6": ("Medical History", self.history_menu),
            "7": ("Prescriptions", self.prescription_menu),
            "8": ("Billing", self.billing_menu),
            "9": ("Dashboard and Reports", self.dashboard)
        }

        try:
            while True:
                print("\n====== HOSPITAL MANAGEMENT SYSTEM ======")
                for key, (name, _) in menus.items():
                    print(f"{key}. {name}")
                print("0. Exit")

                choice = input("Enter choice: ").strip()

                if choice == "0":
                    break

                if choice not in menus:
                    print("Invalid choice.")
                    continue

                try:
                    menus[choice][1]()
                except ValueError as error:
                    print("Invalid input:", error)
                except sqlite3.IntegrityError:
                    print("Record already exists or violates a database rule.")
                except sqlite3.Error as error:
                    print("Database error:", error)

        finally:
            self.conn.close()
            print("Hospital system closed.")


if __name__ == "__main__":
    app = HospitalManagementSystem()
    app.run()
