
# Cyclone Relief & Resource Management System

## 📌 Project Overview

The **Cyclone Relief & Resource Management System** is a web-based decision support application that uses **ontology-based reasoning** to assist disaster management during cyclone events. The system analyzes cyclone parameters such as wind speed and water level to infer severity, evacuation requirements, and responsible authorities.

This project demonstrates the integration of **Semantic Web technologies (OWL axioms)** with a **Python-based backend** and a **simple frontend interface**.

---

## 🎯 Objectives

* To model cyclone disaster knowledge using ontology
* To infer cyclone severity and evacuation needs using OWL axioms
* To identify responsible disaster management authorities automatically
* To provide a simple web interface for real-time analysis

---

## 🧠 System Architecture

**Frontend → Backend → Ontology → Reasoner → Output**

* **Frontend:** HTML, CSS, Vanilla JavaScript
* **Backend:** Python, Flask
* **Ontology:** OWL (designed in Protégé)
* **Reasoner:** Pellet (via owlready2)
* **Data Exchange:** REST API (JSON)

---

## ⚙️ Technologies Used

* HTML5, CSS3, JavaScript
* Python 3
* Flask
* owlready2
* Pellet Reasoner
* Protégé (Ontology Editor)

---

## 🧩 Ontology Design

The ontology models key disaster management concepts such as:

* Cyclone types and severity levels
* Evacuation plans
* Disaster management authorities
* Relationships between cyclone severity and response actions

All inferences are performed using **OWL axioms** (no SWRL rules).

---

## 🔄 Working Flow

1. User enters cyclone details via the frontend
2. Data is sent to the backend using a REST API
3. Backend creates ontology individuals dynamically
4. Severity is classified using numeric thresholds
5. Ontology reasoner infers evacuation and authority
6. Results are returned as JSON and displayed on the UI

---

## ▶️ How to Run the Project

### 1️⃣ Backend Setup

```bash
cd Backend
python -m venv venv
venv\Scripts\activate   # On Windows
pip install flask flask-cors owlready2
python app.py
```

Backend runs at:

```
http://127.0.0.1:5000
```

---

### 2️⃣ Frontend Setup

* Open `index.html` using Live Server or a local server
* Ensure backend is running before submitting the form

---

## 📊 Output

The system displays:

* Cyclone severity level
* Evacuation requirement (Yes/No)
* Responsible disaster management authority

---

## 🚀 Future Enhancements

* Integration with real-time weather APIs
* Map-based visualization of affected areas
* Resource allocation recommendations
* Data persistence and analysis history
* Deployment on cloud platforms

---

## 🎓 Academic Relevance

This project demonstrates:

* Practical use of ontology in decision support systems
* Semantic reasoning using OWL axioms
* Real-world frontend–backend integration
* Clean separation of logic, reasoning, and presentation layers
