# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

# ─────────────────────────────────────────────────────────────────────────────
# ArcadeConsensus — GenLayer Community Arcade
#
# The on-chain backend for the "Consensus Simulator" game.
# Players act as validators — they read a prompt, submit their answer,
# and this contract runs the SAME prompt through real AI validators on-chain.
# The player's answer is compared to the on-chain AI consensus, showing them
# whether they "agreed" with the validator majority.
#
# This is the most powerful demo contract in the arcade because it lets players
# directly experience what the GenLayer equivalence principle does in practice.
#
# Deployed on: Testnet Bradbury
# Part of: github.com/knisaci/genlayer-arcade
# ─────────────────────────────────────────────────────────────────────────────


class ArcadeConsensus(gl.Contract):
    # ── On-chain state ────────────────────────────────────────────────────────
    last_prompt: str            # The prompt that was evaluated
    last_ai_answer: str         # The consensus answer from on-chain validators
    last_player_answer: str     # The player's submitted answer
    last_player_agreed: bool    # Whether the player agreed with consensus
    last_eq_mode: str           # Which eq principle was used
    rounds_played: int          # Total rounds played across all players
    player_agreements: int      # Times a player agreed with the AI consensus

    def __init__(self) -> None:
        self.last_prompt = ""
        self.last_ai_answer = ""
        self.last_player_answer = ""
        self.last_player_agreed = False
        self.last_eq_mode = ""
        self.rounds_played = 0
        self.player_agreements = 0

    # ── Read methods ──────────────────────────────────────────────────────────

    @gl.public.view
    def get_last_round(self) -> str:
        """Return a JSON summary of the last consensus round."""
        return json.dumps({
            "prompt": self.last_prompt,
            "ai_consensus_answer": self.last_ai_answer,
            "player_answer": self.last_player_answer,
            "player_agreed": self.last_player_agreed,
            "eq_mode": self.last_eq_mode,
        })

    @gl.public.view
    def get_global_stats(self) -> str:
        """Return global agreement stats across all players."""
        return json.dumps({
            "rounds_played": self.rounds_played,
            "player_agreements": self.player_agreements,
            "agreement_rate_pct": round(
                (self.player_agreements / self.rounds_played * 100)
                if self.rounds_played > 0 else 0, 1
            )
        })

    # ── Write methods ─────────────────────────────────────────────────────────

    @gl.public.write
    def run_round_strict(self, prompt: str, player_answer: str) -> None:
        """
        Run a consensus round using strict_eq equivalence principle.

        The contract sends the prompt to real AI validators via
        gl.nondet.exec_prompt(). All validators must return identical output
        for consensus to be reached. The player's answer is then compared
        to the on-chain AI consensus.

        Use this for prompts with deterministic, unambiguous answers.

        Args:
            prompt:        The question/task to send to the AI validators.
            player_answer: The player's own answer to compare against consensus.
        """
        player_ans_clean = player_answer.strip().lower()

        def nondet() -> str:
            result = gl.nondet.exec_prompt(
                prompt + "\n\nRespond with a single word or very short phrase only. No explanation."
            )
            return result.strip().lower()

        # All validators independently call the LLM and must agree exactly
        ai_answer = gl.eq_principle.strict_eq(nondet)

        agreed = player_ans_clean == ai_answer.strip().lower()

        self._store_round(prompt, ai_answer, player_answer, agreed, "strict_eq")

    @gl.public.write
    def run_round_comparative(self, prompt: str, player_answer: str) -> None:
        """
        Run a consensus round using prompt_comparative equivalence principle.

        Same as run_round_strict but uses NLP-based comparison, so validators
        that give semantically equivalent answers still reach consensus even
        if the exact wording differs. The player's answer is compared using
        the same NLP approach.

        Use this for prompts where the answer could be expressed multiple ways.

        Args:
            prompt:        The question/task to send to the AI validators.
            player_answer: The player's own answer to compare against consensus.
        """
        def nondet() -> str:
            result = gl.nondet.exec_prompt(prompt)
            return result.strip()

        ai_answer = gl.eq_principle.prompt_comparative(
            nondet,
            principle="The two answers convey the same meaning or conclusion."
        )

        # Compare player answer to AI consensus using NLP too
        def compare_player() -> str:
            compare_prompt = f"""Do these two answers mean the same thing?
Answer A: {ai_answer}
Answer B: {player_answer}
Respond with only: yes or no"""
            result = gl.nondet.exec_prompt(compare_prompt)
            return result.strip().lower()

        agreement_check = gl.eq_principle.strict_eq(compare_player)
        agreed = "yes" in agreement_check

        self._store_round(prompt, ai_answer, player_answer, agreed, "prompt_comparative")

    def _store_round(
        self,
        prompt: str,
        ai_answer: str,
        player_answer: str,
        agreed: bool,
        mode: str
    ) -> None:
        """Internal helper to update on-chain state after a round."""
        self.last_prompt = prompt[:300]
        self.last_ai_answer = ai_answer
        self.last_player_answer = player_answer
        self.last_player_agreed = agreed
        self.last_eq_mode = mode
        self.rounds_played += 1
        if agreed:
            self.player_agreements += 1
