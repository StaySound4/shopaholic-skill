# Source Registry — Recommended Evidence Families

## Purpose

This is a routing registry, not a universal trust ranking. Every source family has:
- **claim roles it can support**;
- **claim roles it cannot prove alone**;
- **region/category applicability**;
- **access/freshness caveats**.

The agent must use the strongest available source appropriate to the claim and preserve `unknown` when access/evidence is insufficient.

## China / PRC authoritative sources

### CQC / CCC certificate and factory information

**Use for:** certificate status, formal model identifiers, applicant/manufacturer/factory relationships where exposed, certification scope.

**Do not infer alone:** consumer durability, comparative performance, actual retail price, product country of origin beyond what the record explicitly states.

**Why it matters:** applicant, manufacturer, and production factory are distinct roles and can reveal private-label/OEM relationships that a marketplace title hides.

### National Enterprise Credit Information Publicity System / authoritative corporate registry sources

**Use for:** legal company identity, registration status, registered relationships/information made public by the registry.

**Do not infer alone:** factory for a specific SKU, product origin, product quality, or current seller authorization.

### SAMR defect product recall / recall query

**Use for:** official recall existence, affected producer/product, disclosed defect, remedy, exact scope where published.

**Do not infer alone:** that an unaffected batch/region has the same defect, or a population failure rate beyond the recall scope.

### SAMR quality supervision / product sampling announcements

**Use for:** official sampling/nonconformity findings, sampled product/company details, tested standards/items as published.

**Do not infer alone:** universal defect rate across all batches or future production.

### National Standards Information Public Service Platform (std.samr.gov.cn)

**Use for:** authoritative legal status (`active` 现行, `upcoming` 即将实施, `superseded` 被替代, `repealed` 废止), official standard code (mandatory GB vs voluntary GB/T), publication date, implementation date, and standard replacement lineage.

**Do not infer alone:** whether a specific retail product batch has passed all testing items without a formal test report or 3C certificate.

### NMPA medical-device registration/UDI data

**Use for:** medical-device identity, registrant/filing information, UDI/product identification and other disclosed regulatory data.

**Do not infer alone:** clinical effectiveness beyond approved claims, comparative superiority, adverse-event incidence rate.
## Global & Domestic Standards and Certifications Matrix

A systematic routing matrix of legally binding and gold-standard voluntary certifications across China, North America, Europe, and international bodies:

### 1. Electrical, Safety & Electromagnetic (EMC)
- **CCC (3C / CNCA / CQC, China)**: Mandatory safety certification for 17 product categories (audio/video, IT, household appliances, lighting, motor vehicles). Proves basic legal market access in mainland China; does not prove durability or premium quality.
- **UL / ETL / CSA (North America)**: OSHA-accredited NRTL electrical, fire, and thermal safety certifications (e.g. UL 60335 for appliances, UL 94 for flammability). Proves North American electrical safety compliance.
- **CE (EU Directives: LVD 2014/35/EU, EMC 2014/30/EU, RED 2014/53/EU)**: Mandatory European economic area conformity. Self-declaration (except high-risk categories); requires EU DoC (Declaration of Conformity).
- **TÜV Rheinland / TÜV SÜD (Germany / Global)**: Independent testing marks for hardware-level low blue light, eye comfort, anti-flicker (e.g. 2PfG 1797), dynamic safety, and electrical safety.
- **GS Mark (Geprüfte Sicherheit, Germany)**: Voluntary German tested-safety mark based on the German Product Safety Act (ProdSG). Higher legal rigor than standard CE self-declaration.
- **PSE (Japan)**: Electrical Appliance and Material Safety Law (Diamond PSE for high-risk Category A; Circle PSE for Category B).
- **IECEE CB Scheme**: International system for mutual acceptance of test certificates dealing with the safety of electrical and electronic products across 50+ member countries.

### 2. Energy Efficiency, Ecology & Chemical Safety
- **China Energy Label (CEL, China)**: Mandatory energy efficiency grading (Grade 1/2/3) across appliances, air conditioning, refrigerators, and displays based on national GB standards.
- **EU EPREL & ErP (European Union)**: Mandatory energy labeling and Eco-design directives (2009/125/EC). EPREL database provides verified energy consumption, noise levels, and repairability indices.
- **ENERGY STAR (US EPA / DOE)**: Government-backed energy efficiency program. Models undergo third-party laboratory verification.
- **RoHS 2.0 (2011/65/EU) & REACH (EC 1907/2006)**: Restricts hazardous substances (Pb, Cd, Hg, Cr6+, PBBs, PBDEs, phthalates) and tracks Substances of Very High Concern (SVHC) in consumer products.
- **California Proposition 65 (Prop 65)**: Mandates clear warnings regarding chemicals known to cause cancer, birth defects, or reproductive toxicity.

