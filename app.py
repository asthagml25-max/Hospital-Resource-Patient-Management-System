
from flask import Flask, request
import sqlite3
from datetime import datetime
from html import escape

app = Flask(__name__)


def setup():
    with sqlite3.connect("hospital.db") as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                contact TEXT NOT NULL,
                disease TEXT
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id TEXT PRIMARY KEY,
                name TEXT,
                specialization TEXT,
                schedule TEXT
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT,
                doctor_id TEXT,
                date TEXT,
                time TEXT
            )
        """)


def page(content):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hospital Management System</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                font-family: Arial, sans-serif;
                background: #eef4f9;
                margin: 0;
                color: #26374a;
            }}

            header {{
                background: linear-gradient(120deg, #1769aa, #2584c7);
                color: white;
                padding: 25px;
                text-align: center;
            }}

            header h1 {{
                margin: 0;
                font-size: 30px;
            }}

            header p {{
                margin-bottom: 0;
            }}

            nav {{
                background: #ffffff;
                padding: 15px;
                text-align: center;
                box-shadow: 0 3px 8px #00000010;
            }}

            nav a {{
                display: inline-block;
                text-decoration: none;
                margin: 5px;
            }}

            button {{
                padding: 12px 15px;
                background: #1769aa;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
            }}

            button:hover {{
                background: #104c80;
            }}

            main {{
                max-width: 1000px;
                margin: 30px auto;
                padding: 0 20px;
                min-height: 55vh;
            }}

            .box {{
                background: white;
                padding: 28px;
                border-radius: 12px;
                box-shadow: 0 4px 15px #0000000d;
                margin-bottom: 22px;
            }}

            h2 {{
                color: #1769aa;
                margin-top: 0;
            }}

            .dashboard {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
                gap: 18px;
            }}

            .card {{
                background: white;
                padding: 22px;
                border-radius: 12px;
                border: 1px solid #dce7f1;
                box-shadow: 0 3px 12px #00000008;
            }}

            .card h3 {{
                color: #1769aa;
                margin-top: 0;
            }}

            .card a {{
                color: #1769aa;
                text-decoration: none;
                font-weight: bold;
            }}

            form {{
                max-width: 650px;
            }}

            input, select {{
                display: block;
                width: 100%;
                padding: 12px;
                margin: 9px 0 17px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-size: 15px;
                background: white;
            }}

            label {{
                font-weight: bold;
                font-size: 14px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
            }}

            th, td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
                text-align: left;
                font-size: 14px;
            }}

            th {{
                background: #dceafa;
                color: #174b7a;
            }}

            tr:hover {{
                background: #f5f9fd;
            }}

            .table-wrap {{
                overflow-x: auto;
            }}

            .message {{
                background: #e8f4ff;
                color: #174b7a;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 15px;
            }}

            footer {{
                text-align: center;
                padding: 22px;
                background: white;
                color: #64748b;
                border-top: 1px solid #dce7f1;
            }}

            @media (max-width: 600px) {{
                header h1 {{
                    font-size: 23px;
                }}

                .box {{
                    padding: 18px;
                }}
            }}
        </style>
    </head>

    <body>
        <header>
            <h1>✚ Hospital Management System</h1>
            <p>Patient Care and Hospital Administration Portal</p>
        </header>

        <nav>
            <a href="/"><button>Home</button></a>
            <a href="/add_patient"><button>Add Patient</button></a>
            <a href="/patients"><button>View Patients</button></a>
            <a href="/add_doctor"><button>Add Doctor</button></a>
            <a href="/doctors"><button>View Doctors</button></a>
            <a href="/add_appointment"><button>Add Appointment</button></a>
            <a href="/appointments"><button>View Appointments</button></a>
            <a href="/exit"><button>Exit</button></a>
        </nav>

        <main>
            {content}
        </main>

        <footer>
            Hospital Management System | Python, Flask and SQLite
        </footer>
    </body>
    </html>
    """


# HOME PAGE

