# 🏥 Medical Appointment System

A full-stack medical appointment booking system that connects **patients**, **doctors**, and **admins** through a seamless platform for managing medical appointments, schedules, and health-related notes.

---

## 📌 Features

### 👨‍⚕️ Doctor Role
- View all assigned appointments.
- Accept or reject appointment requests.
- Add notes to each patient after sessions.
- View weekly schedule categorized by:
  - Accepted appointments.
  - Rejected appointments.
  - All appointments per day.

### 🧑‍💼 Admin Role
- Add, update, or delete doctors and patients.
- Assign appointments manually if needed.

https://github.com/user-attachments/assets/0cca24f5-934e-49c9-8602-f38fba93ce20


- View and manage all system users.
- Monitor system activity.

### 👤 Patient Role
- Register and log in.
- Book appointments with available doctors.
- View accepted/rejected status.
- Cancel upcoming appointments.
- View doctor notes from past appointments.

---

## 🧰 Tech Stack

### 🔹 Backend
- **Django** & **Django REST Framework**
- **JWT Authentication** (using Simple JWT)
- PostgreSQL Database (optional SQLite for dev)
- Custom User Model

### 🔹 Frontend
- **React** + **MUI (Material UI)**
- Axios for API communication
- Day.js for time/date formatting
- React Router DOM

---

## 🚀 Getting Started

### 🔧 Backend Setup

```bash
# Clone the repo
git clone https://github.com/RehabKamal601/medical_project.git
cd medical_project

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Migrate and run server
python manage.py migrate
python manage.py runserver



https://github.com/user-attachments/assets/719d0f70-d6a7-4f37-ab29-bdc155497df9

# Medical-Project-React-Django
