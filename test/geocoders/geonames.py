import unittest
import uuid

import pytest
import pytz

from geopy import Point
from geopy.compat import u
from geopy.exc import GeocoderAuthenticationFailure, GeocoderQueryError
from geopy.geocoders import GeoNames
from test.geocoders.util import GeocoderTestBase, env


class GeoNamesTestCaseUnitTest(GeocoderTestBase):

    def test_user_agent_custom(self):
        geocoder = GeoNames(
            username='DUMMYUSER_NORBERT',
            user_agent='my_user_agent/1.0'
        )
        assert geocoder.headers['User-Agent'] == 'my_user_agent/1.0'


@unittest.skipUnless(
    bool(env.get('GEONAMES_USERNAME')),
    "No GEONAMES_USERNAME env variable set"
)
class GeoNamesTestCase(GeocoderTestBase):

    delta = 0.04

    @classmethod
    def setUpClass(cls):
        cls.geocoder = GeoNames(username=env['GEONAMES_USERNAME'])

    def reverse_timezone_run(self, payload, expected):
        timezone = self._make_request(self.geocoder.reverse_timezone, **payload)
        if expected is None:
            assert timezone is None
        else:
            assert timezone.pytz_timezone == expected
        return timezone

    def test_unicode_name(self):
        self.geocode_run(
            {"query": "Mount Everest, Nepal"},
            {"latitude": 27.987, "longitude": 86.925},
            skiptest_on_failure=True,  # sometimes the result is empty
        )

    def test_query_urlencoding(self):
        location = self.geocode_run(
            {"query": u("Ry\u016b\u014d")},
            {"latitude": 35.65, "longitude": 138.5},
            skiptest_on_failure=True,  # sometimes the result is empty
        )
        assert u("Ry\u016b\u014d") in location.address

    def test_reverse(self):
        location = self.reverse_run(
            {
                "query": "40.75376406311989, -73.98489005863667",
                "exactly_one": True,
            },
            {
                "latitude": 40.75376406311989,
                "longitude": -73.98489005863667,
            },
        )
        assert "Times Square" in location.address

    def test_geocode_empty_response(self):
        self.geocode_run(
            {"query": "sdlahaslkhdkasldhkjsahdlkash"},
            {},
            expect_failure=True,
        )

    def test_reverse_nearby_place_name_raises_for_feature_code(self):
        with pytest.raises(ValueError):
            self.reverse_run(
                {
                    "query": "40.75376406311989, -73.98489005863667",
                    "exactly_one": True,
                    "feature_code": "ADM1",
                },
                {},
            )

        with pytest.raises(ValueError):
            self.reverse_run(
                {
                    "query": "40.75376406311989, -73.98489005863667",
                    "exactly_one": True,
                    "feature_code": "ADM1",
                    "find_nearby_type": "findNearbyPlaceName",
                },
                {},
            )

    def test_reverse_nearby_place_name_lang(self):
        location = self.reverse_run(
            {
                "query": "52.50, 13.41",
                "exactly_one": True,
                "lang": 'ru',
            },
            {},
        )
        assert u'Берлин, Германия' in location.address

    def test_reverse_find_nearby_raises_for_lang(self):
        with pytest.raises(ValueError):
            self.reverse_run(
                {
                    "query": "40.75376406311989, -73.98489005863667",
                    "exactly_one": True,
                    "find_nearby_type": 'findNearby',
                    "lang": 'en',
                },
                {},
            )

    def test_reverse_find_nearby(self):
        location = self.reverse_run(
            {
                "query": "40.75376406311989, -73.98489005863667",
                "exactly_one": True,
                "find_nearby_type": 'findNearby',
            },
            {
                "latitude": 40.75376406311989,
                "longitude": -73.98489005863667,
            },
        )
        assert "New York, United States" in location.address

    def test_reverse_find_nearby_feature_code(self):
        self.reverse_run(
            {
                "query": "40.75376406311989, -73.98489005863667",
                "exactly_one": True,
                "find_nearby_type": 'findNearby',
                "feature_code": "ADM1",
            },
            {
                "latitude": 40.16706,
                "longitude": -74.49987,
            },
        )

    def test_reverse_raises_for_unknown_find_nearby_type(self):
        with pytest.raises(GeocoderQueryError):
            self.reverse_run(
                {
                    "query": "40.75376406311989, -73.98489005863667",
                    "exactly_one": True,
                    "find_nearby_type": "findSomethingNonExisting",
                },
                {},
            )

    def test_reverse_timezone(self):
        new_york_point = Point(40.75376406311989, -73.98489005863667)
        america_new_york = pytz.timezone("America/New_York")

        timezone = self.reverse_timezone_run(
            {"query": new_york_point},
            america_new_york,
        )
        assert timezone.raw['countryCode'] == 'US'

    def test_reverse_timezone_unknown(self):
        self.reverse_timezone_run(
            # Geonames doesn't return `timezoneId` for Antarctica,
            # but it provides GMT offset which can be used
            # to create a FixedOffset pytz timezone.
            {"query": "89.0, 1.0"},
            pytz.UTC,
        )
        self.reverse_timezone_run(
            {"query": "89.0, 80.0"},
            pytz.FixedOffset(5 * 60),
        )

    def test_country_str(self):
        self.geocode_run(
            {"query": "kazan", "country": "TR"},
            {"latitude": 40.2317, "longitude": 32.6839},
        )

    def test_country_list(self):
        self.geocode_run(
            {"query": "kazan", "country": ["CN", "TR", "JP"]},
            {"latitude": 40.2317, "longitude": 32.6839},
        )

    def test_country_bias(self):
        self.geocode_run(
            {"query": "kazan", "country_bias": "TR"},
            {"latitude": 40.2317, "longitude": 32.6839},
        )


class GeoNamesInvalidAccountTestCase(GeocoderTestBase):

    @classmethod
    def setUpClass(cls):
        cls.geocoder = GeoNames(username="geopy-not-existing-%s" % uuid.uuid4())

    def reverse_timezone_run(self, payload, expected):
        timezone = self._make_request(self.geocoder.reverse_timezone, **payload)
        if expected is None:
            assert timezone is None
        else:
            assert timezone.pytz_timezone == expected
        return timezone

    def test_geocode(self):
        with pytest.raises(GeocoderAuthenticationFailure):
            self.geocode_run(
                {"query": "moscow"},
                {},
                expect_failure=True,
            )

    def test_reverse_timezone(self):
        with pytest.raises(GeocoderAuthenticationFailure):
            self.reverse_timezone_run(
                {"query": "40.6997716, -73.9753359"},
                None,
            )
