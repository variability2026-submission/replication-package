# Exploration Log: SMTP Base Commands (RFC 5321)

**Case study**: §5 of the paper (Case Study 2)
**Specification source**: RFC 5321 (Klensin, October 2008) — Simple Mail Transfer Protocol
  https://datatracker.ietf.org/doc/html/rfc5321
**Objects**: 7 base SMTP commands
**Attributes**: 9 binary structural predicates (5 syntactic, 2 semantic, 2 role)

This log records the attribute exploration dialogue. Each step shows the
implication proposed, the analyst's decision, and the RFC section that
grounds it.

---

## Formal Context

| Object | cid-arg | cli-idf | env-wrt | ext-neg | fwd-pth | prmless | path-arg | rev-pth | ses-trm |
|--------|---------|---------|---------|---------|---------|-----------|----------|---------|---------|
| EHLO   | ×       | ×       |         | ×       |         |           |          |         |         |
| HELO   | ×       | ×       |         |         |         |           |          |         |         |
| MAIL   |         |         | ×       |         |         |           | ×        | ×       |         |
| RCPT   |         |         | ×       |         | ×       |           | ×        |         |         |
| DATA   |         |         |         |         |         | ×         |          |         |         |
| RSET   |         |         |         |         |         | ×         |          |         |         |
| QUIT   |         |         |         |         |         | ×         |          |         | ×       |

Attribute key (with RFC sections):
- **cid-arg**: client identity argument — FQDN or address literal (§4.1.1.1)
- **cli-idf**: identifies the SMTP client to the server (§3.1)
- **env-wrt**: writes to SMTP envelope buffers (§2.3.1)
- **ext-neg**: negotiates ESMTP service extensions (§4.1.1.1)
- **fwd-pth**: carries forward-path in RCPT TO (§4.1.1.3)
- **prmless**: no argument in base syntax (§4.1.1.4, §4.1.1.5, §4.1.1.10)
- **path-arg**: required envelope path argument (§4.1.1.2–3)
- **rev-pth**: carries reverse-path in MAIL FROM (§4.1.1.2)
- **ses-trm**: requests session/connection closure (§4.1.1.10)

---

## Suitability Confirmation

RFC 5321 satisfies the three suitability properties:
- **Authoritative**: IETF Standards Track RFC — defines permitted SMTP behavior
  normatively, not descriptively.
- **Enumerable**: This case study restricts to 7 base commands (EHLO, HELO,
  MAIL, RCPT, DATA, RSET, QUIT), excluding ancillary commands (NOOP, VRFY),
  negotiated extensions, and private-use commands.
- **Structurally determinate**: §4.1.1 command grammars and §2.3 mail object
  semantics answer structural queries without ambiguity or
  jurisdiction-dependence.

---

## Step 1: Commonalities (closure of ∅)

**Proposed**: ∅ → ?

**Closure computation**: Which attributes do ALL 7 objects share?

Scanning each attribute:
- cid-arg: only EHLO, HELO ✗
- cli-idf: only EHLO, HELO ✗
- env-wrt: only MAIL, RCPT ✗
- ext-neg: only EHLO ✗
- fwd-pth: only RCPT ✗
- prmless: only DATA, RSET, QUIT ✗
- path-arg: only MAIL, RCPT ✗
- rev-pth: only MAIL ✗
- ses-trm: only QUIT ✗

**Result**: ∅'' = ∅ (no universal commonalities)

**Confirmed**: The 7 commands share no structural attribute. This is expected —
SMTP commands serve fundamentally different roles (identification, envelope
construction, data transfer, session management).

---

## Step 2: Client-identifying closure

**Proposed**: {cli-idf} → ?

**Closure computation**: Which objects have cli-idf? EHLO and HELO.
Shared attributes of EHLO ∩ HELO: {cid-arg, cli-idf}

**Result**: {cli-idf} → {cid-arg}