### 3. Food Contact, Baby, Maternity & Textiles
- **China Food Contact Standards (GB 4806.1~.15 Series, China)**: Mandatory national safety standards for food contact plastics, rubber, silicone, stainless steel, glass, and non-stick coatings.
- **FDA 21 CFR 170-199 (United States)**: US regulations for direct/indirect food contact materials and food-grade silicone/polymers.
- **LFGB § 30/31 (Lebensmittel-, Bedarfsgegenstände- und Futtermittelgesetzbuch, Germany)**: Stringent European food contact safety standard (includes sensory/taste migration tests, significantly stricter than baseline EU regulations).
- **OEKO-TEX® Standard 100 (Global)**: Independent testing for harmful substances in textiles. **Class I** certified products are tested to ensure safety for babies and infants up to 36 months.
- **ECE R129 / i-Size (UNECE / Global)**: State-of-the-art child restraint safety regulation (mandatory Q-dummy side-impact testing, Isofix requirement, height-based sizing), strictly superseding obsolete ECE R44/04.
- **GOTS (Global Organic Textile Standard)**: Worldwide leading organic textile processing standard for fibers with ecological and social criteria.

### 4. Audio, Video, Display & High-Speed Protocols
- **VESA DisplayHDR (VESA, Global)**: Certified display peak luminance, black level, color gamut, and local dimming (DisplayHDR 400/600/1000/1400 and True Black 400/500/600). Exposes fake marketing "HDR1000" claims that lack VESA lab certification.
- **VESA ClearMR (VESA, Global)**: Clear Motion Ratio metric (ClearMR 3000~13000) measuring pure in-focus pixels over blurred pixels during high-speed motion, superseding subjective MPRT/GTG claims.
- **Dolby Vision & Dolby Atmos (Dolby Laboratories)**: Proprietary HDR imaging and spatial audio laboratory licensing.
- **Wi-Fi CERTIFIED™ (Wi-Fi Alliance)**: Interoperability, WPA3 security, and throughput certification for Wi-Fi 6, 6E, and 7 devices.
- **Bluetooth SIG (Bluetooth Qualification)**: Verifies declaration IDs and RF compliance against core specifications.
- **USB-IF (USB Implementers Forum)**: Verifies USB PD 3.1 / EPR (up to 240W) negotiation safety and USB4 40Gbps/80Gbps signal integrity.

### 5. Outdoor, Mountaineering & Industrial Reliability
- **RDS (Responsible Down Standard)**: Audits the entire down and feather supply chain from farm to final product to prevent live-plucking and force-feeding.
- **bluesign® System**: Stringent independent environmental and consumer safety standard eliminating toxic chemicals from the textile manufacturing process.
- **UIAA Safety Label (UIAA 101~130) & CE EN 892 / EN 12277**: Mandatory mountaineering climbing ropes, harnesses, carabiners, and helmet impact certifications.
- **IP Code (IEC 60529 / GB/T 4208)**: Standardized ingress protection ratings (IP65, IP67, IP68 immersion depth/time, IP69K high-pressure steam jet).
- **MIL-STD-810H (US DoD)**: Environmental engineering testing (thermal shock, vibration, humidity, salt fog corrosion, ballistic drop resistance).

## Global identity and compliance sources
### Verified by GS1

**Use for:** GTIN identity, licensed company/organization behind a GTIN, basic product/brand data where available, country of sale and related product identity fields.

**Do not infer alone:** production factory, manufacturing country, origin country, authorized seller, quality.

**Critical caveat:** country where a GTIN licence was issued is not product origin.

### FCC Equipment Authorization (United States)

**Use for:** FCC grantee/device identity, regulatory filings, and strong same-hardware evidence where a documented Change in ID states no change in design/circuitry/construction and original test results remain representative.

**Do not infer alone:** all non-radio internals, production factory unless specifically disclosed, current retail availability, global region equivalence.

