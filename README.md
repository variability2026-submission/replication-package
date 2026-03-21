# Replication Package

**Paper**: Feature Model Derivation from Authoritative Specifications
Using Formal Concept Analysis

**Venue**: VARIABILITY 2026

---

## Contents

This package contains formal contexts, exploration logs, and replication
scripts for the three case studies presented in the paper, plus one
supplementary case study referenced in the validity discussion (§7).

```
replication-package/
├── README.md               ← this file
├── fca_core.py             ← shared FCA implementation
├── phaseouts/              ← Case Study 1 (§4)
│   ├── formal-context.csv
│   ├── exploration-log.md
│   └── phaseouts_fca.py
├── smtp-commands/          ← Case Study 2 (§5)
│   ├── formal-context.csv
│   ├── exploration-log.md
│   └── smtp_fca.py
├── healthcare-claims/      ← Case Study 3 (§6)
│   ├── formal-context.csv
│   ├── exploration-log.md
│   └── healthcare_fca.py
└── loss-limitations/       ← Supplementary (referenced in §7)
    ├── formal-context.csv
    ├── exploration-log.md
    └── losses_fca.py
```

## Requirements

- Python 3.10 or later
- No external dependencies

## Running

From the package root:

```bash
python3 phaseouts/phaseouts_fca.py
python3 smtp-commands/smtp_fca.py
python3 healthcare-claims/healthcare_fca.py
python3 loss-limitations/losses_fca.py
```

Each script reproduces the formal context, computes closures and
implications, and verifies the selected implications reported in the
corresponding paper section.

## Artifacts

### Formal Contexts (`formal-context.csv`)

Machine-readable cross-tables in CSV format. Each row is an object;
columns are binary attributes (1 = present, 0 = absent). These
correspond directly to the cross-tables in the paper (§4.2, §5.2, §6.2).

### Exploration Logs (`exploration-log.md`)

Step-by-step records of the attribute exploration dialogue for each case
study. Each entry documents:

1. The implication proposed by the algorithm
2. Whether it was confirmed or refuted (with counterexample)
3. The specification text that grounds the decision (with section/source
   references)
4. The feature model interpretation

These logs operationalize the paper's auditability claim (§3.7): every
accepted implication is linked to specification text, and every modeling
decision is recorded. A reader with access to the same specification
sources can replay each exploration.

### Replication Scripts (`*_fca.py`)

Python scripts that:
- Define the formal context as a dictionary
- Compute closures, implications, and mutual exclusions
- Verify that the implications reported in the paper hold
- Print the cross-case comparison

The scripts import shared FCA functions from `fca_core.py` at the
package root.

## Specification Sources

| Case Study | Source | Access |
|------------|--------|--------|
| Phaseouts (§4) | IRS Publications 596, 970, 590-A; Schedule 8812 Instructions | https://www.irs.gov/publications |
| SMTP commands (§5) | RFC 5321 (Klensin, 2008) | https://datatracker.ietf.org/doc/html/rfc5321 |
| Healthcare claims (§6) | CMS Medicare Claims Processing Manual; X12 837 Guides | https://www.cms.gov/regulations-and-guidance |
| Loss limitations (§7 ref.) | IRS Publication 925; IRC §§465, 469, 704(d) | https://www.irs.gov/publications |

All IRS publications and the RFC are freely accessible. X12 837
Implementation Guides are published by the Accredited Standards
Committee X12.

## FCA Implementation

`fca_core.py` implements:
- `closure(context, attributes)` — double-prime closure (A'')
- `find_implications(context)` — single-attribute premise implications
- `find_pair_implications(context)` — pair-premise implications
- `impossibility_implications(context)` — pairs that close to full M
- `mutual_exclusions(context)` — attribute pairs that never co-occur

The implementation is intentionally minimal — it covers the operations
used in the paper without requiring concept lattice enumeration or the
full Duquenne-Guigues basis algorithm. For the small contexts in the
case studies (6–8 objects, 8–9 attributes), single-attribute and
pair-attribute closures suffice to reproduce all reported implications.

## Correspondence to Paper

| Paper section | Package artifact |
|---------------|------------------|
| §3, Table 1 | Translation rules applied in each exploration log |
| §4.2, Table | `phaseouts/formal-context.csv` |
| §4.3–4.4 | `phaseouts/exploration-log.md` |
| §5.2, Table | `smtp-commands/formal-context.csv` |
| §5.3–5.4 | `smtp-commands/exploration-log.md` |
| §6.2, Table | `healthcare-claims/formal-context.csv` |
| §6.3–6.4 | `healthcare-claims/exploration-log.md` |
| §7 (Internal Validity) | `loss-limitations/exploration-log.md` |
| Figures 2–5 | Feature models derived at end of each log |

## License

This replication package is provided for academic review and
reproducibility. A persistent, citable version will be published upon
acceptance.
