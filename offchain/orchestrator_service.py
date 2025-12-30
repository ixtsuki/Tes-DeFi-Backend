
import sys
import os, time, json
from dotenv import load_dotenv
from rich.console import Console
from .config import Config
from .risk_agent import RiskAgent
from .audit import emit
from ..sim_chain.price_oracle_sim import PriceOracleSim
from ..sim_chain.mock_chain import MockChain

console = Console()

def main():
    load_dotenv()
    cfg = Config()
    console.rule("[bold magenta]DeFi Vault Cloud — Simulation")
    oracle = PriceOracleSim()
    chain = MockChain(cfg.ltv_policy)
    agent = RiskAgent(cfg.assets, cfg.z_threshold)

    # seed is handled via scripts/seed_positions.py (can be re-run)
    # start loop
    while True:
        prices = oracle.tick()
        agent.update_prices(prices)

        # risk agent proposes actions
        actions = agent.evaluate_positions(chain, prices)

        # orchestrator applies actions idempotently
        for action in actions:
            if action["type"] == "LIQUIDATE":
                chain.liquidate(action["user"], prices, pct=0.5)
                emit({"type":"liquidation_applied","user":action["user"]})

        snap = chain.snapshot()
        console.print({"prices": prices, "positions": {u: dict(coll=v.collateral, debt=v.debt) for u,v in chain.positions.items()}})

        time.sleep(cfg.tick_seconds)
        sys.path.append(os.getcwd())

if __name__ == "__main__":
    main()
