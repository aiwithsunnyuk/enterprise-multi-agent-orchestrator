import streamlit as st
import pandas as pd
from orchestrator.graph import build_orchestrator_graph

st.set_page_config(page_title="Enterprise Agent Orchestrator", page_icon="🤖", layout="wide")

st.title("🤖 Enterprise Multi-Agent Workflow Orchestrator")
st.markdown("Orchestrate parallel autonomous sub-agents with stateful LangGraph message passing.")

with st.sidebar:
    st.header("Orchestrator Controls")
    st.success("State: Connected (LangGraph v0.1)")
    preset = st.selectbox("Sample Enterprise Directives:", [
        "Audit production infrastructure scaling, security posture, and FinOps impact.",
        "Review app-gateway CVE compliance before scheduled release.",
        "Evaluate standard compute node budget impact for cloud expansion."
    ])

user_directive = st.text_area("Input Enterprise Task Directive:", value=preset, height=100)
trigger = st.button("🚀 Dispatch Multi-Agent Graph", use_container_width=True)

if trigger:
    with st.spinner("Executing Graph and Synchronizing Agent Consensus..."):
        graph = build_orchestrator_graph()
        initial_state = {
            "task": user_directive,
            "routed_agents": [],
            "agent_outputs": [],
            "final_synthesis": "",
            "status": "INITIALIZED"
        }
        result = graph.invoke(initial_state)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Sub-Agent Delegations & Telemetry")
            telemetry_data = []
            for agent_msg in result.get("agent_outputs", []):
                telemetry_data.append({
                    "Agent": agent_msg.sender,
                    "Finding": agent_msg.content,
                    "Payload Attributes": len(agent_msg.data)
                })
            st.dataframe(pd.DataFrame(telemetry_data), use_container_width=True)

        with col2:
            st.subheader("Synthesized Consensus Output")
            st.markdown(result.get("final_synthesis"))
            st.success(f"Status: {result.get('status')}")
