"""Deterministic, content-only EXP-018A extraction and decimal scoring.

Rules are an AI-authored challenger implementation, not analyst annotations.
No record IDs, prior scores, identities, or benchmark labels enter extraction.
"""
import copy
import re
import engine
import bc001_config as config

CORRECTIONS = {"outcomes", "relationships", "mechanism", "storage"}
from decimal import Decimal, ROUND_HALF_UP

FEATURES = tuple(f"F{i}" for i in range(2, 9))
RELATIONS = ("F2_to_F3", "F4_to_F3", "F5_to_F6")
WEIGHTS = dict(F2=12, F3=16, F4=14, F5=10, F6=4, F7=1, F8=1,
               F2_to_F3=14, F4_to_F3=10, F5_to_F6=4)
FM = {"E": Decimal("1"), "I": Decimal("0.35"), "A": Decimal("0")}
RM = {"E": Decimal("1"), "I": Decimal("0.25"), "C": Decimal("0"), "A": Decimal("0")}
DOMAIN = {"firearm": 10, "attached_firing_control": 8, "incidental_or_ambiguous": 2, "wrong_domain": 0}
CAPS = {"non_firearm_gun": 5, "storage_only": 15, "holster_only": 20, "incidental_firearm": 20}
PENALTIES = {"generic_without_mechanism": 8, "targeting_dominates": 10, "generic_biometric_lock": 20}

GUN = r"\b(?:fire\s*arms?|handguns?|pistols?|rifles?|shotguns?|guns?|weapons?|revolvers?)\b"
NON_GUN = r"\b(?:(?:weld\w*|spray\w*|nail|toy|glue|heat|grease|caulking|solder\w*|charg\w*|water|paint|airsoft|stun|massage|electron|ion|particle|laser|gas|fuel|inflati\w*|scanning|barcode|code[ -]scanning)[ -]+(?:guns?|rifles?)|gun[ -]+(?:weld\w*|spray\w*|charg\w*)|(?:automobile |car )?point firearm)\b"
STORAGE = r"\b(?:safes?|cabinets?|lockers?|gun\s*cases?|weapon\s*cases?|gun\s*racks?|weapon\s*racks?|storage|strongboxes?|lockboxes?|closets?)\b"
HOLSTER = r"\b(?:holsters?|casings?|retaining device)\b"
BIO = r"\b(?:biometric\w*|finger\s*print\w*|palm[ -]?(?:vein|print)\w*|fac(?:e|ial)[ -]recognition|iris[ -](?:recognition|scan\w*)|retina\w*|heart[ -]rate)\b"
AUTH = r"\b(?:authenticat\w*|authori[sz]\w*|identif\w*|recognition|verif\w*|match\w*|validat\w*|permitted user|registered user|rightful user|legitimate user|owner)\b"
OP = r"(?:\b(?:fir(?:e|ing)|discharg\w*|trigger|firing pin|gun safety latch|operab\w*|operat\w*)\b)"
CONTROL = r"\b(?:lock\w*|unlock\w*|block\w*|unblock\w*|prevent\w*|inhibit\w*|enabl\w*|disabl\w*|allow\w*|permit\w*|restrict\w*|deactivat\w*|activat\w*|control\w*|releas\w*)\b"
GEO = r"\b(?:GPS|geofenc\w*|geo[ -]?locat\w*|geograph\w*|location|positioning|prohibited (?:area|zone)|restricted (?:area|zone)|safe (?:area|zone)|boundar\w*)\b"
GEO_CAUSE = r"(?:\b(?:based on|depending on|in response to|according to|when|within|outside|inside|if|upon|based upon)\b|geofenc\w*|prohibited|restricted (?:area|zone))"
TRACK = r"\b(?:track\w*|traceab\w*|tracing|usage[ -]log\w*|logg\w*|record\w*|collect\w*|shot count\w*|firing count\w*|discharge count\w*|round count\w*|GPS|positioning|geolocat\w*|location)\b"
CENTRAL = r"\b(?:server\w*|database\w*|central(?:ized)? (?:system|database|server|station|management)|national (?:system|database|server)|(?:remote |monitoring )station|remote (?:authority|computer|monitor\w*)|law enforcement|reporting (?:system|destination)|(?:broadcast\w*|transmi\w*|send\w*)[^.;]{0,70}(?:alert|notification))\b"
TRANSMIT = r"\b(?:transmi\w*|send\w*|sent|upload\w*|communicat\w*|report\w*|relay\w*|transfer\w*|notif\w*|updated|sharing|shared|forward\w*)\b"
TARGET = r"\b(?:friend[ /-](?:or[ /-])?foe|target selection|target[ -]select\w*|automatic\w* aiming|AI aiming|automatically (?:aim\w*|fir\w*)|aiming correction)\b"


