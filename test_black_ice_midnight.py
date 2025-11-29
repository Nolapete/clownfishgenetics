# test_black_ice_midnight.py
import os

import django
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from genetics_manager.models import CommercialPhenotypeRecipe  # Your current models
from landing.views import calculate_cross_htmx  # Adjust app name

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clownfishgenetics.settings")
django.setup()


class BlackIceMidnightTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.black_ice = CommercialPhenotypeRecipe.objects.get(
            name__icontains="Black Ice"
        )
        self.midnight = CommercialPhenotypeRecipe.objects.get(
            name__icontains="Midnight"
        )

    def test_black_ice_midnight_cross(self):
        # Simulate HTMX request with session
        request = self.factory.post("/", HTTP_HX_REQUEST="true")
        SessionMiddleware().process_request(request)
        request.session.save()

        # Set parent IDs in session (like your HTMX form does)
        request.session["p1_id"] = self.black_ice.id
        request.session["p2_id"] = self.midnight.id
        request.session.save()

        # Call your view
        response = calculate_cross_htmx(request)

        # Debug output
        print("Black Ice × Midnight Cross Results:")
        print(f"Status: {response.status_code}")
        print(f"Context: {response.context_data}")
        print(f"Parent1: {self.black_ice.name}")
        print(f"Parent2: {self.midnight.name}")
        print(f"Results: {response.context_data.get('results', 'No results')}")

        # Verify expected phenotypes appear
        results = response.context_data["results"]
        expected_phenotypes = ["Black Ice", "Midnight", "Generic"]
        for phenotype in expected_phenotypes:
            self.assertIn(phenotype, results, f"Expected {phenotype} in results")

        print("✅ Test PASSED")


if __name__ == "__main__":
    test = BlackIceMidnightTest()
    test.test_black_ice_midnight_cross()
