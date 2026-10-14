from src.simulator import generate_dataset
from src.train import train_and_evaluate

def main():
    print("\n=== AI Predictive Maintenance: complete pipeline ===")
    data_path = generate_dataset()
    print(f"\nDataset saved: {data_path}")
    train_and_evaluate(data_path)
    print("\nDone! Run `streamlit run app.py` for the dashboard or `python api.py` for the API.")

if __name__ == "__main__":
    main()