def has(pattern, text):
    return bool(re.search(pattern, text, re.I))


def units(title, abstract):
    # Each unit is an exact substring of one permitted input field.
    return [(source, match.group().strip()) for source, text in (("title", title), ("abstract", abstract))
            if text and text != "1818"
            for match in re.finditer(r"[^.!?\n]+(?:[.!?]+|$)", text)
            if match.group().strip()]


def first(us, *patterns):
    return next(((src, text) for src, text in us if all(has(p, text) for p in patterns)), None)


def geographic_control(us):
    # Require a geographic CONDITION tied to operability, not a causal word
    # elsewhere in a long biometric-lock/GPS component list.
    geo_condition = r"(?:geofenc\w*|geograph\w*|GPS|location|coordinates|(?:restricted|prohibited|permitted|safe|designated|predetermined) (?:area|zone|region)|boundar\w*)"
    action = r"(?:disabl\w*|deactivat\w*|inhibit\w*|enabl\w*|(?:prevent\w*|prohibit\w*|restrict\w*)[^,;.!?]{0,35}(?:fir\w*|use|operat\w*)|lock\w*[^,;.!?]{0,25}(?:trigger|firearm|gun))"
    patterns = [action + r"[^;.!?]{0,90}(?:when|if|within|outside|inside|based on|according to|in these|in a|in restricted)[^;.!?]{0,60}" + geo_condition,
                geo_condition + r"[^;.!?]{0,80}(?:such that|so that|causes?|thereby|to disable|will disable)[^;.!?]{0,45}" + action,
                r"(?:when|if|within|outside|inside)[^;.!?]{0,40}" + geo_condition + r"[^;.!?]{0,80}" + action,
                r"(?:prohibit\w*|prevent\w*|restrict\w*)[^;.!?]{0,40}(?:firearm|gun)[^;.!?]{0,25}(?:use|operat\w*|fir\w*)[^;.!?]{0,30}(?:restricted|prohibited) (?:area|zone)"]
    patterns = [pattern.replace("[^;.!?]", "[^,;.!?]") for pattern in patterns]
    return next(((src, text) for src, text in us if any(has(pattern, text) for pattern in patterns)), None)


def evidence(hit=None, status="E", reason=""):
    if not hit:
        return {"status": "A", "source": "", "excerpt": "", "reasoning": ""}
    return {"status": status, "source": hit[0], "excerpt": hit[1], "reasoning": reason}


