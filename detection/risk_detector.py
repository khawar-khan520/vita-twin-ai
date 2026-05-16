def detect_risk(retrieved_entries):

    if not retrieved_entries:
        return {
            "risk_level": "LOW",
            "avg_stress": 0,
            "avg_sleep": 8,
            "reason": ["No data found"]
        }

    stress_values = []
    sleep_values = []

    for entry in retrieved_entries:
        stress = entry.get("stress_level", 0)
        sleep = entry.get("sleep_hours", 8)

        stress_values.append(stress)
        sleep_values.append(sleep)

    avg_stress = sum(stress_values) / len(stress_values)
    avg_sleep = sum(sleep_values) / len(sleep_values)

    # Risk logic
    if avg_stress >= 7 or avg_sleep < 5:
        risk_level = "HIGH"
        reason = ["High stress detected", "Low sleep detected"]

    elif avg_stress >= 4:
        risk_level = "MEDIUM"
        reason = ["Moderate stress detected"]

    else:
        risk_level = "LOW"
        reason = ["Normal mental health indicators"]

    return {
        "risk_level": risk_level,
        "avg_stress": round(avg_stress, 2),
        "avg_sleep": round(avg_sleep, 2),
        "reason": reason
    }