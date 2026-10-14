# AI-Powered Predictive Maintenance for IoT Devices

A beginner-friendly, software-only predictive-maintenance project. It simulates IoT sensor readings, trains a machine-learning classifier, evaluates its performance, and provides a Streamlit dashboard plus a Flask prediction API.

> **Important:** The included sensor data is synthetic simulation data, not real industrial telemetry. The model is an educational prototype and must not be used to make safety-critical maintenance decisions.

## Features
- Simulated temperature, vibration, and current readings
- Failure-risk labels for supervised learning
- Random Forest model training and evaluation
- Saved model and evaluation charts
- Interactive Streamlit dashboard
- Flask `/predict` API endpoint

## Project structure
```text
AI-Predictive-Maintenance-IoT/
├── data/                 # Generated simulated data
├── docs/                 # Project notes
├── images/               # Put screenshots here
├── models/               # Trained model (generated)
├── notebooks/            # Optional experiments
├── outputs/              # Evaluation charts and metrics (generated)
├── src/
│   ├── __init__.py
│   ├── simulator.py
│   ├── train.py
│   └── predict.py
├── api.py                # Flask REST API
├── app.py                # Streamlit dashboard
├── main.py               # Run the complete pipeline
├── requirements.txt
└── .gitignore
```

## Requirements
- Python 3.10–3.12 recommended
- Internet is needed only to install the packages; no hardware or cloud account is required.
- Windows, macOS, or Linux

## Windows setup
Open Command Prompt or the VS Code terminal in this folder:
```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

If `py` is not recognized, try `python` instead.

## macOS / Linux setup
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

The pipeline creates `data/iot_sensor_data.csv`, `models/predictive_maintenance_model.joblib`, `outputs/metrics.json`, and evaluation charts.

## Launch the dashboard
After running `python main.py` once:
```bash
streamlit run app.py
```
Open the local address shown in the terminal (usually `http://localhost:8501`). Adjust sensor readings in the sidebar to get a prediction.

## Launch the API
Open a second terminal, activate the same virtual environment, then run:
```bash
python api.py
```
The API runs locally at `http://127.0.0.1:5000`.

Test from another terminal:
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"temperature\": 78, \"vibration\": 4.8, \"current\": 13.5}"
```
Expected response format:
```json
{"prediction": 1, "risk": "HIGH", "probability": 0.91}
```
Exact probability and metrics can differ by package versions and random split.

## Model inputs
- `temperature`: simulated temperature in °C
- `vibration`: simulated vibration level (arbitrary units)
- `current`: simulated current in A
- `failure`: target label (`1` = simulated failure risk, `0` = normal)

## How the simulation works
The simulator samples plausible ranges and creates a risk label from combined sensor thresholds plus a small amount of noise. The model learns those simulated patterns. This demonstrates a complete ML workflow, but performance on synthetic data does not establish real-world predictive accuracy.

## Outputs and screenshots
Save screenshots of:
1. Dataset preview
2. Terminal showing training/evaluation
3. Confusion matrix (`outputs/confusion_matrix.png`)
4. Feature importance (`outputs/feature_importance.png`)
5. Dashboard with a prediction
6. API test response

## GitHub publishing
Create a repository named `AI-Predictive-Maintenance-IoT`, then from this folder:
```bash
git init
git add .
git commit -m "Build simulated predictive maintenance ML pipeline"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/AI-Predictive-Maintenance-IoT.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username. Do not commit virtual environments or private credentials.

## Suggested improvements
- Replace synthetic data with a documented public industrial dataset.
- Use time-based validation to prevent leakage when working with sequential data.
- Add drift monitoring, alert history, authentication, and deployment tests.
- Calibrate risk thresholds with domain experts before any real-world use.
