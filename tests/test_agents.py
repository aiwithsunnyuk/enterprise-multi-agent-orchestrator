import pytest
from core.agents import CloudInfraAgent, SecurityAuditAgent, FinOpsAgent
from core.tools import EnterpriseToolbox

def test_enterprise_tools():
    infra = EnterpriseToolbox.inspect_cloud_resources("test-cluster")
    assert infra["status"] == "healthy"
    assert "cpu_utilization" in infra

    sec = EnterpriseToolbox.run_cve_compliance_check("test-container")
    assert sec["compliance_policy"] == "SOC2_PASSED"

    fin = EnterpriseToolbox.calculate_cost_impact("test-sku", 2)
    assert fin["monthly_estimated_usd"] == 240.00

def test_sub_agents():
    infra_msg = CloudInfraAgent.execute("evaluate")
    assert infra_msg.sender == "CloudInfraAgent"
    assert "Infrastructure Audit" in infra_msg.content

    sec_msg = SecurityAuditAgent.execute("evaluate")
    assert sec_msg.sender == "SecurityAuditAgent"

    fin_msg = FinOpsAgent.execute("evaluate")
    assert fin_msg.sender == "FinOpsAgent"
