#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replication: Loss Limitation Rules (U.S. Tax Law) -- Supplementary Case Study

Reproduces the formal context, implications, and feature model derivation
described in the exploration log. This case study is referenced in the paper's
validity section as evidence that exploration can surface overlooked objects.

Sources: IRS Publication 925 (Passive Activity and At-Risk Rules),
         IRC §§465, 469, 704(d).

Usage:  python3 losses_fca.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fca_core import (closure, find_implications, mutual_exclusions,
                      print_context, format_implication)

# -- Formal Context (6 objects x 6 attributes) --------------------------------

CONTEXT = {
    "partner":    {"basis", "atRsk", "pasLm", "carry", "suspd", "pThru"},
    "scorp":      {"basis", "atRsk", "pasLm", "carry", "suspd", "pThru"},
    "rental-act": {"pasLm", "carry", "suspd"},
    "rental-pas": {"pasLm", "carry", "suspd"},
    "sched-c":    {"atRsk"},
    "capital":    {"carry"},
}

ABBREV = {
    "basis": "basis", "atRsk": "atRsk", "pasLm": "pasLm",
    "carry": "carry", "suspd": "suspd", "pThru": "pThru",
}

# -- Analysis ------------------------------------------------------------------

def main():
    print("=" * 70)
    print("REPLICATION: Loss Limitation Rules (supplementary)")
    print("=" * 70)

    print("\nFORMAL CONTEXT")
    print_context(CONTEXT, ABBREV)

    # Commonalities
    print("\n" + "=" * 70)
    print("COMMONALITIES")
    print("=" * 70)
    common = closure(CONTEXT, set())
    print(f"  ∅'' = {sorted(common) if common else '∅'}")

    # Single-attribute implications
    print("\n" + "=" * 70)
    print("IMPLICATIONS (single-attribute premises)")
    print("=" * 70)
    implications = find_implications(CONTEXT)
    for i, (p, c) in enumerate(implications, 1):
        print(f"  {i}. {format_implication(p, c)}")

    # Mutual exclusions
    print("\n" + "=" * 70)
    print("MUTUAL EXCLUSIONS")
    print("=" * 70)
    excl = mutual_exclusions(CONTEXT)
    if excl:
        for a1, a2 in excl:
            print(f"  {a1} ⊗ {a2}")
    else:
        print("  (none)")

    # Key results matching paper
    print("\n" + "=" * 70)
    print("SELECTED IMPLICATIONS (paper §7 reference)")
    print("=" * 70)
    print("  (1)  {pThru} → {basis, atRsk, carry}   -- pass-through entails full chain")
    print("  (2)  {basis} → {atRsk}                  -- co-applicability")
    print("  (3)  {pasLm} → {carry, suspd}           -- passive ⇒ carry + suspend")
    print("  (4)  {suspd} → {pasLm, carry}           -- suspended ⇒ passive + carry")

    # Verify
    print("\n  Verification:")
    c_pThru = closure(CONTEXT, {"pThru"})
    print(f"    {{'pThru'}}'' = {sorted(c_pThru)}")
    assert "basis" in c_pThru and "atRsk" in c_pThru and "carry" in c_pThru, \
        "pThru → basis, atRsk, carry failed"

    c_basis = closure(CONTEXT, {"basis"})
    print(f"    {{'basis'}}'' = {sorted(c_basis)}")
    assert "atRsk" in c_basis, "basis → atRsk failed"

    c_pasLm = closure(CONTEXT, {"pasLm"})
    print(f"    {{'pasLm'}}'' = {sorted(c_pasLm)}")
    assert "carry" in c_pasLm and "suspd" in c_pasLm, "pasLm → carry, suspd failed"

    c_suspd = closure(CONTEXT, {"suspd"})
    print(f"    {{'suspd'}}'' = {sorted(c_suspd)}")
    assert "pasLm" in c_suspd and "carry" in c_suspd, "suspd → pasLm, carry failed"

    print("\n  All implications verified. [ok]")

    # Key exploration event
    print("\n" + "=" * 70)
    print("EXPLORATION EVENT: Context Extension")
    print("=" * 70)
    print("""
  The algorithm proposed {pThru} → {basis, atRsk, pasLm, carry, suspd}.
  Initial objects (partner, scorp) confirmed this.

  However, testing against the specification: a materially participating
  partner (IRC §469(c)(1)) has basis and at-risk limitations but is
  NOT subject to passive activity limitation.

  This counterexample refuted the implication and led to:
    - Defining "partner" as specifically a PASSIVE partner
    - Confirming the weaker: {pThru} → {basis, atRsk, carry}

  This is the instance referenced in §7 (Internal Validity) where
  exploration surfaced an object the initial context had overlooked.
""")

if __name__ == "__main__":
    main()
