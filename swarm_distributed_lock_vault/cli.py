"""CLI for Distributed Lock Vault."""
import argparse
from .core import DistributedLockVault

def main():
    parser = argparse.ArgumentParser(description="Swarm Distributed Lock Vault CLI")
    parser.add_argument("--demo", action="store_true", help="Run distributed lock demo")
    args = parser.parse_args()

    vault = DistributedLockVault()
    lease = vault.acquire("src/index.ts", "agent-coder-1", 5.0)
    if lease:
        print(f"Acquired lock on {lease.resource_id} with fencing token #{lease.fencing_token}")
        valid = vault.validate_fencing_token("src/index.ts", lease.fencing_token)
        print("Token validity check:", valid)

if __name__ == "__main__":
    main()
