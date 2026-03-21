# Exploration Log: Phaseout Mechanisms (U.S. Tax Law)

**Case study**: §4 of the paper
**Specification sources**: IRS Publications 596, 970, 590-A, Schedule 8812 Instructions
**Objects**: 8 tax benefits with phaseout behavior
**Attributes**: 8 binary structural predicates

This log records the attribute exploration dialogue. Each step shows the
implication proposed by the algorithm, the analyst's decision (confirmed or
refuted with counterexample), and the specification text that grounds it.

---

## Formal Context

| Object | po | pi | grad | MAGI | AGI | ref | pRef | nRef |
|--------|----|----|------|------|-----|-----|------|------|
| EITC         | × | × | × |   | × | × |   |   |
| CTC          | × |   | × | × |   |   | × |   |
| AOTC         | × |   | × | × |   |   | × |   |
| LifetimeLC   | × |   | × | × |   |   |   | × |
| StudentLn    | × |   | × | × |   |   |   |   |
| IRA          | × |   | × | × |   |   |   |   |
| RothIRA      | × |   | × | × |   |   |   |   |
| RentalAllow  | × |   | × | × |   |   |   |   |

Attribute key:
- **po**: has phaseout (benefit reduces as income rises)
- **pi**: has phase-in (benefit increases as income rises before plateau)
- **grad**: gradual reduction over an income range
- **MAGI**: uses Modified Adjusted Gross Income as income measure
- **AGI**: uses Adjusted Gross Income as income measure
- **ref**: fully refundable (excess beyond tax liability is refunded)
- **pRef**: partially refundable
- **nRef**: nonrefundable (limited to tax liability)

---

## Step 1: Commonalities (closure of ∅)

**Proposed**: ∅ → ?

**Closure computation**: Which attributes do ALL 8 objects share?
- po: all 8 have it ✓
- pi: only EITC ✗
- grad: all 8 have it ✓
- MAGI: EITC uses AGI, not MAGI ✗
- AGI: only EITC ✗
- ref: only EITC ✗
- pRef: only CTC, AOTC ✗
- nRef: only LifetimeLC ✗

**Result**: ∅ → {po, grad}

**Confirmed**: All phaseout mechanisms in the chosen subdomain share these
two structural properties.
- Pub 596 (EITC): "The credit decreases... as your earned income increases"
- Schedule 8812 Instructions (CTC): "modified AGI above... reduced by $50
  for each $1,000"
- Pub 970 (AOTC, LLC): "credit is reduced... if your modified AGI is between"
- Pub 590-A (IRA, Roth): "reduced... if your modified AGI is between"
- Pub 970 (Student Loan): "amount... is gradually reduced"
- Pub 925 (Rental): "reduced by 50% of the amount... over $100,000"

**Interpretation**: po and grad are mandatory features at root.

---

## Step 2: Phase-in closure

**Proposed**: {pi} → ?

**Closure computation**: Which objects have pi? Only EITC.
EITC's full attribute set: {po, pi, grad, AGI, ref}

**Result**: {pi} → {po, grad, AGI, ref}

Since po and grad are already commonalities, the non-trivial new implication is:

**{pi} → {ref, AGI}**

**Confirmed**:
- Pub 596, "Earned Income Credit (EIC)": EITC phases in with earned income
  (unique among these benefits), is fully refundable, and uses AGI/earned
  income (whichever is greater) as the income measure.
- No other phaseout mechanism in this subdomain has a phase-in region.

**Interpretation**: Phase-in entails full refundability and AGI-based
measurement. In the feature model, PhaseIn is an optional child of AGI-based,
with Refundable as a mandatory child of PhaseIn.

---

## Step 3: MAGI closure

**Proposed**: {MAGI} → ?

**Closure computation**: Which objects have MAGI?
CTC, AOTC, LifetimeLC, StudentLn, IRA, RothIRA, RentalAllow (7 objects).

Shared attributes across all 7: {po, grad, MAGI}

**Result**: {MAGI} → {po, grad} (but these are already commonalities)

**No new implication beyond commonalities.**

**Confirmed**: Each of the 7 MAGI-based benefits defines MAGI as its income
measure, but they differ in refundability and other properties.

---

## Step 4: AGI closure

**Proposed**: {AGI} → ?

**Closure computation**: Which objects have AGI? Only EITC.
EITC's attributes: {po, pi, grad, AGI, ref}

**Result**: {AGI} → {po, pi, grad, ref}

