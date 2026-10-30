"""Turn "come here" into a command the base understands.

A rule table, not a model: it is the contract the LLM tool-calls have to match,
and it is testable without a network. Unknown text becomes SMALLTALK so the
dialogue layer can answer instead of the car moving by accident.
"""
from dataclasses import dataclass, field


@dataclass
class Intent:
    action: str
    args: dict = field(default_factory=dict)


RULES = (
    (("come here", "come to me", "approach"), "GOTO_USER", {}),
    (("stop", "halt", "freeze"), "STOP", {}),
    (("forward", "ahead", "go on"), "MOVE", {"v": 0.4}),
    (("back", "reverse"), "MOVE", {"v": -0.4}),
    (("left",), "TURN", {"w": 0.8}),
    (("right",), "TURN", {"w": -0.8}),
    (("follow",), "FOLLOW", {}),
)


def parse(text):
    lowered = (text or "").lower()
    for needles, action, args in RULES:
        if any(needle in lowered for needle in needles):
            return Intent(action, dict(args))
    return Intent("SMALLTALK", {"text": text or ""})
