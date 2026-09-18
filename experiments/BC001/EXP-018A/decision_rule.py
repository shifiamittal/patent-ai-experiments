"""Pre-frozen EXP-018A decision rule, independent of benchmark identities."""
def decide(candidate, champion, comparator, repairs_pass=True):
    recall = ('r20','r50','r100','r200')
    if not repairs_pass:
        return 'REJECT'
    no_worse = all(candidate[k] >= champion[k] for k in recall) and candidate['median'] <= champion['median']
    better = any(candidate[k] > champion[k] for k in recall) or candidate['median'] < champion['median']
    if no_worse and better:
        return 'PROMOTE'
    # Early recall or median deterioration takes precedence over mixed results.
    if candidate['r20'] < champion['r20'] or candidate['r50'] < champion['r50'] or candidate['median'] >= champion['median'] + 10:
        return 'REJECT'
    recovered = any(candidate[k] > comparator[k] for k in recall) or candidate['median'] <= comparator['median'] - 10
    return 'HOLD' if recovered else 'REJECT'
