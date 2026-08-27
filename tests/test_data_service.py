import copy
import os
import unittest

from gtm_agent import data_service

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from gtm_agent.gtm_agent import build_prospect_profile


class UpdateProspectInfoTests(unittest.TestCase):
    prospect_id = "LEAD-39002"

    def setUp(self):
        self.original_record = copy.deepcopy(data_service.PROSPECTS[self.prospect_id])
        self.original_profile = data_service._PROFILES.get(self.prospect_id)
        data_service._PROFILES.pop(self.prospect_id, None)

    def tearDown(self):
        data_service.PROSPECTS[self.prospect_id] = self.original_record
        if self.original_profile is None:
            data_service._PROFILES.pop(self.prospect_id, None)
        else:
            data_service._PROFILES[self.prospect_id] = self.original_profile

    def test_update_persists_technology_to_source_record(self):
        technology = "Terraform"

        data_service.update_prospect_info(self.prospect_id, technology)

        self.assertIn(technology, data_service.fetch_tech_stack(self.prospect_id))

    def test_rebuilt_profile_contains_updated_technology(self):
        technology = "Terraform"
        stale_profile = copy.deepcopy(self.original_record)
        data_service.save_profile_to_db(self.prospect_id, stale_profile)

        data_service.update_prospect_info(self.prospect_id, technology)
        build_prospect_profile.invoke({"prospect_id": self.prospect_id})

        profile = data_service.get_profile_from_db(self.prospect_id)["prospect_profile"]
        self.assertIn(technology, profile["tech_stack"])


if __name__ == "__main__":
    unittest.main()