@app.route("/")
def home():
    with sqlite3.connect("hospital.db") as db:
        patients = db.execute(
            "SELECT COUNT(*) FROM patients"
        ).fetchone()[0]

        doctors = db.execute(
            "SELECT COUNT(*) FROM doctors"
        ).fetchone()[0]

        appointments = db.execute(
            "SELECT COUNT(*) FROM appointments"
        ).fetchone()[0]

    return page(f"""
        <div class="box">
            <h2>Welcome to the Hospital Management System</h2>
            <p>
                Manage patients, doctors and appointments through
                this simple hospital management website.
            </p>
        </div>

        <div class="dashboard">
            <div class="card">
                <h3>Total Patients</h3>
                <h2>{patients}</h2>
                <a href="/patients">View Patient Records</a>
            </div>

            <div class="card">
                <h3>Total Doctors</h3>
                <h2>{doctors}</h2>
                <a href="/doctors">View Doctor Records</a>
            </div>

            <div class="card">
                <h3>Total Appointments</h3>
                <h2>{appointments}</h2>
                <a href="/appointments">View Appointments</a>
            </div>
        </div>

        <div class="box" style="margin-top:22px;">
            <h2>Hospital Services</h2>
            <p>Choose an option from the navigation menu above.</p>
            <p>• Register and view patients</p>
            <p>• Register and view doctors</p>
            <p>• Schedule and view appointments</p>
        </div>
    """)


# ADD PATIENT

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        contact = request.form.get("contact", "").strip()
        disease = request.form.get("disease", "").strip()

        if not all([name, age, gender, contact]):
            return page("""
                <div class="box">
                    <h2>Add Patient</h2>
                    <div class="message">
                        Please fill in all required fields.
                    </div>
                    <a href="/add_patient">Try Again</a>
                </div>
            """)

        try:
            age = int(age)
            if age < 0 or age > 130:
                raise ValueError
        except ValueError:
            return page("""
                <div class="box">
                    <h2>Invalid Age</h2>
                    <div class="message">
                        Please enter a valid age between 0 and 130.
                    </div>
                    <a href="/add_patient">Try Again</a>
                </div>
            """)

        with sqlite3.connect("hospital.db") as db:
            db.execute("""
                INSERT INTO patients
                (name, age, gender, contact, disease)
                VALUES (?, ?, ?, ?, ?)
            """, (name, age, gender, contact, disease))

        return page("""
            <div class="box">
                <h2>Patient Added Successfully!</h2>
                <p>The patient record has been saved.</p>
                <a href="/patients"><button>View Patients</button></a>
                <a href="/add_patient"><button>Add Another Patient</button></a>
            </div>
        """)

    return page("""
        <div class="box">
            <h2>Add Patient</h2>
            <p>Enter the patient's details below.</p>

            <form method="post">
                <label>Patient Name *</label>
                <input name="name" placeholder="Enter full name"
                       maxlength="100" required>

                <label>Age *</label>
                <input type="number" name="age"
                       placeholder="Enter age" min="0" max="130" required>

                <label>Gender *</label>
                <select name="gender" required>
                    <option value="">Select Gender</option>
                    <option>Male</option>
                    <option>Female</option>
                    <option>Other</option>
                    <option>Prefer not to say</option>
                </select>

                <label>Contact Number *</label>
                <input name="contact" placeholder="Enter contact number"
                       maxlength="30" required>

                <label>Disease or Health Issue</label>
                <input name="disease" placeholder="Enter health issue"
                       maxlength="300">

                <button type="submit">Save Patient</button>
            </form>
        </div>
    """)


# VIEW PATIENTS

@app.route("/patients")
def view_patients():
    with sqlite3.connect("hospital.db") as db:
        patients = db.execute("""
            SELECT patient_id, name, age, gender, contact, disease
            FROM patients
            ORDER BY patient_id DESC
        """).fetchall()

    rows = ""

    for p in patients:
        rows += "<tr>" + "".join(
            f"<td>{escape(str(value if value is not None else '-'))}</td>"
            for value in p
        ) + "</tr>"

    if not rows:
        rows = """
            <tr>
                <td colspan="6" style="text-align:center;">
                    No patient records found. Add a patient first.
                </td>
            </tr>
        """

    return page(f"""
        <div class="box">
            <h2>Patient Records</h2>
            <p>View all registered patients below.</p>

            <div class="table-wrap">
                <table>
                    <tr>
                        <th>Patient ID</th>
                        <th>Name</th>
                        <th>Age</th>
                        <th>Gender</th>
                        <th>Contact</th>
                        <th>Disease</th>
                    </tr>
                    {rows}
                </table>
            </div>

            <br>
            <a href="/add_patient"><button>Add Patient</button></a>
        </div>
    """)


