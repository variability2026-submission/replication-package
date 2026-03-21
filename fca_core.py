#!/usr/bin/env python3
"""
FCA Core -- Shared implementation for replication package.

Implements closure computation, implication discovery, mutual exclusion
detection, and context display for Formal Concept Analysis.

No external dependencies -- requires only Python 3.10+.

Reference: Ganter & Wille, "Formal Concept Analysis: Mathematical
Foundations," Springer, 1999.
"""

from __future__ import annotations
from typing import Dict, FrozenSet, Set, Tuple

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

Context = Dict[str, Set[str]]
"""Formal context: maps object names to their attribute sets."""

Implication = Tuple[FrozenSet[str], FrozenSet[str]]
"""An implication (premise, conclusion) where conclusion is the full closure."""


# ---------------------------------------------------------------------------
# Core FCA operations
# ---------------------------------------------------------------------------

def prime_objects(context: Context, attributes: Set[str]) -> Set[str]:
    """A' -- objects that have ALL attributes in A."""
    if not attributes:
        return set(context.keys())
    return {obj for obj, attrs in context.items() if attributes <= attrs}


def prime_attributes(context: Context, objects: Set[str]) -> Set[str]:
    """B' -- attributes shared by ALL objects in B."""
    if not objects:
        # Convention: empty object set → union of all attributes
        return set().union(*context.values()) if context else set()
    result: Set[str] | None = None
    for obj in objects:
        if result is None:
            result = context[obj].copy()
        else:
            result &= context[obj]
    return result if result is not None else set()


def closure(context: Context, attributes: Set[str]) -> Set[str]:
    """A'' -- double prime / closure of an attribute set."""
    return prime_attributes(context, prime_objects(context, attributes))


# ---------------------------------------------------------------------------
# Implication discovery
# ---------------------------------------------------------------------------

def find_implications(context: Context) -> list[Implication]:
    """
    Find implications from empty-set and single-attribute premises.

    Returns a list of (premise, full_closure) tuples where the closure
    contains attributes beyond the premise.  For the small contexts used
    in the paper (6–8 objects, 8–9 attributes), this covers the
    structurally interesting implications; pair-premise implications are
    computed separately where needed (see impossibility check below).
    """
    all_attrs = set().union(*context.values())
    implications: list[Implication] = []

    # Empty premise → commonalities
    common = closure(context, set())
    if common:
        implications.append((frozenset(), frozenset(common)))

    # Single-attribute premises
    for attr in sorted(all_attrs):
        c = closure(context, {attr})
        if c - {attr}:
            implications.append((frozenset({attr}), frozenset(c)))

    return implications


def find_pair_implications(context: Context) -> list[Implication]:
    """Find implications with two-attribute premises (includes impossibilities)."""
    all_attrs = sorted(set().union(*context.values()))
    full = frozenset(all_attrs)
    results: list[Implication] = []

    for i, a1 in enumerate(all_attrs):
        for a2 in all_attrs[i + 1:]:
            pair = {a1, a2}
            c = frozenset(closure(context, pair))
            if c - pair:
                results.append((frozenset(pair), c))
    return results


def impossibility_implications(context: Context) -> list[Implication]:
    """Return pair implications whose closure is the full attribute set M."""
    all_attrs = frozenset().union(*context.values())
    return [(p, c) for p, c in find_pair_implications(context)
            if c == all_attrs]


# ---------------------------------------------------------------------------
# Mutual exclusion detection
# ---------------------------------------------------------------------------

def mutual_exclusions(context: Context) -> list[tuple[str, str]]:
    """Find attribute pairs that never co-occur in any object."""
    all_attrs = sorted(set().union(*context.values()))
    pairs: list[tuple[str, str]] = []
    for i, a1 in enumerate(all_attrs):
        for a2 in all_attrs[i + 1:]:
            if not any(a1 in a and a2 in a for a in context.values()):
                # Verify both actually appear
                if (any(a1 in a for a in context.values()) and
                        any(a2 in a for a in context.values())):
                    pairs.append((a1, a2))
    return pairs


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_context(context: Context,
                  abbrev: Dict[str, str] | None = None) -> None:
    """Print the formal context as a cross-table."""
    all_attrs = sorted(set().union(*context.values()))
    col_w = 7

    # Header
    print(f"{'Object':<18}", end="")
    for attr in all_attrs:
        label = (abbrev or {}).get(attr, attr)[:col_w - 1]
        print(f"{label:<{col_w}}", end="")
    print()
    print("-" * (18 + col_w * len(all_attrs)))

    # Rows
    for obj in sorted(context.keys()):
        print(f"{obj:<18}", end="")
        for attr in all_attrs:
            mark = "×" if attr in context[obj] else "·"
            print(f"{mark:<{col_w}}", end="")
        print()


def format_implication(premise: FrozenSet[str] | Set[str],
                       conclusion: FrozenSet[str] | Set[str],
                       show_new_only: bool = True) -> str:
    """Pretty-print an implication.  If show_new_only, omit premise attrs."""
    p = sorted(premise)
    c = sorted(conclusion - premise) if show_new_only else sorted(conclusion)
    p_str = ", ".join(p) if p else "∅"
    c_str = ", ".join(c) if c else "(closed)"
    return f"{{{p_str}}} → {{{c_str}}}"
