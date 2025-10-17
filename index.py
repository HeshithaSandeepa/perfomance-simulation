import simpy
import random
import numpy as np

# --- (Common Constants) ---
RANDOM_SEED = 42 
SIM_TIME = 420 # 7 hours in minutes
NUM_REPLICATIONS = 10 # run 10 times for accuracy
NUM_TELLERS = 2 #no of workers in this bank
SERVICE_RATE_PER_HR = 6 # 10 minutes per customer 

# --- 2. Distribution Functions ---
def inter_arrival_time(rate_hr):
    return random.expovariate(rate_hr / 60.0)

def service_time(rate_hr):
    return random.expovariate(rate_hr / 60.0)

# --- Customer Process Function ---
def customer(env, name, teller_resource, service_rate, results):
    arrival_time = env.now
    
    with teller_resource.request() as request:
        yield request 
        
        waiting_time = env.now - arrival_time
        results['wait_times'].append(waiting_time)
        
        yield env.timeout(service_time(service_rate))
        # Record total time in for customer request
        results['system_times'].append(env.now - arrival_time)

# --- Experiment Runner Logic (Results) ---
def calculate_metrics(results, num_tellers, sim_time, service_rate):
    if results['wait_times']:
        throughput = len(results['system_times'])
        avg_service_time = 60.0 / service_rate
        total_service_time_needed = throughput * avg_service_time
        total_teller_time_available = num_tellers * sim_time
        
        utilization = total_service_time_needed / total_teller_time_available if total_teller_time_available > 0 else 0
        
        return {
            'Avg_Wait_Time': np.mean(results['wait_times']),
            'Utilization': utilization * 100,
            'Throughput': throughput
        }
    return {'Avg_Wait_Time': 0, 'Utilization': 0, 'Throughput': 0}

# ---  Main Experiment Function ---
def run_experiment(setup_func, num_tellers, arrival_rate, service_rate, scenario_name):
    avg_wait_times = []
    avg_utilization = []
    
    for _ in range(NUM_REPLICATIONS):
        random.seed(RANDOM_SEED + _) 
        results = {'wait_times': [], 'system_times': []}
        env = simpy.Environment()
        
        env.process(setup_func(env, arrival_rate, service_rate, results, num_tellers))
        env.run(until=SIM_TIME)
        
        metrics = calculate_metrics(results, num_tellers, SIM_TIME, service_rate)
        
        if metrics['Throughput'] > 0:
            avg_wait_times.append(metrics['Avg_Wait_Time'])
            avg_utilization.append(metrics['Utilization'])

    final_wait = round(np.mean(avg_wait_times), 2)
    final_util = round(np.mean(avg_utilization), 2)
    
    print(f"\n--- {scenario_name} ---")
    print(f"  Arrival Rate (λ): {arrival_rate}/hr")
    print(f"  Service Rate (μ): {service_rate}/hr")
    print(f"  Avg Wait Time (min): {final_wait}")
    print(f"  Avg Utilization (%): {final_util}%")
    
    return final_wait, final_util, arrival_rate