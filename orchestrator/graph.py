from typing import Dict, Any
from langgraph.graph import StateGraph, END
from core.state import OrchestratorState, AgentMessage
from core.agents import CloudInfraAgent, SecurityAuditAgent, FinOpsAgent

def supervisor_router(state: OrchestratorState) -> OrchestratorState:
    task = state.get("task", "").lower()
    selected_agents = []

    if any(k in task for k in ["scale", "cluster", "deploy", "infrastructure", "perf"]):
        selected_agents.append("infra")
    if any(k in task for k in ["security", "cve", "compliance", "vulnerability", "audit"]):
        selected_agents.append("security")
    if any(k in task for k in ["cost", "budget", "finops", "price", "spend"]):
        selected_agents.append("finops")

    if not selected_agents:
        selected_agents = ["infra", "security", "finops"]

    state["routed_agents"] = selected_agents
    state["status"] = "ROUTED"
    return state

def infra_node(state: OrchestratorState) -> Dict[str, Any]:
    msg = CloudInfraAgent.execute(state["task"])
    return {"agent_outputs": [msg]}

def security_node(state: OrchestratorState) -> Dict[str, Any]:
    msg = SecurityAuditAgent.execute(state["task"])
    return {"agent_outputs": [msg]}

def finops_node(state: OrchestratorState) -> Dict[str, Any]:
    msg = FinOpsAgent.execute(state["task"])
    return {"agent_outputs": [msg]}

def synthesis_node(state: OrchestratorState) -> OrchestratorState:
    outputs = state.get("agent_outputs", [])
    synthesized_text = "### Enterprise Consensus & Decision Action Plan\n\n"
    for item in outputs:
        synthesized_text += f"- **[{item.sender}]**: {item.content}\n"
    
    synthesized_text += "\n**Final Directive**: System is cleared for deployment under standard change controls."
    state["final_synthesis"] = synthesized_text
    state["status"] = "COMPLETED"
    return state

def build_orchestrator_graph():
    builder = StateGraph(OrchestratorState)

    builder.add_node("supervisor", supervisor_router)
    builder.add_node("infra_node", infra_node)
    builder.add_node("security_node", security_node)
    builder.add_node("finops_node", finops_node)
    builder.add_node("synthesizer", synthesis_node)

    builder.set_entry_point("supervisor")

    builder.add_edge("supervisor", "infra_node")
    builder.add_edge("supervisor", "security_node")
    builder.add_edge("supervisor", "finops_node")

    builder.add_edge("infra_node", "synthesizer")
    builder.add_edge("security_node", "synthesizer")
    builder.add_edge("finops_node", "synthesizer")

    builder.add_edge("synthesizer", END)
    return builder.compile()