def extract(title, abstract):
    """Accept content only: deliberately no record-ID parameter."""
    us = units(title, abstract)
    text = title + "\n" + abstract
    auth_pattern = AUTH
    if "outcomes" in CORRECTIONS:
        auth_pattern = AUTH + "|" + engine.OUTCOME
    auth_test = lambda t: engine.outcome_auth(t, BIO, AUTH) if "outcomes" in CORRECTIONS else has(AUTH, t)
    storage_hit = next(((src, t) for src, t in us if engine.physical_container(t, config.STORAGE_NOUN, config.SAFE_ADJECTIVE)), None) if "storage" in CORRECTIONS else first(us, STORAGE)
    op_test = lambda t: engine.controlled_action(t, CONTROL, config.FIRING_OBJECT, config.ACCESS_BOUNDARY, config.UNRELATED_FIRE)
    gun = first(us, GUN)
    non_gun = first(us, NON_GUN)
    # Remove non-firearm compounds before testing a remaining firearm mention.
    substantive_gun = has(r"\b(?:firearms?|handguns?|pistols?|shotguns?|revolvers?|ammunition|bullets?|gunpowder)\b", re.sub(NON_GUN, "", text, flags=re.I))
    wrong = not gun or (non_gun and not substantive_gun)
    # A firing/trigger mechanism distinguishes operating control from safe/holster access.
    direct = first(us, CONTROL, r"\b(?:fir(?:e|ing)|discharg\w*|trigger|firing pin|gun safety latch|operab\w*)\b")
    if "storage" in CORRECTIONS:
        direct = next(((src, t) for src, t in us if op_test(t)), None)
    elif direct and first(us, STORAGE) and not first(us, CONTROL, r"\b(?:fir(?:e|ing)|trigger|firing pin|gun safety latch|operab\w*|discharg\w* (?:a |the )?(?:round|bullet|projectile))\b"):
        direct = None
    storage = bool(storage_hit) and not direct
    holster = bool(first(us, HOLSTER)) and not direct
    firearm_title = has(GUN, re.sub(NON_GUN, "", title, flags=re.I))
    incidental = bool(gun) and not wrong and not firearm_title and not direct and (
        has(r"\b(?:for example|such as|e\.g|including|handbag|luggage|bike locks|airport|screening|contraband)\b", text)
        or not first(us, GUN, r"\b(?:track\w*|monitor\w*|lock\w*|control\w*|sensor\w*|secur\w*)\b"))
    if gun and not wrong and not firearm_title and has(r"\b(?:may|can) (?:also )?be (?:a |an )?(?:firearm|gun|weapon)\b", text):
        incidental = True
    if wrong:
        category, domain_hit = "wrong_domain", non_gun or (us[0] if us else None)
    elif storage or holster or incidental:
        category, domain_hit = "incidental_or_ambiguous", gun
    elif direct and has(r"\b(?:device|mechanism|attachment|adapter|retrofit|trigger lock|gun lock)\b", title):
        category, domain_hit = "attached_firing_control", direct
    else:
        category, domain_hit = "firearm", gun
    result = {"domain_category": category, "domain_evidence": evidence(domain_hit),
              "features": {f: evidence() for f in FEATURES},
              "relationships": {r: evidence() for r in RELATIONS}, "noise_flags": [],
              "gate_evidence": {}, "penalty_evidence": {}, "tracking_only": False}
    flags = result["noise_flags"]
    for flag, hit in (("non_firearm_gun", non_gun if wrong else None),
                      ("storage_only", storage_hit if storage and not wrong else None),
                      ("holster_only", first(us, HOLSTER) if holster and not wrong else None),
                      ("incidental_firearm", gun if incidental else None)):
        if hit:
            flags.append(flag)
            result["gate_evidence"][flag] = evidence(hit)
    f, r = result["features"], result["relationships"]
    if not wrong:
        bio = next(((src, t) for src, t in us if has(BIO, t) and auth_test(t)), None)
        if bio and not has(r"anti[ -]?fingerprint|ballistic fingerprint", bio[1]):
            f["F2"] = evidence(bio)
        elif (bio := first(us, BIO)) and not has(r"anti[ -]?fingerprint|ballistic fingerprint", bio[1]) and next(((src, t) for src, t in us if auth_test(t)), None):
            f["F2"] = evidence(bio, "I", "Biometric sensing and user authorization are stated in separate sentences; identification use is inferred.")
        operational = not storage and not holster and not incidental
        firing_context = r"\b(?:fir(?:e|ing)|discharg\w*|trigger|firing pin|gun safety latch|operab\w*)\b"
        causal = r"\b(?:if|when|only|upon|after|according to|based on|in response to|responsive to|depending on|allows?|enables?|prevents?|controls?|releasing|so that|thereby|through|using)\b"
        auth_control = first(us, auth_pattern, CONTROL, firing_context, causal)
        if operational and auth_control:
            f["F3"] = evidence(auth_control)
        elif operational and direct and next(((src, t) for src, t in us if auth_test(t)), None):
            f["F3"] = evidence(direct, "I", "Firearm firing control is stated alongside user authorization in the title/abstract, but their dependency is not explicit in this excerpt.")
        geo_control = geographic_control(us)
        if operational and geo_control:
            f["F4"] = evidence(geo_control)
            r["F4_to_F3"] = evidence(geo_control)
        result["tracking_only"] = bool(first(us, GEO)) and not geo_control
        track = first(us, TRACK)
        if track and not incidental:
            if has(r"\b(?:GPS|geolocat\w*|usage[ -]log\w*|shot count\w*|tracking|traceab\w*)\b", track[1]) or (has(GUN, track[1]) and has(r"\b(?:track\w*|traceab\w*|tracing|logg\w*|record\w*|collect\w*|location|geograph\w*)\b", track[1])):
                f["F5"] = evidence(track)
            elif operational and has(r"\b(?:record\w*|collect\w*|logg\w*|location|geograph\w*)\b", track[1]):
                f["F5"] = evidence(track, "I", "Data recording or positioning is described within this firearm system; firearm data collection is inferred from that context.")
        central = first(us, CENTRAL)
        if central and not incidental:
            f["F6"] = evidence(central)
        context = first(us, r"\b(?:classif\w*|categori[sz]\w*|distinguish\w*|determin\w*)\b",
                        r"\b(?:self[ -]defen[cs]e|recreational|purpose of (?:firearm |gun )?use|usage context|context of use)\b")
        if context and operational:
            f["F7"] = evidence(context)
        danger = first(us, r"\b(?:heart[ -]rate|physiolog\w*)\b", r"\b(?:danger|threat|emergency)\b", r"\b(?:unlock\w*|enabl\w*|releas\w*)\b")
        if danger and operational:
            f["F8"] = evidence(danger)
        bio_control = first(us, BIO, auth_pattern, CONTROL, firing_context, causal)
        if f["F2"]["status"] != "A" and f["F3"]["status"] != "A":
            if bio_control:
                r["F2_to_F3"] = evidence(bio_control)
            elif auth_control and first(us, BIO, auth_pattern):
                r["F2_to_F3"] = evidence(auth_control, "I", "User authorization governs firing and biometric identification is stated; the biometric result is inferred to supply that authorization.")
            else:
                r["F2_to_F3"] = evidence(first(us, BIO), "C")
        if "relationships" in CORRECTIONS:
            f["F3"] = evidence()
            r["F2_to_F3"] = evidence()
            link = engine.relationship(us, auth_test, op_test, BIO, {"title": title, "abstract": abstract}) if operational else None
            if link:
                src, excerpt, state, rationale = link
                f["F3"] = evidence((src, excerpt), state, rationale)
                if f["F2"]["status"] != "A":
                    if has(BIO, excerpt):
                        r["F2_to_F3"] = evidence((src, excerpt), state, rationale)
                    else:
                        bio_ev = f["F2"]
                        r["F2_to_F3"] = evidence((src, excerpt), "I", "Authentication controls operation in the cited span. Biometric identification is separately supported by " + bio_ev["source"] + ": " + bio_ev["excerpt"] + " The biometric identification is inferred to supply this system's authorization.")
            elif operational:
                # Access to a firearm-coupled authentication/lock device is
                # operational architecture, not access to a physical container.
                architecture = next(((src, t) for src, t in us if has(r"registered|authori[sz]", t) and has(r"access[^.;]{0,80}authentication devices?[^.;]{0,50}(?:coupled|connected)[^.;]{0,30}firearms?", t)), None)
                lock = first(us, r"firearm lock|trigger lock")
                if architecture and lock:
                    reason = "User profiles are registered for access to firearm-coupled authentication devices: " + architecture[1] + " A firearm lock is separately stated: " + lock[1] + " Registration-mediated access to that firearm lock supports inferred operating control; no biometric modality is inferred."
                    f["F3"] = evidence(architecture, "I", reason)
        if "storage" in CORRECTIONS and not operational:
            f["F3"] = evidence()
            r["F2_to_F3"] = evidence()
        data_link = first(us, TRACK, CENTRAL, TRANSMIT)
        if f["F5"]["status"] != "A" and f["F6"]["status"] != "A":
            if data_link:
                r["F5_to_F6"] = evidence(data_link)
            elif (link := first(us, CENTRAL, TRANSMIT)):
                r["F5_to_F6"] = evidence(link, "I", "The system transmits to an external destination and separately collects firearm data; transmission of that data is inferred.")
            else:
                r["F5_to_F6"] = evidence(central, "C")
    generic = first(us, r"\b(?:safety|monitoring|smart|authentication)\b")
    mechanism = first(us, r"\b(?:sensor\w*|circuit\w*|processor\w*|controller\w*|module\w*|actuator\w*|solenoid\w*|algorithm\w*|fingerprint\w*|biometric\w*|GPS|transmitter\w*|receiver\w*|motor\w*|switch\w*|latch\w*|pin|lever|spring|valve|detector\w*|camera\w*)\b")
    if "mechanism" in CORRECTIONS and not mechanism:
        mechanism = engine.functional_architecture(us, config.FUNCTION)
    if generic and not mechanism:
        flags.append("generic_without_mechanism")
        result["penalty_evidence"]["generic_without_mechanism"] = evidence(generic)
    target = first(us, TARGET)
    if target and (has(TARGET, title) or sum(has(TARGET, t) for _, t in us) >= max(1, len(us) / 2)):
        flags.append("targeting_dominates")
        result["penalty_evidence"]["targeting_dominates"] = evidence(target)
    if incidental and first(us, BIO) and first(us, r"\block\w*\b"):
        flags.append("generic_biometric_lock")
        result["penalty_evidence"]["generic_biometric_lock"] = evidence(first(us, BIO))
    return result


