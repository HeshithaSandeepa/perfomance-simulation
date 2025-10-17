import simpy
import random
import argparse
from index import (
    inter_arrival_time, 
    customer, 
    run_experiment,
    NUM_TELLERS,
    SERVICE_RATE_PER_HR
)

# ---  Setup Function (Multiple Queues Logic) ---
def setup(env, arrival_rate, service_rate, results, num_tellers):
    # Teller 2ක්
    teller_a = simpy.Resource(env, capacity=1)
    teller_b = simpy.Resource(env, capacity=1)
    
    i = 0
    while True:
        yield env.timeout(inter_arrival_time(arrival_rate))
        i += 1
        
        # 50% chance to join Teller A, 50% to Teller B (Random Choice)
        if random.random() < 0.5:
            env.process(customer(env, f'C{i}_A', teller_a, service_rate, results))
        else:
            env.process(customer(env, f'C{i}_B', teller_b, service_rate, results))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scenario 1: Multiple Queues Simulation.")
    # Console Input - Get Arrival Rate 
    parser.add_argument('arrival_rate', type=int, help="Customer Arrival Rate (Lambda) per hour (e.g., 18)")
    
    args = parser.parse_args()
    
    # Input එක run_experiment Function එකට යැවීම
    run_experiment(
        setup, 
        NUM_TELLERS, 
        args.arrival_rate, 
        SERVICE_RATE_PER_HR, 
        "Scenario 1: Multiple Queues (Normal-Day/High Load)"
    )