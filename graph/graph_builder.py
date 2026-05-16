"""
knowledge_graph.py - In-memory mental health knowledge graph
Author: VitaTwin AI Team

Implements a Python-native knowledge graph (no Neo4j required).
Nodes: mood, sleep, stress, burnout, anxiety, activity, emotional_state
Relationships: directional weighted edges with explanations
"""

from dataclasses import dataclass, field


@dataclass
class Node:
    id:          str
    label:       str
    description: str
    category:    str   # symptom / state / outcome / protective


@dataclass
class Edge:
    source:      str
    relation:    str
    target:      str
    weight:      float   # 0.0 – 1.0 (how strong the relationship is)
    explanation: str


class MentalHealthKnowledgeGraph:
    """
    A lightweight in-memory knowledge graph for mental health reasoning.
    Nodes and edges are defined from clinical psychology literature.
    """

    def __init__(self):
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge]      = []
        self._build()

    def _add_node(self, id, label, description, category="state"):
        self.nodes[id] = Node(id=id, label=label, description=description, category=category)

    def _add_edge(self, source, relation, target, weight, explanation):
        self.edges.append(Edge(source, relation, target, weight, explanation))

    def _build(self):
        # ── Nodes ──────────────────────────────────────────────────────────────
        self._add_node("low_sleep",          "Low Sleep",           "Sleeping fewer than 6 hours per night",                              "symptom")
        self._add_node("high_stress",        "High Stress",         "Chronic elevated psychological stress",                              "symptom")
        self._add_node("low_mood",           "Low Mood",            "Persistent low emotional state",                                     "symptom")
        self._add_node("high_anxiety",       "High Anxiety",        "Elevated worry, tension, or fear",                                   "symptom")
        self._add_node("social_withdrawal",  "Social Withdrawal",   "Reduced or absent social interaction",                               "symptom")
        self._add_node("low_energy",         "Low Energy",          "Persistent fatigue and lack of motivation",                          "symptom")
        self._add_node("burnout",            "Burnout",             "Exhaustion from chronic unmanaged stress",                           "outcome")
        self._add_node("depression_risk",    "Depression Risk",     "Elevated risk of clinical depression",                               "outcome")
        self._add_node("emotional_decline",  "Emotional Decline",   "Worsening of emotional state over time",                            "outcome")
        self._add_node("cognitive_impair",   "Cognitive Impairment","Reduced concentration, memory, decision-making",                     "outcome")
        self._add_node("physical_health",    "Physical Health",     "General bodily health and functioning",                              "outcome")
        self._add_node("exercise",           "Exercise",            "Regular physical activity",                                          "protective")
        self._add_node("social_support",     "Social Support",      "Meaningful connection with others",                                  "protective")
        self._add_node("sleep_hygiene",      "Sleep Hygiene",       "Consistent healthy sleep practices",                                 "protective")
        self._add_node("mindfulness",        "Mindfulness",         "Meditation, breathing exercises, presence",                          "protective")
        self._add_node("therapy",            "Therapy",             "Professional mental health support",                                 "protective")
        self._add_node("journaling",         "Journaling",          "Regular reflective writing practice",                                "protective")

        # ── Edges (knowledge relationships) ────────────────────────────────────
        # Sleep relationships
        self._add_edge("low_sleep",         "contributes_to",   "high_stress",       0.75, "Sleep deprivation elevates cortisol and stress reactivity")
        self._add_edge("low_sleep",         "contributes_to",   "burnout",           0.80, "Chronic sleep loss is a primary driver of burnout syndrome")
        self._add_edge("low_sleep",         "impairs",          "cognitive_impair",  0.85, "Even one night of <6h sleep reduces working memory by ~40%")
        self._add_edge("low_sleep",         "worsens",          "low_mood",          0.70, "Poor sleep significantly reduces emotional regulation capacity")
        self._add_edge("low_sleep",         "increases",        "high_anxiety",      0.65, "Sleep deprivation amplifies the amygdala's threat response")

        # Stress relationships
        self._add_edge("high_stress",       "leads_to",         "burnout",           0.85, "Chronic unmanaged stress is the primary pathway to burnout")
        self._add_edge("high_stress",       "impairs",          "sleep_hygiene",     0.70, "Stress activates the HPA axis, making sleep onset difficult")
        self._add_edge("high_stress",       "contributes_to",   "high_anxiety",      0.75, "Prolonged stress sensitises the threat-response system")
        self._add_edge("high_stress",       "reduces",          "social_support",    0.50, "Stressed individuals often withdraw from social connection")

        # Mood relationships
        self._add_edge("low_mood",          "signals",          "depression_risk",   0.80, "Persistent low mood is a primary indicator of depressive episodes")
        self._add_edge("low_mood",          "reduces",          "social_support",    0.65, "Low mood reduces motivation to maintain social relationships")
        self._add_edge("low_mood",          "contributes_to",   "low_energy",        0.75, "Emotional pain consumes significant cognitive and physical energy")

        # Burnout relationships
        self._add_edge("burnout",           "causes",           "emotional_decline", 0.90, "Burnout systematically erodes emotional resilience over time")
        self._add_edge("burnout",           "increases",        "social_withdrawal", 0.70, "Burned-out individuals often isolate to conserve energy")
        self._add_edge("burnout",           "leads_to",         "depression_risk",   0.75, "Untreated burnout significantly elevates depression risk")
        self._add_edge("burnout",           "impairs",          "physical_health",   0.60, "Burnout is associated with cardiovascular and immune dysfunction")

        # Anxiety relationships
        self._add_edge("high_anxiety",      "disrupts",         "low_sleep",         0.80, "Anxiety causes hyperarousal that prevents sleep onset and maintenance")
        self._add_edge("high_anxiety",      "contributes_to",   "social_withdrawal", 0.65, "Social anxiety drives avoidance of interpersonal situations")
        self._add_edge("high_anxiety",      "impairs",          "cognitive_impair",  0.70, "Anxiety consumes working memory through worry and rumination")

        # Social withdrawal relationships
        self._add_edge("social_withdrawal", "worsens",          "low_mood",          0.80, "Social isolation removes a key protective factor against depression")
        self._add_edge("social_withdrawal", "indicates",        "depression_risk",   0.75, "Withdrawal from social life is a major depression warning sign")
        self._add_edge("social_withdrawal", "reduces",          "social_support",    0.90, "By definition, withdrawal removes access to support networks")

        # Protective factors
        self._add_edge("exercise",          "reduces",          "high_stress",       0.80, "Exercise reduces cortisol and increases endorphins and BDNF")
        self._add_edge("exercise",          "improves",         "low_mood",          0.75, "Regular exercise is as effective as antidepressants for mild depression")
        self._add_edge("exercise",          "improves",         "sleep_hygiene",     0.70, "Physical activity promotes deeper, more restorative sleep")
        self._add_edge("social_support",    "protects_against", "depression_risk",   0.85, "Strong social networks are the #1 protective factor against depression")
        self._add_edge("social_support",    "reduces",          "high_stress",       0.70, "Social connection reduces cortisol via oxytocin release")
        self._add_edge("mindfulness",       "reduces",          "high_anxiety",      0.75, "Mindfulness practice reduces amygdala reactivity over 8 weeks")
        self._add_edge("mindfulness",       "improves",         "sleep_hygiene",     0.65, "Mindfulness reduces pre-sleep arousal and rumination")
        self._add_edge("therapy",           "treats",           "burnout",           0.85, "CBT and other therapies directly address burnout patterns")
        self._add_edge("therapy",           "treats",           "depression_risk",   0.90, "Therapy is a primary evidence-based treatment for depression")
        self._add_edge("journaling",        "reduces",          "high_anxiety",      0.60, "Expressive writing reduces rumination and anxiety over time")
        self._add_edge("sleep_hygiene",     "protects_against", "burnout",           0.75, "Adequate sleep is the primary recovery mechanism from stress")

    # ── Query methods ──────────────────────────────────────────────────────────

    def get_relationships_for_flags(self, flags: list[str]) -> list[str]:
        """
        Maps risk detection flags to relevant graph edges.
        Returns human-readable relationship strings.
        """
        flag_to_nodes = {
            "BURNOUT_RISK":              ["burnout", "high_stress", "low_sleep"],
            "HIGH_STRESS":               ["high_stress"],
            "LOW_SLEEP":                 ["low_sleep"],
            "CRITICAL_SLEEP_DEPRIVATION":["low_sleep"],
            "ANXIETY_ESCALATION":        ["high_anxiety"],
            "SOCIAL_WITHDRAWAL":         ["social_withdrawal"],
            "EMOTIONAL_DETERIORATION":   ["emotional_decline", "low_mood"],
            "CRITICAL_MOOD":             ["low_mood", "depression_risk"],
        }

        relevant_nodes = set()
        for flag in flags:
            relevant_nodes.update(flag_to_nodes.get(flag, []))

        results = []
        for edge in self.edges:
            if edge.source in relevant_nodes or edge.target in relevant_nodes:
                results.append(
                    f"{edge.source} → [{edge.relation}] → {edge.target} "
                    f"(strength: {edge.weight:.0%}) — {edge.explanation}"
                )
        return results

    def get_protective_factors(self, flags: list[str]) -> list[str]:
        """
        Returns protective factor recommendations based on risk flags.
        """
        protective_nodes = [n for n in self.nodes.values() if n.category == "protective"]
        recommendations  = []

        for node in protective_nodes:
            edges = [
                e for e in self.edges
                if e.source == node.id and e.relation in ["reduces", "improves", "protects_against", "treats"]
            ]
            for edge in edges:
                if any(
                    flag_node in edge.target
                    for flag_node in ["stress", "sleep", "anxiety", "burnout", "depression", "mood"]
                ):
                    recommendations.append(
                        f"{node.label}: {edge.explanation}"
                    )

        return list(set(recommendations))[:6]   # top 6 unique

    def explain_path(self, from_node: str, to_node: str, depth: int = 3) -> list[str]:
        """
        BFS path explanation from one node to another.
        Returns a chain of relationships explaining the connection.
        """
        if from_node not in self.nodes or to_node not in self.nodes:
            return []

        visited = {from_node}
        queue   = [(from_node, [])]

        while queue:
            current, path = queue.pop(0)
            if len(path) >= depth:
                continue
            for edge in self.edges:
                if edge.source == current and edge.target not in visited:
                    new_path = path + [
                        f"{self.nodes[edge.source].label} "
                        f"→ [{edge.relation}] → "
                        f"{self.nodes[edge.target].label}"
                    ]
                    if edge.target == to_node:
                        return new_path
                    visited.add(edge.target)
                    queue.append((edge.target, new_path))
        return []

    def summary(self) -> str:
        return (
            f"Knowledge graph: {len(self.nodes)} nodes, {len(self.edges)} edges. "
            f"Nodes: {', '.join(self.nodes.keys())}."
        )


# ── Singleton instance ─────────────────────────────────────────────────────────
KG = MentalHealthKnowledgeGraph()


if __name__ == "__main__":
    print(KG.summary())
    print("\nRelationships for BURNOUT_RISK + HIGH_STRESS:")
    for r in KG.get_relationships_for_flags(["BURNOUT_RISK", "HIGH_STRESS"]):
        print(" •", r)
    print("\nPath from low_sleep to depression_risk:")
    for step in KG.explain_path("low_sleep", "depression_risk"):
        print(" →", step)