def sanitize(ev, title, abstract, relationship=False):
    allowed = RM if relationship else FM
    ev = copy.deepcopy(ev)
    if ev.get("status") not in allowed:
        raise ValueError("Unknown evidence state")
    source = {"title": title, "abstract": abstract}.get(ev.get("source"), "")
    if ev["status"] != "A" and (not ev.get("excerpt") or ev["excerpt"] not in source or
                                     (ev["status"] == "I" and not ev.get("reasoning", "").strip())):
        return evidence()
    return ev if ev["status"] != "A" else evidence()


def score(fields, title, abstract):
    x = copy.deepcopy(fields)
    x["domain_evidence"] = sanitize(x["domain_evidence"], title, abstract)
    if x["domain_evidence"]["status"] == "A":
        x["domain_category"] = "wrong_domain"
    for f in FEATURES:
        x["features"][f] = sanitize(x["features"][f], title, abstract)
    for r in RELATIONS:
        x["relationships"][r] = sanitize(x["relationships"][r], title, abstract, True)
    if x["tracking_only"]:
        x["features"]["F4"] = evidence()
        x["relationships"]["F4_to_F3"] = evidence()
    for relationship, prerequisite in (("F2_to_F3", ("F2", "F3")), ("F4_to_F3", ("F4",)), ("F5_to_F6", ("F5", "F6"))):
        if any(x["features"][f]["status"] == "A" for f in prerequisite):
            x["relationships"][relationship] = evidence()
    if any(flag not in CAPS and flag not in PENALTIES for flag in x["noise_flags"]):
        raise ValueError("Unknown gate/penalty")
    x["noise_flags"] = sorted(set(x["noise_flags"]))
    points = {"domain": Decimal(DOMAIN[x["domain_category"]])}
    points.update({f: WEIGHTS[f] * FM[x["features"][f]["status"]] for f in FEATURES})
    points.update({r: WEIGHTS[r] * RM[x["relationships"][r]["status"]] for r in RELATIONS})
    primary = [x["features"][f]["status"] for f in FEATURES[:4]]
    established = sum(s != "A" for s in primary)
    explicit = primary.count("E")
    multi = 4 if established == 4 and explicit >= 3 else 2 if established >= 3 and explicit >= 2 else 0
    x["multi_primary_status"] = f"{established} established; {explicit} explicit"
    points["multi_primary"] = Decimal(multi)
    penalty = sum(PENALTIES.get(flag, 0) for flag in x["noise_flags"])
    cap = min([100] + [CAPS[flag] for flag in x["noise_flags"] if flag in CAPS])
    raw = sum(points.values())
    final = min(Decimal(cap), max(Decimal(0), min(Decimal(100), (raw - penalty).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))))
    x.update(points={key: float(value) for key, value in points.items()}, raw_score=float(raw),
             penalty_points=penalty, hard_cap=cap, final_score=float(final),
             predicted_relevance="H" if final >= 75 else "M+" if final >= 55 else "M" if final >= 30 else "L" if final >= 10 else "N",
             explicit_primary_relationships=sum(x["relationships"][r]["status"] == "E" for r in RELATIONS[:2]),
             explicit_primary_features=explicit)
    return x


