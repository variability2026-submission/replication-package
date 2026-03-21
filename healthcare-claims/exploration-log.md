# Exploration Log: Healthcare Claims (HIPAA EDI 837)

**Case study**: §6 of the paper (Case Study 3)
**Specification sources**: CMS Medicare Claims Processing Manual;
  ASC X12 837 Implementation Guides (837P, 837I, 837D)
**Objects**: 6 healthcare claim types
**Attributes**: 8 binary structural predicates

This log records the attribute exploration dialogue. Each step shows the
implication proposed, the analyst's decision, and the specification text
that grounds it.

---

## Formal Context

| Object | 837P | 837I | 837D | facility | admit | refer | proc | tooth |
|--------|------|------|------|----------|-------|-------|------|-------|
| office    | × |   |   |   |   |   | × |   |
| surgery   | × |   |   |   |   | × | × |   |
| inpatient |   | × |   | × | × | × | × |   |
| emergency |   | × |   | × |   |   | × |   |
| dental    |   |   | × |   |   |   | × | × |
| dme       | × |   |   |   |   |   |   |   |

Attribute key:
- **837P**: Professional claim format (X12 837P Implementation Guide)
- **837I**: Institutional claim format (X12 837I Implementation Guide)
- **837D**: Dental claim format (X12 837D Implementation Guide)
- **facility**: Facility NPI required (CMS billing requirements)
- **admit**: Admission/discharge dates required (hospital billing rules)
- **refer**: Referring/attending provider required (Medicare referral rules)
- **proc**: Procedure code required — CPT, ICD-10-PCS, or CDT depending
  on format (HIPAA code set requirements)
- **tooth**: Tooth identification required (ADA dental coding standards)

---

## Suitability Confirmation

The HIPAA 837 transaction standard satisfies the three suitability properties:
- **Authoritative**: Federal regulation under HIPAA Administrative
  Simplification — defines valid claim structures by prescription.
- **Enumerable**: The chosen subdomain contains 6 representative claim types
  spanning the three EDI formats.
- **Structurally determinate**: Which fields are required for which claim
  types is specified precisely in the X12 Implementation Guides and CMS
  manual. Computational variability (diagnosis coding, fee schedules) is
  at terminal features.

---

## Step 1: Commonalities (closure of ∅)

**Proposed**: ∅ → {proc}?

This is the most natural candidate — do all claim types require a procedure
code?

**Closure computation**: Which objects have proc?
office ✓, surgery ✓, inpatient ✓, emergency ✓, dental ✓, dme ✗

**Refuted**: DME (durable medical equipment) claims use HCPCS Level II supply
codes rather than procedure codes. DME is billed on 837P format but does not
require a CPT/CDT/ICD-10-PCS procedure code.

**Counterexample**: dme — has {837P} only.

**Result**: ∅'' = ∅ (no universal commonalities)

**Interpretation**: Unlike phaseouts (where all objects share po and grad),
healthcare claims have no attribute common to all types. This structural
absence is significant — it means the feature model has no mandatory root
attributes.

---

## Step 2: 837I (institutional format) closure

**Proposed**: {837I} → ?

**Closure computation**: Which objects have 837I? inpatient and emergency.
Shared attributes: {837I, facility, proc}

**Result**: {837I} → {facility, proc}

**Confirmed**:
- X12 837I Implementation Guide: Institutional claims require the billing
  facility's NPI in Loop 2010AA (Billing Provider).
- CMS Medicare Claims Processing Manual: Facility-based claims require
  facility identification and procedure reporting.
- Both inpatient and emergency require facility NPI and procedure codes.

**Interpretation**: All institutional claims require facility identification
and procedure codes. In the feature model, facility and proc are mandatory
children of 837I.

---

## Step 3: Admission closure

**Proposed**: {admit} → ?

**Closure computation**: Which objects have admit? Only inpatient.
inpatient's full attribute set: {837I, facility, admit, refer, proc}

**Result**: {admit} → {837I, facility, refer, proc}

**Confirmed**:
- CMS Medicare Claims Processing Manual, Chapter 3 (Inpatient Hospital
  Billing): Inpatient claims require admission date, discharge date,
  attending/referring physician, facility NPI, and procedure codes.
- X12 837I: Admission dates appear in Loop 2300 CLM segment; referring
  provider in Loop 2310A.

**Interpretation**: Admission dates entail the full institutional claim
context. This is the richest implication in the healthcare domain — selecting
admit forces 837I format, facility, referring provider, and procedure codes.
In the feature model, this becomes a cross-tree constraint: admit → refer.

---

## Step 4: 837D (dental format) closure

**Proposed**: {837D} → ?

**Closure computation**: Which objects have 837D? Only dental.
dental's full attribute set: {837D, proc, tooth}

**Result**: {837D} → {proc, tooth}

**Confirmed**:
- X12 837D Implementation Guide: Dental claims require CDT procedure codes
  (Loop 2400 SV3 segment) and tooth identification (Loop 2400 TOO segment).
- ADA dental coding standards: "what was done" (procedure) and "where"
  (tooth number/surface) are both required.

**Interpretation**: Dental format requires both procedure code and tooth
identification — they are coupled. In the feature model, proc and tooth
are mandatory children of 837D.

---

## Step 5: Tooth closure

**Proposed**: {tooth} → ?

**Closure computation**: Which objects have tooth? Only dental.
dental's full attribute set: {837D, proc, tooth}

**Result**: {tooth} → {837D, proc}

