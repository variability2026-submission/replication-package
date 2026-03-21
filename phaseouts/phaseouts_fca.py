#!/usr/bin/env python3
"""
Replication: Phaseout Mechanisms (U.S. Tax Law) -- Case Study 1

Reproduces the formal context, implications, and feature model derivation
from Section 4 of the paper.

Sources: IRS Publications 596, 970, 590-A; Schedule 8812 Instructions.

Usage:  python3 phaseouts_fca.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fca_core import (closure, find_implications, mutual_exclusions,
                      print_context, format_implication)

# ── Formal Context (Table in §4.2) ──────────────────────────────────────

CONTEXT = {
    "EITC":        {"po", "pi", "grad", "AGI", "ref"},
    "CTC":         {"po", "grad", "MAGI", "pRef"},
    "AOTC":        {"po", "grad", "MAGI", "pRef"},
    "LifetimeLC":  {"po", "grad", "MAGI", "nRef"},
    "StudentLn":   {"po", "grad", "MAGI"},
    "IRA":         {"po", "grad", "MAGI"},
    "RothIRA":     {"po", "grad", "MAGI"},
    "RentalAllow": {"po", "grad", "MAGI"},
}

ABBREV = {
    "po": "po", "pi": "pi", "grad": "grad",
    "MAGI": "MAGI", "AGI": "AGI",
    "ref": "ref", "pRef": "pRef", "nRef": "nRef",
}

# ── Analysis ────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("REPLICATION: Phaseout Mechanisms (§4)")
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
    for a1, a2 in mutual_exclusions(CONTEXT):
        print(f"  {a1} ⊗ {a2}")

    # Key results matching paper §4.4
    print("\n" + "=" * 70)
    print("PAPER §4.4 -- SELECTED IMPLICATIONS")
    print("=" * 70)
    print("  (1)  ∅ → {po, grad}           -- commonalities")
    print("  (2)  {pi} → {ref, AGI}        -- phase-in ⇒ refundable + AGI")
    print("  (3)  {pRef} → {MAGI}          -- partial refundability ⇒ MAGI")
    print("  AGI ⊗ MAGI                    -- XOR income measure")

    # Verify
    print("\n  Verification:")
    c_pi = closure(CONTEXT, {"pi"})
    print(f"    {{'pi'}}'' = {sorted(c_pi)}")
    assert "ref" in c_pi and "AGI" in c_pi, "pi → ref, AGI failed"

    c_pRef = closure(CONTEXT, {"pRef"})
    print(f"    {{'pRef'}}'' = {sorted(c_pRef)}")
    assert "MAGI" in c_pRef, "pRef → MAGI failed"

    excl = mutual_exclusions(CONTEXT)
    assert ("AGI", "MAGI") in excl, "AGI ⊗ MAGI not found"
    print("    AGI ⊗ MAGI confirmed")
    print("\n  All paper implications verified. [ok]")

if __name__ == "__main__":
    main()