# ADD DOCTOR

@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":
        doctor_id = request.form.get("doctor_id", "").strip()
        name = request.form.get("name", "").strip()
        specialization = request.form.get("specialization", "").strip()
        schedule = request.form.get("schedule", "").strip()

        if not all([doctor_id, name, specialization, schedule]):
            return page("""
                <div class="box">
                    <h2>Add Doctor</h2>
                    <p class="message">Please fill in all fields.</p>
                    <a href="/add_doctor">Try Again</a>
                </div>
            """)

        try:
            with sqlite3.connect("hospital.db") as db:
                db.execute(
                    "INSERT INTO doctors VALUES (?, ?, ?, ?)",
                    (doctor_id, name, specialization, schedule)
                )

            return page("""
                <div class="box">
                    <h2>Doctor Added Successfully!</h2>
                    <a href="/doctors"><button>View Doctors</button></a>
                    <a href="/add_doctor"><button>Add Another Doctor</button></a>
                </div>
            """)

        except sqlite3.IntegrityError:
            return page("""
                <div class="box">
                    <h2>Doctor ID Already Exists</h2>
                    <p>Please use a different doctor ID.</p>
                    <a href="/add_doctor"><button>Try Again</button></a>
                </div>
            """)

    return page("""
        <div class="box">
            <h2>Add Doctor</h2>
            <form method="post">
                <label>Doctor ID</label>
                <input name="doctor_id" placeholder="e.g. D101" required>

                <label>Doctor Name</label>
                <input name="name" placeholder="Doctor Name" required>

                <label>Specialization</label>
                <input name="specialization"
                       placeholder="e.g. Cardiologist" required>

                <label>Schedule</label>
                <input name="schedule"
                       placeholder="e.g. Monday-Friday, 10 AM-2 PM" required>

                <button type="submit">Save Doctor</button>
            </form>
        </div>
    """)


# VIEW DOCTORS

@app.route("/doctors")
def view_doctors():
    with sqlite3.connect("hospital.db") as db:
        doctors = db.execute(
            "SELECT * FROM doctors ORDER BY name"
        ).fetchall()

    rows = ""

    for d in doctors:
        rows += "<tr>" + "".join(
            f"<td>{escape(str(value))}</td>" for value in d
        ) + "</tr>"

    if not rows:
        rows = """
            <tr>
                <td colspan="4" style="text-align:center;">
                    No doctors registered yet.
                </td>
            </tr>
        """

    return page(f"""
        <div class="box">
            <h2>Doctor Records</h2>
            <div class="table-wrap">
                <table>
                    <tr>
                        <th>Doctor ID</th>
                        <th>Name</th>
                        <th>Specialization</th>
                        <th>Schedule</th>
                    </tr>
                    {rows}
                </table>
            </div>
            <br>
            <a href="/add_doctor"><button>Add Doctor</button></a>
        </div>
    """)


# ADD APPOINTMENT

