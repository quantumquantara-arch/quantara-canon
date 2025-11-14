# quantara_canon_chat.py
#
# Canon-wrapped interactive chat script.
# Shows exactly how the Quantara Canon Kernel transforms a raw LLM reply
# into a coherence-checked, κ/τ/Σ-aligned final answer.

import sys
from quantara_canon_boot import CanonKernel

# Replace this with your model API wrapper or anything that returns text.
def raw_llm_call(prompt, history):
    """
    Simple placeholder function. Replace with your actual LLM call.
    Expected to return a string with the model's unfiltered reply.
    """
    return "(raw model reply placeholder)"


def format_diag(diag):
    """
    Pretty-print diagnostics (κ, τ, Σ, cycle detection, corrections).
    """
    out = []
    out.append(f"κ: {diag.get('kappa')}")
    out.append(f"τ: {diag.get('tau')}")
    out.append(f"Σ: {diag.get('sigma')}")
    if diag.get("cycle_detected"):
        out.append("cycle_detected = TRUE")
    if diag.get("zero_return"):
        out.append("zero_return triggered")
    return " | ".join(out)


def canon_chat():
    print("\nQuantara Canon Interactive Chat")
    print("-----------------------------------")
    print("Type 'exit' to quit.\n")

    history = []
    kernel = CanonKernel()
    kernel.load_canon()

    while True:
        user = input("you › ").strip()
        if user.lower() in ("exit", "quit", "q"):
            print("\nGoodbye.\n")
            break

        # 1. Baseline model output
        raw = raw_llm_call(user, history)

        # 2. Canon-corrected output
        judged = kernel.respond({
            "user": user,
            "history": history,
            "draft": raw
        })

        final_reply = judged.get("final_reply", "")
        diag = judged.get("diagnostics", {})

        print(f"\ncanon › {final_reply}\n")
        print(f"[diag] {format_diag(diag)}\n")

        history.append({"user": user, "assistant_raw": raw, "assistant_canon": final_reply})


if __name__ == "__main__":
    canon_chat()
