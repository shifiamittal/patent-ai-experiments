"""Content-only interpretation primitives; domain terms are supplied by callers.

Mechanism-general; validated on BC001 only. Conservative deterministic rules,
not a general natural-language entailment model.
"""
import re

OUTCOME = r'\b(?:invalid|valid|unsuccessful|successful|failed|failure|success|incorrect|correct|unrecognized|recognized|unauthorized|authorized|not correctly identified|not identified)\b'
CAUSAL = r'\b(?:if|when|unless|only|upon|after|according to|based on|in response to|responsive to|depending on|allows?|enables?|prevents?|controls?|releasing|so that|thereby|through|using|configured to)\b'
ANAPHOR = r'\b(?:this|that|the|its) (?:result|outcome|authorization|authentication|identification|match)|\b(?:if so|otherwise|on success|on failure)\b'


def has(pattern, text):
    return bool(re.search(pattern, text, re.I))


def outcome_auth(text, credential, auth):
    return has(auth, text) or any(
        has(credential, text[max(0, m.start()-65):m.end()+65])
        for m in re.finditer(OUTCOME, text, re.I))


def clean_senses(text, excluded):
    # Spaces preserve offsets; evidence always comes from original input.
    return re.sub(excluded, lambda m: ' ' * len(m.group()), text, flags=re.I)


def physical_container(text, noun, adjective):
    return has(noun, clean_senses(text, adjective))


def controlled_action(text, action, object_pattern, access_boundary, exclusions):
    text = clean_senses(text, exclusions)
    for clause in re.split(r'[.;!?]', text):
        if has(access_boundary, clause):
            # Permit an independently stated operating action in a later clause.
            clauses = re.split(r'[,;]|\band\b', clause)
        else:
            clauses = [clause]
        for part in clauses:
            if has(access_boundary, part):
                continue
            for obj in re.finditer(object_pattern, part, re.I):
                vicinity = part[max(0, obj.start()-85):obj.end()+65]
                if has(action, vicinity):
                    return True
    return False


def relationship(units, auth_test, operation_test, credential, field_text):
    """Return (source, exact span, status, rationale), or None.

    Explicit links require a causal cue and close authentication/control facts.
    Adjacent result anaphora supports explicit multi-sentence evidence; a
    repeated authentication-device referent supports reasoned inference.
    """
    for source, text in units:
        if auth_test(text) and operation_test(text) and has(CAUSAL, text):
            # Split lists at semicolons and require the facts within a clause.
            for clause in re.split(r';', text):
                if auth_test(clause) and operation_test(clause) and has(CAUSAL, clause):
                    return source, text, 'E', ''
    for (s1, a), (s2, b) in zip(units, units[1:]):
        if s1 != s2 or not auth_test(a) or not operation_test(b):
            continue
        original = field_text[s1]
        start = original.find(a)
        end = original.find(b, start+len(a)) + len(b)
        span = original[start:end]
        if has(ANAPHOR, b) and has(CAUSAL, b):
            return s1, span, 'E', ''
        if has(r'\b(?:authentication|identification|authorization) (?:device|system|module)\b', a) and has(r'\b(?:same|this|that|the) (?:device|system|module)\b', b):
            return s1, span, 'I', 'The first sentence states authentication; the adjacent sentence assigns operating control to the same named device. Shared-device reference supports the dependency, without an explicit result condition.'
    return None


def functional_architecture(units, relevant_function):
    component = r'\b(?:servers?|stations?|devices?|components?|processors?|controllers?|processing units?|control units?)\b'
    named_function = r'\b(?:authentication|enrollment|enrolment|processing|control|lock|locking) (?:devices?|components?|stations?|units?)\b'
    for source, text in units:
        if has(named_function, text):
            return source, text
        for match in re.finditer(component, text, re.I):
            context = text[max(0, match.start()-70):match.end()+180]
            if has(relevant_function, context):
                return source, text
    return None