@app.route("/add_appointment", methods=["GET", "POST"])
def add_appointment():
    with sqlite3.connect("hospital.db") as db:
        doctors = db.execute(
            "SELECT doctor_id, name FROM doctors ORDER BY name"
        ).fetchall()

    if request.method == "POST":
        patient = request.form.get("patient", "").strip()
        doctor_id = request.form.get("doctor_id", "").strip()
        date = request.form.get("date", "").strip()
        time = request.form.get("time", "").strip()

        if not all([patient, doctor_id, date, time]):
            return page("""
                <div class="box">
                    <h2>Add Appointment</h2>
                    <p class="message">Please fill in all fields.</p>
                    <a href="/add_appointment">Try Again</a>
                </div>
            """)

        try:
            appointment_date = datetime.strptime(date, "%Y-%m-%d").date()
            datetime.strptime(time, "%H:%M")

            if appointment_date < datetime.today().date():
                return page("""
                    <div class="box">
                        <h2>Invalid Appointment Date</h2>
                        <p>Please select today or a future date.</p>
                        <a href="/add_appointment">Try Again</a>
                    </div>
                """)

        except ValueError:
            return page("""
                <div class="box">
                    <h2>Invalid Date or Time</h2>
                    <p>Please select a valid appointment date and time.</p>
                    <a href="/add_appointment">Try Again</a>
                </div>
            """)

        with sqlite3.connect("hospital.db") as db:
            doctor = db.execute(
                "SELECT doctor_id FROM doctors WHERE doctor_id=?",
                (doctor_id,)
            ).fetchone()

            if not doctor:
                return page("""
                    <div class="box">
                        <h2>Invalid Doctor</h2>
                        <p>Please select a registered doctor.</p>
                        <a href="/add_appointment">Try Again</a>
                    </div>
                """)

            booked = db.execute("""
                SELECT appointment_id FROM appointments
                WHERE doctor_id=? AND date=? AND time=?
            """, (doctor_id, date, time)).fetchone()

            if booked:
                return page("""
                    <div class="box">
                        <h2>Time Slot Unavailable</h2>
                        <p>The doctor already has an appointment at this time.</p>
                        <a href="/add_appointment"><button>Choose Another Time</button></a>
                    </div>
                """)

            db.execute("""
                INSERT INTO appointments
                (patient_name, doctor_id, date, time)
                VALUES (?, ?, ?, ?)
            """, (patient, doctor_id, date, time))

        return page("""
            <div class="box">
                <h2>Appointment Added Successfully!</h2>
                <a href="/appointments"><button>View Appointments</button></a>
                <a href="/add_appointment"><button>Book Another Appointment</button></a>
            </div>
        """)

    if not doctors:
        return page("""
            <div class="box">
                <h2>Add Appointment</h2>
                <p>Please add a doctor before booking an appointment.</p>
                <a href="/add_doctor"><button>Add Doctor</button></a>
            </div>
        """)

    options = "".join(
        f'<option value="{escape(d[0], quote=True)}">'
        f'{escape(d[1])} ({escape(d[0])})</option>'
        for d in doctors
    )

    return page(f"""
        <div class="box">
            <h2>Add Appointment</h2>
            <form method="post">
                <label>Patient Name</label>
                <input name="patient" placeholder="Enter patient name" required>

                <label>Select Doctor</label>
                <select name="doctor_id" required>
                    <option value="">Select Doctor</option>
                    {options}
                </select>

                <label>Appointment Date</label>
                <input type="date" name="date"
                       min="{datetime.today().strftime('%Y-%m-%d')}" required>

                <label>Appointment Time</label>
                <input type="time" name="time" required>

                <button type="submit">Book Appointment</button>
            </form>
        </div>
    """)


# VIEW APPOINTMENTS

@app.route("/appointments")
def view_appointments():
    with sqlite3.connect("hospital.db") as db:
        appointments = db.execute("""
            SELECT a.appointment_id, a.patient_name,
                   d.name, a.date, a.time
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.date, a.time
        """).fetchall()

    rows = ""

    for a in appointments:
        rows += "<tr>" + "".join(
            f"<td>{escape(str(value))}</td>" for value in a
        ) + "</tr>"

    if not rows:
        rows = """
            <tr>
                <td colspan="5" style="text-align:center;">
                    No appointments scheduled yet.
                </td>
            </tr>
        """

    return page(f"""
        <div class="box">
            <h2>Appointment Records</h2>
            <div class="table-wrap">
                <table>
                    <tr>
                        <th>Appointment ID</th>
                        <th>Patient Name</th>
                        <th>Doctor Name</th>
                        <th>Date</th>
                        <th>Time</th>
                    </tr>
                    {rows}
                </table>
            </div>
            <br>
            <a href="/add_appointment"><button>Add Appointment</button></a>
        </div>
    """)


# EXIT

@app.route("/exit")
def exit_app():
    return page("""
        <div class="box">
            <h2>Thank You!</h2>
            <p>You have reached the exit page of the Hospital Management System.</p>
            <p>Your saved records remain in the database.</p>
            <p>To stop the Python server, press Ctrl+C in the VS Code terminal.</p>
            <a href="/"><button>Return Home</button></a>
        </div>
    """)


if __name__ == "__main__":
    setup()
    print("Hospital Management System is running.")
    print("Open Chrome and visit http://127.0.0.1:5000")
    app.run(debug=True)
