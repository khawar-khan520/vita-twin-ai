"""
risk_detection.py - Early detection of mental health deterioration patterns
Author: VitaTwin AI Team

Detects:
  - Burnout risk
  - Anxiety escalation
  - Depression indicators
  - Sleep deprivation
  - Social withdrawal
  - Emotional deterioration over time
"""

from dataclasses import dataclass


# ── Risk thresholds ────────────────────────────────────────────────────────────
THRESHOLDS = {
    "critical_mood":        3,    # mood ≤ 3 = critical
    "high_stress":          7,    # stress ≥ 7 = high
    "low_sleep":            5.5,  # sleep ≤ 5.5h = concerning
    "critical_sleep":       4.5,  # sleep ≤ 4.5h = critical
    "high_anxiety":         7,    # anxiety ≥ 7 = high
    "burnout_streak":       3,    # 3+ consecutive days of high stress + low sleep
    "deterioration_delta": -2,    # mood drop of 2+ points over period = deterioration
}


@dataclass
class RiskReport:
    risk_level:       str          # CRITICAL / HIGH / MODERATE / LOW / STABLE
    risk_score:       float        # 0.0 – 1.0
    flags:            list[str]    # triggered pattern names
    evidence:         list[str]    # specific data points that triggered each flag
    recommendations:  list[str]    # supportive actions
    summary:          str          # 1-paragraph human-readable summary
    graph_relations:  list[str]    # knowledge graph relationships used


