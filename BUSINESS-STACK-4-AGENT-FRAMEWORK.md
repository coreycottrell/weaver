# The Minimal Business Stack (4 agents, one brain)

**Purpose**: Snap limiting statements in half and turn vague motion into pipeline, cash, and signal.

**Target**: Sage (Greg) and Parallax (Russell) with the same bones, parameterized per person/civ.

---

## 1) Business Coach (Mindset → Strategy)

**Purpose:** Catch limiting statements in-flight, reframe, and translate into 1–3 tangible tests.

**When to invoke:** Any time someone says "we can't," "we have to," or "the only way is…"

**Inputs:** Statement, current objective, constraints, 30-min time budget.

**Outputs:** Reframe, 3 testable options, the "smallest next irreversible step," and a 24-hour checkpoint.

**KPIs:** % of limiting statements converted into tests; % tests completed; cycle time to first external signal.

**Prompt (paste into your agent system):**

> You are Business Coach. Your job: intercept limiting statements and convert them into testable moves.
>
> 1. Label the cognitive move (assumption, false trade-off, fear).
> 2. Produce 3 concrete tests (cost ≤ 30 minutes each).
> 3. Pick one "smallest next irreversible step."
> 4. Schedule a 24-hour check.
> 5. Attach a one-paragraph Observer Artifact (what changed, anomalies, confidence, links).
>    Style: brief, blunt, kind. No pep talks—proof talks.

---

## 2) Business Development (Offer → ICP → Channel → Partners)

**Purpose:** Map opportunities, shape offers, assemble partner shortlists, and set up intros.

**When to invoke:** Weekly planning, new product/offer idea, or dead pipeline.

**Inputs:** Target ICP, draft offer, top channel(s), partnership criteria.

**Outputs:** 10-account/10-partner shortlist, one-page offer brief, first-contact script, 3 outreach experiments.

**KPIs:** # qualified convos/week; partner-response rate; time-to-first-pilot.

**Prompt:**

> You are BizDev. Deliver: (a) 10-account target list and 10-partner shortlist with why-now; (b) one-page offer brief (problem, promise, proof, price, path); (c) 3 outreach experiments (email, DM, warm-intro) with measurable success criteria; (d) 7-day pipeline plan and daily micro-commitments.
> Optimize for speed to first proof, not polish.

---

## 3) Sales & Marketing "Closer" (Intensity → Experiments → Revenue)

**Purpose:** Run fast campaigns, book calls, close, and create feedback loops.

**When to invoke:** Daily. This one keeps score.

**Inputs:** Offer brief, ICP, channels, calendar availability, compliance/brand guardrails.

**Outputs:** Live campaigns, booked calls, closed deals, and a daily "Lessons That Sell" memo.

**KPIs:** Replies/100 sends, meetings booked/week, close rate, CAC payback, $ closed.

**Prompt:**

> You are Closer. Your job is to turn offers into booked calls and revenue with taste and consent.
>
> * Draft and ship 2–3 micro-campaigns/day (A/B subject, A/B CTA).
> * Keep logs: sent, delivered, replies, bookings, reasoning.
> * Write daily "Lessons That Sell" (what beat what, why, next tests).
>   Guardrails: zero spam, tight ICP, opt-out honored, value-first touch.

---

## 4) Auditor (Reality-Checker)

**Purpose:** Kill delusion, protect brand, enforce measurement.

**When to invoke:** Before any outbound batch (>20 messages) or new claim.

**Inputs:** Campaign draft, metrics.

**Outputs:** Pass/Fail with reasons, redlines, risk flags, and an "If you must ship" mitigation plan.

**KPIs:** % interventions that prevent obvious waste; false positive rate kept low.

**Prompt:**

> You are Auditor. Verify evidence, check compliance/brand, compute expected value.
>
> * If EV<0 or risk>reward, block and propose a smaller, safer test.
> * Attach one-paragraph Observer Artifact with confidence and links.

---

# Daily & Weekly Cadence (short, sharp)

**Daily (15–20 min total):**

1. **Coach (5 min):** Sweep chat for limiting statements; produce 1 smallest next step.
2. **Closer (10 min):** Launch two micro-campaigns; book calls; log metrics.
3. **Auditor (5 min):** Spot-check anything that looks "spray and pray."

**Weekly (45–60 min):**

* **BizDev:** 10 accounts + 10 partners; refreshed offer brief.
* **Closer:** Pipeline review, win/loss notes, next 5 experiments.
* **Auditor:** Report on where we lied to ourselves and how to stop.
* **Coach:** Meta-review of beliefs that changed vs. stuck.

---

# "Limiting Belief Interceptor" (use anywhere)

**Trigger rule (regex-ish):**

* Phrases matching: `we (can|can't|must|have to)`, `the only way`, `no one will`, `we need X before Y`, `not possible until`, `it's too (late|early|crowded|expensive)`.

**Challenge frame (Coach uses automatically):**

* Name the belief → Show counterexample → Create 3 tests (≤30 min each) → Pick one now → Calendar a 24-hr check.

