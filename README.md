# LLMs_Collision_Avoidance_Decision

This study proposes a scenario-aware collision avoidance (SACA) framework that integrates predictive risk assessment, data-driven reasoning, and scenario-preview-based deployment to improve collision avoidance decision-making.

## Features

- Risk Assessment: Uses a trained MLP model to evaluate collision risks for obstacles and traffic participants
- Scenario Analysis: Generates detailed scenario descriptions based on vehicle and obstacle data
- Decision Making: Leverages LLMs for intelligent collision avoidance decisions
- Data Storage: Stores and retrieves similar scenarios for better decision support

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd LLMs_Collision_Avoidance_Decision
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
.
├── HJ_Reachability/           # Risk assessment model files
├── Test_scene/               # Test scenarios and data
├── main.py                   # Main entry point
├── risk_assessment.py        # Risk assessment module
├── decision_maker_openai.py  # Decision making using OpenAI
├── database_manager.py       # Database operations
├── config.py                 # Configuration settings
└── requirements.txt          # Project dependencies
```

## Usage

1. Run the main program:
```bash
python main.py
```

2. The program will:
   - Collect vehicle and obstacle data
   - Assess collision risks
   - Generate scenario descriptions
   - Make collision avoidance decisions
   - Store results for future reference

## Model Details

The risk assessment model is based on a custom MLP (Multi-Layer Perceptron) with:
- Input dimension: 4 (relative position, velocity, etc.)
- Hidden layers: 256 neurons
- Output: HJ Reachability Value

### Model Configuration
If you need to use a different model, please modify the model path in `config.py`:
```python
OPENAI_MODEL = “gpt-4o-mini”  # Change this to your model path
```

## Dependencies

- torch: Deep learning framework
- numpy: Numerical computing
- openai: OpenAI API integration
- langchain: LLM framework
- chromadb: Vector database for scenario storage
- googletrans: Translation support
- oss2: Cloud storage integration
