# AI-Driven-EV-BMS-DigitalTwin
# ⚡ AI-Driven EV Battery Management System (BMS) Digital Twin

A zero-hardware, software-in-the-loop (SIL) Battery Management System simulator built entirely on **Python, MySQL, and Streamlit**. This project models the core components of an Electric Vehicle (EV) battery pack, estimates the State of Charge (SOC) dynamically, and runs a predictive logic engine to intercept hazardous thermal runaways.

---

## 📌 Problem Statement
Traditional Battery Management Systems heavily rely on hardware-dependent, static algorithms. These systems often struggle to accurately predict rapid thermal variations and calculate non-linear State-of-Charge (SOC) under dynamic driving loads. This leads to severe "range anxiety" for users and increases the risk of undetected thermal runaways (battery fires) in extreme operational conditions.

## 💡 Reason Behind the Problem
Lithium-ion battery cells exhibit highly volatile, non-linear electrochemical behaviors. Physical sensors mounted on a battery pack can only report current boundary readings ($Voltage, Current, Temperature$). They lack the inherent ability to forecast internal stress conditions, simulate worst-case failure scenarios, or scale telemetry handling without expensive, high-risk physical laboratory testing setups.

## 🚀 The Solution
This project introduces a **Digital Twin Framework** that bypasses physical constraints entirely through software simulation:
1. **Data Layer (MySQL):** Simulates the vehicle's electronic control unit (ECU) data logger, ingesting streaming streams of live pack parameters.
2. **Analytical Layer (Python):** Cleanses incoming database logs, maps precise non-linear Open-Circuit Voltage (OCV) curves to evaluate real-time SOC, and evaluates boundary limits for predictive cell health.
3. **Frontend Analytics Dashboard (Streamlit):** Translates dense operational parameters into a scannable, interactive user interface featuring real-time telemetry charting, dynamic safety status triggers, and variable workload simulators.

---

## 🏗️ System Architecture & Workflow



1. User alters the **Virtual Hardware Simulator** controls via the Streamlit sidebar dashboard.
2. Simulated telemetry payload ($V, I, T$) is pushed and committed into the **MySQL Database Engine**.
3. The **Python Backend** dynamically fetches the latest logs, passing them through analytical estimation filters.
4. **Streamlit UI Components** re-render dynamically, displaying performance charts, raw metrics, and safety flags.

---

## 🌟 Key Advantages
* **Zero Hardware Constraints:** Eliminates components cost and physical laboratory hazards, offering a safe playground to simulate over-voltage and over-temperature battery stresses.
* **Proactive Safety Integration:** Intercepts high-rate temperature surges before a fault state arises, showcasing modern proactive fault management.
* **Fleet Management Foundation:** The structured relational database tier creates a framework capable of handling remote telemetry logging for thousands of virtual assets concurrently.

---

## 🛠️ Tech Stack & Prerequisites
Make sure you have the following installed on your machine:
* **Database:** MySQL Server (v8.0+)
* **Runtime:** Python (v3.9+)
* **Libraries:** `streamlit`, `mysql-connector-python`, `pandas`, `numpy`

---

## 🚀 Setup & Installation Instructions

### 1. Database Initialization
Execute the following schema script within your MySQL instance to construct the target repository database:
```sql
CREATE DATABASE EV_BMS_DB;
USE EV_BMS_DB;

CREATE TABLE BatteryTelemetry (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    voltage FLOAT,      
    current FLOAT,      
    temperature FLOAT   
);