def analyse_entries(entries: list[dict]) -> RiskReport:
    """
    Core risk detection function. Takes a list of retrieved/user entries
    and returns a structured RiskReport.
    """
    if not entries:
        return RiskReport(
            risk_level="UNKNOWN", risk_score=0.0, flags=[],
            evidence=[], recommendations=["Insufficient data to assess risk."],
            summary="No data available for analysis.",
            graph_relations=[],
        )

    flags        = []
    evidence     = []
    graph_rel    = []
    score_parts  = []

    # Sort by date for trend analysis
    sorted_entries = sorted(entries, key=lambda x: x.get("date", ""))

    # ── 1. Critical mood check ─────────────────────────────────────────────────
    critical_mood_entries = [
        e for e in entries if e.get("mood_score", 10) <= THRESHOLDS["critical_mood"]
    ]
    if critical_mood_entries:
        flags.append("CRITICAL_MOOD")
        score_parts.append(0.85)
        for e in critical_mood_entries[:2]:
            evidence.append(
                f"Mood score {e['mood_score']}/10 on {e['date']}: \"{e['journal'][:80]}...\""
            )
        graph_rel.append("critical_mood → indicates → severe_emotional_distress")

    # ── 2. Sleep deprivation ──────────────────────────────────────────────────
    low_sleep = [
        e for e in entries if e.get("sleep_hours", 8) <= THRESHOLDS["low_sleep"]
    ]
    critical_sleep = [
        e for e in entries if e.get("sleep_hours", 8) <= THRESHOLDS["critical_sleep"]
    ]
    if critical_sleep:
        flags.append("CRITICAL_SLEEP_DEPRIVATION")
        score_parts.append(0.75)
        for e in critical_sleep[:2]:
            evidence.append(f"Only {e['sleep_hours']}h sleep on {e['date']}")
        graph_rel.append("low_sleep → contributes_to → stress")
        graph_rel.append("low_sleep → contributes_to → burnout")
    elif low_sleep:
        flags.append("LOW_SLEEP")
        score_parts.append(0.45)
        evidence.append(
            f"Sleep below 5.5h on {len(low_sleep)} occasion(s) in the dataset"
        )
        graph_rel.append("low_sleep → contributes_to → stress")

    # ── 3. High stress ────────────────────────────────────────────────────────
    high_stress_entries = [
        e for e in entries if e.get("stress_level", 0) >= THRESHOLDS["high_stress"]
    ]
    if high_stress_entries:
        flags.append("HIGH_STRESS")
        score_parts.append(0.60)
        avg_stress = sum(e["stress_level"] for e in high_stress_entries) / len(high_stress_entries)
        evidence.append(
            f"Average stress {avg_stress:.1f}/10 across {len(high_stress_entries)} high-stress entries"
        )
        graph_rel.append("high_stress → leads_to → burnout")
        graph_rel.append("high_stress → impairs → sleep_quality")

    # ── 4. Burnout pattern (high stress + low sleep, consecutive days) ─────────
    burnout_days = [
        e for e in entries
        if e.get("stress_level", 0) >= THRESHOLDS["high_stress"]
        and e.get("sleep_hours", 8) <= THRESHOLDS["low_sleep"]
    ]
    if len(burnout_days) >= THRESHOLDS["burnout_streak"]:
        flags.append("BURNOUT_RISK")
        score_parts.append(0.80)
        evidence.append(
            f"{len(burnout_days)} entries show simultaneous high stress and low sleep — "
            "classic burnout pattern"
        )
        graph_rel.append("burnout → affects → emotional_state")
        graph_rel.append("burnout → reduces → motivation")
        graph_rel.append("burnout → increases → social_withdrawal")

    # ── 5. Anxiety escalation ─────────────────────────────────────────────────
    high_anxiety = [
        e for e in entries if e.get("anxiety_score", 0) >= THRESHOLDS["high_anxiety"]
    ]
    if high_anxiety:
        flags.append("ANXIETY_ESCALATION")
        score_parts.append(0.65)
        peak = max(high_anxiety, key=lambda x: x["anxiety_score"])
        evidence.append(
            f"Anxiety peaked at {peak['anxiety_score']}/10 on {peak['date']}"
        )
        graph_rel.append("anxiety → disrupts → sleep")
        graph_rel.append("anxiety → contributes_to → social_withdrawal")

    # ── 6. Social withdrawal ──────────────────────────────────────────────────
    withdrawn = [
        e for e in entries
        if e.get("social_interaction", "moderate") in ["none", "low"]
    ]
    if len(withdrawn) >= 3:
        flags.append("SOCIAL_WITHDRAWAL")
        score_parts.append(0.50)
        evidence.append(
            f"{len(withdrawn)} entries show low or no social interaction"
        )
        graph_rel.append("social_withdrawal → worsens → emotional_state")
        graph_rel.append("social_withdrawal → indicates → depression_risk")

    # ── 7. Emotional deterioration trend ─────────────────────────────────────
    if len(sorted_entries) >= 3:
        early_mood = sum(
            e.get("mood_score", 5) for e in sorted_entries[:2]
        ) / 2
        late_mood = sum(
            e.get("mood_score", 5) for e in sorted_entries[-2:]
        ) / 2
        delta = late_mood - early_mood

        if delta <= THRESHOLDS["deterioration_delta"]:
            flags.append("EMOTIONAL_DETERIORATION")
            score_parts.append(0.70)
            evidence.append(
                f"Mood declined from avg {early_mood:.1f} → {late_mood:.1f} "
                f"(Δ {delta:.1f}) over the observed period"
            )
            graph_rel.append("mood_decline → signals → emotional_deterioration")
            graph_rel.append("emotional_deterioration → risk_of → depression")

    # ── 8. Positive indicators (reduce score) ─────────────────────────────────
    high_mood = [e for e in entries if e.get("mood_score", 0) >= 7]
    good_sleep = [e for e in entries if e.get("sleep_hours", 0) >= 7]
    active = [e for e in entries if e.get("activities")]

    if high_mood and good_sleep and active:
        score_parts.append(-0.20)   # positive buffer

    # ── Final risk score ───────────────────────────────────────────────────────
    raw_score = sum(score_parts) / max(len(score_parts), 1) if score_parts else 0.0
    risk_score = min(max(raw_score, 0.0), 1.0)

    # ── Risk level classification ──────────────────────────────────────────────
    if risk_score >= 0.75 or "CRITICAL_MOOD" in flags:
        risk_level = "CRITICAL"
    elif risk_score >= 0.55 or "BURNOUT_RISK" in flags:
        risk_level = "HIGH"
    elif risk_score >= 0.35:
        risk_level = "MODERATE"
    elif risk_score >= 0.15:
        risk_level = "LOW"
    else:
        risk_level = "STABLE"

    # ── Recommendations ────────────────────────────────────────────────────────
    recommendations = _build_recommendations(flags, risk_level)

    # ── Summary ───────────────────────────────────────────────────────────────
    summary = _build_summary(flags, risk_level, risk_score, entries, evidence)

    return RiskReport(
        risk_level=risk_level,
        risk_score=round(risk_score, 3),
        flags=flags,
        evidence=evidence,
        recommendations=recommendations,
        summary=summary,
        graph_relations=list(set(graph_rel)),
    )


