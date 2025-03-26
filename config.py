# config.py
import os

# 1) OpenAI API Key
OPENAI_API_KEY = "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"
XAI_API_KEY = "xai-fWTPMBOAnC0styn4gqU0cQsmK5uR5Kni6ALMldULer9IkvYMzjfxd11XVTueDCu50wvHeh0ABCWBhQ43"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY  # 让其他模块也能从环境变量中获取

# 2) Chroma Database
CHROMA_PERSIST_DIR = "./collision_avoidance_chroma_db"

# 3) OpenAI Model & Hyperparameters
OPENAI_MODEL = "gpt-4o-mini"
XAI_MODEL = "grok-2-latest"
# OPENAI_MODEL = "ft:gpt-4o-mini-2024-07-18:tsinghua-university:0305:B7pPgZJq"
# OPENAI_MODEL = "ft:gpt-4o-2024-08-06:tsinghua-university::B38EMfMa"
TEMPERATURE_DECISION = 0  # For decision generation
TEMPERATURE_EVAL = 0       # For evaluation generation

# 4) Retrieval
NUM_SIMILAR_SCENARIOS = 1    # k值: 每次检索多少个相似历史场景

# 5) Decision Code Meaning
DECISION_CODES = {
    0: "Full emergency braking",
    1: "Turn left sharply to change lanes and resume direction",
    2: "Turn right sharply to change lanes and resume direction",
    3: "Turn left to change lanes, with braking",
    4: "Turn right to change lanes, with braking",
    5: "T-type drift avoidance maneuver, ending with the car perpendicular to the lane, facing left",
    6: "T-type drift avoidance maneuver, ending with the car perpendicular to the lane, facing right",
    7: "No need to intervene"
}


# # =================== DECISION RULES ===================
DECISION_PROMPT_References = """
# References for decision making:
# 1.The energy-absorbing structures of a vehicle are typically located at the front and rear ends, designed to absorb impact forces and reduce harm to the driver. In contrast, the sides of the vehicle are structurally weaker.\\\\n\\\\nAdditionally, electric vehicle (EV) battery protection mechanisms are primarily designed for front and rear collisions. As a result, side collisions pose a greater risk to EVs, potentially leading to fires.\\\\n\\\\nBased on these structural and battery protection mechanisms, it is preferable to direct collisions toward the front or rear of the vehicle whenever possible. For high-speed lateral approaching targets (TTC <= 1.3s), a T-type drift avoidance maneuver should be employed to ensure that the rear of the vehicle collides with the target.\\\\n\\\\nTherefore, when a collision avoidance intervention is necessary and the target meets the following conditions:\\\\n- Located in front of the vehicle,\\\\n- Lateral distance is less than 8 meters,\\\\n- Lateral velocity is greater than 4 m/s and directed towards the vehicle, \\\\n\\\\nthe 5 or 6 maneuver (T-type drift avoidance maneuver) should be applied.\n
# Whichever side is safer is the one you should turn to for T-type collision avoidance.
"""

