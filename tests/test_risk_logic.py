
from collections import deque
from offchain.risk_agent import RiskAgent

def test_zscore_computation_starts_zero():
    agent = RiskAgent(["ETH"], 3.0)
    z = agent.current_zscores()
    assert "ETH" in z and z["ETH"] == 0.0

def test_liquidation_signal_when_history_spikes():
    agent = RiskAgent(["ETH"], 2.0)
    # feed calm prices then a spike
    for p in [100,101,102,103,104,300]:
        agent.update_prices({"ETH": p})
    z = agent.current_zscores()["ETH"]
    assert abs(z) > 2.0
