---
name: israeli-telecom-comparator
description: Compare cellular plans, internet packages, TV bundles, and triple deals across all Israeli telecom providers including Partner, Cellcom, Pelephone, HOT, Golan Telecom, Bezeq, Yes, and MVNOs. Use when a user needs to find the best telecom deal, switch carriers, compare 5G or fiber plans, evaluate family packages, or understand number portability in Israel. Covers eSIM support, contract vs. no-contract options, international roaming, and negotiation tips. Do NOT use for enterprise or business-grade telecom solutions, VoIP/SIP trunk setup, or network infrastructure engineering.
license: MIT
---


# Israeli Telecom Comparator

## Instructions

### Step 1: Identify the User's Telecom Needs

Ask the user to clarify what they are looking for. The Israeli telecom market has several distinct product categories:

- **Cellular plan** (prepaid or postpaid, single line or family)
- **Home internet** (fiber, DSL, cable)
- **TV package** (satellite, cable, IPTV, streaming add-ons)
- **Triple/quad bundle** (internet + TV + landline, sometimes with cellular)
- **Specific feature** (5G, eSIM, roaming, number portability)

Then establish priorities: price, speed, coverage, contract flexibility, or a carrier preference.

### Step 2: Map the Israeli Provider Landscape

Reference the correct providers for each service type:

**Cellular carriers with their own radio network:**
- Partner - facilities-based operator
- Cellcom - facilities-based operator
- Pelephone (Bezeq subsidiary) - facilities-based operator
- HOT Mobile - a network operator, but it does not run a separate radio network of its own: it shares one with Partner. Treat Partner and HOT Mobile as a single coverage footprint

Partner and HOT Mobile share one radio network, so their coverage footprint is effectively the same. HOT Mobile itself is being sold to a Delek Israel / Keystone / Leumi Partners consortium at an enterprise value of NIS 1.8 billion; the Competition Authority cleared the merger on 5 August 2026. Whether the deal has closed, whether the HOT Mobile brand survives it, and what happens to HOT bundles that include mobile are all unsettled at the time of writing, so confirm before recommending a HOT triple that includes a cellular line.

**Cellular operators riding a host network (virtual operators and shared-network operators):**
- wecom - holds its own licence and spectrum but shares Cellcom's radio network (MOCN). Pelephone signed a non-binding MOU in July 2026 to buy it, so its independence may not last
- Golan Telecom - Cellcom-owned since 2020, rides Cellcom's network, known for low flat-rate plans
- Rami Levy Communications - rides Pelephone's network
- 019 Mobile - rides Partner's network (the shared Partner/HOT Mobile radio)
- Expon (Xphone) - rides the shared Partner/HOT Mobile radio
- Neptucom - rides the Pelephone and Partner networks
- Walla Mobile - rides HOT Mobile
- 012 Mobile (Partner) - Partner began folding this brand into Partner itself in March 2024; treat any 012 quote as a Partner plan

A virtual operator's coverage is its HOST's coverage. "MVNO" says something about price and customer service, not about where the signal reaches.

**Home internet providers:**
- Bezeq - the incumbent fixed-line operator, selling both fiber and copper-based service depending on the address
- Partner Fiber - fiber, partly on its own build and partly leased; confirm which infrastructure actually serves the address
- HOT - cable and fiber
- Cellcom Fiber - fiber, likewise a mix of own and leased infrastructure; confirm per address
- IBC - a fiber infrastructure operator selling wholesale to retail ISPs rather than direct to most households

**TV providers:**
- Yes (Bezeq subsidiary) - satellite and IPTV (Yes+)
- HOT - cable TV and IPTV
- Partner TV - IPTV service
- Cellcom TV - IPTV service
- Streaming-only: Netflix, Disney+, Apple TV+, often bundled by carriers

### Step 3: Gather Current Plan Details

If the user is switching or comparing against their current plan, collect:

