from unittest.mock import patch

import pytest

import geopy.exc
import geopy.geocoders
from geopy.geocoders import What3Words
from test.geocoders.util import BaseTestGeocoder, env


class What3WordsTestCaseUnitTest(BaseTestGeocoder):
    dummy_api_key = 'DUMMYKEY1234'

    async def test_user_agent_custom(self):
        geocoder = What3Words(
            api_key=self.dummy_api_key,
            user_agent='my_user_agent/1.0'
        )
        assert geocoder.headers['User-Agent'] == 'my_user_agent/1.0'

    @patch.object(geopy.geocoders.options, 'default_scheme', 'http')
    def test_default_scheme_is_ignored(self):
        geocoder = What3Words(api_key=self.dummy_api_key)
        assert geocoder.scheme == 'https'


@pytest.mark.skipif(
    not bool(env.get('WHAT3WORDS_KEY')),
    reason="No WHAT3WORDS_KEY env variable set"
)
class What3WordsTestCase(BaseTestGeocoder):
    @classmethod
    def make_geocoder(cls, **kwargs):
        return What3Words(
            env['WHAT3WORDS_KEY'],
            timeout=3,
            **kwargs
        )

    async def test_geocode(self):
        await self.geocode_run(
            {"query": "piped.gains.jangle"},
            {"latitude": 53.037611, "longitude": 11.565012},
        )

    async def test_reverse(self):
        await self.reverse_run(
            {"query": "53.037611,11.565012", "lang": 'DE'},
            {"address": 'fortschrittliche.voll.schnitt'},
        )

    async def test_unicode_query(self):
        await self.geocode_run(
            {
                "query": (
                    "\u0070\u0069\u0070\u0065\u0064\u002e\u0067"
                    "\u0061\u0069\u006e\u0073\u002e\u006a\u0061"
                    "\u006e\u0067\u006c\u0065"
                )
            },
            {"latitude": 53.037611, "longitude": 11.565012},
        )

    async def test_empty_response(self):
        with pytest.raises(geopy.exc.GeocoderQueryError):
            await self.geocode_run(
                {"query": "definitely.not.existingiswearrrr"},
                {},
                expect_failure=True
            )

    async def test_not_exactly_one(self):
        await self.geocode_run(
            {"query": "piped.gains.jangle", "exactly_one": False},
            {"latitude": 53.037611, "longitude": 11.565012},
        )
        await self.reverse_run(
            {"query": (53.037611, 11.565012), "exactly_one": False},
            {"address": "piped.gains.jangle"},
        )

    async def test_result_language(self):
        await self.geocode_run(
            {"query": "piped.gains.jangle", "lang": 'DE'},
            {"address": 'fortschrittliche.voll.schnitt'},
        )

    async def test_check_query(self):
        result_check_threeword_query = self.geocoder._check_query(
            "\u0066\u0061\u0068\u0072\u0070\u0072"
            "\u0065\u0069\u0073\u002e\u006c\u00fc"
            "\u0067\u006e\u0065\u0072\u002e\u006b"
            "\u0075\u0074\u0073\u0063\u0068\u0065"
        )

        assert result_check_threeword_query
