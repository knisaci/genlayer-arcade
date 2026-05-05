# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

# ─────────────────────────────────────────────────────────────────────────────
# ArcadeConsensus — GenLayer Community Arcade
# Deployed on Testnet Bradbury: 0x45F287e4FA97bf273B7fFfE02e4C023FEF295311
#
# Live consensus simulator. Powers the "Consensus Simulator" game.
# Players act as validators — they read a prompt, submit their answer,
# and this contract runs the SAME prompt through real Bradbury AI validators
# via gl.exec_prompt() with gl.eq_principle_strict_eq().
#
# The player's answer is then compared to the on-chain AI consensus,
# showing them whether they "agreed" with the validator majority.
#
# This is the most powerful demo in the arcade — it lets players directly
# experience what the GenLayer equivalence principle does in practice.
#
# Note on validator selection: 5 validators are randomly selected per
# transaction on Testnet Bradbury. The exact nodes and LLMs they use
# cannot be predicted in advance — this is by design.
# ─────────────────────────────────────────────────────────────────────────────


class ArcadeConsensus(gl.Contract):
    last_prompt: str
    last_ai_answer: str
    last_player_answer: str
    last_agreed: str

    def __init__(self):
        self.last_prompt = "none"
        self.last_ai_answer = "none"
        self.last_player_answer = "none"
        self.last_agreed = "false"

    @gl.public.view
    def get_last_round(self) -> str:
        """Return the last round result as JSON."""
        return json.dumps({
            "prompt": self.last_prompt,
            "ai_answer": self.last_ai_answer,
            "player_answer": self.last_player_answer,
            "agreed": self.last_agreed,
        })

    @gl.public.write
    def run_round(self, prompt: str, player_answer: str) -> None:
        """
        Run a consensus round and compare the player's answer to the
        on-chain AI consensus.

        The contract sends the same prompt to real Bradbury validators
        via gl.exec_prompt(). All validators independently call their own
        LLM and must return identical output for gl.eq_principle_strict_eq()
        to pass. The player's answer is then compared to the consensus result.

        Args:
            prompt:        The prompt sent to AI validators on-chain.
            player_answer: The player's own answer to compare against consensus.
        """
        def nondet():
            res = gl.exec_prompt(
                prompt + "\n\nRespond with a single word or short phrase only. No explanation."
            )
            return res.strip().lower()

        ai_answer = gl.eq_principle_strict_eq(nondet)

        agreed = player_answer.strip().lower() == ai_answer.strip().lower()

        self.last_prompt = prompt
        self.last_ai_answer = ai_answer
        self.last_player_answer = player_answer
        self.last_agreed = "true" if agreed else "false"
