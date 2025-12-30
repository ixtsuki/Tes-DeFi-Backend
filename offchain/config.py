import os
from dataclasses import dataclass, field

@dataclass
class Config:
    # Menggunakan field(default_factory=dict) untuk menghindari ValueError
    ltv_policy: dict = field(default_factory=lambda: {
        "ETH": float(os.getenv("LTV_ETH", "0.80")),
        "WBTC": float(os.getenv("LTV_WBTC", "0.75")),
        "USDC": float(os.getenv("LTV_USDC", "0.90"))
    })
    sim_tick: int = int(os.getenv("SIM_TICK_SECONDS", "5"))
    risk_z_threshold: float = float(os.getenv("RISK_Z_THRESHOLD", "2.0"))