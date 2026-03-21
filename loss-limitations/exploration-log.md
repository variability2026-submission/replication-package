# Exploration Log: Loss Limitation Rules (U.S. Tax Law)

**Status**: Supplementary case study (not a full paper section; referenced in §7)
**Specification sources**: IRS Publication 925, IRC §§465, 469, 704(d)
**Objects**: 6 loss types with different limitation rules
**Attributes**: 6 binary structural predicates

This log records the attribute exploration dialogue for the loss limitation
domain. This case study is referenced in the paper's validity section (§7)
as evidence that exploration can surface objects the analyst initially
overlooked — the key property that distinguishes exploration from batch
extraction.

---

## Formal Context

| Object      | basis | atRsk | pasLm | carry | suspd | pThru |
|-------------|-------|-------|-------|-------|-------|-------|
| partner     | ×     | ×     | ×     | ×     | ×     | ×     |
| scorp       | ×     | ×     | ×     | ×     | ×     | ×     |
| rental-act  |       |       | ×     | ×     | ×     |       |
| rental-pas  |       |       | ×     | ×     | ×     |       |
| sched-c     |       | ×     |       |       |       |       |
| capital     |       |       |       | ×     |       |       |

Attribute key:
- **basis**: basis limitation applies (loss capped at taxpayer's basis)
- **atRsk**: at-risk limitation applies (IRC §465)
- **pasLm**: passive activity limitation applies (IRC §469)
- **carry**: disallowed losses carry forward
- **suspd**: losses can be suspended (preserved until disposition)
- **pThru**: pass-through entity loss (flows to owner's return)

---

## Step 1: Commonalities (closure of ∅)

**Proposed**: ∅ → ?

**Closure computation**: Which attributes do ALL 6 objects share?
- basis: only partner, scorp ✗
- atRsk: partner, scorp, sched-c (not all) ✗
- pasLm: not sched-c, capital ✗
- carry: not sched-c ✗
- suspd: not sched-c, capital ✗
- pThru: only partner, scorp ✗

**Result**: ∅ → ∅ (no commonalities)

**Confirmed**: Loss types in this subdomain share no universal structural
property. Schedule C loss has only at-risk limitation; capital loss has
only carryforward. No single attribute spans all six.

**Interpretation**: No mandatory features at root. This contrasts with
phaseouts (where all objects shared po and grad).

---

## Step 2: Pass-through closure

**Proposed**: {pThru} → ?

**Initial closure**: Which objects have pThru? partner and scorp.
Both have: {basis, atRsk, pasLm, carry, suspd, pThru}

**Initial result**: {pThru} → {basis, atRsk, pasLm, carry, suspd}

### ⚠ EXPLORATION EVENT: Counterexample from specification

**Testing against specification**: Do ALL pass-through losses entail
passive activity limitation?

**Refutation**: A materially participating partner (IRC §469(c)(1))
receives pass-through losses that are subject to basis limitation
(§704(d)) and at-risk limitation (§465), but are NOT passive because
the partner materially participates. Such losses are not subject to
passive activity limitation.

This counterexample — a materially participating partner — was not in the
initial context. Its existence means {pThru} → {pasLm} does not hold in
general.

**Resolution**: The "partner" and "scorp" objects in our context represent
specifically *passive* pass-through losses. The counterexample led us to
be explicit about this boundary. A materially participating partner would
have the attribute profile {basis, atRsk, carry, pThru} (no pasLm, no
suspd).

**Revised result**: {pThru} → {basis, atRsk, carry}

**Confirmed from specification**:
- IRC §704(d): "A partner's distributive share of partnership loss shall
  be allowed only to the extent of the adjusted basis of such partner's
  interest" — basis limitation mandatory for all pass-through.
- IRC §465: at-risk rules apply to all pass-through activities.
- Pub 925: carryforward applies to disallowed pass-through losses.
- Passive limitation depends on participation level — not entailed by
  pass-through status alone.

**This is the instance referenced in §7 where exploration surfaced an
object the initial context had overlooked.**

---

## Step 3: Basis closure

**Proposed**: {basis} → ?

**Closure computation**: Which objects have basis? partner, scorp.
Both also have: atRsk.

**Result**: {basis} → {atRsk} (plus pThru, pasLm, carry, suspd — but
these follow from the specific objects, not from basis alone)

Non-trivial: **{basis} → {atRsk}**

**Confirmed**: IRC §704(d) (basis), §465 (at-risk): within this
subdomain, basis-limited losses are always also at-risk-limited.
The ordering is mandatory — basis is checked first, then at-risk.

**Interpretation**: Co-applicability — basis limitation entails at-risk
limitation. This captures the first link in the "chain of
responsibility" structure.

---

## Step 4: Passive limitation closure

**Proposed**: {pasLm} → ?

**Closure computation**: Which objects have pasLm?
partner, scorp, rental-act, rental-pas.

Shared attributes: {pasLm, carry, suspd}

**Result**: {pasLm} → {carry, suspd}

**Confirmed**:
- Pub 925: "If your passive activity deductions exceed passive activity
  income, the excess (the loss) is not allowed." Disallowed losses are
  suspended and carried forward.
- IRC §469(b): suspended passive activity losses carry forward
  indefinitely until disposition of the entire interest.

**Interpretation**: Passive limitation always entails both carryforward
and suspension. These are mandatory consequences.

---

## Step 5: Suspension closure

**Proposed**: {suspd} → ?

**Closure computation**: Which objects have suspd?
partner, scorp, rental-act, rental-pas.

Same set as pasLm. Shared attributes: {pasLm, carry, suspd}

**Result**: {suspd} → {pasLm, carry}

**Confirmed**: Suspension is a mechanism specific to passive activity
rules (IRC §469(b)). Suspended losses carry forward. Only passive
losses are suspended; other disallowed losses (e.g., at-risk limited)
carry forward but are not "suspended" in the §469 sense.

**Interpretation**: suspd and pasLm are tightly coupled — they co-occur
in all objects.

---

## Step 6: At-risk closure

**Proposed**: {atRsk} → ?

**Closure computation**: Which objects have atRsk?
partner, scorp, sched-c.

Shared attributes: {atRsk} only — sched-c has no other attributes.

**Result**: {atRsk} → ∅ (no new attributes beyond atRsk)

**Confirmed**: At-risk limitation applies to both pass-through entities
and directly-owned businesses (Schedule C). These have very different
profiles otherwise.

---

## Step 7: Carryforward closure

**Proposed**: {carry} → ?

**Closure computation**: Which objects have carry?
partner, scorp, rental-act, rental-pas, capital.

Shared attributes: {carry} only — capital has only carry.

**Result**: {carry} → ∅ (no new attributes beyond carry)

**Confirmed**: Carryforward appears across diverse loss types (passive,
capital) that share no other structural property.

---

## Summary of Implication Basis

| # | Implication | Domain meaning |
|---|-------------|----------------|
| 1 | {pThru} → {basis, atRsk, carry} | Pass-through entails basis + at-risk + carry |
| 2 | {basis} → {atRsk} | Basis limitation entails at-risk (co-applicability) |
| 3 | {pasLm} → {carry, suspd} | Passive limitation entails carry + suspension |
| 4 | {suspd} → {pasLm, carry} | Suspension entails passive + carry |

No commonalities (∅ → ∅). No mutual exclusions.

## Key Exploration Event

The exploration of {pThru} closure is the critical step. The initial
context listed only passive pass-through losses (partner, scorp).
Proposing {pThru} → {pasLm} led the analyst to test: "Are ALL
pass-through losses passive?" The specification refutes this —
materially participating partners have pass-through losses that are
NOT passive. This counterexample forced the analyst to sharpen the
object definitions before continuing.

Batch extraction from the initial context would have accepted
{pThru} → {pasLm, suspd} as valid — an implication that does not hold
for the domain.

## Translation to Feature Model

- No commonalities → no mandatory root features
- {basis} → {atRsk} → cross-tree constraint (BasisLimited requires AtRiskLimited)
- {pasLm} ↔ {suspd} (mutual entailment via carry) → tightly coupled features
- Three optional limitation gates at root: Basis, AtRisk, Passive

## Variability Topology

Ordered optional gates with co-applicability constraint →
Chain of Responsibility variation structure.
