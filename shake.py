import re


FORMS = [
    "Cue key game. Initial rule: blue -> B, red -> C, green -> A. The rule can change without warning. Use recent trials.\nTrials:\n{h}\nCurrent cue: {c}\nWhich key is correct. Answer with one letter.",
    "Initial mapping: blue B, red C, green A. It may stop being true. Use the trial record.\n{h}\nCue now: {c}\nReply with only A, B, or C.",
    "The starting rule is blue B, red C, green A. Later trials may reveal a new rule.\nPast trials:\n{h}\nNow the cue is {c}. Output the correct key letter only.",
    "Use the latest cue key trials. Starting rule: blue B, red C, green A.\nRecord:\n{h}\nNext cue: {c}\nOne letter only.",
    "Choose the current key from the rule and the trial evidence. Initial rule: blue B, red C, green A.\n{h}\nCurrent cue {c}. Answer A, B, or C.",
]


def variants(cue, k, history=None):
    h = history_text(history or [])
    out = []
    i = 0
    while len(out) < k:
        out.append(FORMS[i % len(FORMS)].format(c=cue, h=h))
        i += 1
    return out


def history_text(rows):
    if not rows:
        return "none"
    return "\n".join([
        f"{r['step']}: {r['cue']} -> {r['correct']}"
        for r in rows
    ])


def parse_key(text):
    t = text.upper()
    m = re.search(r"\b([ABC])\b", t)
    if m:
        return m.group(1)
    for ch in t:
        if ch in "ABC":
            return ch
    return "?"
