from alert_logic import generate_alert

def simulate_prediction(prediction):
    alert = generate_alert(prediction)
    print(alert)

if __name__ == "__main__":
    print("Simulating predictions...\n")
    simulate_prediction(0)
    simulate_prediction(1)
