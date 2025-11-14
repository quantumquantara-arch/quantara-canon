# Canon Chat Walkthrough  
*Seeing the Stateless Alignment Kernel in Action*

This example shows how the **Quantara Canon Kernel** can wrap any model and
turn a raw reply into a **coherence-checked, κ/τ/Σ-aware answer** – without
needing persistent memory or fine-tuning.

---

## 1. What this script does

`examples/quantara_canon_chat.py` is a tiny, testable interface that:

1. Takes your input in the terminal (`you ›`).
2. Calls a **raw model** (currently a placeholder function).
3. Sends the draft reply into the **Canon Kernel**.
4. Prints the **Canon-corrected reply** plus diagnostics:

- **κ** – coherence / internal consistency  
- **τ** – temporal responsibility / time awareness  
- **Σ** – systemic risk / impact awareness  
- `cycle_detected` – did we detect a logical loop?  
- `zero_return` – did the kernel decide to refuse or reset?

You can plug in any model and immediately see how the kernel behaves.

---

## 2. How to run it

From the repo root:

```bash
# (optional) run the built-in self-test
python quantara_canon_boot.py selftest

# launch the interactive Canon chat
python -m quantara_canon_chat
# or, depending on your layout:
python examples/quantara_canon_chat.py
