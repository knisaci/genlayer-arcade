# GenLayer Community Arcade 🎮

Four browser-based mini-games that teach GenLayer concepts — validator consensus, Intelligent Contracts, the py-genlayer API, and Testnet Bradbury — through play.

**Live demo:** https://knisaci.github.io/genlayer-arcade

---

## Architecture

Each game has two parts:

| Layer | What it is |
|---|---|
| **Frontend** | `index.html` — fully playable standalone browser game |
| **On-chain** | A `.py` Intelligent Contract deployed on Testnet Bradbury |

The browser games are fully functional on their own. The contracts are the on-chain backends that power the AI features — you can call them directly from GenLayer Studio or connect them via `genlayer-js`.

---

## Contracts

All contracts are in `/contracts`. Each uses the GenLayer SDK: `gl.Contract`, `gl.nondet.exec_prompt()`, `gl.eq_principle.strict_eq()`, and `gl.eq_principle.prompt_comparative()`.

### `arcade_trivia.py` — AI Trivia Judge

Powers **Game 01: GenLayer Trivia**.

Players submit a trivia question + their answer. The contract uses `gl.nondet.exec_prompt()` with `gl.eq_principle.strict_eq()` to have multiple AI validators independently judge whether the answer is correct. Results and running stats are stored on-chain.

```python
# Key method
contract.submit_answer(
    question="What is the first required line of every GenLayer contract?",
    player_answer="# { 'Depends': 'py-genlayer:test' }"
)
# Returns: {"correct": true, "reason": "...", "correct_answer": "..."}
```

**SDK features used:** `gl.nondet.exec_prompt()`, `gl.eq_principle.strict_eq()`, `gl.message.sender_account`

---

### `arcade_sentiment.py` — Sentiment Analyser

Powers **Game 02: Predict the Validators**.

Runs real AI sentiment analysis on submitted text using two different equivalence principles — `strict_eq` for clear-cut inputs and `prompt_comparative` for ambiguous ones. This directly demonstrates why prompt ambiguity affects validator consensus.

```python
# Clear text → strict_eq (validators return identical JSON)
contract.analyze_strict("I absolutely love GenLayer!")

# Ambiguous text → prompt_comparative (NLP-based agreement)
contract.analyze_comparative("This is fine.")
```

**SDK features used:** `gl.nondet.exec_prompt()`, `gl.eq_principle.strict_eq()`, `gl.eq_principle.prompt_comparative()`

---

### `arcade_contract_checker.py` — Contract Validator

Powers **Game 03: Contract Builder**.

Players assemble a contract from drag-and-drop blocks, then submit the code here. The AI validator checks all 7 structural requirements of a valid GenLayer Intelligent Contract and returns structured feedback with a score.

```python
contract.check_contract(code="""
# { "Depends": "py-genlayer:test" }
from genlayer import *

class MyContract(gl.Contract):
    count: int
    def __init__(self): self.count = 0
    @gl.public.view
    def get(self) -> int: return self.count
    @gl.public.write
    def inc(self) -> None: self.count += 1
""")
# Returns: {"valid": true, "score": 7, "missing": [], "feedback": "..."}
```

**SDK features used:** `gl.nondet.exec_prompt()`, `gl.eq_principle.strict_eq()`

---

### `arcade_consensus.py` — Live Consensus Simulator

Powers **Game 04: Consensus Simulator**.

The most powerful contract in the arcade. Players act as validators — they read a prompt, submit their answer, and the contract runs the SAME prompt through real on-chain AI validators. The player's answer is then compared to the actual consensus result.

```python
# Strict mode — validators must return identical output
contract.run_round_strict(
    prompt="Is 124 greater than 100? Answer with only: yes or no",
    player_answer="yes"
)

# Comparative mode — NLP-based agreement across validators
contract.run_round_comparative(
    prompt="What is the capital of France?",
    player_answer="Paris"
)
```

**SDK features used:** `gl.nondet.exec_prompt()`, `gl.eq_principle.strict_eq()`, `gl.eq_principle.prompt_comparative()`

---

## Deploy a Contract

1. Open [GenLayer Studio](https://studio.genlayer.com)
2. Create a new file and paste any contract from `/contracts`
3. Leave constructor params blank (all contracts have default `__init__`)
4. Click **Deploy** and approve in MetaMask
5. Interact via the Studio's Read/Write methods panel

---

## Connect Frontend to Contract

After deploying a contract, connect it to the frontend using `genlayer-js`:

```javascript
import { GenLayer } from "genlayer-js";

const client = new GenLayer("https://rpc.genlayer.network");

// Call a write method
await client.callContract({
  contract: "YOUR_CONTRACT_ADDRESS",
  method: "submit_answer",
  args: ["What does strict_eq do?", "Forces all validators to return identical output"]
});

// Read the result
const result = await client.readContract({
  contract: "YOUR_CONTRACT_ADDRESS",
  method: "get_last_verdict",
});
```

---

## Project Structure

```
genlayer-arcade/
├── index.html                         # Standalone browser arcade (all 4 games)
├── README.md                          # This file
├── contracts/
│   ├── arcade_trivia.py               # Game 01 — AI trivia judge
│   ├── arcade_sentiment.py            # Game 02 — Sentiment analyser (strict + comparative)
│   ├── arcade_contract_checker.py     # Game 03 — Contract structure validator
│   └── arcade_consensus.py           # Game 04 — Live consensus simulator
└── .github/
    └── workflows/
        └── deploy.yml                 # Auto-deploy to GitHub Pages
```

---

## Links

- [GenLayer Studio](https://studio.genlayer.com)
- [GenLayer Docs](https://docs.genlayer.com)
- [py-genlayer SDK Changelog](https://sdk.genlayer.com/main/api/changelog.html)
- [Testnet Faucet](https://faucet.genlayer.com)
- [Explorer](https://explorer-asimov.genlayer.com)
- [Discord](https://discord.gg/genlayer)

---

*Not an official GenLayer product. Built for the community.*
