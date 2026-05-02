# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

# ─────────────────────────────────────────────────────────────────────────────
# ArcadeSentiment — GenLayer Community Arcade
#
# AI sentiment analysis contract used by the "Predict the Validators" game.
# Players predict whether validators will Agree or Disagree on a given text's
# sentiment — then this contract runs the real analysis on-chain so they can
# compare their prediction to the actual outcome.
#
# This contract intentionally uses both strict_eq (for clear-cut prompts) and
# prompt_comparative (for ambiguous inputs) to demonstrate the difference.
#
# Deployed on: Testnet Bradbury
# Part of: github.com/knisaci/genlayer-arcade
# ─────────────────────────────────────────────────────────────────────────────


class ArcadeSentiment(gl.Contract):
    # ── On-chain state ────────────────────────────────────────────────────────
    last_text: str           # The last text that was analysed
    last_result: str         # JSON result from the AI analysis
    last_mode: str           # Which eq principle was used: "strict" or "comparative"
    analysis_count: int      # Total number of analyses run

    def __init__(self) -> None:
        self.last_text = ""
        self.last_result = ""
        self.last_mode = ""
        self.analysis_count = 0

    # ── Read methods ──────────────────────────────────────────────────────────

    @gl.public.view
    def get_last_result(self) -> str:
        """Return the last AI sentiment analysis result as JSON."""
        return self.last_result

    @gl.public.view
    def get_analysis_count(self) -> int:
        """Return the total number of analyses run through this contract."""
        return self.analysis_count

    # ── Write methods ─────────────────────────────────────────────────────────

    @gl.public.write
    def analyze_strict(self, text: str) -> None:
        """
        Analyse sentiment using strict_eq equivalence principle.

        Use this for clear-cut texts where all validators should produce
        identical JSON output. Demonstrates how unambiguous prompts lead
        to unanimous validator consensus.

        Args:
            text: The text to analyse for sentiment.
        """
        prompt = f"""Analyse the sentiment of the following text.

You MUST respond with ONLY this exact JSON structure — no other text:
{{"sentiment": "positive", "confidence": "high", "reason": "one sentence"}}
or
{{"sentiment": "negative", "confidence": "high", "reason": "one sentence"}}
or
{{"sentiment": "neutral", "confidence": "high", "reason": "one sentence"}}

Text to analyse: {text}

Rules:
- sentiment must be exactly one of: positive, negative, neutral
- reason must be a single concise sentence
- confidence must be exactly: high, medium, or low
- Respond with ONLY the JSON object. No markdown. No explanation.
"""

        def nondet() -> str:
            result = gl.nondet.exec_prompt(prompt)
            result = result.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(result)
            return json.dumps({
                "sentiment": str(parsed["sentiment"]).lower(),
                "confidence": str(parsed["confidence"]).lower(),
                "reason": str(parsed["reason"]),
                "mode": "strict_eq",
            }, sort_keys=True)

        self.last_text = text
        self.last_result = gl.eq_principle.strict_eq(nondet)
        self.last_mode = "strict"
        self.analysis_count += 1

    @gl.public.write
    def analyze_comparative(self, text: str) -> None:
        """
        Analyse sentiment using prompt_comparative equivalence principle.

        Use this for ambiguous texts where different validators may word
        their answers differently but mean the same thing. Demonstrates
        how comparative equivalence handles natural language variance.

        Args:
            text: The text to analyse for sentiment.
        """
        def nondet() -> str:
            prompt = f"""What is the overall sentiment of this text?
Text: {text}
Answer with one word only: positive, negative, or neutral."""
            result = gl.nondet.exec_prompt(prompt)
            return result.strip().lower()

        self.last_text = text
        # prompt_comparative uses NLP to check if two answers mean the same thing
        # even if they're worded differently across validators
        result = gl.eq_principle.prompt_comparative(
            nondet,
            principle="The two answers express the same sentiment classification."
        )
        self.last_result = json.dumps({
            "sentiment": result,
            "mode": "prompt_comparative",
            "text": text,
        }, sort_keys=True)
        self.last_mode = "comparative"
        self.analysis_count += 1
