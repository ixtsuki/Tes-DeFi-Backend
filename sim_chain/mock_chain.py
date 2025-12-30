
import math, time, json
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Position:
    collateral: Dict[str, float] = field(default_factory=dict)
    debt: Dict[str, float] = field(default_factory=dict)

class MockChain:
    def __init__(self, ltv_policy: Dict[str, float]):
        self.positions: Dict[str, Position] = {}
        self.ltv_policy = ltv_policy  # e.g., {"ETH": 0.70, "WBTC": 0.60, "USDC": 0.90}
        self.events: List[dict] = []

    def seed(self, user: str, coll: Dict[str, float], debt: Dict[str, float]):
        self.positions[user] = Position(collateral=dict(coll), debt=dict(debt))

    def get_ltv(self, user: str, prices: Dict[str, float]) -> float:
        pos = self.positions[user]
        coll_val = sum(prices[a] * amt for a, amt in pos.collateral.items())
        debt_val = sum(prices[a] * amt for a, amt in pos.debt.items())
        if coll_val == 0:
            return math.inf if debt_val > 0 else 0.0
        return (debt_val / coll_val) * 100.0

    def repay(self, user: str, asset: str, amount: float):
        pos = self.positions[user]
        pos.debt[asset] = max(0.0, pos.debt.get(asset, 0.0) - amount)
        self.events.append({"ts": time.time(), "type": "repay", "user": user, "asset": asset, "amount": amount})

    def liquidate(self, user: str, prices: Dict[str, float], pct: float = 0.5):
        # sell some collateral to repay debt
        pos = self.positions[user]
        repay_val = 0.0
        for a, d_amt in list(pos.debt.items()):
            if d_amt <= 0:
                continue
            need_val = prices[a] * d_amt * pct
            # consume collateral in order
            for c, c_amt in list(pos.collateral.items()):
                if c_amt <= 0:
                    continue
                take = min(c_amt, need_val / prices[c])
                need_val -= prices[c] * take
                pos.collateral[c] = round(c_amt - take, 6)
                repay_amt = round(take * prices[c] / prices[a], 6)
                pos.debt[a] = round(max(0.0, d_amt - repay_amt), 6)
                repay_val += prices[c] * take
                if need_val <= 0:
                    break
            if need_val > 0:
                # couldn't cover; leave residual debt
                pass
        self.events.append({"ts": time.time(), "type": "liquidate", "user": user, "repay_val": repay_val})

    def snapshot(self) -> dict:
        return {
            "positions": self.positions,
            "events": self.events[-25:]
        }
