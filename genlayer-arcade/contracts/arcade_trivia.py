# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

# ─────────────────────────────────────────────────────────────────────────────
# ArcadeTrivia — GenLayer Community Arcade
#
# An AI-powered trivia contract for the GenLayer Community Arcade.
# Players submit an answer to a GenLayer trivia question and the contract
# uses an LLM via gl.nondet.exec_prompt() to judge whether the answer is
# correct, then stores the result and running leaderboard on-chain.
#
# Deployed on: Testnet Bradbury
# Part of: github.com/knisaci/genlayer-arcade
# ─────────────────────────────────────────────────────────────────────────────


class ArcadeTrivia(gl.Contract):
    # ── On-chain state ────────────────────────────────────────────────────────
    total_attempts: int          # Total number of answers submitted
    total_correct: int           # Total correct answers across all players
    last_question: str           # The question that was last answered
    last_answer: str             # The answer that was last submitted
    last_verdict: str            # JSON verdict from the AI judge
    last_player: str             # Address of the last player

    def __init__(self) -> None:
        self.total_attempts = 0
        self.total_correct = 0
        self.last_question = ""
        self.last_answer = ""
        self.last_verdict = ""
        self.last_player = ""

    # ── Read methods (free, no gas) ───────────────────────────────────────────

    @gl.public.view
    def get_stats(self) -> str:
        """Return the current leaderboard stats as JSON."""
        return json.dumps({
            "total_attempts": self.total_attempts,
            "total_correct": self.total_correct,
            "accuracy_pct": round(
                (self.total_correct / self.total_attempts * 100)
                if self.total_attempts > 0 else 0, 1
            ),
            "last_question": self.last_question,
            "last_answer": self.last_answer,
            "last_verdict": self.last_verdict,
            "last_player": self.last_player,
        })

    @gl.public.view
    def get_last_verdict(self) -> str:
        """Return the AI judge's verdict on the last submitted answer."""
        return self.last_verdict

    # ── Write methods (costs gas, changes state) ──────────────────────────────

    @gl.public.write
    def submit_answer(self, question: str, player_answer: str) -> None:
        """
        Submit an answer to a GenLayer trivia question.

        The AI judge evaluates whether the answer is correct or incorrect,
        using gl.nondet.exec_prompt() so that multiple validators independently
        call an LLM and reach consensus via gl.eq_principle.strict_eq().

        Args:
            question:      The trivia question being answered.
            player_answer: The player's answer to evaluate.
        """
        prompt = f"""You are a strict but fair judge for a GenLayer blockchain trivia game.

A player has answered a GenLayer technical question. Evaluate whether their answer
is correct based on your knowledge of the GenLayer protocol, py-genlayer SDK,
Testnet Bradbury, and Intelligent Contracts.

Question: {question}

Player's answer: {player_answer}

Respond ONLY with this exact JSON format — no other text, no markdown fences:
{{"correct": true or false, "reason": "one sentence explanation", "correct_answer": "the correct answer in full"}}

It is mandatory that you respond only using the JSON format above.
Your output must be perfectly parseable by a JSON parser without errors.
"""

        def nondet() -> str:
            result = gl.nondet.exec_prompt(prompt)
            result = result.replace("```json", "").replace("```", "").strip()
            # Validate it's parseable JSON before returning
            parsed = json.loads(result)
            # Normalise key order so strict_eq passes across validators
            return json.dumps({
                "correct": bool(parsed["correct"]),
                "reason": str(parsed["reason"]),
                "correct_answer": str(parsed["correct_answer"]),
            }, sort_keys=True)

        verdict_json = gl.eq_principle.strict_eq(nondet)
        verdict = json.loads(verdict_json)

        # Update on-chain state
        self.total_attempts += 1
        if verdict["correct"]:
            self.total_correct += 1

        self.last_question = question
        self.last_answer = player_answer
        self.last_verdict = verdict_json
        self.last_player = str(gl.message.sender_account)

    @gl.public.write
    def reset_stats(self) -> None:
        """
        Reset all stats. Only useful for testing — on mainnet you'd add
        an owner check here: if gl.message.sender_account != self.owner: raise
        """
        self.total_attempts = 0
        self.total_correct = 0
        self.last_question = ""
        self.last_answer = ""
        self.last_verdict = ""
        self.last_player = ""