**Confirmed**: Tooth identification only appears in dental claims. The
presence of tooth data entails dental format and procedure codes.

**Interpretation**: Confirms the coupling — tooth and 837D are co-dependent.
This is the converse of the {837D} → {tooth} direction.

---

## Step 6: Facility closure

**Proposed**: {facility} → ?

**Closure computation**: Which objects have facility? inpatient and emergency.
Shared attributes: {837I, facility, proc}

**Result**: {facility} → {837I, proc}

**Confirmed**: Within this subdomain, facility NPI appears only on
institutional claims. No professional (837P) or dental (837D) claim requires
facility information — physicians bill for services under their individual
NPI; facilities bill separately on 837I.

**Note**: This implication ({facility} → {837I}) is not explicitly stated in
billing guides as a rule, but emerges structurally from the data. It holds
because the claim types in this subdomain that require facility NPI are
exactly the institutional claim types. It reflects the structural fact that
facility-based billing uses the institutional format.

---

## Step 7: Referring provider closure

**Proposed**: {refer} → ?

**Closure computation**: Which objects have refer? surgery and inpatient.
Shared attributes: {proc, refer}

**Result**: {refer} → {proc}

**Confirmed**:
- CMS Medicare referral requirements: When a referring/attending provider
  is present, the claim also has procedure codes.
- surgery has {837P, proc, refer}; inpatient has {837I, facility, admit,
  refer, proc}. The only shared non-trivial attribute beyond refer is proc.

**Interpretation**: Referral always accompanies procedures — there are no
referral-only claims in this subdomain. In the feature model, this means
refer requires proc (though proc can exist without refer).

---

## Step 8: 837P (professional format) closure

**Proposed**: {837P} → ?

**Closure computation**: Which objects have 837P? office, surgery, dme.
Shared attributes: {837P} only.

**Result**: {837P}'' = {837P} (closed set — no new attributes)

**Confirmed**: Professional claims have no universally required fields beyond
the format itself. office has proc; surgery has proc and refer; dme has
neither. The professional format is the most permissive.

**Interpretation**: 837P children (proc, refer) are both optional. This
contrasts with 837I (facility and proc mandatory) and 837D (proc and tooth
mandatory).

---

## Step 9: Observed disjointness — format attributes

**Check**: Pairwise disjointness of 837P, 837I, 837D?

| Pair | Co-occurrence? |
|------|---------------|
| 837P ⊗ 837I | No object has both ✓ |
| 837P ⊗ 837D | No object has both ✓ |
| 837I ⊗ 837D | No object has both ✓ |

**Verified**: Each claim type uses exactly one format. The X12 Implementation
Guides define three separate transaction sets — a claim is submitted on
exactly one format.

**Interpretation**: The three formats form a strict XOR partition. This is
the primary variability dimension of the feature model.

---

## Step 10: Observed disjointness — cross-format attributes

Several additional disjointness pairs follow from the format partition:

| Pair | Explanation |
|------|-------------|
| 837D ⊗ facility | Dental claims don't require facility NPI |
| 837D ⊗ admit | Dental claims don't have admissions |
| 837D ⊗ refer | Dental claims don't require referrals |
| 837P ⊗ facility | Professional claims don't carry facility |
| 837P ⊗ admit | Professional claims have no admission |
| 837I ⊗ tooth | Institutional claims aren't dental |
| 837P ⊗ tooth | Professional claims aren't dental |
| facility ⊗ tooth | Facility-based and dental are disjoint domains |
| admit ⊗ tooth | Admission and dental are disjoint |
| refer ⊗ tooth | Referral and dental are disjoint |

**Total**: 13 mutual exclusion pairs observed.

These follow from the format partition — since formats are exclusive and
certain attributes are tied to specific formats, cross-format attribute
pairs are automatically exclusive.

---

## Summary of Implication Basis

### Primary implications (5)

| # | Implication | Source | Domain meaning |
|---|-------------|--------|----------------|
| 1 | {837I} → {facility, proc} | X12 837I Guide, CMS Manual | Institutional claims require facility and procedure |
| 2 | {admit} → {837I, facility, refer, proc} | CMS Ch. 3 | Admission entails full institutional context |
| 3 | {837D} → {proc, tooth} | X12 837D Guide, ADA | Dental requires procedure and tooth ID |
| 4 | {tooth} → {837D, proc} | X12 837D Guide | Tooth ID entails dental format |
| 5 | {refer} → {proc} | CMS referral rules | Referral accompanies procedures |

### Additional closures

| Implication | Note |
|-------------|------|
| {facility} → {837I, proc} | Emergent — not explicitly stated in guides |
| {837P}'' = {837P} | No mandatory children for professional format |

### Observed disjointness (13 pairs)

Format attributes partition claims into three exclusive groups. Cross-format
attribute pairs inherit this exclusion.

---

## Translation to Feature Model

- No commonalities → no mandatory root attributes
- Format XOR → top-level alternative group (837P | 837I | 837D)
- {837I} → {facility, proc} → facility, proc mandatory under 837I
- {837D} → {proc, tooth} → proc, tooth mandatory under 837D
- 837P has no mandatory children → proc, refer optional under 837P
- admit optional under 837I; when selected, forces refer (cross-tree)
- refer optional under 837I (independent of admit)

See Figure 5 in the paper.

## Variability Topology

XOR format selection + format-dependent mandatory children → Builder
variation structure. Earlier choices (format) constrain later steps
(which fields become required), requiring stepwise, branch-conditional
construction.
