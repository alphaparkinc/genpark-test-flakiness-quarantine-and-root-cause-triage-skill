"""Example usage for Autonomous Test Flakiness Quarantine & Failure Root-Cause Triager."""
from client import TestFlakinessTriager

if __name__ == "__main__":
    history = [
        {"test_id": "test_auth_flow", "runs": ["PASS", "PASS", "PASS"]},
        {"test_id": "test_async_websocket", "runs": ["PASS", "FAIL", "PASS", "FAIL"]}
    ]
    res = TestFlakinessTriager.triage_tests(history)
    print("Quarantined Tests:", res["quarantined_count"])
    print("Results:", res["triage_results"])
