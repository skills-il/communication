# Israeli holiday gate: deriving the Hebcal query

Reference for Step 6 of SKILL.md. Every statement here was confirmed by enumerating the live Hebcal feed for 2026-01-01 to 2026-12-31 on 2026-08-19, not by reading the API docs.

**No single flag or `subcat` value means "Israeli day off", so the query above is an allowlist minus an exclusion.** Each of the following was confirmed by enumerating the full 2026 feed, not by reading the docs:

- **`category` is useless as a filter.** With `min=on`, 2 February 2026 returns Tu BiShvat as `subcat: "minor"`, an ordinary working day, as do Lag BaOmer and Tu B'Av. Drop `min=on` entirely.
- **`subcat: "major"` is necessary but far too broad.** It carries the real chagim and their erevs, but the 2026 feed also files all nine Chanukah days and all ten Chol HaMoed days (`Pesach II (CH''M)` and friends) under it. Chanukah and Chol HaMoed are working days in Israel, with reduced hours at most. Selecting `major` wholesale suppresses business mail for nine consecutive days in December, which is the same defect as the Tu BiShvat case one bullet up. Hence the title exclusion.
- **Do NOT add `mf=on`.** It adds exactly five fast days for 2026 (Ta'anit Esther, Ta'anit Bechorot, Tzom Tammuz, Tzom Gedaliah, Asara B'Tevet) and **all five are ordinary working days**. The two fasts that actually stop work, Yom Kippur and Tish'a B'Av, never carry `subcat: "fast"` at all; they already arrive under `major`. A `subcat=="fast"` branch is either dead code without the flag or actively wrong with it.
- **`mod=on` mixes days off with working days.** Modern holidays arrive as `subcat: "modern"`, and the 14 entries in 2026 include Yom HaZikaron and Yom HaAtzma'ut (genuine days off) alongside Hebrew Language Day, Family Day, Yom HaAliyah, Yom HaShoah, Herzl Day and Sigd (working days). Match the two by title.
- `nx=on` adds Rosh Chodesh under `category: "roshchodesh"` with no `subcat` at all. Working days, so the flag is omitted.

With those choices the 2026 feed yields exactly 20 blocking dates: each chag and its erev (Purim, Pesach I and VII, Shavuot, Tish'a B'Av, Rosh Hashana I and II, Yom Kippur, Sukkot I, Hoshana Raba, Shmini Atzeret), plus Yom HaZikaron and Yom HaAtzma'ut. Erev chag arrives as `subcat: "major"`; treat it like Friday and do not send after ~14:00 Israel time. Hebcal titles use a curly apostrophe (U+2019), so match on prefixes rather than typing a full title with an ASCII quote. One known miss: Shushan Purim, a non-working day in Jerusalem only, is not in this feed at all; ask the recipient's city if that matters.
