from tests.dialects.test_dialect import Validator


class TestGoogle(Validator):
    dialect = "google"

    def test_google(self):
        self.validate_identity("DECLARE x STRING;")
