
import time, statistics
from collections import deque
from typing import Dict, Deque

from .audit import emit

class RiskAgent:
    def __init__(self, assets, z_threshold: float):
        self.z_threshold = z_threshold
        self.history: Dict[str, Deque[float]] = {a: deque(maxlen=60) for a in assets}

    def update_prices(self, prices: Dict[str, float]):
        # maintain rolling window
        for a, p in prices.items():
            self.history[a].append(p)

    def current_zscores(self) -> Dict[str, float]:
        z = {}
        for a, series in self.history.items():
            if len(series) < 5:
                z[a] = 0.0
                continue
            m = statistics.mean(series)
            s = statistics.pstdev(series) if len(series) > 1 else 0.0
            z[a] = 0.0 if s == 0 else (series[-1] - m) / s
        return z

    def evaluate_positions(self, chain, prices: Dict[str, float]):
        # returns a list of actions for orchestrator
        actions = []
        z = self.current_zscores()
        for user, pos in chain.positions.items():
            ltv = chain.get_ltv(user, prices) / 100.0  # convert to [0,1]
            policy = max(chain.ltv_policy.values())  # simple global cap for demo
            if ltv > policy or any(abs(val) > self.z_threshold for val in z.values()):
                actions.append({"type": "LIQUIDATE", "user": user, "reason": {"ltv": ltv, "zscores": z}})
                emit({"type":"risk_signal", "user":user, "ltv":ltv, "zscores":z})
        return actions