**High-value OEM use:** an explicit Section 2.933 Change in ID relationship is much stronger than visual similarity for a same-design inference.

### Bluetooth SIG Qualified Product database

**Use for:** Bluetooth qualification records searchable by company/product/model; qualification identity and declared public product record.

**Do not infer alone:** retail availability, overall device quality, factory/origin, every marketed SKU’s exact equivalence.

**Caveat:** the SIG database itself states results are informational and accuracy/completeness is not guaranteed; use as an identity/compliance anchor, not universal truth.

### USB-IF Product Search

**Use for:** products certified to bear the USB-IF logo and that passed the USB-IF Compliance Program, with certification-date context.

**Do not infer alone:** a product absent from the public listing is noncompliant, because the public list has scope/display limitations and certification status may vary.

**Caveat:** members maintain listing content; older certifications require careful interpretation against current program iterations.

### UL Product iQ

**Use for:** UL certification identity, manufacturer certification records, model/file/category information supported by Product iQ.

**Do not infer alone:** general product reliability, current seller authenticity, origin, performance beyond the certified scope.


### IEEE Standards Association (standards.ieee.org) & International Standards (IEC / ISO)

**Use for:** verifying authoritative international standard codes, standard titles, technical definitions, and measurement practices (e.g. **IEEE 1789-2015** for mitigating LED flicker health risks, IEC 62885-2 / ASTM F558 for vacuum air watts, IEC 62368-1 for AV/ICT safety).

**Do not infer alone:** that a product meets a standard simply because marketing claims "flicker-free" or "eye-care" without verified test data (modulation depth and frequency).
## EU / US product registries

### EPREL — European Product Registry for Energy Labelling

**Use for:** covered energy-labelled product-model identity, supplier role, brand/trademark, product information sheet, regulatory model data, first placement on EU market where exposed, end-of-placement information where exposed, GTIN where supplied.

**Do not infer alone:** the EPREL supplier is necessarily the original manufacturer; EU first-placement date is global release date; registered efficiency data proves unrelated durability claims.

**Critical caveat:** the supplier can be an EU manufacturer, authorized representative, or importer, and brand/trademark may differ from supplier name.

### ENERGY STAR Product Finder

**Use for:** ENERGY STAR certified model data for covered categories, structured/downloadable certification/product data.

**Do not infer alone:** superiority on non-ENERGY-STAR dimensions, global SKU identity, consumer reliability.

### EPEAT Registry

**Use for:** EPEAT-registered electronics/models and applicable sustainability criteria/registration information.

**Do not infer alone:** performance superiority, safety beyond relevant criteria, global availability.

## Safety and recall sources

### US CPSC Recall Database / API

**Use for:** machine-readable/public US consumer-product recall records, recall scope, hazard/remedy as published.

**Do not infer alone:** global recall scope, unaffected variants, incident prevalence outside disclosed information.

### EU Safety Gate

**Use for:** alerts shared by EU/national authorities for dangerous non-food products, risk and measures disclosed in an alert.

**Do not infer alone:** worldwide impact, unaffected variants, prevalence outside the alert scope.

### FDA medical-device databases / recall data / MAUDE

**Use for:** US regulatory device records, recalls, and adverse-event signal investigation as appropriate.

**Do not infer alone from MAUDE:** incidence/prevalence, causation, or comparative safety. Passive adverse-event reporting can be incomplete, duplicated, inaccurate, unverified, and biased.

## Market/price sources & foreign e-commerce data forensics

### Official manufacturer stores & regional portals

**Use for:** current official offer, official regional SKU, warranty terms, accessories, declared MSRP/current official price.

**Do not infer alone:** market-clearing street price, independent quality superiority.

### Major retailers / authorized dealers (China & Global: JD, Tmall, Amazon, B&H, BestBuy)

**Use for:** observed current offers, stock, exact retail package/SKU, return/warranty channel where stated.

**Foreign Marketplace Forensics (Amazon / B&H / BestBuy / eBay)**:
- **Seller & Fulfillment Tiering**:
  - `Sold & Shipped by Retailer` (e.g. Amazon.com Direct): Highest authenticity and direct manufacturer supply.
  - `Fulfilled by Platform (FBA)`: Platform logistics, but commingled inventory (混仓) poses counterfeit risks; inspect seller feedback history.
  - `3rd-Party Merchant (FBM)`: High risk of grey market, unverified return policies, and voided official regional warranties.
