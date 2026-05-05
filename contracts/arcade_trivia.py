# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

# ─────────────────────────────────────────────────────────────────────────────
# ArcadeTrivia — GenLayer Community Arcade
# Deployed on Testnet Bradbury: 0xEC2A6C2EaB711146b151d5D441DE47136Faf5E6C
#
# AI-powered trivia judge. Players submit a question and their answer.
# The contract uses gl.exec_prompt() with gl.eq_principle_strict_eq() to have
# multiple Bradbury validators independently judge whether the answer is
# correct. Verdict and stats are stored on-chain.
# ─────────────────────────────────────────────────────────────────────────────


class ArcadeTrivia(gl.Contract):
    last_verdict: str

    def __init__(self):
        self.last_verdict = "none"

    @gl.public.view
    def get_last_verdict(self) -> str:
        return self.last_verdict

    @gl.public.write
    def submit_answer(self, question: str, player_answer: str) -> None:
        """
        Submit an answer to a GenLayer trivia question.

        Uses gl.exec_prompt() so multiple Bradbury validators independently
        call a real LLM to judge the answer. gl.eq_principle_strict_eq()
        ensures all validators must agree on the verdict before it is
        accepted and stored on-chain.

        Args:
            question:      The trivia question.
            player_answer: The player's answer to evaluate.
        """
        prompt = f"""You are a GenLayer trivia judge.

Question: {question}
Player answer: {player_answer}

Respond ONLY with this JSON, nothing else:
{{"correct": true, "reason": "one sentence"}}

It is mandatory that you respond only using the JSON format above.
"""
        def nondet():
            res = gl.exec_prompt(prompt)
            res = res.replace("```json", "").replace("```", "").strip()
            dat = json.loads(res)
            return json.dumps({
                "correct": bool(dat["correct"]),
                "reason": str(dat["reason"]),
            }, sort_keys=True)

        self.last_verdict = gl.eq_principle_strict_eq(nondet)
