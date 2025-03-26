# main.py

import time
import config


from Test_scene.scenario_manager_test1 import (
    get_self_car_data,
    get_obstacle_data,
    get_traffic_participants_data,
    build_scenario_description,
    get_execution_result
)
from risk_assessment import run_collision_risk_model
from database_manager import store_scenario, retrieve_similar_scenarios
from decision_maker_openai import generate_collision_avoidance_decision, generate_decision_evaluation
from database_manager import store_scenario, retrieve_similar_scenarios

def main():
    # 1. Data Collection
    ego_vehicle = get_self_car_data()
    obstacles = get_obstacle_data() 
    participants = get_traffic_participants_data()

    # 2. Risk Assessment
    obstacle_risk_levels, participant_risk_levels = run_collision_risk_model(
        ego_vehicle, 
        obstacles,
        participants
    )

    # 3. Scenario Analysis
    
    scenario_text = build_scenario_description(
        ego_vehicle,
        obstacles,
        participants, 
        obstacle_risk_levels,
        participant_risk_levels
    )
    print("=== Current Scenario ===")
    print(scenario_text)

    # 4. Retrieve similar scenarios
    similar_docs = retrieve_similar_scenarios(scenario_text)
    print("=== similar_docs===")
    print(similar_docs)

    # 5. Decision Making
    decision_start = time.perf_counter()
    decision_code, decision_api_time, messages = generate_collision_avoidance_decision(
        scenario_text, 
        similar_docs
    )
    decision_end = time.perf_counter()
    decision_duration = decision_end - decision_start

    print("\n=== Decision Code ===")
    print(decision_code, "->", config.DECISION_CODES.get(decision_code, "Unknown"))

    # 6. Execution & Evaluation
    execution_result = get_execution_result(decision_code)
    eval_text, eval_api_time = generate_decision_evaluation(
        scenario_text,
        decision_code, 
        execution_result
    )
    print("\n=== Evaluation ===")
    print(eval_text)

    # 7. Store scenario
    # store_scenario(scenario_text, decision_code, eval_text)
    print("\n[Info] Stored scenario, decision, and evaluation.")

    # 8. Performance Metrics
    print(f"[Timing Info] Decision Generation Time: {decision_duration:.4f} seconds")
    print(f"[Timing] OpenAI decision call: {decision_api_time:.4f} s")
    print(messages)

if __name__ == "__main__":
    main()
