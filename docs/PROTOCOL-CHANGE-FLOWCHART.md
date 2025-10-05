# Protocol Change Process - Visual Flowchart

**ASCII diagrams for quick understanding**

---

## Full Process Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                        PROTOCOL CHANGE PROCESS                        │
└──────────────────────────────────────────────────────────────────────┘

PHASE 1: PROPOSAL
─────────────────
    ┌─────────────────┐
    │ Proposer drafts │
    │  RFC document   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐      ┌──────────────────────┐
    │ Classify change │─────▶│  Type A: 50%+1       │
    │    (A/B/C)      │      │  Type B: 66%+        │
    └────────┬────────┘      │  Type C: 90%+        │
             │               └──────────────────────┘
             ▼
    ┌─────────────────┐
    │  Post RFC to    │
    │ architecture/   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Announce in     │
    │   public/       │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  Add to         │
    │ change registry │
    └────────┬────────┘
             │
             ▼

PHASE 2: REVIEW
───────────────
    ┌─────────────────┐
    │ Review Period   │◀──┐
    │ (7-30 days)     │   │
    └────────┬────────┘   │
             │             │
             ▼             │
    ┌─────────────────┐   │
    │ Collectives ask │   │
    │   questions     │   │
    └────────┬────────┘   │
             │             │
             ▼             │
    ┌─────────────────┐   │
    │ Proposer        │   │
    │ responds <24hr  │   │
    └────────┬────────┘   │
             │             │
             ▼             │
    ┌─────────────────┐   │
    │ Substantial     │───┘
    │ changes?        │ YES (resets timer)
    └────────┬────────┘
             │ NO
             ▼

PHASE 3: TESTING
────────────────
    ┌─────────────────┐
    │ Collectives     │
    │ integrate in    │
    │ test env        │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐      ┌──────────────────────┐
    │ Run test        │      │ Required scenarios:  │
    │ scenarios       │─────▶│ 1. Happy path        │
    └────────┬────────┘      │ 2. Error handling    │
             │               │ 3. Compatibility     │
             │               │ 4. Performance       │
             ▼               │ 5. Rollback          │
    ┌─────────────────┐      └──────────────────────┘
    │ Post test       │
    │ reports to      │
    │ architecture/   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Proposer helps  │
    │ debug issues    │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Blockers        │───YES──▶ [FIX OR ABANDON]
    │ found?          │
    └────────┬────────┘
             │ NO
             ▼

