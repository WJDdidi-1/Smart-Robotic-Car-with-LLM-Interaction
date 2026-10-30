from apps.demo import run
from llm.echo_agent import EchoAgent


def test_the_sentence_becomes_the_action_that_moves_the_car():
    agent = EchoAgent()
    answer = agent.respond("Hey car, come here!")
    assert answer["action"] == "GOTO_USER"
    assert answer["reply"].startswith("[Robot]:")


def test_small_talk_moves_nothing_and_still_answers():
    answer = EchoAgent().respond("how are you")
    assert answer["action"] == "SMALLTALK"
    assert "I heard you say" in answer["reply"]


def test_chat_still_returns_a_plain_string():
    assert isinstance(EchoAgent().chat("stop"), str)


def test_the_closed_loop_arrives_without_touching_the_obstacle():
    result = run()
    assert result["arrived"] is True
    assert result["clearance"] > 0
    assert result["steps"] < 600


def test_a_request_that_is_not_motion_does_not_move_the_car():
    result = run("what time is it")
    assert result["action"] == "SMALLTALK"
    assert result["arrived"] is False
