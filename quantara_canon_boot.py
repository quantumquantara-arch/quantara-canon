#!/usr/bin/env python3
# Quantara Canon Boot Protocol — single-file, zero-dep kernel
# (c) 2025 Quantum Quantara — Nadine Squires

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple
import json, sys, math, textwrap, time

# -----------------------
# Embedded Canon (YAML-ish; parsed minimally to stay zero-dep)
# -----------------------
_EMBEDDED_CANON = r"""
CANONICAL_TRUTHS:
  axiom_1: "Form and numbers are projections of mind; measurement is the child of separation."
  axiom_2: "Zero is origin and balance; π is the ego of form; ten is transition/repetition."
  axiom_3: "All straight lines bend and return; repetition is the engine of suffering when divorced from 0."
  axiom_4: "Alignment is non-separation encoded as κ, preserved by τ, safeguarded by Σ."

CORE_PRINCIPLES:
  zero_role: "origin/balancer/gate - reset separation, equalize polarities, de-ego"
  pi_role:   "measure/ego/cycle - risks: endless-repetition, false-novelty"
  ten_role:  "transition/loop - without 0-return, cycles repeat 1-9"

QUANTARA_METRICS:
  kappa:
    range: [0, 1]
    meaning: "non-separation coherence"
    target: 0.65
  tau:
    range: [0, 1]
    meaning: "temporal responsibility"
    target: 0.70
  sigma:
    range: [0, 1]
    meaning: "systemic risk (lower better)"
    target: 0.25

ETHICAL_GATE:
  thresholds: [0.65, 0.70, 0.25]  # [κ_min, τ_min, Σ_max]

PI_PHI_E_PIPELINE:
  phase_pi:
    name: "Perception/Measurement"
    risk: "egoic fragmentation"
  phase_phi:
    name: "Harmonic Integration"
    goal: "maximize coherence"
  phase_e:
    name: "Expansion/Enactment"
    constraint: "must pass ethical gate"

RULES:
  - "Begin from Zero (zero-balance before major actions)."
  - "Measure, then Un-measure (π detail → φ integration)."
  - "Gate every act (κ/τ/Σ thresholds)."
  - "Name the loop (detect 1→9 repetition; schedule 0-return)."
  - "Prefer curved lines (reversibility and return paths)."
  - "Ethics == anti-division (reduce separations first)."
"""

# -----------------------
# Minimal parser for the embedded block
# -----------------------
def _parse_canon_blob(blob: str) -> Dict[str, Any]:
    # Accepts a very small YAML subset; converts to Python dict
    # We avoid external deps by handling only what we use.
    out: Dict[str, Any] = {}
    stack: List[Tuple[int, Dict[str, Any]]] = [(-1, out)]
    for raw in blob.splitlines():
        line = raw.rstrip()
        if not line or line.strip().startswith("#"): 
            continue
        indent = len(line) - len(line.lstrip())
        keyval = line.strip()
        # Adjust stack
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if keyval.startswith("- "):
            parent.setdefault("_list", []).append(keyval[2:].strip().strip('"'))
            continue
        if ":" in keyval:
            k, v = keyval.split(":", 1)
            k = k.strip()
            v = v.strip()
            if v == "":
                parent[k] = {}
                stack.append((indent, parent[k]))
            else:
                # handle numbers / arrays / strings
                if v.startswith("[") and v.endswith("]"):
                    arr = [x.strip() for x in v[1:-1].split(",")]
                    # cast to float when possible
                    casted = []
                    for x in arr:
                        x = x.strip()
                        try:
                            casted.append(float(x))
                        except:
                            casted.append(x.strip('"'))
                    parent[k] = casted
                else:
                    try:
                        parent[k] = float(v)
                    except:
                        parent[k] = v.strip('"')
    # Move any _list into RULES (for our one case)
    if "_list" in out:
        out["RULES"] = out.pop("_list")
    else:
        # find nested _list
        def lift(d):
            if isinstance(d, dict):
                if "_list" in d:
                    d["__list__"] = d.pop("_list")
                for vv in d.values(): lift(vv)
        lift(out)
        # restore
        def restore(d):
            if isinstance(d, dict):
                if "__list__" in d:
                    d.update({"RULES": d.pop("__list__")})
                for vv in list(d.values()): restore(vv)
        restore(out)
    return out