1. Current provider and plan name
2. Monthly cost (including VAT, 18% in Israel)
3. Data allowance, or unlimited status
4. Contract end date, and the balance still owed on any subsidised device (this, not an exit fee, is what a commitment actually costs to leave; see Step 10)
5. Bundled services (internet, TV, landline)
6. Number of lines

### Step 4: Research Plans Using Comparison Platforms

Direct the user to Israeli telecom comparison platforms for up-to-date pricing:

- **Kama Ze** (https://www.kamaze.co.il) - cellular plans, filterable by data, price and operator
- **Mishtalem Li** (https://www.mishtalemli.co.il) - internet and TV packages
- **SmartCut** (https://www.smartcut.co.il) - cellular plans with reviews, and per-brand pages naming each operator's host network
- **Haboreret** (https://www.haboreret.co.il) - telecom news and comparisons
- **Kama Ze Ole** (https://www.kamazeole.co.il) - telecom packages, useful to olim and English speakers

Also reference official provider websites for the most current offers:
- Each operator publishes its own coverage map; reach it from the operator's own site rather than a saved deep link, since these operators run single-page sites whose URLs change
- HOT: http://www.hot.net.il
- Golan Telecom: https://www.golantelecom.co.il
- Bezeq: https://www.bezeq.co.il

### Step 5: Compare Cellular Plans

When comparing cellular plans, evaluate these dimensions:

1. **Monthly price** - Consumer telecom prices in Israel are normally advertised VAT-inclusive (VAT is 18%). A price quoted before VAT is a signal you are being shown a business tariff, so establish which you are looking at before comparing, and never gross up a consumer price by default
2. **Data allowance** - Most Israeli plans offer unlimited data, but throttling thresholds differ (e.g., full speed up to 50GB, then throttled)
3. **Network quality** - Coverage is a property of the HOST network, not of the brand: a virtual operator riding Cellcom has Cellcom's coverage. What differs between a budget brand and its host is priority during congestion, customer service, and which extras (5G, eSIM, roaming) are resold. Compare hosts, not logos; 5G availability varies by area
4. **5G access** - Offered by Partner, Cellcom, Pelephone, and HOT Mobile; coverage is broad in built-up areas and patchier outside them, but do not quote a coverage claim you have not read off the operator's own map on the day. Check the map for the user's area:
   - Each operator publishes its own 5G coverage map; find it from the operator's site navigation
5. **2G/3G wind-down (IN PROGRESS, not complete)** - on 1 February 2026 the operators vacated the first-GHz bands that carried 2G/3G, for reuse by 4G/5G. That was the FIRST STAGE only: the Ministry of Communications separated frequency-vacating from service closure, and the legacy networks continue to operate in reduced form on other frequencies. Dialling the emergency centres (100, 101, 102) from old handsets stays available until the end of 2028, (the skill does not assert what network arrangement the Ministry will mandate to deliver that; the notice does not say). Coverage quality on old devices may degrade, so still confirm VoLTE support before recommending a SIM-only plan, but do NOT tell a user their feature phone, alarm panel or elevator emergency line has already stopped working.
6. **eSIM support** - Widely available, activation typically through the carrier's app. Do not assert from memory which operators do and do not support it, in either direction; read it off the operator's own eSIM page on the day
7. **Contract terms** - Budget carriers (Golan, 012, Rami Levy) typically offer no-contract plans; major carriers tie a subsidised device to a commitment period, so read the term off the specific offer rather than assuming a standard length
8. **International roaming** - Compare roaming packages for frequent travellers; some plans include specific country bundles. Three protections are worth stating outright, because roaming is where four-figure bills happen: data roaming is blocked by default unless the subscriber has separately and explicitly agreed to the terms of receiving it, though that consent is routinely taken at sign-up, so have the user confirm with the operator before travelling that the block is actually in force on their line rather than assuming the default holds; voice roaming can be blocked on request, which the operator must action within one business day; and the subscriber may at any time set a maximum spend after which the service is cut off. Premium services are a separate matter: an operator may not supply a premium service to a mobile destination at all, and may only bill for one delivered to a fixed line
9. **Family discounts** - Multi-line plans from the same carrier are usually cheaper per line than the same number of separate plans; get the per-line price in writing rather than the headline bundle price

### Step 6: Compare Internet Packages

For home internet comparisons:

1. **Understand that home internet is TWO products, not one.** Israeli households buy infrastructure (the physical line: Bezeq, HOT, IBC) and an internet service provider, and they can be bought either as two separate contracts with two bills, or as a single wholesale-market package where the ISP leases the infrastructure and bills you once. Establish which the user has before comparing anything: it determines how many contracts they must cancel, and cancelling one half while the other keeps billing is a common and expensive mistake. The infrastructure, not the ISP brand, sets the speed ceiling available at the address, so switching ISP alone will not raise it
2. **Check infrastructure availability** - Fiber (FTTH) is not available everywhere; use the provider's address checker when available
3. **Speed tiers** - Providers publish a ladder of speeds from a basic tier up to multi-gigabit fiber. Read the current tier list off each provider's own package page rather than assuming a fixed ladder; the tiers are renamed and re-priced often.
4. **Technology type matters**:
   - FTTH (Fiber to the Home): lowest latency, highest reliability, symmetric upload/download available
   - VDSL2 over copper: the slowest of the three, and distance-dependent, so the speed sold is not always the speed delivered
   - DOCSIS cable: the standard supports far more downstream than upstream, so cable plans are asymmetric; the ceiling actually sold is set by the operator's package, not by the standard. Establish which of the three technologies actually serves the address rather than inferring it from the provider's name
5. **Router/equipment fees** - Some providers charge monthly router rental; others include it
6. **Installation fees** - Fiber installation is sometimes waived during promotions and sometimes charged; ask for the installation fee in writing before signing
7. **Contract length** - A commitment period is normal, but it does not carry an exit fee for a household subscriber (see Step 10). What a commitment actually binds is the promotional price and any equipment you are paying off

### Step 7: Compare TV Packages

For TV package comparisons:

1. **Channel lineup** - Compare on the specific league or competition the user actually wants, not on a channel name: sports rights move between providers at each rights cycle, so a channel that carried a league last season may not carry it now
2. **DVR/recording** - Cloud DVR capacity varies
3. **Multi-room** - Additional set-top boxes for extra rooms carry a separate monthly fee per box; ask for the per-box price
4. **Streaming integration** - Some providers bundle Netflix, Disney+ or Apple TV+ at a discount
5. **4K/HDR content** - Check per provider and per device
6. **On-demand library** - VOD catalogue size and freshness differ significantly
7. **Do not assume TV must come from the line owner** - an over-the-top TV service runs over any internet connection, so "bundle or separate" is a three-way comparison: the infrastructure owner's TV, another provider's TV over the same line, or no TV subscription at all

### Step 8: Evaluate Bundle Deals (Triple/Quad Packages)

Bundled packages are often the best value in Israel:

The four large groups each sell a triple: Bezeq with Yes, HOT, Partner and Cellcom. Partner's and Cellcom's fold in cellular; Bezeq/Yes and HOT are the traditional internet plus TV plus landline shape.

Compare the total bundle price against buying the same services separately, and remember from Step 10 that a bundled rate can revert when you drop one of its legs. Only the two quotes side by side will tell you the real gap.

### Step 9: Advise on Number Portability (Switching Carriers)

If the user wants to switch cellular carriers while keeping their number:

1. The receiving carrier handles the porting process (the user does not need to contact the old carrier)
2. **Porting is fast, not a multi-day wait.** The Ministry of Communications numbering plan caps the actual carrier switch at half an hour for a mobile number and one hour for a fixed line, and at three hours where the number is one of a whole block. The Communications Law sets an outer bound of one business day. What can take longer is the receiving carrier's own sign-up steps (ID checks, credit, SIM or eSIM delivery) before the port is even submitted, so quote that as the variable, never the port itself
3. The user does NOT have to wait out a commitment to port. Porting is available on request; it simply does not erase what is still owed to the abandoned provider (see Step 10)
4. Number portability is free by law in Israel, and the abandoned carrier may not charge for it either
5. The user keeps their phone number across any carrier
6. During the porting window, there may be a brief service interruption (usually minutes)
7. **Never cancel the old line first.** Cancel it and the number is released, and there is nothing left to port. The receiving carrier's porting notice is what disconnects the abandoned provider, and it does so immediately on receipt
8. **A completed port ends the SERVICE, not the debt.** The abandoned provider stops serving that number, but outstanding device instalments and any contractual monthly payment for the commitment period survive the port. Read that together with Step 10, which is what limits those charges
9. **A debt or a live commitment is NOT a lawful ground to refuse a port.** The numbering rules say so expressly. The permitted grounds are narrow: the subscriber is not held by that provider, an earlier porting notice for the same subscriber is still being processed, a malformed number, a written block requested by a business subscriber on its own number, and a prepaid number with less than NIS 30 of cumulative top-ups. If a carrier blocks a port over a balance, quote this

### Step 10: Get the Exit Rules Right Before Recommending a Commitment

This is the single most misunderstood area of Israeli telecom, and getting it wrong costs the user real money. The governing rule is in the Communications Law, not the Consumer Protection Law:

1. **There is no exit fee.** Under Communications Law section 51A, a cellular subscriber who cancels owes the operator no payment for cancelling, and the operator may not withhold from them a benefit they would have received but for the cancellation. Section 51A covers any cellular engagement of up to one hundred phone lines, with no bill ceiling, so a small business on a plain cellular contract is protected too. Section 51D covers a licensed provider (internet, fixed line, broadcasting) and any combined bundle, but there it is limited to a subscriber whose average monthly bills are under NIS 5,000, so a large bundled account can fall outside. Note the routing rule: if the cellular line sits inside a bundle, section 51D governs it, not 51A.
2. **The limit of that.** A price whose stated condition was the very service or line you dropped may lawfully revert: a bundle rate that assumed three services, a per-line rate that assumed five lines. What the operator may NOT do is withdraw a benefit on the services you kept because you cancelled another. Price the switch on what the remaining services will actually cost.
3. **What the operator MAY still collect** is the remaining instalments on terminal equipment the user bought (a subsidised handset, a router) plus debts already accrued. Section 51B bars the operator from accelerating those instalments: the user keeps paying the device off on the original schedule, at the original amounts, after cancelling the service.
4. **Ignore the "8 percent times the months remaining" formula.** That ceiling existed only between 2011 and 2012 and was deleted by amendment 53. Israeli consumer sites still republish it; it is not the law.
5. **Cancellation takes effect within three business days** of the notice, or six if it was sent by registered mail (Consumer Protection Law section 13D(c)). Billing should stop accordingly.
6. **Separately, a phone-sold or online subscription can be cancelled outright as a distance sale**: fourteen days for an ordinary consumer, and four months for a consumer aged 65 or over, a person with a disability, or a new immigrant, where the deal involved an actual conversation with the seller.

7. **You can cancel by the same route you signed up.** A provider that lets customers sign up online must place a prominent, dedicated cancellation link on its home page (Consumer Protection Law section 14I), and cancellation may also be given by phone or in person. Once notice is given, the provider must disconnect no later than the business day after the notice, and may not charge for the disconnection itself. This next-business-day duty is the one to quote at the provider; the three-business-day figure in point 5 is the outer bound for the contract ending, not a licence to keep billing you for three days. If a call centre stalls you, the statutory wait for a human agent on fault, billing and termination calls is six minutes, and you may not be pushed to voicemail unless you choose it.

Practical consequence for a comparison: the "commitment vs no commitment" axis in Israel is mostly about the device and the promotional price, not about being trapped. Say so, and price the device separately.

### Step 11: Provide Negotiation and Savings Tips

Help the user maximize savings:

1. **Call the retention department (machlekat shimur)** - Existing customers can often get a better rate by saying they intend to leave; ask for "shimur lekokhot" (customer retention). How much is on offer varies by carrier, tenure and the competing quote you can name, so bring one
2. **Time purchases around holidays** - Major sales happen before Rosh Hashana, Passover, and Black Friday
3. **Check employer/organization discounts** - Employers, unions and other organizations often hold group deals with carriers
4. **Consider prepaid for low usage** - Light users are often better off on a prepaid or small-data plan from a budget operator than on an unlimited plan
5. **Negotiate device separately** - Buying a phone separately and choosing a SIM-only plan is often cheaper than carrier-subsidised devices. A carrier-locked handset is not a constraint you have to accept: Communications Law section 51C forbids a provider or a terminal-equipment dealer from restricting a device to one network at all, including by pricing. There is no "pay the device off first" condition on that
6. **Review bills periodically** - Carriers restructure plans often, so a plan that was competitive becomes outdated in place
7. **Stack family lines** - One account is normally cheaper per line than separate accounts; ask for the per-additional-line price

## Examples

### Example 1: Finding the Cheapest Family Cellular Plan

User says: "I need a family plan for 4 lines with unlimited data. What are the best options in Israel?"

Actions:
1. Identify the requirement: 4 lines, unlimited data, family pricing
2. Compare multi-line pricing:
   - Budget virtual operators (Golan Telecom, Rami Levy Communications and others): typically the cheapest per-line base price, sometimes with a small multi-line discount; confirm on the day rather than assuming which is cheapest
   - Facilities-based operators (Partner, Cellcom, Pelephone): usually a higher per-line price
   - Pull the current per-line price from the operator's own page or a comparison platform on the day; Israeli cellular pricing changes month to month
3. Do NOT tell the user a budget brand has worse coverage. Golan rides Cellcom, so its coverage IS Cellcom's. What can differ is priority during congestion, customer service, and whether 5G, eSIM and roaming are resold on that plan. Check those, not the map
4. Recommend checking comparison platforms with the "family plan" filter for the most current pricing

Result: Present a table with cost per line, total family cost, host network, 5G availability and contract terms. Frame the trade-off honestly: a budget brand on a given host has that host's coverage, so the premium buys service, congestion priority and resold extras, not reach.

### Example 2: Choosing a Home Internet and TV Bundle

User says: "I'm moving to a new apartment in Tel Aviv. I need internet and TV. What should I get?"

Actions:
1. Check fiber availability at the exact address using the providers' address checkers
2. Present the fiber-based options available there:
   - Bezeq fiber with Yes, HOT fiber with HOT TV, Partner fiber with Partner TV
   - Quote all three at the exact address on the day; bundle prices are promotional and negotiable
3. Compare channel lineups on the specific leagues, competitions and content the user names, not on channel numbers
4. Ask whether the user also wants cellular in the bundle
5. Get a quote from each by phone; prices are promotional and negotiable

Result: Check availability at the exact address first, then get quotes from at least two providers. Where all of them serve the address, the decision usually comes down to content and bundled cellular discounts.

### Example 3: Switching to 5G and Setting Up eSIM

User says: "I want to switch to a 5G plan and use eSIM on my new iPhone. Which carriers support this?"

Actions:
1. Confirm eSIM and 5G support on each candidate operator's own eSIM page, on the day. Do not answer this from training data in either direction: capability claims about named operators go stale, and a stale negative is the costlier error because it pushes a price-sensitive user off a cheaper option. Budget brands are not automatically excluded (Golan Telecom, for one, documents eSIM activation on its own site)
2. Check 5G coverage at the user's location on the operator's own map, and resolve the host network first: a virtual operator's coverage is its host's
3. Compare the 5G plan against the equivalent 4G plan from the same operator; the premium varies by operator and promotion
4. Walk through eSIM activation: download the carrier app, request the eSIM, scan the QR code, activate. The user can also keep a physical SIM from one carrier and add an eSIM from another

Result: Confirm eSIM and 5G on each candidate operator's own page rather than ruling a carrier out from memory. eSIM activation is done through the carrier's mobile app.

## Gotchas

- Israeli telecom plans change frequently (monthly promotions). Agents with static training data may recommend plans or prices that no longer exist. Always verify current pricing.
- Number portability (niud mispar) in Israel is capped at half an hour for a mobile number, not days. Agents routinely import multi-day porting timelines from other countries, or repeat the older "1 to 3 business days" figure. Quote the receiving carrier's sign-up steps as the variable instead.
- Golan Telecom disrupted the Israeli market in 2012 with low-cost plans, but their plan structures have changed significantly since. Agents may reference outdated Golan pricing as a benchmark.
- Israeli telecom contracts distinguish between "commitment" (hitkashrut) and "no-commitment" (lelo hitkashrut) plans, but under Communications Law sections 51A and 51D there is no exit fee for an ordinary household subscriber. Agents trained on other markets, and Israeli sites still republishing the repealed 8 percent formula, will invent a penalty that does not exist. Only the remaining device instalments and accrued debts survive cancellation, and they may not be accelerated.
- A brand is not a network. Golan rides Cellcom, 019 and Expon ride Partner/HOT, Walla rides HOT Mobile, Neptucom rides Pelephone and Partner, and wecom rides Cellcom despite holding its own licence. An agent comparing "coverage by carrier" without resolving the host will produce a table that is simply wrong.
- Triple deals (telecom + internet + TV) in Israel often bundle from different providers (e.g., HOT internet + Partner cellular). Agents may assume all services come from a single provider.
- The 2G/3G wind-down is staged and NOT finished. The first-GHz bands were vacated on 1.2.2026; the old networks still run on other frequencies, and emergency dialling from legacy handsets is guaranteed to the end of 2028. Treat an old alarm panel, GPS tracker or elevator line as at RISK of degraded coverage and on a deadline, not as already disconnected.
- "5G" on an Israeli plan may be Standalone (SA) or Non-Standalone (NSA), and NSA still anchors to a 4G control plane, so it does not deliver the full 5G latency benefit. The skill does not assert any operator's current SA status: if a user is specifically chasing low-latency 5G (gaming, AR), have them ask the carrier whether the plan and their coverage area are SA, and treat any answer from training data as unreliable.
- VoLTE and VoWiFi are now the default voice paths as the legacy networks wind down. Older 4G-only handsets may have spotty VoLTE on some Israeli carriers, and the skill does not carry a device cutoff list; verify the specific model on the carrier's own compatible-device list before recommending.
- WhatsApp calling has largely replaced premium international voice minutes for personal use. Carriers still sell international call packages, but for someone calling family abroad in WhatsApp-using countries, the value is mostly mobile-data quality (5G coverage at home and roaming abroad), not voice minutes.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Ministry of Communications (משרד התקשורת) | https://www.gov.il/he/departments/ministry_of_communications | Official rules on number portability, complaints, 5G policy, 2G/3G shutdown announcements |
| Consumer Protection Authority, telecom guidance | https://www.gov.il/he/pages/cpfta_consumers_communication | What a provider must disclose at the point of sale, and how to complain |
| Communications Law (Telecommunications and Broadcasts), consolidated | https://www.nevo.co.il/law_html/law01/032_002.htm | Section 5A(f) portability duty, sections 51A / 51B / 51D on cancellation, exit payments and device instalments |
| Ministry of Communications numbering plan, portability | https://www.gov.il/BlobFolder/policy/05082018_2/en/The_numbering_plan-02-2023-mobility.pdf | Maximum permitted porting times |
| Partner | Operator's own site | Cellular plans, fiber, TV, 5G coverage map |
| Cellcom | Operator's own site | Cellular plans, Cellcom Fiber, Cellcom TV, 5G coverage map |
| Pelephone | Operator's own site | Cellular plans, 5G coverage map |
| HOT (cable + mobile) | https://www.hot.net.il | HOT Mobile plans, cable internet, HOT TV, fiber checker |
| Bezeq | https://www.bezeq.co.il | Fiber/DSL home internet, address fiber checker |
| Yes (satellite/IPTV) | https://www.yes.co.il | TV channel lineup, Yes+ streaming |
| Golan Telecom (MVNO on Cellcom) | https://www.golantelecom.co.il | Low-cost no-contract plans |
| Rami Levy Communications (MVNO on Pelephone) | https://mobile.rami-levy.co.il/ | Budget cellular plans |
| 019 Mobile (MVNO) | Operator's own site | International calling and budget cellular |
| SmartCut comparison | https://www.smartcut.co.il | Crowd-sourced cellular plan comparisons and reviews |

## Troubleshooting

### Error: "Number porting is taking longer than expected"

Cause: The carrier switch itself is capped at half an hour for a mobile number (one hour for a fixed line, three hours for a number inside a whole block), with a statutory outer bound of one business day. So a wait measured in days is almost never the port; it is the receiving carrier not having submitted it yet. Common blockers are an unpaid balance with the old carrier, ID details that do not match the account holder, or a SIM or eSIM that has not been activated.

Solution:
1. Ask the RECEIVING carrier whether the porting request has actually been submitted, and on what date. This is the question that separates the two failure modes
2. Verify that there is no unpaid balance with the old carrier
3. Confirm that the ID number (teudat zehut) provided matches the account holder exactly
4. If the request was submitted more than one business day ago, cite the numbering plan's time limits to the carrier, and complain to the Ministry of Communications through their official channels

### Error: "Fiber internet speed is much slower than advertised"

Cause: Usually the home network rather than the line: Wi-Fi limits, peak-hour congestion, old cabling. It can also be the access technology, since a copper-based service is distance-dependent and cable is asymmetric by design, so the sold speed was never the delivered speed.

Solution:
1. Test over a wired connection, not Wi-Fi, at https://www.speedtest.net. This is the test that separates the two causes
2. Wired speed fine, Wi-Fi slow: it is the home network, not the provider
3. Wired speed also slow: take the result to the provider's technical support, and confirm which technology actually serves the address before accepting that the speed is normal for the package
4. If the provider will not resolve it, complain to the Ministry of Communications

### Error: "I signed a contract and want to cancel early"

Cause: The user has usually been told, by the carrier or by an out-of-date web page, that leaving early triggers a penalty. For an ordinary household subscriber in Israel it does not. Communications Law section 51A (cellular) and section 51D (fixed line, internet, broadcasting, and combined bundles, where the average monthly bill is under NIS 5,000) bar the provider from charging anything for cancellation or withdrawing a benefit because of it.

Solution:
1. Cancel in writing and keep the notice. The contract ends within three business days, or six if you sent it by registered mail
2. Expect a bill only for two things: instalments still outstanding on equipment you bought, and debts already accrued. Nothing else is lawful
3. If the carrier demands the device balance in one payment, refuse: section 51B bars accelerating it. You continue paying the original instalments on the original dates
4. If you are quoted a percentage-based exit fee, ask which section of the Communications Law authorises it. The 8 percent formula many sites still publish was repealed in 2012
5. If the deal was sold to you by phone or online, you may also have a straight distance-sale cancellation right: fourteen days, or four months if you are 65 or over, a person with a disability, or a new immigrant and the sale involved a conversation
6. Escalate an unlawful charge to the Ministry of Communications, and the retention department is still worth a call if you would rather stay on a better price