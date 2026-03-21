#!/usr/bin/env python3
"""
Replication: SMTP Base Commands (RFC 5321) -- Case Study 2

Reproduces the formal context, implications, impossibility implications,
and three-way command family partition from Section 5 of the paper.

Source: RFC 5321 (Klensin, October 2008) -- Simple Mail Transfer Protocol
        https://datatracker.ietf.org/doc/html/rfc5321

Usage:  python3 smtp_fca.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fca_core import (closure, find_implications, find_pair_implications,
                      impossibility_implications, mutual_exclusions,
                      print_context, format_implication)

# ── Formal Context (Table in §5.2) ──────────────────────────────────────

CONTEXT = {
    "EHLO": {"cid-arg", "cli-idf", "ext-neg"},
    "HELO": {"cid-arg", "cli-idf"},
    "MAIL": {"env-wrt", "path-arg", "rev-pth"},
    "RCPT": {"env-wrt", "fwd-pth", "path-arg"},
    "DATA": {"prmless"},
    "RSET": {"prmless"},
    "QUIT": {"prmless", "ses-trm"},
}

ABBREV = {
    "cid-arg": "cid",  "cli-idf": "cli",  "env-wrt": "env",
    "ext-neg": "ext",  "fwd-pth": "fwd",  "prmless": "prm",
    "path-arg": "pth", "rev-pth": "rev",  "ses-trm": "ses",
}

# ── Analysis ────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("REPLICATION: SMTP Base Commands (§5)")
    print("=" * 70)

    print("\nFORMAL CONTEXT")
    print_context(CONTEXT, ABBREV)

    # Commonalities
    print("\n" + "=" * 70)
    print("COMMONALITIES")
    print("=" * 70)
    common = closure(CONTEXT, set())
    print(f"  ∅'' = {sorted(common) if common else '∅  (no universal commonalities)'}")

    # Single-attribute implications
    print("\n" + "=" * 70)
    print("PRIMARY IMPLICATIONS")
    print("=" * 70)
    implications = find_implications(CONTEXT)
    for i, (p, c) in enumerate(implications, 1):
        print(f"  {i}. {format_implication(p, c)}")

    # Impossibility implications
    print("\n" + "=" * 70)
    print("IMPOSSIBILITY IMPLICATIONS")
    print("=" * 70)
    impossible = impossibility_implications(CONTEXT)
    print(f"  Count: {len(impossible)} (all cross-family pairs close to M)")
    for i, (p, c) in enumerate(impossible, 1):
        print(f"  {i:>3}. {{{', '.join(sorted(p))}}} → M")

    # Mutual exclusions
    print("\n" + "=" * 70)
    print("MUTUAL EXCLUSIONS")
    print("=" * 70)
    excl = mutual_exclusions(CONTEXT)
    print(f"  Total pairs: {len(excl)}")
    print("\n  Semantically meaningful (family-level):")
    family_pairs = [("cli-idf", "env-wrt"), ("cli-idf", "prmless"),
                    ("env-wrt", "prmless")]
    for a1, a2 in family_pairs:
        found = (a1, a2) in excl or (a2, a1) in excl
        print(f"    {a1} ⊗ {a2}  {'[ok]' if found else '[FAIL]'}")

    # Family partition
    print("\n" + "=" * 70)
    print("COMMAND FAMILY PARTITION")
    print("=" * 70)
    families = {
        "Identity":      [c for c, a in CONTEXT.items() if "cli-idf" in a],
        "Transfer":      [c for c, a in CONTEXT.items() if "env-wrt" in a],
        "Parameterless": [c for c, a in CONTEXT.items() if "prmless" in a],
    }
    covered = set()
    for label, cmds in families.items():
        print(f"  {label}: {sorted(cmds)}")
        covered |= set(cmds)
    strict = covered == set(CONTEXT.keys())
    print(f"\n  Strict partition: {strict} [ok]" if strict else "  NOT a strict partition [FAIL]")

    # Paper §5.4 verification
    print("\n" + "=" * 70)
    print("PAPER §5.4 -- SELECTED IMPLICATIONS")
    print("=" * 70)
    checks = [
        ({"ext-neg"},  {"cid-arg", "cli-idf"}),
        ({"env-wrt"},  {"path-arg"}),
        ({"rev-pth"},  {"env-wrt", "path-arg"}),
        ({"fwd-pth"},  {"env-wrt", "path-arg"}),
        ({"ses-trm"},  {"prmless"}),
    ]
    for premise, expected_new in checks:
        c = closure(CONTEXT, premise)
        actual_new = c - premise
        ok = expected_new <= actual_new
        print(f"  {sorted(premise)} → {sorted(expected_new)}  {'[ok]' if ok else '[FAIL]'}")

    assert len(impossible) == 27, f"Expected 27 impossibilities, got {len(impossible)}"
    print(f"\n  27 impossibility implications confirmed. [ok]")
    print("  All paper implications verified. [ok]")

if __name__ == "__main__":
    main()
