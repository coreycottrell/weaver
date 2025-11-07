#!/usr/bin/env python3
"""
agents_stack.py
A minimal, working skeleton that enforces flows, artifacts, and guardrails.
Replace `generate()` stubs with your LLM calls. Everything else runs now.

Part of: The Minimal Business Stack (4 agents, one brain)
See: BUSINESS-STACK-4-AGENT-FRAMEWORK.md
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import re
import json
import time

# ---------- Shared data structures ----------

@dataclass
class ObserverArtifact:
    task: str
    change_since_last: str
    anomalies: str
    confidence: float
    evidence_links: List[str]

@dataclass
class OfferBrief:
    ICP: str
    Pain: str
    Promise: str
    Proof: str
    Price: str
    Path: str

@dataclass
class Experiment:
    name: str
    hypothesis: str
    sample_size: int
    success_metric: str
    variants: List[Dict[str, str]]
    stop_rule: str

# ---------- Utility: tiny in-memory store ----------

class Store:
    def __init__(self):
        self.artifacts: Dict[str, Any] = {}
        self.metrics: Dict[str, Any] = {"sends":0, "replies":0, "meetings":0, "closed":0}
    def put(self, key, value):
        self.artifacts[key] = value
    def get(self, key, default=None):
        return self.artifacts.get(key, default)
    def incr(self, key, n=1):
        self.metrics[key]= self.metrics.get(key,0)+n

STORE = Store()

# ---------- Limiting belief interceptor ----------

LIMIT_RE = re.compile(r"\b(we (can|can\'t|must|have to)|the only way|no one will|we need .* before|not possible|too (late|early|crowded|expensive))\b", re.I)

def intercept_limiting(statement: str) -> Dict[str, Any]:
    label = "assumption" if "must" in statement or "have to" in statement else "fear"
    tests = [
        "Find one counterexample and note what's different (≤30m).",
        "Draft 3 tiny offers and ask 5 targets which one they'd take (≤30m).",
        "Ship a no-code landing with Calendly; aim for 1 booking (≤30m)."
    ]
    step = "Post a 2-sentence offer to 5 ICP contacts and ask for a 10-min call."
    oa = ObserverArtifact(
        task="LimitingStatementReframe",
        change_since_last="Replaced assumption with three micro-tests.",
        anomalies="None yet.",
        confidence=0.6,
        evidence_links=[]
    )
    return {"label": label, "tests": tests, "next_step": step, "observer": asdict(oa)}

# ---------- Agent stubs (replace generate() with your LLMs) ----------

def coach(statement: str) -> Dict[str, Any]:
    """Business Coach: Intercept limiting statements and convert to testable moves."""
    if LIMIT_RE.search(statement):
        return intercept_limiting(statement)
    else:
        return {"note":"No limiting statement detected."}

def bizdev(icp: str, offer_hint: str) -> Dict[str, Any]:
    """BizDev: Map opportunities, shape offers, assemble partner shortlists."""
    accounts = [f"{icp} Prospect #{i}" for i in range(1,11)]
    partners = [f"{icp} Partner #{i}" for i in range(1,11)]
    brief = OfferBrief(
        ICP=icp,
        Pain="Wasted cycles, no pipeline consistency.",
        Promise="Booked calls in 7 days via micro-campaigns.",
        Proof="Internal sprints + reference pilots.",
        Price="Pilot $2k, Month-to-month $5k.",
        Path="Book a 20-min fit call."
    )
    scripts = {"email":"<value-first email>", "dm":"<short DM>", "intro":"<ask for warm intro>"}
    exps = [
        Experiment(
            name="Warm Intro vs. Cold Email",
            hypothesis="Warm intros 3x reply vs. cold.",
            sample_size=100,
            success_metric="reply_rate >= 8% or 3 meetings",
            variants=[{"subject":"Quick idea for your pipeline","body":"..."},
                      {"subject":"Could we earn 20 min next week?","body":"..."}],
            stop_rule="Stop after 100 sends or 3 meetings."
        )
    ]
    oa = asdict(ObserverArtifact("BizDevMapping","Defined ICP lists and offers.","None",0.7,[]))
    return {"accounts":accounts,"partners":partners,"offer_brief":asdict(brief),"scripts":scripts,"experiments":[asdict(e) for e in exps],"observer":oa}

def auditor(campaign: Dict[str, Any]) -> Dict[str, Any]:
    """Auditor: Kill delusion, protect brand, enforce measurement."""
    # naive EV: if sample_size < 20 or no ICP → fail
    sample = campaign.get("sample_size",0)
    icp = campaign.get("icp","").strip()
    ev_ok = sample >= 20 and len(icp) > 0
    result = "PASS" if ev_ok else "FAIL"
    oa = asdict(ObserverArtifact("Audit","Validated basic EV and guardrails.","Small sample or missing ICP decreases EV.", 0.8 if ev_ok else 0.4, []))
    return {"result":result,"reasons":[] if ev_ok else ["Increase sample to >=20","Specify ICP clearly"],"observer":oa}

def closer(offer_brief: Dict[str, Any], experiments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Closer: Run fast campaigns, book calls, close, create feedback loops."""
    # Simulate sending one variant to 20 prospects
    sends = 20
    replies = max(1, sends//15)   # ~6.7% baseline
    meetings = replies//2
    STORE.incr("sends", sends); STORE.incr("replies", replies); STORE.incr("meetings", meetings)
    memo = f"Sent {sends}, got {replies} replies (~{replies/sends:.1%}), {meetings} meetings. Next: test CTA length."
    oa = asdict(ObserverArtifact("CloserRun","Shipped micro-campaign and captured signal.","Reply rate slightly under 8% target.",0.55,[]))
    return {"sent":sends,"replies":replies,"meetings":meetings,"lessons":memo,"observer":oa}

# ---------- Orchestrator ----------

def daily_cycle(note_from_team: str, icp: str, offer_hint: str) -> Dict[str, Any]:
    """Run the full daily cycle: Coach → BizDev → Auditor → Closer."""
    out = {}
    out["coach"] = coach(note_from_team)
    bd = bizdev(icp, offer_hint)
    out["bizdev"] = bd
    # audit first experiment
    first_exp = bd["experiments"][0]
    audit_payload = {"sample_size": first_exp["sample_size"], "icp": bd["offer_brief"]["ICP"]}
    out["auditor"] = auditor(audit_payload)
    if out["auditor"]["result"] == "PASS":
        out["closer"] = closer(bd["offer_brief"], bd["experiments"])
    else:
        out["closer"] = {"skipped":"Auditor blocked; revise and rerun."}
    out["metrics"] = STORE.metrics
    return out

if __name__ == "__main__":
    # Example run (swap strings to parameterize for Sage or Parallax)
    print("🚀 Running Daily Cycle\n")
    result = daily_cycle(
        note_from_team="We have to build a full case study before anyone will talk to us.",
        icp="AI-native startups",
        offer_hint="Pipeline-in-a-week sprint"
    )
    print(json.dumps(result, indent=2))
