# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

# ─────────────────────────────────────────────────────────────────────────────
# ArcadeContractChecker — GenLayer Community Arcade
# Deployed on Testnet Bradbury: 0x871dA1C5FF3738C3007c9E91BaE67fD284E497FB
#
# AI contract validator. Powers the "Contract Builder" game.
# Players drag and drop code blocks to assemble a contract, then submit
# the code here. The contract uses gl.exec_prompt() with
# gl.eq_principle_strict_eq() to have Bradbury validators check all 7
# structural requirements of a valid Intelligent Contract.
# ─────────────────────────────────────────────────────────────────────────────


class ArcadeContractChecker(gl.Contract):
    last_feedback: str

    def __init__(self):
        self.last_feedback = "none"

    @gl.public.view
    def get_last_feedback(self) -> str:
        return self.last_feedback

    @gl.public.write
    def check_contract(self, code: str) -> None:
        """
        Submit Python code to be validated as a GenLayer Intelligent Contract.

        The AI validator checks for all 7 required structural elements:
        1. Runner comment on line 1
        2. from genlayer import *
        3. Class extending gl.Contract
        4. At least one typed state variable
        5. An __init__ constructor
        6. At least one @gl.public.view method
        7. At least one @gl.public.write method

        Uses gl.exec_prompt() with gl.eq_principle_strict_eq() — all
        Bradbury validators must agree on the score and feedback.

        Args:
            code: The Python source code to validate.
        """
        prompt = f"""You are a GenLayer Intelligent Contract validator.

Check if the following Python code is a valid GenLayer contract.

Required elements:
1. Line 1 must be: # {{ "Depends": "py-genlayer:test" }}
2. Must have: from genlayer import *
3. Class must extend gl.Contract
4. Must have at least one typed state variable
5. Must have def __init__(self)
6. Must have at least one @gl.public.view method
7. Must have at least one @gl.public.write method

Code:
{code}

Respond ONLY with this exact JSON, nothing else:
{{"valid": true, "score": 7, "feedback": "one sentence"}}

It is mandatory that you respond only using the JSON format above.
"""
        def nondet():
            res = gl.exec_prompt(prompt)
            res = res.replace("```json", "").replace("```", "").strip()
            dat = json.loads(res)
            return json.dumps({
                "valid": bool(dat["valid"]),
                "score": int(dat["score"]),
                "feedback": str(dat["feedback"]),
            }, sort_keys=True)

        self.last_feedback = gl.eq_principle_strict_eq(nondet)
