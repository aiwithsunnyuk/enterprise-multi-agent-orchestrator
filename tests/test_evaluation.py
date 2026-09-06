import pytest
from orchestrator.graph import build_orchestrator_graph

def test_evaluation_graph_execution():
    """EVAL: Benchmarks parallel agent orchestration and consensus generation."""
    graph = build_orchestrator_graph()
    state_input = {
        "task": "Perform a holistic check on production infrastructure and compliance",
        "routed_agents": [],
        "agent_outputs": [],
        "final_synthesis": "",
        "status": "INIT"
    }

    final_state = graph.invoke(state_input)

    # Verification criteria
    assert final_state["status"] == "COMPLETED", "Eval Failure: Graph failed to complete state transition"
    assert len(final_state["agent_outputs"]) >= 3, "Eval Failure: Sub-agent parallel fan-out failed"
    assert "Enterprise Consensus" in final_state["final_synthesis"], "Eval Failure: Missing synthesis output"
