from typing import TypedDict, Annotated, Sequence, Dict, Any, List
import operator
from pydantic import BaseModel, Field

class AgentMessage(BaseModel):
    sender: str
    content: str
    data: Dict[str, Any] = Field(default_factory=dict)

class OrchestratorState(TypedDict):
    task: str
    routed_agents: List[str]
    agent_outputs: Annotated[List[AgentMessage], operator.add]
    final_synthesis: str
    status: str
