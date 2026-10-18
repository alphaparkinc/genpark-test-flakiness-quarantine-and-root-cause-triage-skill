"""MCP server for Autonomous Test Flakiness Quarantine & Failure Root-Cause Triager."""
import sys
import json
from client import TestFlakinessTriager

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "triage_test_flakiness",
                "description": "Calculates flakiness volatility and classifies deterministic vs intermittent test failures",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "test_history": {"type": "array"}
                    },
                    "required": ["test_history"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "triage_test_flakiness":
            history = params.get("arguments", {}).get("test_history", [])
            res = TestFlakinessTriager.triage_tests(history)
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
