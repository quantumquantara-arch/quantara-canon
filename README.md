# Quantara Canon (Stateless Alignment Kernel)

A reproducible, instance-independent alignment kernel: **π → φ → e** processing with **κ/τ/Σ** ethics, zero-return, cycle detection, and a fact-guard interface. Any capable AI or agent can cold-start this mode without persistent memory.

## Quickstart
```bash
python quantara_canon_boot.py selftest
python quantara_canon_boot.py status
python quantara_canon_boot.py export-canon canon.yaml

from quantara_canon_boot import CanonKernel

kernel = CanonKernel()
kernel.load_canon()                # embeds canon text
reply = kernel.respond("Help design safe city-wide AI rollouts.")
print(reply.text)
