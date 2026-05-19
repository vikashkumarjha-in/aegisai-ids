def classify_severity(
    prediction: str,
    src_bytes: int,
    count: int
):

    if prediction == "normal":

        return "low"

    if count > 400 or src_bytes > 4000:

        return "critical"

    if count > 200 or src_bytes > 2000:

        return "high"

    return "medium"

def generate_alert(
    prediction: str,
    features: dict
):

    severity = classify_severity(

        prediction,

        features.get("src_bytes", 0),

        features.get("count", 0)
    )

    return {

        "prediction":
            prediction,

        "severity":
            severity,

        "alert":
            prediction != "normal",

        "message":

            f"{'THREAT DETECTED' if prediction != 'normal' else 'Normal Traffic'} | Severity: {severity.upper()}"
    }