def detect_risk(entries):
    """
    Simple rule-based mental health risk detection
    """

    stress_scores = [e["stress_level"] for e in entries]
    sleep_hours = [e["sleep_hours"] for e in entries]

    avg_stress = sum(stress_scores) / len(stress_scores)
    avg_sleep = sum(sleep_hours) / len(sleep_hours)

    risk_level = "LOW"

    if avg_stress >= 8 and avg_sleep <= 5:
        risk_level = "HIGH"
    elif avg_stress >= 6:
        risk_level = "MEDIUM"

    explanation = {
        "avg_stress": avg_stress,
        "avg_sleep": avg_sleep,
        "risk_level": risk_level,
        "reason": []
    }

    if avg_stress >= 6:
        explanation["reason"].append("Consistently high stress levels detected")

    if avg_sleep <= 5:
        explanation["reason"].append("Low sleep pattern observed")

    return explanation


# test
if __name__ == "__main__":
    sample = [
        {"stress_level": 8, "sleep_hours": 4},
        {"stress_level": 7, "sleep_hours": 5},
        {"stress_level": 9, "sleep_hours": 3}
    ]

    print(detect_risk(sample))