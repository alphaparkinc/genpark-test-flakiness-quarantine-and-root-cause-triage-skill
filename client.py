"""Autonomous Test Flakiness Quarantine & Failure Root-Cause Triager.
100% Python Standard Library.
"""

class TestFlakinessTriager:
    """Calculates flakiness volatility index across multi-run CI/CD executions and triages deterministic regressions from intermittent timing flakes."""

    @staticmethod
    def triage_tests(test_history: list) -> dict:
        results = []
        for item in test_history:
            tid = item.get("test_id", "test_case")
            runs = item.get("runs", [])
            if not runs:
                continue

            transitions = 0
            for i in range(len(runs) - 1):
                if runs[i] != runs[i+1]:
                    transitions += 1

            flakiness_score = transitions / max(1, len(runs) - 1)
            is_flaky = flakiness_score >= 0.3 or ("PASS" in runs and "FAIL" in runs)

            verdict = "QUARANTINE_FLAKY" if is_flaky else ("DETERMINISTIC_PASS" if all(r == "PASS" for r in runs) else "DETERMINISTIC_REGRESSION")
            results.append({
                "test_id": tid,
                "flakiness_index": round(flakiness_score, 2),
                "verdict": verdict,
                "recommendation": "Mark @pytest.mark.flaky(reruns=3)" if is_flaky else "No quarantine needed"
            })

        return {
            "total_tested": len(results),
            "quarantined_count": sum(1 for r in results if "QUARANTINE" in r["verdict"]),
            "triage_results": results
        }
