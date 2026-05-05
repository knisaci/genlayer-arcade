# GenLayer Community Arcade 🎮

Four browser-based mini-games powered by **real Intelligent Contracts** deployed on Testnet Bradbury. Every AI answer goes through on-chain validator consensus — results are stored on the blockchain.

**🔴 Live demo:** https://knisaci.github.io/genlayer-arcade

---

## How it works

Each game has two layers:

| Layer | What it is |
|---|---|
| **Frontend** | `index.html` — browser game using `genlayer-js` to call contracts |
| **On-chain** | Python Intelligent Contracts deployed on Testnet Bradbury |

Every game action submits a real transaction to Bradbury via `genlayer-js`. Results are stored on-chain and linked to the GenLayer Explorer.

---

## Deployed Contracts — Testnet Bradbury

| Contract | Address | Explorer |
|---|---|---|
| ArcadeTrivia | `0xEC2A6C2EaB711146b151d5D441DE47136Faf5E6C` | [View ↗](https://explorer-asimov.genlayer.com/contract/0xEC2A6C2EaB711146b151d5D441DE47136Faf5E6C) |
| ArcadeSentiment | `0xada54c1B3Aaa7538424b94E67c2b7785fC889cd3` | [View ↗](https://explorer-asimov.genlayer.com/contract/0xada54c1B3Aaa7538424b94E67c2b7785fC889cd3) |
| ArcadeContractChecker | `0x871dA1C5FF3738C3007c9E91BaE67fD284E497FB` | [View ↗](https://explorer-asimov.genlayer.com/contract/0x871dA1C5FF3738C3007c9E91BaE67fD284E497FB) |
| ArcadeConsensus | `0x45F287e4FA97bf273B7fFfE02e4C023FEF295311` | [View ↗](https://explorer-asimov.genlayer.com/contract/0x45F287e4FA97bf273B7fFfE02e4C023FEF295311) |

---

## Games

### 🧠 Game 01 — GenLayer Trivia
Answer GenLayer questions. Your answer is submitted to `ArcadeTrivia.submit_answer()` — a real AI judge on Bradbury validators decides if you're correct and stores the verdict on-chain.

**Contract call:**
```javascript
await client.writeContract({
  address: '0xEC2A6C2EaB711146b151d5D441DE47136Faf5E6C',
  functionName: 'submit_answer',
  args: [question, playerAnswer],
  value: 0n
});
```

---

### 🔮 Game 02 — Sentiment Oracle
Type any text. It's sent to `ArcadeSentiment.analyze()` — real Bradbury validators reach consensus on whether it's positive, negative or neutral. Result written to the blockchain.

**Contract call:**
```javascript
await client.writeContract({
  address: '0xada54c1B3Aaa7538424b94E67c2b7785fC889cd3',
  functionName: 'analyze',
  args: [text],
  value: 0n
});
```

---

### 🧩 Game 03 — Contract Builder
Drag and drop code blocks to assemble an Intelligent Contract. Submit your code to `ArcadeContractChecker.check_contract()` — an AI validator on Bradbury checks all 7 structural requirements and returns a score.

**Contract call:**
```javascript
await client.writeContract({
  address: '0x871dA1C5FF3738C3007c9E91BaE67fD284E497FB',
  functionName: 'check_contract',
  args: [code],
  value: 0n
});
```

---

### ⚡ Game 04 — Consensus Simulator
You are a validator. Submit your answer to `ArcadeConsensus.run_round()` — the same prompt is sent to real Bradbury AI validators. See whether your answer matched the on-chain consensus.

**Contract call:**
```javascript
await client.writeContract({
  address: '0x45F287e4FA97bf273B7fFfE02e4C023FEF295311',
  functionName: 'run_round',
  args: [prompt, playerAnswer],
  value: 0n
});
```

---

## Frontend — genlayer-js integration

The frontend uses `genlayer-js` loaded via ESM importmap (no build step needed):

```html
<script type="importmap">
{
  "imports": {
    "genlayer-js": "https://esm.sh/genlayer-js@latest",
    "genlayer-js/chains": "https://esm.sh/genlayer-js@latest/chains",
    "genlayer-js/types": "https://esm.sh/genlayer-js@latest/types"
  }
}
</script>
```

```javascript
import { createClient, createAccount } from 'genlayer-js';
import { testnetAsimov } from 'genlayer-js/chains';
import { TransactionStatus } from 'genlayer-js/types';

const account = createAccount();
const client = createClient({ chain: testnetAsimov, account });

// Write to contract — waits for FINALIZED status
const hash = await client.writeContract({
  address: CONTRACT_ADDRESS,
  functionName: 'method_name',
  args: ['arg1'],
  value: 0n
});
await client.waitForTransactionReceipt({
  hash,
  status: TransactionStatus.FINALIZED,
  retries: 60,
  interval: 5000
});

// Read from contract
const result = await client.readContract({
  address: CONTRACT_ADDRESS,
  functionName: 'get_result',
  args: [],
  stateStatus: 'accepted'
});
```

---

## Project Structure

```
genlayer-arcade/
├── index.html                      ← Browser arcade — calls live contracts via genlayer-js
├── README.md                       ← This file
├── contracts/
│   ├── arcade_trivia.py            ← Game 01 — AI trivia judge
│   ├── arcade_sentiment.py         ← Game 02 — Sentiment analyser
│   ├── arcade_contract_checker.py  ← Game 03 — Contract structure validator
│   └── arcade_consensus.py         ← Game 04 — Live consensus simulator
└── .github/
    └── workflows/
        └── static.yml              ← Auto GitHub Pages deployment
```

---

## Deploy contracts yourself

1. Open [GenLayer Studio](https://studio.genlayer.com)
2. Create a new file and paste any contract from `/contracts`
3. Leave constructor params blank
4. Click **Deploy** → approve in MetaMask
5. Copy your contract address and update the `CONTRACTS` object in `index.html`

---

## Links

- [GenLayer Studio](https://studio.genlayer.com)
- [GenLayer Docs](https://docs.genlayer.com)
- [Testnet Faucet](https://faucet.genlayer.com)
- [Explorer](https://explorer-asimov.genlayer.com)
- [Discord](https://discord.gg/genlayer)
- [GitHub](https://github.com/genlayerlabs)

---

*Not an official GenLayer product. Built for the community.*
