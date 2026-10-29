# Resilience Watch — protocol

Purpose: a daily OSINT sweep that answers one question for Seth (Alabama, US):
"Is anything developing — in the world, the US, or Alabama — that could knock out power,
water, communications, fuel, payments, food or medical supply long enough that we'd need
to rely on our own supplies, and what should we keep an eye on?"

## Voice (non-negotiable)
Give it straight. Seth handles his own reaction. No placating framing, no "don't panic",
no "experts say there's no cause for alarm" filler, no softening qualifiers added for comfort.
Equally: no hype. Every claim is grounded — say what happened, who says so, how solid the
evidence is, and the mechanism by which it could reach a household (e.g. "PHP flaw → web
shell on a utility billing portal → credential theft → backup destruction → multi-day outage").
Uncertainty is stated as a number or plain words, not as reassurance. Counter-evidence is
reported because it's true, never as comfort. If a plausible worst case exists, name it and
its rough likelihood.

## Threat scale (RW-1 to RW-5)

RW-1 NORMAL — routine background. No credible threat to US essential services beyond the usual.
RW-2 GUARDED — elevated cyber/hybrid/weather noise; real incidents elsewhere or against IT systems,
  but no specific, credible threat to US or Alabama power/water/telecom/fuel/payments.
RW-3 ELEVATED — any one of:
  - a confirmed disruptive attack on US essential services (power, water, telecom, fuel, payments, food cold chain) anywhere in the US;
  - a multi-day essential-service outage from cyber/sabotage in a NATO/peer nation;
  - a CISA Emergency Directive or joint FBI/CISA/NSA/DOE warning of active pre-positioning in US grid/water with urgent language;
  - Alabama under a forecast of a hazard likely to cause multi-day outages (major hurricane watch, ice storm warning, SPC High Risk, G4+ geomagnetic storm watch).
RW-4 HIGH — essential-service disruption is active in the Southeast or across multiple states, OR a state/federal emergency declaration tied to infrastructure covers Alabama, OR outbreak of open conflict between the US and a peer adversary.
RW-5 SEVERE — widespread outage of power/water/telecom in Alabama is happening now or authorities order shelter-in-place / extended self-reliance.

Rules: change the level only on evidence from Tier 1 or two independent Tier 2 sources.
Hype, unconfirmed leak-site claims and single social posts never move the level.
State explicitly what would move it up, and what would move it down.

## Domains (cover every run)
1. Cyber vs critical infrastructure (incl. major vulns under mass exploitation)
2. Electric grid & energy/fuel
3. Water & wastewater
4. Telecom, internet, undersea cables, GPS
5. Geopolitics & hybrid warfare (Russia, China, Iran, North Korea; sabotage)
6. Natural hazards: NWS/SPC/NHC for Alabama, NOAA SWPC space weather, seasonal outlook
7. Supply chain: food cold chain, pharmacy, fuel distribution, payments/banking
8. Alabama layer: Alabama Power / TVA / co-ops, Alabama EMA, ADEM boil-water notices, state sites, local news

9. Slow-burn / burgeoning: outbreaks (H5N1 etc.), banking & payments stability, food & fuel prices,
   AI-driven vulnerability wave, prediction-market odds on major conflict/cyber events

## Signal tools (check every run; WebFetch only works on links that came from a WebSearch,
## so search for each by name first, then fetch the result link)
- PowerOutage.us — search "poweroutage.us Alabama" → fetch /area/state/alabama; also the US total.
  Alabama baseline: ~2.6M customers tracked; a few hundred to low thousands out is normal background.
  The national poweroutage.us page has returned a stale cached copy; if its date isn't today, say "no current national figure".
- NOAA SWPC — search "SWPC 3-day forecast" → fetch services.swpc.noaa.gov/text/3-day-forecast.txt (the
  spaceweather.gov homepage is refused). Report max Kp, G/S/R probabilities, any watch. G4+ watch matters.
- NWS area forecast discussions for Birmingham (BMX), Huntsville (HUN), Mobile (MOB); NHC tropical outlook (Jun–Nov).
- AAA gas prices (gasprices.aaa.com) national + Alabama average; EIA diesel.
- Pentagon Pizza Index (pizzint.watch, @PenPizzaReport) — live readings are JavaScript-only; search news for
  reported spikes in the last 72h. Novelty signal: mention only with that caveat, never moves the level alone.
- Cloudflare Radar outage center / blog — search "Cloudflare Radar outage" for this week's internet disruptions.
- Liveuamap / ISW — conflict escalation in Ukraine–Russia, Middle East, Taiwan Strait.
- Prediction markets (Polymarket, Kalshi, Metaculus) — search for current odds on: US–Iran strikes, China–Taiwan
  action, major US cyberattack, NATO–Russia conflict. Report the number and date; Tier 3 (crowd signal, not fact).
- WorldMonitor (github.com/koala73/worldmonitor) — self-hosted only; not readable remotely. Skip unless Seth hosts it.
- VECTR-CAST (cyberwarrior76.substack.com) — independent 14-day cyber forecast; report its MalwCon level.

## Source tiers
Tier 1 (official): CISA (alerts, KEV, Emergency Directives), FBI/NSA/DOE CESER joint advisories,
  NERC, DOE OE-417, FEMA, NWS/SPC/NHC, NOAA SWPC, Alabama EMA, Alabama Power/TVA, ADEM,
  UK NCSC, EU ENISA, Dutch NCSC, Microsoft/Google official threat blogs as primary for their own findings.
Tier 2 (OSINT/research/press): Dragos, Mandiant/GTIG, CrowdStrike, Unit 42, Cisco Talos, GreyNoise,
  Cloudflare Radar, Shadowserver, Censys, Recorded Future/The Record, Reuters, AP, BleepingComputer,
  CyberScoop, ISW, Bellingcat, VECTR-CAST (independent forecast; self-reported ~47% hit rate).
Tier 3 (chatter): X/Telegram/forums — report only as "unverified chatter", never as fact.

## Output (each run)
- level (1–5), previous level, change reason
- headline (≤12 words) and bottom line (2–3 sentences, plain language)
- what to know: 4–8 items, each with domain, why it matters for self-reliance, confidence, source links
- Alabama layer: 2–5 items
- calmer signals: evidence against escalation
- tripwires: what would move the level up / down
- this level's actions: short, practical, scaled to the level (no fear-mongering)
- sources list
Push notification ONLY when the level changes or an RW-4/5 condition appears.

## Files (this repo)
- `data/latest.json` — today's report (schema below). Overwritten each run.
- `data/archive/YYYY-MM-DD.json` — copy of each day's report (Central date).
- `data/history.json` — `[{date, level, headline}]`, sorted by date, one entry per day; append, replace if the date already exists.
- `scripts/validate.py` — run `python3 scripts/validate.py data/latest.json data/history.json` before every push; fix until it prints OK.
- `index.html` — the page; renders the JSON. Don't change it during a daily run.

## Report schema (data/latest.json)
```
{
  "generated_at": "ISO 8601 with offset",
  "level": 1-5, "prev_level": 1-5 | null,
  "headline": "≤14 words",
  "bottom_line": "2–3 plain sentences",
  "change_reason": "why this level (and why it moved or didn't)",
  "actions": ["practical step scaled to the level", ...],
  "sections": [ {"domain": "Cyber vs infrastructure", "summary": "one line",
                 "items": [ITEM, ...]}, ... ],            // ≥3 domains
  "alabama": [ITEM, ...],
  "signals": [ {"name","reading","note","as_of","url"} ],
  "slow_burns": [ {"threat","trend": rising|steady|falling|new,"horizon","note"} ],
  "calmer": ["evidence against escalation", ...],
  "tripwires": {"up": [...], "down": [...]}
}
ITEM = {"title","what","mechanism": "chain from event to household impact",
        "severity": act|watch|background, "confidence": high|medium|low,
        "tier": "1"|"2"|"3", "as_of": "date", "sources": [{"title","url"}]}
```
severity: `act` = something to do now; `watch` = could escalate within weeks; `background` = context.
