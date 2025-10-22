import simpy
import random
import statistics
import time

RANDOM_SEED = 42        
SIM_TIME = 120             # Simulation time 2h
MIN_SERVICE_TIME = 3.0   
MAX_SERVICE_TIME = 10.0  

# =========================================================================
# Simulation Model Logic
# =========================================================================
# bank, customers , queue management

class BankBranch:
   
    def __init__(self, env, num_counters):
        self.env = env
        self.counter = simpy.Resource(env, capacity=num_counters)

    def serve_customer(self, customer_name,results_collector):
       #customer arrive time
        arrival_time = self.env.now
        
        with self.counter.request() as request:
            #wait for counter to be free
            yield request
            
            wait_time = self.env.now - arrival_time
            results_collector['wait_times'].append(wait_time)

            service_time = random.expovariate(MIN_SERVICE_TIME / MAX_SERVICE_TIME)
            yield self.env.timeout(service_time)
            #for utilization tracking
            results_collector['service_times'].append(service_time)

#make customers
def customer_generator(env, bank, interarrival_time, results_collector):
  
    customer_id = 0
    while True:
        # wait for next customer
        time_to_next_arrival = random.expovariate(1.0 / interarrival_time)
        yield env.timeout(time_to_next_arrival)
        
        # new customer arrives
        customer_id += 1
        customer_name = f'Customer {customer_id}'
        
        env.process(bank.serve_customer(customer_name, results_collector))

# =========================================================================
# run simulation for given scenario
# =========================================================================

def run_simulation(scenario_name, num_counters, interarrival_time, sim_duration):
  
    print(f"   > Scenario: '{scenario_name}' (Counter = {num_counters}) running...")
    
    results = {'wait_times': [], 'service_times': []}
    random.seed(RANDOM_SEED)  
    
    env = simpy.Environment()
    bank = BankBranch(env, num_counters) 
    env.process(customer_generator(env, bank, interarrival_time, results))
    
    env.run(until=sim_duration)
    utilization = 0.0 

    if results['wait_times']:
        avg_wait = statistics.mean(results['wait_times'])
        max_wait = max(results['wait_times'])
        total_customers = len(results['wait_times'])

        # --- Utilization Calculation
        if results['service_times']: # service_times තියෙනවද බලන්න
            total_busy_time = sum(results['service_times'])
            total_available_time = num_counters * sim_duration
            if total_available_time > 0:
                utilization = (total_busy_time / total_available_time) * 100.0
        
        return {
            "name": scenario_name,
            "avg_wait": avg_wait,
            "max_wait": max_wait,
            "total_customers": total_customers,
            "utilization_percent": utilization

        }
    else:
        return {"name": scenario_name, "avg_wait": 0, "max_wait": 0, "total_customers": 0}

# =========================================================================
# 4. (Main Program)
# =========================================================================

# get user input for number of counters
def get_num_counters():
    while True: 
        try:
            user_input = input("\n>>> Enter No of Counters (ex: 2): ")
            num = int(user_input)
            if num < 1:
                print("Error:Your must enter 1 or more counters")
            else:
                return num 
        except ValueError:
            print("Error: Invalid input. Please enter a valid integer.")


if __name__ == "__main__":
    
    print("===== Bank Simulation =====")
    

    counters_to_test = get_num_counters()
    start_time = time.time()
    
    # ---define 3 scenarios---
    scenarios_to_run = [
        {
            "name": "Scenario 1: Normal Day",
            "interarrival_time": 5.0 
        },
        {
            "name": "Scenario 2: Salary Day",
            "interarrival_time": 3.0
        },
        {
            "name": "Scenario 3: Aswesuma Day",
            "interarrival_time": 2.0 
        }
    ]
    
    # run all scenarios
    all_results = []
    for s in scenarios_to_run:
        result = run_simulation(
            scenario_name=s["name"],
            num_counters=counters_to_test,  
            interarrival_time=s["interarrival_time"],
            sim_duration=SIM_TIME
        )
        all_results.append(result)
        
    end_time = time.time()

    # final result table
    print("\n\n" + "="*50)
    print(f"Tested Counters {counters_to_test}")
    print("="*50)
    
    print(f"{'Scenario':<30} | {'Total Customers':<15} | {'Normal Waiting Time':<25} | {'Maximum Waiting Time':<25} | {'Utilization (%)':<15}")
    print("-"*120)
    
    for res in all_results:
        print(f"{res['name']:<30} | {res['total_customers']:<15} | {res['avg_wait']:<25.2f} | {res['max_wait']:<25.2f} | {res['utilization_percent']:<15.2f}")