def sort_key(row):
    return (-row["final_score"], -row["explicit_primary_relationships"], -row["explicit_primary_features"],
            {"E": 0, "I": 1, "A": 2}[row["features"]["F3"]["status"]], row["penalty_points"], row["record_id"])


def rank_records(records):
    ids = [row[0] for row in records]
    if any(not isinstance(rid, str) or not rid for rid in ids) or len(ids) != len(set(ids)):
        raise ValueError("Record IDs must be nonempty and unique")
    rows = []
    for rid, title, abstract in records:
        row = score(extract(title, abstract), title, abstract)
        row.update(record_id=rid, title=title, abstract=abstract)
        rows.append(row)
    rows.sort(key=sort_key)
    for rank, row in enumerate(rows, 1):
        row["rank"] = rank
    return rows


def validate(records, rows):
    ids = [r[0] for r in records]
    out = [r["record_id"] for r in rows]
    checks = {"row_count": len(rows) == len(records), "unique_ids": len(out) == len(set(out)),
              "exact_coverage": sorted(ids) == sorted(out), "no_unknown_ids": not set(out) - set(ids),
              "sequential_ranks": [r["rank"] for r in rows] == list(range(1, len(rows) + 1)),
              "bounded_scores": all(0 <= r["final_score"] <= 100 for r in rows),
              "deterministic_order": rows == sorted(rows, key=sort_key),
              "evidence_supported": True, "inferences_reasoned": True, "no_tracking_only_F4": True,
              "formula_recomputed": True, "content_preserved": True}
    source = {rid: (title, abstract) for rid, title, abstract in records}
    for row in rows:
        checks["content_preserved"] &= source.get(row["record_id"]) == (row["title"], row["abstract"])
        for ev in [row["domain_evidence"], *row["features"].values(), *row["relationships"].values()]:
            if ev["status"] in ("E", "I"):
                checks["evidence_supported"] &= bool(ev["excerpt"]) and ev["excerpt"] in row.get(ev["source"], "")
            if ev["status"] == "I":
                checks["inferences_reasoned"] &= bool(ev["reasoning"].strip())
        if row["tracking_only"]:
            checks["no_tracking_only_F4"] &= row["features"]["F4"]["status"] == "A" and row["points"]["F4_to_F3"] == 0
        checks["formula_recomputed"] &= row["final_score"] == score(row, row["title"], row["abstract"])["final_score"]
    if not all(checks.values()):
        raise ValueError(checks)
    return checks
