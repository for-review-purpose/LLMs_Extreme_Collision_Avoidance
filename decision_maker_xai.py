# decision_maker.py
import time
from openai import OpenAI
import config  # Import config
import re

def generate_collision_avoidance_decision(current_scenario_text, similar_docs):
    # Build system_prompt, user_prompt
    system_prompt = f"""\
    Now you are an assistant for driving decision-making in automotive crisis conditions.If the recommended maneuver is 3 or 4 (Turn left/right to change lanes, with braking), explicitly state the target reduced speed and justify why that speed is appropriate. Reason first, make sure the answer is logical. Your response should use the following format:
    <reasoning for decision>
    Response to user:  
    
    Meaning of Action_id:
    {''.join([f"{k} => {v}" for k, v in config.DECISION_CODES.items()])}
    
    """

    if not similar_docs:
        historical_text = "No historical data is available."
    else:
        lines = []
        for i, doc in enumerate(similar_docs):
            lines.append(
                f"[Historical Case {i+1}]\n"
                f"{doc.page_content}\n"
                f"Decision Code: {doc.metadata.get('decision_code', 'None')}\n"
                f"Evaluation: {doc.metadata.get('evaluation', 'None')}\n"
            )
        historical_text = "\n\n".join(lines)

    user_prompt = (
        f"{config.DECISION_PROMPT_References}"
        f"CURRENT SCENARIO:\n{current_scenario_text}\n\n"
        f"HISTORICAL SCENARIOS:\n{historical_text}\n\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],

    start_time = time.perf_counter()

    client = OpenAI(
        api_key=config.XAI_API_KEY,
        base_url="https://api.x.ai/v1",
    )

    response = client.chat.completions.create(
        model=config.XAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
    )

    # response = openai.chat.completions.create(
    #     model=config.OPENAI_MODEL,
    #     max_tokens=3000,
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_prompt}
    #     ],
    #     temperature=config.TEMPERATURE_DECISION  # Use config param
    # )
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    token_usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    decision_str = response.choices[0].message.content.strip()

    pattern = r"Response to user:\s*(\d+)"
    match = re.search(pattern, decision_str)
    if match:
        decision_code = int(match.group(1))
    else:
        decision_code = 8  # fallback

    # 打印 token 使用情况（可选）
    print("[Token Usage] Prompt Tokens: {}, Completion Tokens: {}, Total Tokens: {}".format(
        token_usage.get("prompt_tokens", 0),
        token_usage.get("completion_tokens", 0),
        token_usage.get("total_tokens", 0)
    ))

    return decision_code,elapsed_time,decision_str

def generate_decision_evaluation(scenario_text, decision_code, execution_result):
    system_prompt = (
        "You are a collision avoidance strategy evaluator. "
        "Provide an analysis of the chosen strategy and potential improvements.=Please reply with no more than two sentences and no more than 50 words."
    )
    user_prompt = (
        f"SCENARIO:\n{scenario_text}\n\n"
        f"DECISION CODE: {decision_code}\n\n"
        f"EXECUTION RESULT:\n{execution_result}\n\n"
        "Please evaluate this decision and suggest improvements."
    )

    start_time = time.perf_counter()

    client = OpenAI(
        api_key=config.OPENAI_API_KEY,
        base_url="https://api.x.ai/v1",
    )

    response = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=config.TEMPERATURE_EVAL  # Use config param
    )
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    return response.choices[0].message.content.strip(),elapsed_time