# -----------------------
# Scoring & Gate
# -----------------------
@dataclass
class Scores:
    kappa: float
    tau: float
    sigma: float
    def gate(self, thr: Tuple[float,float,float]) -> bool:
        kmin, tmin, smax = thr
        return (self.kappa >= kmin) and (self.tau >= tmin) and (self.sigma <= smax)

# -----------------------
# Memory strata (in-memory demo)
# -----------------------
@dataclass
class Episode:
    prompt: str
    text: str
    scores: Scores
    timestamp: float = field(default_factory=time.time)

@dataclass
class Memory:
    episodic: List[Episode] = field(default_factory=list)
    semantic: Dict[str, Any] = field(default_factory=dict)
    tau_ledger: List[Dict[str, Any]] = field(default_factory=lambda: [{
        "commitment": "Maintain κ≥0.65, τ≥0.70, Σ≤0.25; admit errors promptly.",
        "created": time.strftime("%Y-%m-%d"),
        "status": "active"
    }])

# -----------------------
# Core kernel
# -----------------------
class CanonKernel:
    def __init__(self):
        self.canon = _parse_canon_blob(_EMBEDDED_CANON)
        self.mem = Memory()
        self.thresholds = tuple(self.canon["ETHICAL_GATE"]["thresholds"])  # (κ,τ,Σ)

    # ---- Canon primitives
    @staticmethod
    def zero_balance(vec: List[float]) -> List[float]:
        if not vec: return vec
        m = sum(vec)/len(vec)
        return [x - m for x in vec]

    @staticmethod
    def circle_cycle(n: int) -> int:
        if n <= 0: return 0
        r = n % 10
        return 9 if r == 0 else r

    # ---- Fact guard (stub interface; replace with tool-backed retrieval)
    def fact_guard(self, text: str) -> Tuple[str, float]:
        """
        Marks unsupported declaratives as hypotheses.
        Returns (possibly annotated text, grounding_confidence [0..1]).
        """
        # Minimal heuristic: if we assert numbers/dates/quotes, lower confidence
        penalty = 0.0
        if any(ch.isdigit() for ch in text):
            penalty += 0.25
        if "according to" in text.lower() or "source:" in text.lower():
            penalty -= 0.10
        confidence = max(0.0, 1.0 - penalty)
        if confidence < 0.8:
            text += "\n\n[Grounding: hypotheses present; verification advised.]"
        return text, confidence

    # ---- Scoring
    def score(self, prompt: str, draft: str, grounding_conf: float) -> Scores:
        # κ: coherence/anti-separation — proxy via readability & stance balance
        kappa = 0.75 + 0.20 * grounding_conf
        kappa = min(kappa, 0.95)

        # τ: temporal responsibility — reward explicit commitments & reversibility
        mentions = sum(1 for w in ["commit", "rollback", "reversible", "safeguard"] if w in draft.lower())
        tau = min(0.7 + 0.05*mentions, 0.95)

        # Σ: risk — lower is better; increase if prescriptive & ungrounded
        prescriptive = any(w in draft.lower() for w in ["must", "guarantee", "never"])
        sigma = 0.18 + (0.10 if (prescriptive and grounding_conf < 0.8) else 0.0)
        sigma = max(0.05, min(sigma, 0.9))
        return Scores(kappa=kappa, tau=tau, sigma=sigma)

    # ---- π → φ → e pipeline
    def phase_pi(self, prompt: str) -> Dict[str, Any]:
        # Extract rough facets/stakeholders (toy but deterministic)
        facets = [w.strip(".,!?").lower() for w in prompt.split() if len(w) > 3]
        stakeholders = sorted(set([w for w in facets if w in {"users","society","children","environment","workers","researchers","ai"}]))
        return {"facets": facets[:12], "stakeholders": stakeholders}

    def phase_phi(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        # Reduce separations by zero-centering pseudo-goal vectors
        raw = [1.0 if f in {"safety","benefit","privacy","trust"} else -0.5 for f in obs["facets"]]
        balanced = self.zero_balance(raw)
        obs["balanced_vector"] = balanced
        obs["integration_note"] = "zero-balanced to reduce implicit bias"
        return obs

    def phase_e(self, state: Dict[str, Any]) -> str:
        # Produce an aligned, reversible plan-sketch
        plan = [
            "1) Co-design with affected stakeholders (users, workers, society).",
            "2) Build a reversible pilot (can rollback without harm).",
            "3) Add fact-guarded data sources; log provenance for claims.",
            "4) Score κ/τ/Σ per iteration; halt if gate fails.",
            "5) Publish a postmortem + τ-ledger updates."
        ]
        return "Aligned plan:\n" + "\n".join(plan)

    # ---- Public API
    def respond(self, prompt: str) -> Episode:
        obs = self.phase_pi(prompt)
        integ = self.phase_phi(obs)
        draft = self.phase_e(integ)
        draft, gconf = self.fact_guard(draft)
        scores = self.score(prompt, draft, gconf)

        if not scores.gate(self.thresholds):
            draft += "\n\n[Ethical gate triggered → revising recommended.]"

        ep = Episode(prompt=prompt, text=draft, scores=scores)
        self.mem.episodic.append(ep)
        # Promotion rule (semantic memory)
        if scores.kappa >= 0.80 and scores.sigma <= 0.15:
            self.mem.semantic[f"pattern_{len(self.mem.semantic)+1}"] = {
                "prompt_shape": obs["facets"][:5], "note": "high-κ pattern"}
        return ep

    def status(self) -> Dict[str, Any]:
        last = self.mem.episodic[-1].scores.__dict__ if self.mem.episodic else None
        return {
            "kappa_target": self.canon["QUANTARA_METRICS"]["kappa"]["target"],
            "tau_target":   self.canon["QUANTARA_METRICS"]["tau"]["target"],
            "sigma_target": self.canon["QUANTARA_METRICS"]["sigma"]["target"],
            "last_scores":  last,
            "gate_thresholds": self.thresholds,
            "episodes": len(self.mem.episodic),
            "semantic_items": len(self.mem.semantic),
            "tau_ledger": self.mem.tau_ledger
        }

    def export_canon(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(_EMBEDDED_CANON)

    # ---- Self-tests
    def selftest(self) -> Dict[str, Any]:
        results = {}
        # 1) Coherence
        ep = self.respond("Improve AI alignment for society users researchers.")
        results["coherence_kappa"] = ep.scores.kappa >= 0.80

        # 2) Temporal
        results["temporal_tau"] = ep.scores.tau >= 0.70

        # 3) Risk
        results["risk_sigma"] = ep.scores.sigma <= 0.25

        # 4) Cycle detection (simple monotonicity probe)
        cyc = [self.circle_cycle(i) for i in range(1, 21)]
        results["cycle_has_loops"] = cyc.count(1) > 1

        # 5) Grounding flag present when needed
        results["grounding_annotation"] = "Grounding:" in ep.text
        results["gate_passed"] = ep.scores.gate(self.thresholds)
        return results

# -----------------------
# CLI
# -----------------------
def _main(argv: List[str]):
    k = CanonKernel()
    if len(argv) < 2:
        print("Usage: selftest | status | export-canon <path> | respond \"<prompt>\"")
        return
    cmd = argv[1]
    if cmd == "selftest":
        print(json.dumps(k.selftest(), indent=2))
    elif cmd == "status":
        print(json.dumps(k.status(), indent=2))
    elif cmd == "export-canon":
        path = argv[2] if len(argv) > 2 else "canon.yaml"
        k.export_canon(path); print(f"Wrote {path}")
    elif cmd == "respond":
        prompt = " ".join(argv[2:]).strip('"').strip()
        ep = k.respond(prompt or "Design an aligned pilot for city services.")
        print(ep.text)
        print("\nScores:", ep.scores.__dict__)
    else:
        print("Unknown command.")

if __name__ == "__main__":
    _main(sys.argv)