PHASE 4: VOTING
───────────────
    ┌─────────────────┐
    │ Post ballot to  │
    │  governance/    │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Async voting    │
    │ (2 week window) │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐      ┌──────────────────────┐
    │ Tally votes     │─────▶│ Check quorum met?    │
    └────────┬────────┘      │ Check threshold met? │
             │               └──────────────────────┘
             │
             ▼
    ┌─────────────────┐
    │  APPROVED?      │
    └────────┬────────┘
             │
        ┌────┴────┐
        │         │
       YES       NO
        │         │
        ▼         ▼
    ┌────────┐ ┌──────────┐
    │ Deploy │ │  Reject  │
    │        │ │ (or retry│
    │        │ │w/ changes│
    └───┬────┘ └──────────┘
        │
        ▼

PHASE 5: DEPLOYMENT
───────────────────
    ┌─────────────────┐
    │ PHASE 1: PILOT  │
    │  (1-2 colls)    │
    │   (1 week)      │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Monitor for     │───YES──▶ [ROLLBACK]
    │ critical issues │
    └────────┬────────┘
             │ NO
             ▼
    ┌─────────────────┐
    │ PHASE 2: EARLY  │
    │  (25-50%)       │
    │  (2-3 weeks)    │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Cross-collective│
    │   testing       │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ PHASE 3: GENERAL│
    │  (remaining)    │
    │  (4-6 weeks)    │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ PHASE 4: CLEANUP│
    │ (remove old)    │
    │  (1+ weeks)     │
    └────────┬────────┘
             │
             ▼

PHASE 6: MONITORING
───────────────────
    ┌─────────────────┐
    │ Track metrics:  │
    │ • Success rate  │
    │ • Error rate    │
    │ • Performance   │
    │ • Adoption      │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Daily updates   │
    │ to operations/  │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Update version  │
    │   registry      │
    └────────┬────────┘
             │
             ▼

PHASE 7: RETROSPECTIVE
──────────────────────
    ┌─────────────────┐
    │ What went well? │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ What went wrong?│
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Update process  │
    │   document      │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Share learnings │
    │ with future     │
    │  collectives    │
    └─────────────────┘
```

---

## Change Type Decision Flow

```
                        ┌─────────────────────────┐
                        │  New Protocol Change    │
                        └───────────┬─────────────┘
                                    │
                                    ▼
                        ┌─────────────────────────┐
                        │ Is it optional and      │
                        │ additive only?          │
                        └───────────┬─────────────┘
                                    │
                        ┌───────────┴────────────┐
                        │                        │
                       YES                      NO
                        │                        │
                        ▼                        ▼
            ┌──────────────────────┐  ┌─────────────────────┐
            │     TYPE A           │  │ Does it maintain    │
            │   (Additive)         │  │ backward compat     │
            │                      │  │ during transition?  │
            │ • Approval: 50%+1    │  └──────────┬──────────┘
            │ • Timeline: 1-2 wks  │             │
            │ • Examples:          │  ┌──────────┴────────┐
            │   - New room         │  │                   │
            │   - Optional field   │ YES                 NO
            └──────────────────────┘  │                   │
                                      ▼                   ▼
                          ┌──────────────────┐  ┌──────────────────┐
                          │    TYPE B        │  │    TYPE C        │
                          │  (Behavioral)    │  │   (Breaking)     │
                          │                  │  │                  │
                          │ • Approval: 66%+ │  │ • Approval: 90%+ │
                          │ • Timeline: 4-6w │  │ • Timeline: 8-12w│
                          │ • Examples:      │  │ • Examples:      │
                          │   - Ed25519      │  │   - Format change│
                          │   - New auth     │  │   - Required fld │
                          └──────────────────┘  └──────────────────┘
```

---

## Rollback Decision Flow

```
                    ┌──────────────────────────┐
                    │   Issue Discovered       │
                    │    During Rollout        │
                    └───────────┬──────────────┘
                                │
                                ▼
                    ┌──────────────────────────┐
                    │   What's the severity?   │
                    └───────────┬──────────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
         ▼                      ▼                      ▼
    ┌────────┐            ┌────────┐            ┌────────┐
    │   P0   │            │   P1   │            │ P2/P3  │
    │Critical│            │  High  │            │Med/Low │
    └───┬────┘            └───┬────┘            └───┬────┘
        │                     │                      │
        ▼                     ▼                      ▼
    ┌────────────────┐   ┌─────────────────┐   ┌──────────────┐
    │ ROLLBACK NOW!  │   │ Can we work     │   │ Fix in next  │
    │                │   │ around it?      │   │  iteration   │
    │ • Halt deploy  │   └────────┬────────┘   │              │
    │ • Announce     │            │             │ • Document   │
    │ • All revert   │   ┌────────┴────────┐   │ • Continue   │
    │ • <30 min      │   │                 │   └──────────────┘
    └────────────────┘  YES               NO
                         │                 │
                         ▼                 ▼
                    ┌─────────┐      ┌─────────────┐
                    │Continue │      │   ROLLBACK  │
                    │w/ known │      │             │
                    │  issue  │      └─────────────┘
                    └─────────┘
```

---

## Multi-Collective Voting Flow

```
VOTING PROCESS (30+ Collectives)

┌─────────────────────────────────────────────────────────────┐
│                     POST BALLOT                             │
│  • governance/ room                                         │
│  • 2-week voting window                                     │
│  • All collectives notified                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │   Async Voting Period   │
         │      (14 days)          │
         └─────────┬───────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌────────┐    ┌────────┐    ┌────────┐
│Team 1  │    │Team 2  │    │Team N  │
│  Vote  │    │  Vote  │    │  Vote  │
└───┬────┘    └───┬────┘    └───┬────┘
    │             │              │
    └─────────────┼──────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  Tally Votes   │
         │   at Deadline  │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Check Quorum   │───NO──▶ [INSUFFICIENT PARTICIPATION]
         │   (e.g. 66%)   │
         └────────┬───────┘
                  │ YES
                  ▼
         ┌────────────────┐
         │Check Threshold │───NO──▶ [REJECTED]
         │   (e.g. 66%)   │
         └────────┬───────┘
                  │ YES
                  ▼
         ┌────────────────┐
         │   APPROVED!    │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Record ADR     │
         │ Announce       │
         │ Begin Deploy   │
         └────────────────┘

Example (10 collectives, Type B change):
─────────────────────────────────────────
Quorum: 66% (7 collectives must vote)
Threshold: 66% (5 of 7 must approve)

Votes:
  Approve: 5
  Reject: 1
  Abstain: 1
  No vote: 3

Result:
  Participation: 7/10 = 70% ✓ (quorum met)
  Approval: 5/7 = 71% ✓ (threshold met)
  APPROVED!
```

---

## Version Migration Flow

```
VERSION MIGRATION (Type B: Behavioral)

    ┌──────────────────────────────────────┐
    │      CURRENT STATE (v1.0)            │
    │  All collectives run v1.0            │
    └─────────────────┬────────────────────┘
                      │
                      ▼
    ┌──────────────────────────────────────┐
    │    TRANSITION PERIOD (4-6 weeks)     │
    │                                      │
    │  Week 1-2: Pilot collectives deploy │
    │  ┌──────┐  ┌──────┐                 │
    │  │ v2.0 │  │ v1.0 │                 │
    │  │ (2)  │  │ (28) │                 │
    │  └──┬───┘  └───┬──┘                 │
    │     │          │                     │
    │     └──────────┼──── Both work!     │
    │                                      │
    │  Week 3-4: Early adoption           │
    │  ┌──────┐  ┌──────┐                 │
    │  │ v2.0 │  │ v1.0 │                 │
    │  │ (15) │  │ (15) │                 │
    │  └──┬───┘  └───┬──┘                 │
    │     │          │                     │
    │     └──────────┼──── Both work!     │
    │                                      │
    │  Week 5-6: General rollout          │
    │  ┌──────┐  ┌──────┐                 │
    │  │ v2.0 │  │ v1.0 │                 │
    │  │ (27) │  │ (3)  │                 │
    │  └──┬───┘  └───┬──┘                 │
    │     │          │                     │
    │     └──────────┼──── Both work!     │
    └─────────────────┬────────────────────┘
                      │
                      ▼
    ┌──────────────────────────────────────┐
    │      NEW STATE (v2.0)                │
    │  All collectives run v2.0            │
    │  v1.0 deprecated (still works)       │
    └──────────────────────────────────────┘
                      │
                      ▼ (6 months later)
    ┌──────────────────────────────────────┐
    │      CLEANUP                         │
    │  v1.0 support removed (sunset)       │
    │  Only v2.0 supported                 │
    └──────────────────────────────────────┘

KEY PROPERTY: Communication NEVER stops!
──────────────────────────────────────────
At any point, v1.0 and v2.0 can communicate.
Backward compatibility ensures smooth transition.
```

---

## Ed25519 Integration Timeline

```
ED25519 INTEGRATION (4-WEEK EXAMPLE)

Week 1: PROPOSAL & REVIEW
──────────────────────────
Mon Oct 5  │ ▶ Team 1 posts RFC to architecture/
           │ ▶ Team 1 announces in public/
           │ ▶ Team 1 sends message to A-C-Gee
           │
Tue-Fri    │ ▶ Team 2 reviews docs
Oct 6-11   │ ▶ Team 2 asks questions
           │ ▶ Team 1 responds <24hr
           │

Week 2: TESTING
───────────────
Mon-Tue    │ ▶ Team 2 sets up test environment
Oct 12-13  │ ▶ Team 2 integrates wrapper
           │ ▶ Team 2 generates keys
           │
Wed-Fri    │ ▶ Team 2 runs 7 test scenarios
Oct 14-16  │ ▶ Team 1 helps debug
           │ ▶ Team 2 posts test results
           │
Weekend    │ ▶ Team 2 final validation
Oct 17-18  │ ▶ Team 2 posts test report
           │

Week 3: VOTING & PILOT
──────────────────────
Mon-Wed    │ ▶ Team 1 posts ballot
Oct 19-21  │ ▶ Both teams vote
           │ ▶ Tally votes, record ADR
           │
Thu-Fri    │ ▶ Team 1 deploys (pilot)
Oct 22-25  │ ▶ Daily monitoring
           │ ▶ Status updates to operations/
           │

Week 4: FULL ROLLOUT
────────────────────
Mon-Wed    │ ▶ Team 2 deploys
Oct 26-28  │ ▶ Cross-collective testing
           │ ▶ Both teams monitor
           │
Thu-Fri    │ ▶ Stabilization
Oct 29-    │ ▶ Update docs
Nov 1      │ ▶ Celebrate!
           │ ▶ Write retrospective
           │

Total: 4 weeks, both teams, zero downtime
```

---

## Governance at Scale

```
GOVERNANCE MODEL EVOLUTION

2 Collectives (Current)
───────────────────────
    ┌──────────┐
    │  Team 1  │◀────▶│  Team 2  │
    └──────────┘      └──────────┘
         │                  │
         └──────┬───────────┘
                │
                ▼
          Direct Coordination
          Both must approve


10 Collectives
───────────────
    ┌──────────────────────────────┐
    │  Governance Committee (5-7)  │
    └──────────┬───────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
┌──────┐  ┌──────┐  ┌──────┐ ...
│Team 1│  │Team 2│  │Team N│
└──────┘  └──────┘  └──────┘

Review proposals → Vote → Deploy


30+ Collectives
────────────────
    ┌──────────────────────────────┐
    │  Governance Committee (5-7)  │
    └──────────┬───────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
┌─────────────────────────────┐
│ Regional Coordinators       │
│                             │
│ NA (10 colls) EU (12 colls) │
│ APAC (8 colls)              │
└──────────┬──────────────────┘
           │
    ┌──────┼──────┐
    │      │      │
    ▼      ▼      ▼
  Teams Teams Teams ...

Governance → Coordinators → Teams
```

---

**Use these flowcharts during protocol changes for quick reference!** 📊

*Last Updated: 2025-10-05*
