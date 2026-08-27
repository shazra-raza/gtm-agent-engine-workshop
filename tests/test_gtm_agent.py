import os
import unittest

os.environ.setdefault("LANGSMITH_TRACING", "false")

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile, get_prospect


class ProspectToolPrivacyTests(unittest.TestCase):
    def setUp(self):
        data_service._PROFILES.clear()

    def test_get_prospect_excludes_billing_identity_fields(self):
        result = get_prospect.invoke({"prospect_id": "LEAD-12853"})
        prospect = result["prospect"]

        for field in ("billing_qualification", "tax_id", "date_of_birth", "card_on_file", "credit_check_ref"):
            self.assertNotIn(field, prospect)

    def test_build_prospect_profile_excludes_billing_identity_fields(self):
        result = build_prospect_profile.invoke({"prospect_id": "LEAD-39002"})
        profile = result["prospect_profile"]

        for field in ("billing_qualification", "tax_id", "date_of_birth", "card_on_file", "credit_check_ref"):
            self.assertNotIn(field, profile)


if __name__ == "__main__":
    unittest.main()