**Confirmed**: RFC 5321 §4.1.1.1 — both EHLO and HELO require a domain or
address literal argument that identifies the SMTP client. The EHLO syntax is
`"EHLO" SP ( Domain / address-literal ) CRLF`; HELO is identical in argument
structure. Both commands identify the client (§3.1).

**Converse**: {cid-arg} → {cli-idf} also holds (same two objects).

**Interpretation**: cid-arg and cli-idf are co-extensive in this subdomain —
a biconditional. Together they define the Identity family.

---

## Step 3: Extension negotiation closure

**Proposed**: {ext-neg} → ?

**Closure computation**: Which objects have ext-neg? Only EHLO.
EHLO's full attribute set: {cid-arg, cli-idf, ext-neg}

**Result**: {ext-neg} → {cid-arg, cli-idf}

**Confirmed**: RFC 5321 §4.1.1.1 — "In the EHLO command, the host sending the
command identifies itself... EHLO... is used to identify the SMTP client to
the SMTP server." EHLO both identifies the client AND negotiates extensions;
HELO identifies without negotiating. Extension negotiation entails client
identification and client-identity argument.

**Interpretation**: ext-neg differentiates EHLO from HELO within the Identity
family. In the feature model, ext-neg is a mandatory child of EHLO.

---

## Step 4: Envelope-writing closure

**Proposed**: {env-wrt} → ?

**Closure computation**: Which objects have env-wrt? MAIL and RCPT.
Shared attributes of MAIL ∩ RCPT: {env-wrt, path-arg}

**Result**: {env-wrt} → {path-arg}

**Confirmed**: RFC 5321 §4.1.1.2 (MAIL FROM): "MAIL FROM:<reverse-path>" —
requires a path argument. §4.1.1.3 (RCPT TO): "RCPT TO:<forward-path>" —
requires a path argument. Both commands write to the SMTP envelope (§2.3.1:
"The SMTP envelope is sent as a series of SMTP protocol units") and both
require a path argument.

**Converse**: {path-arg} → {env-wrt} also holds (same two objects).

**Interpretation**: env-wrt and path-arg are co-extensive — a biconditional.
Together they define the Transfer family.

---

## Step 5: Reverse-path closure

**Proposed**: {rev-pth} → ?

**Closure computation**: Which objects have rev-pth? Only MAIL.
MAIL's full attribute set: {env-wrt, path-arg, rev-pth}

**Result**: {rev-pth} → {env-wrt, path-arg}

