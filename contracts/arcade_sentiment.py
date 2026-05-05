# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

# ─────────────────────────────────────────────────────────────────────────────
# ArcadeSentiment — GenLayer Community Arcade
# Deployed on Testnet Bradbury: 0xada54c1B3Aaa7538424b94E67c2b7785fC889cd3
#
# AI sentiment analysis contract. Powers the "Sentiment Oracle" game.
# Players type any text — the contract sends it to real Bradbury validators
# via gl.exec_prompt(). All validators must agree on the sentiment via
# gl.eq_principle_strict_eq() before the result is stored on-chain.
#
# This directly demonstrates how clear, structured prompts lead to unanimous
# validator consensus on Testnet Bradbury.
# ─────────────────────────────────────────────────────────────────────────────


class ArcadeSentiment(gl.Contract):
    last_result: str

    def __init__(self):
        self.last_result = "none"

    @gl.public.view
    def get_last_result(self) -> str:
        return self.last_result

    @gl.public.write
    def analyze(self, text: str) -> None:
        """
        Analyse the sentiment of any submitted text.

        Uses gl.exec_prompt() with gl.eq_principle_strict_eq() — all
        5 randomly selected Bradbury validators independently call their
        own LLM and must return identical JSON before consensus is reached.

        Args:
            text: The text to analyse for sentiment.
        """
        prompt = f"""Analyze the sentiment of the following text.

Respond ONLY with this exact JSON, nothing else:
{{"sentiment": "positive", "reason": "one sentence"}}
or
{{"sentiment": "negative", "reason": "one sentence"}}
or
{{"sentiment": "neutral", "reason": "one sentence"}}

Text: {text}

It is mandatory that you respond only using the JSON format above.
"""
        def nondet():
            res = gl.exec_prompt(prompt)
            res = res.replace("```json", "").replace("```", "").strip()
            dat = json.loads(res)
            return json.dumps({
                "sentiment": str(dat["sentiment"]).lower(),
                "reason": str(dat["reason"]),
            }, sort_keys=True)

        self.last_result = gl.eq_principle_strict_eq(nondet)
