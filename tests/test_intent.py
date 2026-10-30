import pytest

from intent.parser import Intent, parse


@pytest.mark.parametrize(
    "text,action",
    [
        ("Hey car, come here!", "GOTO_USER"),
        ("stop right now", "STOP"),
        ("go forward a bit", "MOVE"),
        ("back up please", "MOVE"),
        ("turn left", "TURN"),
        ("turn right", "TURN"),
        ("follow me", "FOLLOW"),
    ],
)
def test_rules_cover_the_phrases_people_actually_say(text, action):
    assert parse(text).action == action


def test_move_carries_a_speed_and_turn_carries_a_rate():
    assert parse("forward").args["v"] > 0
    assert parse("back").args["v"] < 0
    assert parse("left").args["w"] > 0


def test_unknown_text_moves_nothing():
    intent = parse("what is the weather like")
    assert intent.action == "SMALLTALK"
    assert set(intent.args) == {"text"}


def test_empty_text_moves_nothing():
    assert parse("   ").action == "SMALLTALK"


def test_rules_are_case_insensitive():
    assert parse("COME HERE").action == "GOTO_USER"


def test_intent_defaults_do_not_share_a_dict():
    a, b = Intent("STOP"), Intent("STOP")
    a.args["x"] = 1
    assert b.args == {}
