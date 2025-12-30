
from dotenv import load_dotenv
from offchain.config import Config
from sim_chain.mock_chain import MockChain

def main():
    load_dotenv()
    cfg = Config()
    chain = MockChain(cfg.ltv_policy)
    # Seed three accounts with collateral and some debt
    chain.seed("0xAlice", {"ETH": 2.5, "USDC": 2000}, {"USDC": 500})
    chain.seed("0xBob", {"WBTC": 0.4}, {"USDC": 1500})
    chain.seed("0xCarol", {"ETH": 1.2, "WBTC": 0.1}, {"USDC": 300})

    snap = chain.snapshot()
    print("Seeded positions:")
    for u, pos in snap["positions"].items():
        print(u, "collateral=", pos.collateral, "debt=", pos.debt)

if __name__ == "__main__":
    main()
