# app.py
import os
import sys
import json
import time
import argparse
from datetime import datetime
from web3 import Web3

DEFAULT_RPC = os.environ.get("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")

def get_tx_receipt_latency(w3: Web3, tx_hash: str, retries: int = 3, delay: float = 1.5) -> float:
    """
    Measure how long it takes for a transaction receipt to become available.
    """
    start = time.time()
    for attempt in range(1, retries + 1):
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt is not None:
                return time.time() - start
        except Exception:
            pass
        print(f"⏳ Waiting for transaction receipt... attempt {attempt}/{retries}")
        time.sleep(delay)
    raise RuntimeError("Transaction receipt not found after retries.")

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="zk-tx-soundness — verify transaction inclusion latency and RPC reliability for Aztec/Zama and general Web3 testing."
    )
    p.add_argument("--rpc", default=DEFAULT_RPC, help="EVM RPC URL (default from RPC_URL)")
    p.add_argument("--tx", required=True, help="Transaction hash to verify")
    p.add_argument("--retries", type=int, default=3, help="Number of receipt check attempts (default: 3)")
    p.add_argument("--delay", type=float, default=1.5, help="Delay between attempts in seconds (default: 1.5)")
    p.add_argument("--json", action="store_true", help="Output results as JSON")
    return p.parse_args()

def main() -> None:
    args = parse_args()
    start_time = time.time()

    if not args.rpc.startswith("http"):
        print("❌ Invalid RPC URL format. It must start with 'http' or 'https'.")
        sys.exit(1)

    w3 = Web3(Web3.HTTPProvider(args.rpc, request_kwargs={"timeout": 20}))
    if not w3.is_connected():
        print("❌ RPC connection failed. Check your RPC_URL or --rpc argument.")
        sys.exit(1)

    print(f"🕒 Timestamp: {datetime.utcnow().isoformat()}Z")
    print("🔧 zk-tx-soundness")
    print(f"🔗 RPC: {args.rpc}")
    print(f"🔍 Transaction: {args.tx}")
#Validate transaction hash format
    if not args.tx.startswith("0x") or len(args.tx) != 66:
        print("❌ Invalid transaction hash format. It should be a 0x-prefixed 66-character string.")
        sys.exit(1)
    try:
        receipt_time = get_tx_receipt_latency(w3, args.tx, args.retries, args.delay)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(2)

    try:
        receipt = w3.eth.get_transaction_receipt(args.tx)
        block_number = receipt.blockNumber
        status = "✅ Success" if receipt.status == 1 else "❌ Failed"
    except Exception:
        block_number = None
        status = "⚠️ Unknown (receipt not available)"

    print(f"🧱 Block Number: {block_number}")
    print(f"📦 Transaction Status: {status}")
    print(f"⚡ Inclusion Latency: {receipt_time:.2f}s")
    elapsed = time.time() - start_time
    print(f"⏱️ Completed in {elapsed:.2f}s")

    if args.json:
        output = {
            "rpc": args.rpc,
            "transaction": args.tx,
            "block_number": block_number,
            "status": status,
            "latency_seconds": round(receipt_time, 2),
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "elapsed_seconds": round(elapsed, 2)
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    sys.exit(0)

if __name__ == "__main__":
    main()
