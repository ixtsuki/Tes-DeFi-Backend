
# Architecture Notes — DeFi Vault Cloud (Simulation Edition)

- Containers target **AWS Fargate/EKS**; use EventBridge for scheduled ticks.
- Persist **positions** and **events** in DynamoDB or Postgres when moving beyond sim.
- Plug real **Chainlink** or exchange APIs into the orchestrator (adapter module).
- Replace MockChain with **web3.py** calls to actual contracts in a production edition.
- Add **GitHub Actions** for CI (lint, tests) and CD (build/push container).
