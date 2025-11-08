# zk-tx-soundness

## Overview
**zk-tx-soundness** is a Python command-line utility that measures how long it takes for a transaction to be **included and confirmed** on an EVM-compatible network.  
It’s particularly useful for verifying **RPC responsiveness** and **transaction inclusion times** in zk-focused ecosystems like **Aztec** or **Zama**, where proof validity and sequencing consistency matter.

## Features
- Tracks transaction receipt inclusion time  
- Measures RPC latency and retry response  
- Displays block number and transaction status  
- Supports JSON output for monitoring and CI  
- Works with Ethereum, L2s, and testnets  

## Installation
1. Requires Python 3.9+  
2. Install dependencies:
   pip install web3
3. Set your RPC endpoint:
   export RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

## Usage
Check transaction inclusion speed:
   python app.py --tx 0xYourTransactionHash

Retry more times or increase delay:
   python app.py --tx 0xYourTransactionHash --retries 5 --delay 2.5

JSON output:
   python app.py --tx 0xYourTransactionHash --json

## Example Output
🕒 Timestamp: 2025-11-08T13:28:45.012Z  
🔧 zk-tx-soundness  
🔗 RPC: https://mainnet.infura.io/v3/YOUR_KEY  
🔍 Transaction: 0x123abc456def789...  
⏳ Waiting for transaction receipt... attempt 1/3  
✅ Transaction confirmed  
🧱 Block Number: 21051321  
📦 Transaction Status: ✅ Success  
⚡ Inclusion Latency: 4.38s  
⏱️ Completed in 5.04s  

## Notes
- **Latency Meaning:** The reported latency represents how long it took for the RPC to return a valid transaction receipt.  
- **Retries:** Useful for observing block propagation delays and RPC queue responsiveness.  
- **RPC Nodes:** Different providers may return transaction receipts at different speeds depending on node sync and caching.  
- **CI/CD Monitoring:** Use this script in automation pipelines to validate that zk-related transactions (e.g., Aztec proofs) finalize within expected time windows.  
- **ZK Security Context:** In zk systems, fast and consistent transaction confirmation ensures proof freshness and prevents timing discrepancies.  
- **Timeouts:** If you frequently hit retry limits, switch to a faster or region-specific RPC.  
- **L2 & Testnets:** Works with Ethereum mainnet, Polygon, Arbitrum, Base, Optimism, and any custom devnet.  
- **Exit Codes:**  
  `0` → Success  
  `2` → Transaction not found or failed to confirm.  
