from rag.retriever import retrieve
from detection.risk_detector import detect_risk


def run_pipeline(query):

    # Step 1: Retrieve relevant entries
    retrieved_entries = retrieve(query)

    # Step 2: Risk detection
    risk_output = detect_risk(retrieved_entries)

    # Step 3: Build explanation
    explanation = {
        "summary": f"Detected {risk_output['risk_level']} mental health risk based on stress and sleep patterns.",
        "key_factors": risk_output.get("reason", [])
    }

    # Step 4: Simple graph insights
    graph_edges = []

    for entry in retrieved_entries:

        mood = entry.get("mood", "unknown")
        stress = entry.get("stress_level", 0)

        if stress >= 7:
            graph_edges.append(
                f"{mood} → High Stress"
            )

    # Step 5: Final response
    response = {
        "query": query,
        "retrieved_entries": retrieved_entries,
        "risk_assessment": risk_output,
        "explanation": explanation,
        "graph_edges": graph_edges,
        "raw_logs": retrieved_entries
    }

    return response


# Local test
if __name__ == "__main__":

    test_query = "stress burnout low sleep"

    result = run_pipeline(test_query)

    print(result)