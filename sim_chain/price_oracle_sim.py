
import os, random, time
from dataclasses import dataclass
from typing import Dict

@dataclass
class PriceState:
    value: float
    drift: float = 0.0

class PriceOracleSim:
    def __init__(self):
        self.prices: Dict[str, PriceState] = {}
        self._init_from_env()

    def _init_from_env(self):
        bases = {
            "ETH": float(os.getenv("BASE_PRICE_ETH", "3200")),
            "WBTC": float(os.getenv("BASE_PRICE_WBTC", "68000")),
            "USDC": float(os.getenv("BASE_PRICE_USDC", "1.0")),
        }
        for k, v in bases.items():
            self.prices[k] = PriceState(value=v)

    def tick(self) -> Dict[str, float]:
        out = {}
        for sym, st in self.prices.items():
            # jitter around base with mild random shocks
            shock = random.gauss(0, st.value * 0.002)  # 0.2% std
            # occasional larger move
            if random.random() < 0.03:
                shock += random.choice([-1, 1]) * st.value * random.uniform(0.01, 0.03)
            st.value = max(0.0001, st.value + shock + st.drift)
            out[sym] = round(st.value, 2)
        return out
