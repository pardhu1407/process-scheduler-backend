from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for processes (replace with database in production)
processes_db = []

@app.route('/api/processes', methods=['GET', 'POST'])
def handle_processes():
    if request.method == 'POST':
        data = request.json
        processes_db.extend(data['processes'])
        return jsonify({"message": "Processes saved successfully", "count": len(processes_db)}), 201
    else:
        return jsonify({"processes": processes_db})

@app.route('/api/processes/clear', methods=['POST'])
def clear_processes():
    global processes_db
    processes_db = []
    return jsonify({"message": "All processes cleared"})

@app.route('/api/processes/random', methods=['POST'])
def generate_random_processes():
    global processes_db
    count = request.json.get('count', 5)
    new_processes = []
    
    for i in range(count):
        new_processes.append({
            "arrivalTime": random.randint(0, 10),
            "burstTime": random.randint(1, 10),
            "priority": random.randint(1, 5)
        })
    
    processes_db.extend(new_processes)
    return jsonify({"message": f"{count} random processes generated", "processes": new_processes})

@app.route('/api/simulate/<algorithm>', methods=['POST'])
def simulate(algorithm):
    data = request.json
    processes = data.get('processes', [])
    time_quantum = data.get('timeQuantum', 2)
    
    if not processes:
        return jsonify({"error": "No processes provided"}), 400
    
    # Here you would call your actual simulation functions
    # For now, we'll return mock data
    results = {
        "gantt": generate_mock_gantt(processes, algorithm),
        "metrics": generate_mock_metrics(processes, algorithm)
    }
    
    return jsonify(results)

def generate_mock_gantt(processes, algorithm):
    gantt = []
    colors = {
        'fcfs': 'blue',
        'sjf': 'green',
        'priority': 'orange',
        'roundRobin': 'yellow',
        'srtf': 'purple'
    }
    current_time = 0
    
    for i, process in enumerate(processes):
        duration = process['burstTime']
        if algorithm == 'roundRobin':
            duration = min(duration, 2)  # Mock time quantum of 2
        
        gantt.append({
            "name": f"P{i+1}",
            "startTime": current_time,
            "endTime": current_time + duration,
            "duration": duration * 20,  # Scale for visualization
            "color": colors.get(algorithm, 'blue')
        })
        current_time += duration
    
    return gantt

def generate_mock_metrics(processes, algorithm):
    avg_waiting = random.uniform(1, 10)
    avg_turnaround = avg_waiting + random.uniform(1, 5)
    
    return {
        "avgWaitingTime": round(avg_waiting, 2),
        "avgTurnaroundTime": round(avg_turnaround, 2),
        "avgResponseTime": round(avg_waiting * 0.8, 2),
        "cpuUtilization": round(random.uniform(70, 95), 2)
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)