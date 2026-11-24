"""Core Distributed Lock Vault implementation."""
import time
from typing import Dict, Optional

class LockLease:
    def __init__(self, resource_id: str, owner_id: str, fencing_token: int, expires_at: float):
        self.resource_id = resource_id
        self.owner_id = owner_id
        self.fencing_token = fencing_token
        self.expires_at = expires_at

class DistributedLockVault:
    def __init__(self):
        self.locks: Dict[str, LockLease] = {}
        self.token_counter = 100

    def acquire(self, resource_id: str, owner_id: str, ttl_seconds: float = 10.0) -> Optional[LockLease]:
        now = time.time()
        existing = self.locks.get(resource_id)
        if existing and now < existing.expires_at and existing.owner_id != owner_id:
            return None  # Locked by another

        self.token_counter += 1
        lease = LockLease(resource_id, owner_id, self.token_counter, now + ttl_seconds)
        self.locks[resource_id] = lease
        return lease

    def release(self, resource_id: str, owner_id: str) -> bool:
        existing = self.locks.get(resource_id)
        if existing and existing.owner_id == owner_id:
            del self.locks[resource_id]
            return True
        return False

    def validate_fencing_token(self, resource_id: str, token: int) -> bool:
        existing = self.locks.get(resource_id)
        if not existing:
            return False
        return existing.fencing_token == token and time.time() < existing.expires_at
