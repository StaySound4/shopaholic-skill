# 22 — Build official domestic and global source-routing playbooks

**What to build:** Provide lightweight **Wayfinding & Search Routing Playbooks (指路导航剧本)** pointing to authoritative official portals and search syntax anchors across 5 domains (Electrical/Safety: CCC, UL, CE, TÜV, PSE; Energy/Ecology: CEL, EPREL, ENERGY STAR; Food/Baby/Health: GB 4806, FDA, LFGB, OEKO-TEX, ECE R129; Audio/Display: VESA DisplayHDR, Dolby, Wi-Fi, Bluetooth, USB-IF; Outdoor: RDS, bluesign, UIAA, IP/MIL-STD), strictly prioritizing live portal routing over static text hoarding.

**Blocked by:** 09, 10, 13, 14

**Status:** ready-for-agent

## Acceptance criteria

- [ ] Playbooks function as search/portal routers (pointing to `std.samr.gov.cn`, UL Product iQ, EPREL, VESA list, etc.) rather than static repositories of full standard texts.
- [ ] High-precision search anchor syntaxes are provided for each registry to enable fast live runtime verification.
- [ ] Each source family explicitly states its evidence proof role (what it proves vs what it cannot prove alone).
- [ ] Includes China identity/company/recall/regulated sources and international gold-standard registries.
- [ ] Access/rate/account caveats and fallback degraded-mode paths are explicit.
## Verification procedure

Pass: FCC Change in ID supports same-design inference; `std.samr.gov.cn` verifies active standard status; VESA DisplayHDR registry unmasks fake HDR1000 claims. Adversarial: missing USB-IF public listing cannot be converted into “noncompliant”.

## Evidence to attach
- Raw unedited output(s).
- Structured artifact(s) produced by this ticket when applicable.
- Scorer/test output with command or reproducible invocation.
- Source snapshot/locator and access status for evidence-dependent checks.
- Short limitations/blockers note, even when all criteria pass.

## Stop conditions

- STOP if any blocker is incomplete.
- STOP and mark the verification invalid if the only way to pass is to change the expected result after seeing the output.
- STOP with a blocked state rather than guessing when a required authoritative fact/source/tool cannot be accessed.
- Do not implement later tickets just to make this ticket look complete; open/follow the blocker instead.
