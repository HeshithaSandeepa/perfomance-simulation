import simpy
import argparse
from index import (
    inter_arrival_time, 
    customer, 
    run_experiment,
    NUM_TELLERS,
    SERVICE_RATE_PER_HR
)

# --- Setup Function (Single Queue Logic) ---
def setup(env, arrival_rate, service_rate, results, num_tellers):
    # 2 Tellers 1 Queue
    bank_tellers = simpy.Resource(env, capacity=num_tellers) 
    i = 0
    while True:
        yield env.timeout(inter_arrival_time(arrival_rate))
        i += 1
        env.process(customer(env, f'C{i}', bank_tellers, service_rate, results))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scenario 2/3: Single Queue Simulation.")
    # Console Input -Get arrival Rate
    parser.add_argument('arrival_rate', type=int, help="Customer Arrival Rate (Lambda) per hour (e.g., 18 or 22 for High Load)")
    
    args = parser.parse_args()
    
    # Input එක run_experiment Function එකට යවයි
    run_experiment(
        setup, 
        NUM_TELLERS, 
        args.arrival_rate, 
        SERVICE_RATE_PER_HR, 
        "Scenario 2: Single Queue (Optimized 1 Queue/High Load)"
    )