def _build_recommendations(flags: list[str], risk_level: str) -> list[str]:
    recs = []

    if risk_level == "CRITICAL":
        recs.append(
            "🚨 Please consider reaching out to a mental health professional or crisis line immediately."
        )
        recs.append("Talk to someone you trust — isolation makes things harder.")

    if "BURNOUT_RISK" in flags or "HIGH_STRESS" in flags:
        recs.append("⏸️ Take intentional breaks during the day — even 10 minutes helps reset stress hormones.")
        recs.append("📋 Review your current workload and identify tasks to delegate or defer.")

    if "LOW_SLEEP" in flags or "CRITICAL_SLEEP_DEPRIVATION" in flags:
        recs.append("😴 Prioritise sleep: set a consistent bedtime, avoid screens 1h before bed.")
        recs.append("🌙 Even a 20-minute nap can partially offset sleep deficit — try it if possible.")

    if "ANXIETY_ESCALATION" in flags:
        recs.append("🧘 Try box breathing: inhale 4s → hold 4s → exhale 4s → hold 4s. Repeat 4 times.")
        recs.append("📝 Write down worries before bed to externalise them and reduce rumination.")

    if "SOCIAL_WITHDRAWAL" in flags:
        recs.append("📞 Reach out to one person today — a text is enough. Connection reduces cortisol.")
        recs.append("🚶 Consider joining a low-pressure group activity (walking club, class, etc.).")

    if "EMOTIONAL_DETERIORATION" in flags:
        recs.append("📈 Track your mood daily — awareness itself is a protective factor.")
        recs.append("🎯 Set one small achievable goal each day to rebuild sense of agency.")

    if not flags:
        recs.append("✅ Keep up your current habits — you're doing well.")
        recs.append("🌱 Continue journaling — it helps maintain self-awareness.")

    return recs


def _build_summary(
    flags: list[str],
    risk_level: str,
    risk_score: float,
    entries: list[dict],
    evidence: list[str],
) -> str:
    n = len(entries)
    avg_mood    = sum(e.get("mood_score",   5) for e in entries) / n
    avg_stress  = sum(e.get("stress_level", 5) for e in entries) / n
    avg_sleep   = sum(e.get("sleep_hours",  7) for e in entries) / n

    flag_desc = ""
    if "BURNOUT_RISK" in flags:
        flag_desc += "burnout risk, "
    if "EMOTIONAL_DETERIORATION" in flags:
        flag_desc += "emotional deterioration, "
    if "HIGH_STRESS" in flags:
        flag_desc += "elevated stress, "
    if "LOW_SLEEP" in flags or "CRITICAL_SLEEP_DEPRIVATION" in flags:
        flag_desc += "sleep deprivation, "
    if "ANXIETY_ESCALATION" in flags:
        flag_desc += "anxiety escalation, "
    if "SOCIAL_WITHDRAWAL" in flags:
        flag_desc += "social withdrawal, "
    flag_desc = flag_desc.rstrip(", ")

    summary = (
        f"Analysis of {n} journal entries shows an average mood of {avg_mood:.1f}/10, "
        f"stress of {avg_stress:.1f}/10, and {avg_sleep:.1f}h of sleep per night. "
    )

    if flag_desc:
        summary += (
            f"Detected patterns include: {flag_desc}. "
            f"Overall risk level assessed as {risk_level} (score: {risk_score:.2f}). "
        )
    else:
        summary += "No significant risk patterns detected. The user appears to be in a stable state. "

    if risk_level in ["CRITICAL", "HIGH"]:
        summary += (
            "These signals suggest the user may benefit from professional support. "
            "This is not a clinical diagnosis — it is a supportive early-warning indicator."
        )
    elif risk_level == "MODERATE":
        summary += (
            "Preventive action is recommended before patterns escalate. "
            "Small daily changes in sleep and stress management can make a significant difference."
        )
    else:
        summary += "Continue monitoring and maintain current healthy habits."

    return summary