# Hospital Management System Database

## Project Overview

This project implements a comprehensive SQL database for a hospital management system using SQLite. It manages patients, doctors, appointments, medical tests, prescriptions, and insurance claims in a structured relational database.

### Key Features

- Patient demographics and contact management
- Doctor directory with specialties
- Appointment scheduling and status tracking
- Prescription records linked to appointments
- Medical tests catalog with cost tracking
- Patient test history and results
- Insurance claim processing and approvals

### Database Tables

1. **Patients** - Patient information and demographics
2. **Doctors** - Doctor profiles and specialties
3. **Appointments** - Appointment scheduling and status
4. **Prescriptions** - Medication prescriptions
5. **MedicalTests** - Available tests and costs
6. **PatientTests** - Patient test history and results
7. **InsuranceClaims** - Insurance claim records

---

## Setup & Installation

### Prerequisites

- Python 3.7 or higher
- Jupyter Notebook
- pip (Python package manager)

### Step 2: Create Virtual environment

Open terminal and run:

```bash
python -m venv .venv
```

### Step 2: Install Dependencies

Open terminal and run:

```bash
pip install -r requirements.txt
```

### Step 3: Open the Project

- Navigate to `app.ipynb` and open it in Jupyter
- Run all cells sequentially from top to bottom

### Step 4: Run the Notebook

The notebook will:

1. Load SQL extension
2. Create SQLite database connection (`hospital.db`)
3. Create all 7 tables with relationships
4. Insert sample data
5. Execute example queries

---

**Project Location:** `d:\sql probelms\hospital-db\`  
**Database File:** `hospital.db` (auto-created on first run)
