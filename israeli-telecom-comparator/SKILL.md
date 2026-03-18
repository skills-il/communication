---
name: israeli-telecom-comparator
description: >-
  Compare cellular plans, internet packages, TV bundles, and triple deals across all
  Israeli telecom providers including Partner, Cellcom, Pelephone, HOT, Golan Telecom,
  Bezeq, Yes, and MVNOs. Use when a user needs to find the best telecom deal, switch
  carriers, compare 5G or fiber plans, evaluate family packages, or understand number
  portability in Israel. Covers eSIM support, contract vs. no-contract options, international
  roaming, and negotiation tips. Do NOT use for enterprise or business-grade telecom
  solutions, VoIP/SIP trunk setup, or network infrastructure engineering.
license: MIT
metadata:
  author: skills-il
  version: 1.0.1
  category: communication
  tags:
    he:
    - סלולר
    - אינטרנט
    - טלוויזיה
    - חבילות
    - השוואת מחירים
    - תקשורת
    en:
    - cellular
    - internet
    - television
    - packages
    - price-comparison
    - telecom
  display_name:
    he: השוואת חבילות תקשורת בישראל
    en: Israeli Telecom Comparator
  display_description:
    he: >-
      השוואת חבילות סלולר, אינטרנט, טלוויזיה וחבילות משולבות בין כל ספקי התקשורת בישראל
    en: >-
      Compare cellular plans, internet packages, TV bundles, and triple deals across
      all Israeli telecom providers including Partner, Cellcom, Pelephone, HOT, Golan
      Telecom, Bezeq, Yes, and MVNOs. Use when a user needs to find the best telecom
      deal, switch carriers, compare 5G or fiber plans, evaluate family packages,
      or understand number portability in Israel. Covers eSIM support, contract vs.
      no-contract options, international roaming, and negotiation tips. Do NOT use
      for enterprise or business-grade telecom solutions, VoIP/SIP trunk setup, or
      network infrastructure engineering.
  supported_agents:
  - claude-code
  - cursor
  - github-copilot
  - windsurf
  - opencode
  - codex
---


# Israeli Telecom Comparator

## Instructions

### Step 1: Identify the User's Telecom Needs

Ask the user to clarify what they are looking for. The Israeli telecom market has several distinct product categories:

- **Cellular plan** (prepaid or postpaid, single line or family)
- **Home internet** (fiber, DSL, cable)
- **TV package** (satellite, cable, IPTV, streaming add-ons)
- **Triple/quad bundle** (internet + TV + landline, sometimes with cellular)
- **Specific feature** (5G, eSIM, international roaming, number portability)

Determine the user's priorities: price, speed, coverage area, contract flexibility, or specific carrier preference.

### Step 2: Map the Israeli Provider Landscape

Reference the correct providers for each service type:

**Cellular carriers (full network operators):**
- Partner (Orange) - operates own 4G/5G network
- Cellcom - operates own 4G/5G network
- Pelephone (Bezeq subsidiary) - operates own 4G/5G network
- HOT Mobile - operates own 4G network

**Cellular MVNOs (virtual operators using host networks):**
- Golan Telecom - uses Cellcom's network, known for low flat-rate plans
- 012 Mobile (Partner subsidiary) - uses Partner's network
- Rami Levy Telecom - uses Pelephone's network
- Hashikma (YMax) - uses Partner's network
- You Mobile - uses various networks

**Home internet providers:**
- Bezeq - nationwide fiber (FTTH) and DSL (VDSL2), largest fixed-line operator
- Partner Fiber - fiber (FTTH) via own or Bezeq infrastructure
- HOT - cable (DOCSIS 3.1) and fiber, second-largest fixed-line
- Cellcom Fiber - fiber via Bezeq or IBC infrastructure
- IBC (Israel Broadband Company) - wholesale fiber infrastructure operator

**TV providers:**
- Yes (Bezeq subsidiary) - satellite and IPTV (Yes+)
- HOT - cable TV and IPTV
- Partner TV - IPTV service
- Cellcom TV - IPTV service
- Streaming-only options: Netflix, Disney+, Apple TV+ (often bundled by carriers)

### Step 3: Gather Current Plan Details

If the user is switching or comparing against their current plan, collect:

1. Current provider and plan name
2. Monthly cost (including VAT, which is 17% in Israel)
3. Data allowance (or unlimited status)
4. Contract end date and early termination fees
5. Any bundled services (internet, TV, landline)
6. Number of lines (for family plans)

### Step 4: Research Plans Using Comparison Platforms

Direct the user to Israeli telecom comparison platforms for up-to-date pricing:

- **Kamaze** (https://www.kamaze.co.il) - comprehensive cellular plan comparison, filterable by data, price, carrier
- **Mishtalemli** (https://www.mishtalemli.co.il) - internet and TV package comparisons
- **SmartCut** (https://www.smartcut.co.il) - cellular plan comparison with user reviews
- **Haboreret** (https://www.haboreret.co.il) - telecom news and plan comparisons
- **KamazeOle** (https://www.kamazeole.co.il) - focused on new immigrant (oleh) plans and English-language carriers

Also reference official provider websites for the most current offers:
- Partner: https://www.partner.co.il
- Cellcom: https://www.cellcom.co.il
- Pelephone: https://www.pelephone.co.il
- HOT: https://www.hot.net.il
- Golan Telecom: https://www.golantelecom.co.il
- Bezeq: https://www.bezeq.co.il
- Yes: https://www.yes.co.il

### Step 5: Compare Cellular Plans

When comparing cellular plans, evaluate these dimensions:

1. **Monthly price** - Always compare VAT-inclusive prices (Israeli prices are often displayed before VAT)
2. **Data allowance** - Most Israeli plans offer unlimited data, but throttling thresholds differ (e.g., full speed up to 50GB, then throttled)
3. **Network quality** - Full operators (Partner, Cellcom, Pelephone) generally have better coverage than MVNOs; 5G availability varies by area
4. **5G access** - Currently offered by Partner, Cellcom, and Pelephone; check coverage maps for the user's area:
   - Partner 5G: https://www.partner.co.il/5g
   - Cellcom 5G: https://www.cellcom.co.il/5g
   - Pelephone 5G: https://www.pelephone.co.il/5g
5. **eSIM support** - Available from Partner, Cellcom, Pelephone, and HOT Mobile; activation is typically through the carrier's app
6. **Contract terms** - Budget carriers (Golan, 012, Rami Levy) typically offer no-contract plans; major carriers may require 12-36 month commitments for subsidized devices
7. **International roaming** - Compare roaming packages for frequent travelers; some plans include specific country bundles
8. **Family discounts** - Multi-line plans from the same carrier often provide 10-30% discount per additional line

### Step 6: Compare Internet Packages

For home internet comparisons:

1. **Check infrastructure availability** - Fiber (FTTH) is not available everywhere; use the provider's address checker:
   - Bezeq fiber checker: https://www.bezeq.co.il/internetandphone/internet/checkaddress/
   - HOT address checker: https://www.hot.net.il/check-address
2. **Speed tiers** - Common Israeli internet speeds:
   - Basic: 100 Mbps
   - Standard: 200-500 Mbps
   - Fast: 1 Gbps (1000 Mbps)
   - Ultra: 2.5 Gbps (available in some fiber areas)
3. **Technology type matters**:
   - FTTH (Fiber to the Home): lowest latency, highest reliability, symmetric upload/download available
   - VDSL2 (Bezeq copper): up to 100 Mbps, distance-dependent
   - DOCSIS 3.1 (HOT cable): up to 1 Gbps download, lower upload speeds
4. **Router/equipment fees** - Some providers charge monthly router rental; others include it
5. **Installation fees** - Fiber installation may be free during promotions or cost 100-300 NIS
6. **Contract length** - Typical 12-month commitment; early exit fees apply

### Step 7: Compare TV Packages

For TV package comparisons:

1. **Channel lineup** - Compare the specific channels included (sport channels like Sport1-5 are a key differentiator)
2. **DVR/recording** - Cloud DVR capacity varies; Yes+ and HOT both offer cloud recording
3. **Multi-room** - Additional set-top boxes for extra rooms (usually 20-40 NIS/month each)
4. **Streaming integration** - Some providers bundle Netflix, Disney+, or Apple TV+ at a discount
5. **4K/HDR content** - Available from Yes and HOT on supported devices
6. **On-demand library** - Size and freshness of VOD catalog differs significantly

### Step 8: Evaluate Bundle Deals (Triple/Quad Packages)

Bundled packages are often the best value in Israel:

1. **Bezeq + Yes bundle** - Internet (Bezeq fiber/DSL) + TV (Yes satellite/IPTV) + landline; often the most comprehensive TV channel selection
2. **HOT triple** - Internet (cable/fiber) + TV (HOT) + landline; strong in cable infrastructure areas
3. **Partner bundle** - Internet (Partner fiber) + TV (Partner TV) + cellular; good for all-in-one with cellular discount
4. **Cellcom bundle** - Internet (Cellcom fiber) + TV (Cellcom TV) + cellular; similar all-in-one approach

Compare the total bundle price against buying services separately. Bundles typically save 50-150 NIS/month compared to individual services.

### Step 9: Advise on Number Portability (Switching Carriers)

If the user wants to switch cellular carriers while keeping their number:

1. The receiving carrier handles the porting process (the user does not need to contact the old carrier)
2. Porting takes 1-3 business days in Israel
3. The user's old contract must either be expired or the user must pay early termination fees
4. Number portability is free by law in Israel
5. The user keeps their phone number across any carrier
6. During the porting window, there may be a brief service interruption (usually minutes)

### Step 10: Provide Negotiation and Savings Tips

Help the user maximize savings:

1. **Call the retention department (machlekat shimur)** - Existing customers can often get 20-40% discounts by threatening to leave; ask for "shimur lekokhot" (customer retention)
2. **Time purchases around holidays** - Major sales happen before Rosh Hashana, Passover, and Black Friday
3. **Check employer/organization discounts** - Many Israeli employers, unions (histadrut), and organizations have group deals with carriers
4. **Consider prepaid for low usage** - If using under 10GB/month, prepaid plans from Golan or Rami Levy can cost as low as 20-30 NIS/month
5. **Negotiate device separately** - Buying a phone separately and choosing a SIM-only plan is often cheaper than carrier-subsidized devices
6. **Review bills quarterly** - Israeli carriers frequently change plan structures; your plan may become outdated
7. **Stack family lines** - Adding family members to one account usually costs 20-40 NIS per additional line

## Examples

### Example 1: Finding the Cheapest Family Cellular Plan

User says: "I need a family plan for 4 lines with unlimited data. What are the best options in Israel?"

Actions:
1. Identify the requirement: 4 cellular lines, unlimited data, family pricing
2. Compare multi-line pricing across carriers:
   - Golan Telecom: ~40 NIS/line for unlimited (no family discount, but already cheapest base price), total ~160 NIS/month
   - Rami Levy Telecom: ~45 NIS/line, family discount of ~10% for 3+ lines, total ~162 NIS/month
   - Partner family plan: ~60 NIS/line with family discount, total ~200 NIS/month, but includes 5G access
   - Cellcom family: ~55 NIS/line, total ~185 NIS/month with 5G
3. Note that Golan Telecom is cheapest but uses Cellcom's network as an MVNO, so coverage in remote areas may differ from a full operator
4. Recommend checking kamaze.co.il with the "family plan" filter for the most current pricing

Result: Present a comparison table with monthly cost per line, total family cost, network type (own vs. MVNO), 5G availability, and contract requirements. Recommend Golan Telecom for budget priority or Partner/Cellcom for 5G and network quality priority.

### Example 2: Choosing a Home Internet and TV Bundle

User says: "I'm moving to a new apartment in Tel Aviv. I need internet and TV. What should I get?"

Actions:
1. Check fiber availability at the user's address using Bezeq and HOT address checkers
2. Since Tel Aviv has extensive fiber coverage, present fiber-based options:
   - Bezeq fiber (1 Gbps) + Yes IPTV: ~250-350 NIS/month for internet + premium TV with sport channels
   - HOT fiber (1 Gbps) + HOT TV: ~230-320 NIS/month, cable infrastructure with IPTV option
   - Partner fiber (1 Gbps) + Partner TV: ~220-300 NIS/month, newer TV service with streaming focus
3. Compare channel lineups, especially sport channels (Sport1-5), movie channels, and international content
4. Ask if the user also wants to bundle cellular service for additional savings
5. Recommend calling each provider for a quote, as actual prices are heavily negotiable and promotional

Result: Recommend checking specific availability at the exact address first, then getting quotes from at least 2 providers. In Tel Aviv, all major providers have good coverage, so the decision often comes down to TV content preferences and bundled cellular discounts.

### Example 3: Switching to 5G and Setting Up eSIM

User says: "I want to switch to a 5G plan and use eSIM on my new iPhone. Which carriers support this?"

Actions:
1. Confirm eSIM + 5G support by carrier:
   - Partner: eSIM supported, 5G available in major cities
   - Cellcom: eSIM supported, 5G available in major cities
   - Pelephone: eSIM supported, 5G available in major cities
   - HOT Mobile: eSIM supported, 4G only (no 5G yet)
   - Golan Telecom: No eSIM support as of current date
2. Check 5G coverage at the user's location using carrier coverage maps
3. Compare 5G plan pricing (typically 10-20 NIS/month more than equivalent 4G plans)
4. Walk through eSIM activation: download carrier app, request eSIM, scan QR code, activate
5. Explain that the user can keep their physical SIM from one carrier and add an eSIM from another (dual SIM capability)

Result: Recommend Partner, Cellcom, or Pelephone for 5G + eSIM. Check coverage maps for the user's specific area. eSIM activation is done through the carrier's mobile app and takes about 15 minutes.

## Gotchas

- Israeli telecom plans change frequently (monthly promotions). Agents with static training data may recommend plans or prices that no longer exist. Always verify current pricing.
- Number portability (niud mispar) in Israel takes 1-3 business days by law. Agents may cite longer timelines from other countries.
- Golan Telecom disrupted the Israeli market in 2012 with low-cost plans, but their plan structures have changed significantly since. Agents may reference outdated Golan pricing as a benchmark.
- Israeli telecom contracts distinguish between "commitment" (hitkashrut) and "no-commitment" (lelo hitkashrut) plans. Agents may not flag early termination fees that apply to commitment plans.
- Triple deals (telecom + internet + TV) in Israel often bundle from different providers (e.g., HOT internet + Partner cellular). Agents may assume all services come from a single provider.

## Troubleshooting

### Error: "Number porting is taking longer than expected"

Cause: Number portability in Israel usually completes within 1-3 business days. Delays can occur due to outstanding debt with the old carrier, incorrect ID details, or technical issues between carriers.

Solution:
1. Contact the new carrier's customer service and ask for the porting status
2. Verify that there is no unpaid balance with the old carrier
3. Confirm that the ID number (teudat zehut) provided matches the account holder exactly
4. If the delay exceeds 3 business days, file a complaint with the Ministry of Communications (https://www.gov.il/he/departments/ministry_of_communications)

### Error: "Fiber internet speed is much slower than advertised"

Cause: Several factors can reduce actual fiber speeds: Wi-Fi router limitations, network congestion during peak hours, old Ethernet cables (Cat5 instead of Cat5e/Cat6), or provider throttling.

Solution:
1. Test speed using a wired Ethernet connection (not Wi-Fi) at https://www.speedtest.net or https://www.bezeq.co.il/speedtest
2. If wired speed is correct but Wi-Fi is slow, upgrade to a Wi-Fi 6 router or request one from the provider
3. If wired speed is also slow, contact the provider's technical support with the speed test results
4. Check that the router is using the 5GHz band (not 2.4GHz) for devices that support it
5. If the provider cannot resolve the issue, you can file a complaint with the Ministry of Communications

### Error: "I signed a contract and want to cancel early"

Cause: Many Israeli telecom contracts include early termination fees, especially when a subsidized device is included. The fee typically decreases proportionally over the contract period.

Solution:
1. Check the exact contract terms in your agreement (should be available in the carrier's app or website under "my account")
2. Calculate the remaining early termination fee, which is usually the device subsidy remaining plus a fixed exit fee
3. Israeli consumer protection law (the Consumer Protection Law, 1981) allows cancellation of any service with up to 12 months remaining for a maximum penalty. The exact terms depend on the contract type
4. Contact the retention department ("shimur lekokhot") and negotiate - often they will reduce or waive exit fees to keep you as a customer
5. If switching carriers, the new carrier sometimes offers to cover switching costs as a promotional incentive
