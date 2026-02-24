# YACS: Yet Another Centralized Scheduler

## Project Overview
YACS is a centralized scheduling framework designed to simulate a Master-Worker architecture for executing Map-Reduce jobs. The system manages a central Master entity that coordinates task distribution across multiple simulated worker machines, balancing the load based on various scheduling algorithms.

This project was developed as a final class project for CS322: Big Data at PES University.

## Features
* **Centralized Master:** Orchestrates job requests, manages task dependencies, and tracks worker availability.
* **Worker Simulation:** Simulates three machines with configurable processing slots.
* **Map-Reduce Support:** Handles jobs containing mappers and reducers, ensuring reducers only start after all associated mappers are complete.
* **Scheduling Algorithms:** Supports three distinct scheduling strategies:
    * **Round Robin (RR):** Assigns tasks in a cyclic manner to the first available worker.
    * **Random:** Selects a worker at random to process the next task.
    * **Least Load (LL):** Assigns tasks to the worker with the maximum number of empty slots.
* **Multi-threaded Architecture:** Utilizes Python’s `threading` and `socket` libraries to handle parallel requests and worker communication.

## Tech Stack
* **Language:** Python
* **Concurrency:** Multithreading with Mutex Locks to prevent race conditions
* **Networking:** TCP Socket Programming
* **Analysis:** Matplotlib and NumPy for performance logging and plotting

## Project Structure
* `master.py`: The core scheduler that listens for jobs (Port 5000) and worker updates (Port 5001).
* `worker.py`: Simulates task execution using `time.sleep()` based on task duration.
* `config.json`: Configuration file defining worker IDs, available slots, and communication ports.
* `analysis.py`: Calculates mean and median performance metrics for the different algorithms.
* `plot.py`: Generates visualizations of slot utilization over time.
* `requests.py`: Simulates sending job requests to the Master.

## Installation & Usage

### 1. Configure Workers
Modify `config.json` to define your worker environment:
```json
{
  "workers": [
    {"worker_id": 1, "slots": 5, "port": 4000},
    {"worker_id": 2, "slots": 7, "port": 4001},
    {"worker_id": 3, "slots": 3, "port": 4002}
  ]
}
```

### 2. Run the Framework
You must start the workers first, followed by the master with a specified algorithm.

**Start Workers (Example for Worker 1):**
```bash
python worker.py 4000 1
```

**Start Master:**
Provide the scheduling algorithm (`RR`, `Random`, or `LL`) as a command-line argument:
```bash
python master.py RR
```

**Send Requests:**
```bash
python requests.py
```

### 3. Performance Analysis
After the jobs are completed, run the analysis script to view the mean and median task completion times:
```bash
python analysis.py
```

## Performance Results
Based on testing with 10 job requests, the **Round Robin** algorithm generally provided the best performance, though margins between algorithms were small.

## Contributors
* R. Tharun Raj (Master, Worker)
* G. Deepank (Algorithms, Plotting)
* Darshan A. Pirgal (Worker, Plotting)
* K. Sreesh Reddy (Master, Debugging)
