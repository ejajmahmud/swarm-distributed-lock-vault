"""Tests for DistributedLockVault."""
import unittest
from swarm_distributed_lock_vault.core import DistributedLockVault

class TestDistributedLockVault(unittest.TestCase):
    def test_lock_exclusivity(self):
        vault = DistributedLockVault()
        l1 = vault.acquire("res1", "owner1", 5.0)
        self.assertIsNotNone(l1)

        l2 = vault.acquire("res1", "owner2", 5.0)
        self.assertIsNone(l2)  # Should fail

        vault.release("res1", "owner1")
        l3 = vault.acquire("res1", "owner2", 5.0)
        self.assertIsNotNone(l3)
        self.assertTrue(l3.fencing_token > l1.fencing_token)
