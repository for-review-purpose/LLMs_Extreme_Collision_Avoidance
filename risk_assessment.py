"""
risk_assessment.py

Provides functions to calculate risk levels for both obstacles and traffic participants.
"""

import torch
import torch.nn as nn
import random
import os
# from scenario_manager3 import get_self_car_data  # To get ego vehicle data

# Define the MLP model matching the .pth parameters
class CustomMLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(CustomMLP, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x

# Load model at module level to avoid redundant loading in each function call
def load_model(model_path="HJ_Reachability/safe_value_params.pth"):
    """
    Load the trained model parameters and return the model.
    """
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the model file
    model_path = os.path.join(current_dir, model_path)
    
    input_dim = 4      # First layer kernel shape: [256, 4]
    hidden_dim = 256   # Hidden layer kernel shape: [256, 256]
    output_dim = 1     # Output layer kernel shape: [1, 256]

    model = CustomMLP(input_dim, hidden_dim, output_dim)

    # Load saved parameters
    params = torch.load(model_path)

    # Map the parameters to PyTorch model keys
    mapped_params = {
        'fc1.weight': params['MLP_0_Dense_0_kernel'].T.clone().detach(),
        'fc1.bias': params['MLP_0_Dense_0_bias'].clone().detach(),
        'fc2.weight': params['MLP_0_Dense_1_kernel'].T.clone().detach(),
        'fc2.bias': params['MLP_0_Dense_1_bias'].clone().detach(),
        'fc3.weight': params['OutputVDense_kernel'].T.clone().detach(),
        'fc3.bias': params['OutputVDense_bias'].clone().detach(),
    }

    # Load the mapped parameters into the model
    model.load_state_dict(mapped_params)
    model.eval()  # Set to evaluation mode

    print("[INFO] Model parameters loaded successfully!")
    return model

# Load model once at module level
model = load_model("HJ_Reachability/safe_value_params.pth")

def preprocess_input(ego_vehicle, obstacle):
    """
    Preprocess ego vehicle and obstacle data into [x, y, phi, vx] format for the model.

    Normalization rules:
    - x = (-ego_x + 50) / 50: Relative x position normalized
    - y = abs(ego_y) / 8: Absolute y distance normalized
    - phi = abs(ego_phi) / 40: Yaw angle normalized (default to 0 if unavailable)
    - vx = ego_vx / 18: X velocity normalized
    """
    # Extract ego vehicle data
    ego_x, ego_y = ego_vehicle["coordinate"]
    ego_vx, ego_vy = ego_vehicle["velocity"]
    phi = 0.0  # Default yaw angle (adjust if available)

    # Extract obstacle data
    obs_x, obs_y = obstacle["center"]

    # Compute relative coordinates with obstacle as center
    rel_x = ego_x - obs_x
    rel_y = ego_y - obs_y

    # Normalize the inputs
    x = (rel_x + 50) / 50
    y = abs(rel_y) / 8
    phi_normalized = abs(phi) / 40
    vx_normalized = ego_vx / 18

    # Create input tensor [x, y, phi, vx]
    input_vector = torch.tensor([x, y, phi_normalized, vx_normalized], dtype=torch.float32)
    return input_vector

def run_collision_risk_model(ego_vehicle, obstacles, participants):
    """
    Calculate risk levels for obstacles and participants.

    Returns:
        - obstacle_risk_levels: { obstacle_id: risk_value in [0..1] }
        - participant_risk_levels: { participant_id: risk_value in [0..1] }

    Uses the loaded PyTorch model for obstacle risk assessment.
    """
    # Get ego vehicle data for relative calculations

    # Process obstacles
    obstacle_risk_levels = {}
    for obs in obstacles:
        obs_id = obs["id"]
        if "center" in obs:
            # Preprocess input data
            input_vector = preprocess_input(ego_vehicle, obs)

            # Run the model to get risk score
            with torch.no_grad():
                risk_score = model(input_vector.unsqueeze(0))  # Add batch dimension (1, 4)

            # Convert to scalar and clamp to [0, 1]
            risk_score = risk_score.item()
            risk = (risk_score + 30) / 30
            risk = max(0.0, min(1.0, risk))
            obstacle_risk_levels[obs_id] = round(risk, 2)
        else:
            # Default risk for obstacles without "center"
            obstacle_risk_levels[obs_id] = round(random.uniform(0.3, 0.35), 2)

    # Process participants
    participant_risk_levels = {}
    for p in participants:
        pid = p["id"]
        if p["type"] == "Pedestrian":
            participant_risk_levels[pid] = 1
        elif p["type"] == "Small Car":
            participant_risk_levels[pid] = 0.5
        else:
            participant_risk_levels[pid] = 0.8

    return obstacle_risk_levels, participant_risk_levels

# Test the module if run independently
if __name__ == "__main__":
    from scenario_manager3 import get_self_car_data
    ego_vehicle = get_self_car_data()
    print("[TEST] Running risk assessment with dummy data...")

    # Dummy test data
    obstacles = [{"id": "obs1", "center": (25, 5)}]
    participants = [{"id": "p1", "type_code": 0}]

    obs_risks, part_risks = run_collision_risk_model(ego_vehicle, obstacles, participants)
    print("Obstacle Risks:", obs_risks)
    print("Participant Risks:", part_risks)
