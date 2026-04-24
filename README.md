# GenLayer Community Arcade 🎮

Four browser-based mini-games that teach GenLayer concepts — validator consensus, Intelligent Contracts, the py-genlayer API, and Testnet Bradbury — through play.

**Live demo:** https://YOUR_USERNAME.github.io/genlayer-arcade

---

## Games

| # | Game | What you learn |
|---|---|---|
| 01 | 🧠 **GenLayer Trivia** | Runner comments, API names, transaction states, consensus |
| 02 | 🔮 **Predict the Validators** | How AI validators vote and why prompt clarity matters |
| 03 | 🧩 **Contract Builder** | Drag-and-drop contract anatomy — basic then AI-powered |
| 04 | ⚡ **Consensus Simulator** | Be a validator, cast your vote, watch consensus resolve |

---

## Deploy in 3 steps

### Option A — GitHub Pages (recommended)

```bash
# 1. Fork or clone this repo
git clone https://github.com/YOUR_USERNAME/genlayer-arcade
cd genlayer-arcade

# 2. Push to GitHub
git add .
git commit -m "Initial deploy"
git push origin main

# 3. Enable GitHub Pages
# Go to: Settings → Pages → Source → Deploy from branch → main → / (root)
```

Your site will be live at:
```
https://YOUR_USERNAME.github.io/genlayer-arcade
```

---

### Option B — Vercel (fastest, custom domain support)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from the project folder
vercel

# For production
vercel --prod
```

Or connect your GitHub repo at vercel.com — it auto-deploys on every push.

---

### Option C — Submit to GenLayer docs/community

1. Fork the [genlayer-docs](https://github.com/genlayerlabs/genlayer-docs) repo
2. Add the `index.html` to an `/arcade` or `/community/games` directory
3. Open a PR with the title: `[Community] Add interactive mini-games hub`
4. Reference this repo in the PR description

---

## Project structure

```
genlayer-arcade/
├── index.html          # Everything — single self-contained file
└── README.md           # This file
```

The entire arcade is a single `index.html` file. No build step, no dependencies, no npm. Just open it in a browser.

---

## Contributing

Want to add more questions, scenarios, or a new game? 

- **Add trivia questions** — extend the `T` array in the `<script>` section
- **Add predict scenarios** — extend the `P` array
- **Add consensus sim rounds** — extend the `S` array
- **Add a new game** — add a card to `.game-grid` and write a `render*()` function

PRs welcome.

---

## Links

- [GenLayer Studio](https://studio.genlayer.com) — deploy your own contract
- [GenLayer Docs](https://docs.genlayer.com)
- [Testnet Faucet](https://faucet.genlayer.com)
- [Explorer](https://explorer-asimov.genlayer.com)
- [Discord](https://discord.gg/genlayer)

---

*Not an official GenLayer product. Built for the community.*
