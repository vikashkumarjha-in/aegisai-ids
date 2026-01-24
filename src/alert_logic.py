def generate_alert(prediction):
    """
    Converts model prediction into IDS alert
    """
    if prediction == 1:
        return " ALERT: Intrusion Detected"
    else:
        return " Normal Traffic"
