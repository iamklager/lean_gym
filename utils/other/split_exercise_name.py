import re

def split_exercise_name(name):
    pattern = r'^(.*?)\s*(?:[–—-]\s*(.*?))?\s*(?:\((.*?)\))?$'
    match = re.match(pattern, name)
    assert match is not None
    exercise = match.group(1).strip()
    hands = match.group(2).strip() if match.group(2) else ' '
    type = match.group(3).strip() if match.group(3) else ' '
    return [exercise, type, hands]