- **Price History & Deal De-biasing (Keepa / CamelCamelCamel logic)**:
  - Track 90-180 day historical pricing to expose artificial List Price inflation and pre-deal price jumps before Prime Day / Black Friday.
- **Review Authenticity & ASIN Hijacking Forensics (FakeSpot / ReviewMeta logic)**:
  - Filter out incentivized Vine reviews, unverified purchases, and Review Hijacking (merging old high-rating ASINs from towels/cases into new electronic gadgets).
- **Refurbished / Open-Box Grading**:
  - Segment `Brand New`, `Amazon Renewed (Certified Refurbished)`, and `Amazon Warehouse (Like New / Very Good / Good)`, accounting for shortened warranties and cosmetic wear.

**Do not infer alone:** historical range without time-separated data, product durability, objective ranking.

### Used marketplaces / specialist used dealers (Xianyu, eBay, B&H Used, MPB, KEH)

**Use for:** current used offer distribution, condition conventions, liquidity clues, listing-level serial/version evidence where available.

**Do not infer alone:** completed transaction price unless the source actually exposes completed sales; hidden defect absence; seller claims without verification.

## Independent measurement, deep global labs, and field evidence

### Instrumented independent testing & deep global labs (RTINGS, AnandTech, Tom's Hardware, LTT Labs, Consumer Reports, Wirecutter, Project Farm, GearLab)

**Use for:** calibrated instrument measurements, internal PCB/teardown observations, thermal/noise/power curves, component stepping, and repeatable benchmark test suites.

**Required metadata where possible:** retail vs manufacturer sample, test method, instruments, firmware/revision, sample size, sponsorship/loaner/affiliate relationship.

**Do not infer alone:** population defect rate from one unit; all later revisions/batches are identical.

### Enthusiast communities, repair technicians, and long-term feedback (Reddit r/BuyItForLife, r/HardwareSwap, Head-Fi, Audio Science Review, iFixit, XDA, Chiphell, 酷安, 黑猫投诉)

**Use for:** failure hypotheses, recurring symptom discovery, repairability indices, component interchangeability, and long-term user friction across multi-year lifecycles.

**Do not infer alone:** population failure rate without exposure denominator and deduplication; causality from anecdote alone.
## Source selection rules

1. Start from the **claim**, then choose source role; never start from a favorite website and force it to answer every question.
2. For product identity, prefer regulatory/standardized identifiers over marketplace marketing names.
3. For corporate roles, prefer authoritative registry/certificate data over “About us” pages.
4. For measured performance, prefer transparent independent methods over seller/manufacturer marketing.
5. For safety, prefer official recalls/mandatory actions; use anecdotes as investigation signals.
6. For current price, market sources are appropriate; for historical price, require real temporal history.
7. Record commercial/sample relationships instead of blanket-discarding all sponsored/brand sources.
8. Treat inaccessible authoritative sources as evidence gaps, not permission to upgrade weaker sources silently.

## Current official landing references checked for this engineering pack

Last checked: **2026-08-27**. These are navigation anchors, not permanent guarantees of API/access behavior.

- NMPA UDI database: `https://udi.nmpa.gov.cn/`
- SAMR defect-product recall: `https://www.samr.gov.cn/zlfzj/qxcpzh/`
- SAMR recall query: `https://qxzh.samr.gov.cn/qxzh/qxxxcx/wechat.jsp`
- FCC Change in ID KDB reference: `https://apps.fcc.gov/oetcf/kdb/forms/FTSSearchResultPage.cfm?id=188453&switch=P`
- Bluetooth SIG Qualified Product search: `https://qualification.bluetooth.com/Listings/Search`
- USB-IF Product Search: `https://www.usb.org/products`
- EPREL supplier/model guidance: `https://energy-efficient-products.ec.europa.eu/suppliers_en`
- US CPSC Recalls API information: `https://www.cpsc.gov/Recalls/CPSC-Recalls-Application-Program-Interface-API-Information`
- EU product safety / Safety Gate entry: `https://commission.europa.eu/topics/business-and-industry/product-safety_en`
- GS1 Verified by GS1 service/support: `https://www.gs1.org/services/verified-by-gs1`
- UL Product iQ information: `https://www.ul.com/thecodeauthority`

Every future integration ticket must re-check current access method, licensing/terms, authentication/rate limits, and response semantics before implementing automated retrieval.
