# 🏦 Bank Queue Performance Simulation  


## 📘 Overview  

This project simulates the performance of a **bank branch queue system** using **Python** and the **SimPy** library.  
It models customer arrivals, service times, and counter utilization to analyze performance under varying workloads.  

---

## ⚙️ Key Features  

✅ **Three Customer Load Scenarios**  
| Scenario | Description | Avg. Arrival Interval |
|-----------|--------------|------------------------|
| 🟢 Scenario 1 | Normal Day | 5.0 min between arrivals |
| 🟡 Scenario 2 | Salary Day | 3.0 min between arrivals |
| 🔴 Scenario 3 | Aswesuma Day | 2.0 min between arrivals |

✅ **Performance Metrics**
- 🧍‍♂️ **Total Customers Served**
- ⏱️ **Average Wait Time (Normal Waiting Time)**
- 🕒 **Maximum Wait Time**
- 💼 **Counter Utilization (%)**

✅ **Dynamic Counter Configuration**  
You can set the number of available **counters (tellers)** for each simulation run.  

---

## 🧩 Requirements  

You’ll need **Python 3.8+** and the following package:  

```bash
pip install simpy
```
The modules statistics, random, and time are part of Python’s standard library.

## How to Run

- Navigate to the project directory in your terminal.
- Run the simulation script:
```bash
python bank_simulation.py
```