Non-trivial: {AGI} → {pi, ref}

**Confirmed**: Within this subdomain, the only AGI-based benefit (EITC) is
also the only one with phase-in and the only fully refundable one.
- Pub 596: EITC uses "adjusted gross income" (or earned income if greater),
  has a phase-in range, and is fully refundable.

**Note**: This implication is context-specific — it holds because EITC is the
sole AGI-based benefit in this subdomain. A broader subdomain including
Saver's Credit (AGI-based, nonrefundable, no phase-in) would refute it.

---

## Step 5: Partial refundability closure

**Proposed**: {pRef} → ?

**Closure computation**: Which objects have pRef? CTC and AOTC.
Shared attributes: {po, grad, MAGI, pRef}

**Result**: {pRef} → {po, grad, MAGI}

Non-trivial: **{pRef} → {MAGI}**

**Confirmed**:
- Schedule 8812 Instructions (CTC): "Enter the amount from... modified
  adjusted gross income" — partially refundable, MAGI-based.
- Pub 970 (AOTC): "modified adjusted gross income" — 40% refundable portion,
  MAGI-based.

**Interpretation**: All partially refundable benefits use MAGI. In the feature
model, PartialRef is an optional modifier under MAGI-based.

---

## Step 6: Nonrefundable closure

**Proposed**: {nRef} → ?

**Closure computation**: Which objects have nRef? Only LifetimeLC.
LifetimeLC's attributes: {po, grad, MAGI, nRef}

**Result**: {nRef} → {po, grad, MAGI}

Non-trivial: {nRef} → {MAGI}

**Confirmed**: Pub 970 (Lifetime Learning Credit): uses MAGI, nonrefundable.

**Note**: Context-specific — a broader subdomain including Saver's Credit
(nonrefundable, AGI-based) would refute {nRef} → {MAGI}.

---

## Step 7: Observed disjointness — AGI ⊗ MAGI

**Check**: Does any object have both AGI and MAGI?

Scanning the context: No. EITC has AGI; the other 7 have MAGI. No overlap.

**Verified against specification**: Each IRS publication defines exactly one
income measure per benefit. There is no benefit that uses both AGI and MAGI
for phaseout computation. The distinction is normative — the specification
defines which measure applies.

**Interpretation**: AGI and MAGI form an XOR group (alternative) in the
feature model. This is the primary variability dimension.

---

## Step 8: Observed disjointness — refundability attributes

**Check**: Pairwise disjointness of ref, pRef, nRef?

- ref ⊗ pRef: EITC has ref; CTC/AOTC have pRef. No overlap. ✓
- ref ⊗ nRef: EITC has ref; LifetimeLC has nRef. No overlap. ✓
- pRef ⊗ nRef: CTC/AOTC have pRef; LifetimeLC has nRef. No overlap. ✓

**Note**: StudentLn, IRA, RothIRA, RentalAllow have NONE of ref/pRef/nRef.
These are deductions, not credits — refundability does not apply.
(See paper footnote: "Deductions have no refundability attribute.")

**Interpretation**: For credits, refundability is a three-way partition
(ref | pRef | nRef). For deductions, the dimension is absent. In the feature
model, refundability attributes are optional modifiers.

---

## Summary of Implication Basis

| # | Implication | Domain meaning |
|---|-------------|----------------|
| 1 | ∅ → {po, grad} | All phaseouts are gradual reductions (commonalities) |
| 2 | {pi} → {ref, AGI} | Phase-in entails refundable + AGI-based (EITC) |
| 3 | {pRef} → {MAGI} | Partial refundability entails MAGI-based |
| 4 | {nRef} → {MAGI} | Nonrefundable entails MAGI-based (in this subdomain) |
| 5 | AGI ⊗ MAGI | Mutually exclusive income measures (XOR) |
| 6 | ref ⊗ pRef ⊗ nRef | Mutually exclusive refundability (where applicable) |

## Translation to Feature Model

- Implications 1 → mandatory root features (po, grad)
- Implication 5 → XOR group: AGI-based vs MAGI-based
- Implication 2 → PhaseIn optional under AGI; Refundable mandatory under PhaseIn
- Implications 3–4 → PartialRef, NonRef optional under MAGI-based
- Implication 6 → confirms partition, no cross-tree constraint needed

See Figure 2 in the paper.

## Variability Topology

Strong commonalities at root + XOR income measure + optional refundability
modifiers → Decorator variation structure.
