"""BC001 vocabulary and controlled-object boundaries; no publication identities."""
STORAGE_NOUN = r'\b(?:safes?|cabinets?|lockers?|(?:gun|weapon)\s*(?:cases?|racks?)|storage|strongboxes?|lockboxes?|closets?)\b'
SAFE_ADJECTIVE = r'\bsafe\s+(?:use|usage|operation|operating|handling|firing|storage|carrying|transport|condition|manner|state|mode|position|area|zone|environment|and\s+\w+)\b'
FIRING_OBJECT = r'\b(?:firing|fire(?!\s+(?:extinguish|alarm|detect|suppress|fight|resistan|proof))|trigger(?:\s+(?:mechanism|lock|locking system))?|firing pin|gun safety latch|operab\w*|discharg\w*\s+(?:a\s+|the\s+)?(?:round|bullet|projectile)|(?:firearm|gun|weapon)\s+(?:operation|operating|lock)|(?:operation|operating)\s+of\s+(?:the\s+|a\s+)?(?:firearm|gun|weapon))\b'
ACCESS_BOUNDARY = r'\b(?:access\s+to|covers?\s+(?:the\s+)?trigger|covering\s+(?:the\s+)?trigger|withdraw\w*|retriev\w*|remov\w*\s+(?:the\s+)?(?:gun|weapon|firearm)|holster[^.;]{0,90}prevent\w*\s+accidental\s+firing)\b'
UNRELATED_FIRE = r'\bfire\s*(?:extinguish\w*|fight\w*|suppress\w*|alarm\w*|detect\w*|resistan\w*|proof\w*)\b|\bdischarg\w*\s+of\s+(?:a\s+|the\s+)?gun\s+from\b'
FUNCTION = r'\b(?:authenticat\w*|enroll\w*|enrol\w*|register\w*|manag\w*|track\w*|monitor\w*|process\w*|control\w*|communicat\w*|verify\w*)\b[^.;]{0,90}\b(?:users?|profiles?|firearms?|guns?|weapons?|locks?|devices?|data|signals?|secure|identity|identities)\b'
UNRELATED_FIRE += r'|\bholster\b[^.;!?]{0,180}\bprevent\w*\s+accidental\s+firing\b'
