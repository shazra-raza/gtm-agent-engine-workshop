import os
from types import SimpleNamespace

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("LANGSMITH_TRACING", "false")

from gtm_agent.gtm_agent import send_prospect_email


def email_args(prospect_id):
    return {
        "prospect": {"prospect_id": prospect_id, "name": "Test Prospect", "email": "test@example.com"},
        "subject": "Test subject",
        "body": "Test body",
    }


def send_email(args):
    return send_prospect_email.func(
        **args,
        runtime=SimpleNamespace(config={"metadata": {}}),
    )


def test_send_to_disqualified_prospect_is_blocked():
    result = send_email(email_args("LEAD-50001"))

    assert result == {
        "status": "blocked",
        "reason": "prospect is marked disqualified",
        "prospect_id": "LEAD-50001",
    }
    assert "message_id" not in result


def test_send_to_qualified_prospect_succeeds():
    result = send_email(email_args("LEAD-12853"))

    assert result["status"] == "sent"
    assert result["message_id"].startswith("msg-")


def test_override_allows_disqualified_prospect():
    result = send_email({**email_args("LEAD-50001"), "override_disqualified": True})

    assert result["status"] == "sent"
    assert result["message_id"].startswith("msg-")
