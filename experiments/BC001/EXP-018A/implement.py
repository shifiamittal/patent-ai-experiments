"""Reproducibly derive the unchanged scoring core plus interpretation hooks."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / 'components/relevance-scorer/rs_v0.3_feature_aware_ta'
NEW = ROOT / 'components/relevance-scorer/rs_v0.4_extraction_gate_repair_ta'
s = (OLD/'scorer.py').read_text()
s = s.replace('EXP-016A extraction', 'EXP-018A extraction')
s = s.replace('import re\n', 'import re\nimport engine\nimport bc001_config as config\n\nCORRECTIONS = {"outcomes", "relationships", "mechanism", "storage"}\n')
s = s.replace('    gun = first(us, GUN)', '''    auth_pattern = AUTH
    if "outcomes" in CORRECTIONS:
        auth_pattern = AUTH + "|" + engine.OUTCOME
    auth_test = lambda t: engine.outcome_auth(t, BIO, AUTH) if "outcomes" in CORRECTIONS else has(AUTH, t)
    storage_hit = next(((src, t) for src, t in us if engine.physical_container(t, config.STORAGE_NOUN, config.SAFE_ADJECTIVE)), None) if "storage" in CORRECTIONS else first(us, STORAGE)
    op_test = lambda t: engine.controlled_action(t, CONTROL, config.FIRING_OBJECT, config.ACCESS_BOUNDARY, config.UNRELATED_FIRE)
    gun = first(us, GUN)''')
start = s.index('    if direct and first(us, STORAGE)')
end = s.index('    firearm_title =', start)
s = s[:start] + '''    if "storage" in CORRECTIONS:
        direct = next(((src, t) for src, t in us if op_test(t)), None)
    elif direct and first(us, STORAGE) and not first(us, CONTROL, r"\\b(?:fir(?:e|ing)|trigger|firing pin|gun safety latch|operab\\w*|discharg\\w* (?:a |the )?(?:round|bullet|projectile))\\b"):
        direct = None
    storage = bool(storage_hit) and not direct
    holster = bool(first(us, HOLSTER)) and not direct
''' + s[end:]
s = s.replace('("storage_only", first(us, STORAGE) if storage', '("storage_only", storage_hit if storage')
s = s.replace('bio = first(us, BIO, AUTH)', 'bio = next(((src, t) for src, t in us if has(BIO, t) and auth_test(t)), None)')
s = s.replace('first(us, AUTH)', 'next(((src, t) for src, t in us if auth_test(t)), None)')
s = s.replace('first(us, AUTH, CONTROL, firing_context, causal)', 'first(us, auth_pattern, CONTROL, firing_context, causal)')
s = s.replace('first(us, BIO, AUTH, CONTROL, firing_context, causal)', 'first(us, BIO, auth_pattern, CONTROL, firing_context, causal)')
s = s.replace('first(us, BIO, AUTH)', 'first(us, BIO, auth_pattern)')
point = s.index('        data_link =')
s = s[:point] + '''        if "relationships" in CORRECTIONS:
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
''' + s[point:]
s = s.replace('    if generic and not mechanism:', '    if "mechanism" in CORRECTIONS and not mechanism:\n        mechanism = engine.functional_architecture(us, config.FUNCTION)\n    if generic and not mechanism:')
(NEW/'scorer.py').write_text(s)
r = (OLD/'run_blind.py').read_text().replace('"input.json", "scorer.py"', '"engine.py", "bc001_config.py", "input.json", "scorer.py"')
(NEW/'run_blind.py').write_text(r)
