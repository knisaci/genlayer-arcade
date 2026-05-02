# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

# ─────────────────────────────────────────────────────────────────────────────
# ArcadeContractChecker — GenLayer Community Arcade
#
# The on-chain backend for the "Contract Builder" game.
# Players drag and drop code blocks to assemble a contract, then submit
# their assembled code here. The AI validator checks whether the submitted
# code is a structurally valid GenLayer Intelligent Contract, identifies
# what's missing or wrong, and stores feedback on-chain.
#
# This contract uses gl.nondet.exec_prompt() with gl.eq_principle.strict_eq()
# so all validators independently analyse the code and must agree on the verdict.
#
# Deployed on: Testnet Bradbury
# Part of: github.com/knisaci/genlayer-arcade
# ─────────────────────────────────────────────────────────────────────────────


class ArcadeContractChecker(gl.Contract):
    # ── On-chain state ────────────────────────────────────────────────────────
    last_submission: str     # The last code submitted for checking
    last_feedback: str       # JSON feedback from the AI validator
    total_checks: int        # Total number of submissions checked
    total_valid: int         # Number of submissions that were valid contracts

    def __init__(self) -> None:
        self.last_submission = ""
        self.last_feedback = ""
        self.total_checks = 0
        self.total_valid = 0

    # ── Read methods ──────────────────────────────────────────────────────────

    @gl.public.view
    def get_last_feedback(self) -> str:
        """Return the AI validator's feedback on the last code submission."""
        return self.last_feedback

    @gl.public.view
    def get_stats(self) -> str:
        """Return submission stats as JSON."""
        return json.dumps({
            "total_checks": self.total_checks,
            "total_valid": self.total_valid,
            "pass_rate_pct": round(
                (self.total_valid / self.total_checks * 100)
                if self.total_checks > 0 else 0, 1
            )
        })

    # ── Write methods ─────────────────────────────────────────────────────────

    @gl.public.write
    def check_contract(self, code: str) -> None:
        """
        Submit a Python code snippet to be validated as a GenLayer contract.

        The AI validator checks for:
        - Presence and correct format of the runner comment on line 1
        - Correct import: from genlayer import *
        - Class extending gl.Contract
        - At least one state variable with type annotation
        - An __init__ constructor
        - At least one @gl.public.view method
        - At least one @gl.public.write method

        Args:
            code: The Python source code to validate.
        """
        prompt = f"""You are an expert GenLayer Intelligent Contract validator.

Analyse the following Python code and determine whether it is a valid
GenLayer Intelligent Contract. Check for ALL of these requirements:

REQUIRED ELEMENTS:
1. Line 1 must be exactly: # {{ "Depends": "py-genlayer:test" }}
2. Must have: from genlayer import *
3. Class must extend gl.Contract (e.g. class MyContract(gl.Contract):)
4. Must have at least one typed state variable (e.g. count: int)
5. Must have a def __init__(self) constructor
6. Must have at least one @gl.public.view decorated method
7. Must have at least one @gl.public.write decorated method

CODE TO VALIDATE:
```python
{code}
```

Respond ONLY with this exact JSON — no markdown, no explanation:
{{
  "valid": true or false,
  "score": integer from 0 to 7 (number of requirements met),
  "missing": ["list of requirement descriptions that are missing"],
  "issues": ["list of specific problems found in the code"],
  "feedback": "one encouraging sentence of overall feedback"
}}

It is mandatory that you respond only using the JSON format above.
Your output must be perfectly parseable by a JSON parser without errors.
"""

        def nondet() -> str:
            result = gl.nondet.exec_prompt(prompt)
            result = result.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(result)
            return json.dumps({
                "valid": bool(parsed["valid"]),
                "score": int(parsed["score"]),
                "missing": [str(m) for m in parsed.get("missing", [])],
                "issues": [str(i) for i in parsed.get("issues", [])],
                "feedback": str(parsed["feedback"]),
            }, sort_keys=True)

        feedback_json = gl.eq_principle.strict_eq(nondet)
        feedback = json.loads(feedback_json)

        self.last_submission = code[:500]  # Store first 500 chars on-chain
        self.last_feedback = feedback_json
        self.total_checks += 1
        if feedback["valid"]:
            self.total_valid += 1
