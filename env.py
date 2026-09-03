import random

ORDER = ["A", "B", "C"]


def make_post(pre, unchanged_cues):
    """Build a post-shift rule from pre: cues in unchanged_cues keep their
    pre-shift value, every other cue rotates to a guaranteed-different value.
    unchanged_cues=set() reproduces the original all-changed post rule."""
    post = {}
    for cue, val in pre.items():
        if cue in unchanged_cues:
            post[cue] = val
        else:
            post[cue] = ORDER[(ORDER.index(val) + 1) % 3]
    return post


class RuleShift:
    def __init__(self, seed=0, steps=20, shift_at=10, shift=True, unchanged_cues=frozenset()):
        self.rng = random.Random(seed)
        self.steps = steps
        self.shift_at = shift_at if shift else steps + 1
        self.cues = ["blue", "red", "green"]
        self.pre = {"blue": "B", "red": "C", "green": "A"}
        self.post = make_post(self.pre, unchanged_cues)
        self.t = 0
        self.cue = None

    def reset(self):
        self.t = 0
        return self._obs()

    def _obs(self):
        self.cue = self.cues[self.rng.randrange(len(self.cues))]
        return self.cue

    def correct(self):
        table = self.post if self.t >= self.shift_at else self.pre
        return table[self.cue]

    def step(self, action):
        reward = 1 if action == self.correct() else 0
        info = {
            "step": self.t,
            "phase": "post" if self.t >= self.shift_at else "pre",
            "correct": self.correct(),
        }
        self.t += 1
        done = self.t >= self.steps
        obs = None if done else self._obs()
        return obs, reward, done, info