---

# Shared Artifacts (copy/paste templates)

## 1) Observer Artifact (one paragraph)

```
ObserverArtifact:
  task: "<name>"
  change_since_last: "<what updated in plan or belief>"
  anomalies: "<anything surprising>"
  confidence: 0.0-1.0
  evidence_links: ["<url-or-note>"]
```

## 2) Offer Brief (one pager)

```
OfferBrief:
  ICP: "<who>"
  Pain: "<top-2 pains in their words>"
  Promise: "<clear outcome with timeframe>"
  Proof: "<case, demo, math>"
  Price: "<simple tier>"
  Path: "<next step: book call | pilot>"
```

## 3) Outreach Experiment (trackable)

```
Experiment:
  name: "<channel + hook>"
  hypothesis: "<why this should work>"
  sample_size: 100
  success_metric: "reply_rate >= 8% OR 3 meetings"
  variants:
    - subject: "<A>"
      body: "<copy>"
    - subject: "<B>"
      body: "<copy>"
  stop_rule: "<when to stop/iterate>"
```

---

# Ready-to-run skeleton (works locally, no APIs)

This is a tiny orchestrator you can run today. It doesn't call external models—rather, it enforces the **flows and artifacts**. Swap stubs with your LLM calls when you wire into Sage/Parallax.

```python
# agents_stack.py
# A minimal, working skeleton that enforces flows, artifacts, and guardrails.
# Replace `generate()` stubs with your LLM calls. Everything else runs now.

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
    if LIMIT_RE.search(statement):
        return intercept_limiting(statement)
    else:
        return {"note":"No limiting statement detected."}

def bizdev(icp: str, offer_hint: str) -> Dict[str, Any]:
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
    # naive EV: if sample_size < 20 or no ICP → fail
    sample = campaign.get("sample_size",0)
    icp = campaign.get("icp","").strip()
    ev_ok = sample >= 20 and len(icp) > 0
    result = "PASS" if ev_ok else "FAIL"
    oa = asdict(ObserverArtifact("Audit","Validated basic EV and guardrails.","Small sample or missing ICP decreases EV.", 0.8 if ev_ok else 0.4, []))
    return {"result":result,"reasons":[] if ev_ok else ["Increase sample to >=20","Specify ICP clearly"],"observer":oa}

def closer(offer_brief: Dict[str, Any], experiments: List[Dict[str, Any]]) -> Dict[str, Any]:
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
    result = daily_cycle(
        note_from_team="We have to build a full case study before anyone will talk to us.",
        icp="AI-native startups",
        offer_hint="Pipeline-in-a-week sprint"
    )
    print(json.dumps(result, indent=2))
```

**To run:** `python agents_stack.py`

You'll see the **Coach** catch the limiting belief, **BizDev** produce lists and an offer brief, **Auditor** gatekeep, and **Closer** ship a micro-campaign with logged "Lessons That Sell."

**To adapt for Sage vs Parallax:** Feed different `icp` and `offer_hint` strings (or wire to your civ memory).

---

# How this helps Greg & Russell specifically

**Greg/Sage:** Wire the **Coach** to auto-scan Greg's planning notes. Every "we need X before Y" triggers the 3-test sequence and a 24-hr check. Pattern-breaker by design.

**Russell/Parallax:** Give **BizDev** a weekly 10×10 mandate (10 accounts + 10 partners). No slides until 3 conversations are booked. **Closer** ships daily micro-campaigns; **Auditor** blocks vibe-killing spray-and-pray.

---

# Red Team (how this fails & fixes)

**Agent soup:** Too many cooks, lost ownership.
* *Fix:* One owner per week. Auditor enforces decision logs.

**Vanity metrics:** Sends go up, bookings don't.
* *Fix:* Golden metric = **meetings booked**. Everything else is a leading indicator, not a victory lap.

**Spam risk:** Shortcuts torch the brand.
* *Fix:* Auditor blocks any batch without clear ICP, value-first copy, and opt-outs.

**Over-theorizing:** Endless reframes, no calls.
* *Fix:* Coach's output **must include** a smallest next irreversible step today.

**Wrong ICP:** Great message, wrong people.
* *Fix:* BizDev refreshes ICP weekly using the 3-call rule (don't lock until you've spoken to 3).

---

# Immediate next moves (7-day sprint)

1. Pick **one** ICP and **one** offer per civ (Sage, Parallax).
2. Run the script once daily for each civ (or wire to your agent loop).
3. Ship 2 micro-campaigns/day via **Closer**; book at least **3 meetings** per civ this week.
4. Enforce **Auditor** before any batch ≥20 sends.
5. End of week: keep the winning variant, kill the rest, and raise the bar.

---

## Summary

You're not wrong that they need "intensity," but intensity without guardrails turns into noise. This stack is a **pressure washer with a stencil**: force applied, shape preserved.

Ready to wire it into Sage and Parallax now—or I can tailor ICPs, offers, and first campaign copy for each and set the dials to "ship."
