from rag.retriever import retrieve
from detection.risk_detector import detect_risk


def run_pipeline(query):

    # Step 1: Retrieve relevant mental health entries
    retrieved_entries = retrieve(query)

    # Step 2: Risk detection on retrieved data
    risk_output = detect_risk(retrieved_entries)

    # Step 3: Knowledge Graph layer (EXPLAINABILITY)
    from graph.graph_builder import MentalHealthGraph
    kg = MentalHealthGraph()
    graph_edges = kg.get_relationships()

    # Step 4: Raw logs (for UI transparency)
    raw_logs = retrieved_entries

    # Step 5: Build explanation
    explanation = {
        "summary": f"Risk level detected: {risk_output['risk_level']}",
        "key_factors": risk_output.get("reason", [])
    }

    # Step 6: Final structured response
    response = {
        "query": query,
        "retrieved_entries": retrieved_entries,
        "risk_assessment": risk_output,
        "explanation": explanation,
        "graph_edges": graph_edges,
        "raw_logs": raw_logs
    }

    return response


# test run
if __name__ == "__main__":
    query = "stress, burnout, low sleep"
    output = run_pipeline(query)

    print("\n=== FINAL AI INSIGHT ===\n")
    print(output)