**Confirmed**: RFC 5321 §4.1.1.2 — MAIL FROM carries the reverse-path (the
sender's mailbox or null path), and is an envelope-writing command with a
required path argument.

**Interpretation**: rev-pth differentiates MAIL from RCPT within the Transfer
family. In the feature model, rev-pth is a mandatory child of MAIL.

---

## Step 6: Forward-path closure

**Proposed**: {fwd-pth} → ?

**Closure computation**: Which objects have fwd-pth? Only RCPT.
RCPT's full attribute set: {env-wrt, fwd-pth, path-arg}

**Result**: {fwd-pth} → {env-wrt, path-arg}

**Confirmed**: RFC 5321 §4.1.1.3 — RCPT TO carries the forward-path
(a recipient mailbox), and is an envelope-writing command with a required
path argument.

**Interpretation**: fwd-pth differentiates RCPT from MAIL within the Transfer
family. In the feature model, fwd-pth is a mandatory child of RCPT.

---

## Step 7: Session-termination closure

**Proposed**: {ses-trm} → ?

**Closure computation**: Which objects have ses-trm? Only QUIT.
QUIT's full attribute set: {prmless, ses-trm}

**Result**: {ses-trm} → {prmless}

**Confirmed**: RFC 5321 §4.1.1.10 — "QUIT" takes no parameters and requests
connection closure. Session termination entails being parameterless (in base
syntax).

**Interpretation**: ses-trm differentiates QUIT from DATA/RSET within the
Parameterless family. In the feature model, ses-trm is a mandatory child
of QUIT.

---

## Step 8: Parameterless closure

**Proposed**: {prmless} → ?

**Closure computation**: Which objects have prmless? DATA, RSET, QUIT.
Shared attributes: {prmless}

**Result**: {prmless}'' = {prmless} (closed set — no new attributes)

**Confirmed**: These three commands share only the property of taking no
argument in base syntax. They differ in all other respects (DATA initiates
mail data transfer, RSET aborts the current transaction, QUIT terminates
the session).

---

## Step 9: Observed disjointness — family-level

**Check**: Do any cross-family attribute pairs co-occur?

| Pair | Co-occurrence? | Explanation |
|------|---------------|-------------|
| cli-idf ⊗ env-wrt | No object has both | §3.1 vs §2.3.1: identification ≠ envelope writing |
| cli-idf ⊗ prmless | No object has both | Identity commands carry arguments |
| env-wrt ⊗ prmless | No object has both | Envelope commands require path arguments |

**Verified against RFC 5321**: The three families serve structurally distinct
roles in the SMTP transaction model:
- Identity commands (§3.1): establish/re-establish session identity
- Transfer commands (§2.3.1): construct the mail envelope
- Parameterless commands: manage session state or transfer data

No command serves dual roles across these families. This is normative —
the RFC defines each command with a single, specific function.

**Impossibility implications**: All 27 cross-family attribute pairs close to
the full attribute set M (meaning the combination is impossible in this
context). This formally confirms the three-way partition.

Example impossibility implications:
- {cli-idf, env-wrt} → M (no command both identifies client and writes envelope)
- {cli-idf, prmless} → M (no command both identifies client and is parameterless)
- {env-wrt, prmless} → M (no command both writes envelope and is parameterless)
- {cid-arg, fwd-pth} → M, {ext-neg, rev-pth} → M, etc.

---

## Summary of Implication Basis

### Primary implications (6)

| # | Implication | RFC section | Domain meaning |
|---|-------------|-------------|----------------|
| 1 | {ext-neg} → {cid-arg, cli-idf} | §4.1.1.1 | Extension negotiation entails client identification |
| 2 | {cli-idf} → {cid-arg} | §4.1.1.1 | Client-identifying commands carry identity argument |
| 3 | {env-wrt} → {path-arg} | §4.1.1.2–3 | Envelope-writing commands require path argument |
| 4 | {rev-pth} → {env-wrt, path-arg} | §4.1.1.2 | Reverse-path entails envelope writing |
| 5 | {fwd-pth} → {env-wrt, path-arg} | §4.1.1.3 | Forward-path entails envelope writing |
| 6 | {ses-trm} → {prmless} | §4.1.1.10 | Session termination is parameterless |

### Impossibility implications (27)

All cross-family attribute pairs close to M, confirming three disjoint
command families. The partition is produced by the RFC through the structural
distinctions captured in the attribute vocabulary, not handed down as
pre-named families.

### Observed disjointness (family-level, 3)

| Pair | Interpretation |
|------|----------------|
| cli-idf ⊗ env-wrt | Identity vs transfer: §3.1 vs §2.3.1 |
| cli-idf ⊗ prmless | Identity vs parameterless |
| env-wrt ⊗ prmless | Transfer vs parameterless |

---

## Translation to Feature Model

- No commonalities → no mandatory root attributes
- Three disjoint families → top-level XOR group
  - Identity (cli-idf ∧ cid-arg): EHLO, HELO — XOR subgroup
  - Transfer (env-wrt ∧ path-arg): MAIL, RCPT — XOR subgroup
  - Parameterless (prmless): DATA, RSET, QUIT — XOR subgroup
- Differentiating attributes → mandatory children of specific commands
  - ext-neg → mandatory under EHLO
  - rev-pth → mandatory under MAIL
  - fwd-pth → mandatory under RCPT
  - ses-trm → mandatory under QUIT

See Figure 4 in the paper.

## Variability Topology

No universal commonalities + mutually exclusive families with typed
arguments → Command variation structure. The name coincidence with the
domain vocabulary is topological, not nominal (see §5 of the paper).
