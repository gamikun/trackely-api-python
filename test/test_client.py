from __future__ import absolute_import
from trackely_client.api import APIClient
from os.path import join
import httpretty
import unittest
import requests
import json


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = APIClient('A', 'B')
        self.url = APIClient.BASE_URL

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    @httpretty.activate
    def test_create_campaign(self):
        httpretty.register_uri(httpretty.POST,
            join(self.url, 'campaigns'),
            body=json.dumps({
                'success': True,
                'campaign': {
                    'id': 'abc',
                }
            })
        )
        response = self.client.create_campaign(
            'This is a nice try'
        )
        self.assertTrue(response['success'])
        self.assertEqual(response['campaign']['id'], 'abc')

    @httpretty.activate
    def test_create_ad(self):
        httpretty.register_uri(httpretty.POST,
            join(self.url, 'ads'),
            body=json.dumps({
                'success': True,
                'ad': {
                    'id': 'abc',
                    'campaign_id': 'XYZ',
                    'pixel_id': 'FCK'
                }
            })
        )
        response = self.client.create_ad(
            'This is a nice try'
        )
        self.assertTrue(response['success'])
        self.assertEqual(response['ad']['id'], 'abc')
        self.assertEqual(response['ad']['campaign_id'], 'XYZ')
        self.assertEqual(response['ad']['pixel_id'], 'FCK')

    @httpretty.activate
    def test_create_pixel(self):
        httpretty.register_uri(httpretty.POST,
            join(self.url, 'pixels'),
            body=json.dumps({
                'success': True,
                'pixel': {
                    'id': 'abc',
                    'campaign_id': 'XYZ',
                    'url': join(self.url, 'pixel', 'XYZ.gif'),
                }
            })
        )

        res = self.client.create_pixel('Pixel')

        self.assertTrue(res['success'])
        self.assertEqual(res['pixel']['id'], 'abc')
        self.assertEqual(res['pixel']['campaign_id'], 'XYZ')
        self.assertEqual(res['pixel']['url'], join(self.url, 'pixel', 'XYZ.gif'))

    @httpretty.activate
    def test_get_campaigns(self):
        httpretty.register_uri(httpretty.GET,
            join(self.url, 'campaigns'),
            body=json.dumps({
                'success': True,
                'campaigns': [
                    {'id': 'abcd', 'description': 'One'},
                    {'id': 'dcba', 'description': 'Two'},
                ]
            })
        )

        res = self.client.get_campaigns()

        self.assertTrue(res['success'])
        self.assertEqual(len(res['campaigns']), 2)
        self.assertEqual(res['campaigns'][0]['id'], 'abcd')
        self.assertEqual(res['campaigns'][1]['id'], 'dcba')

    @httpretty.activate
    def test_get_ads(self):
        # ------------------- #
        # WITHOUT campaign ID #
        # ------------------- #
        httpretty.register_uri(httpretty.GET,
            join(self.url, 'ads'),
            body=json.dumps({
                'success': True,
                'ads': [
                    {'id': 'abcd', 'description': 'Three'},
                    {'id': 'dcba', 'description': 'Four'},
                ]
            })
        )

        res = self.client.get_ads()
        self.assertTrue(res['success'])
        self.assertIsInstance(res['ads'], list)
        self.assertEqual(len(res['ads']), 2)

        # ------------------- #
        # WITH campaign ID    #
        # ------------------- #
        httpretty.register_uri(httpretty.GET,
            join(self.url, 'ads'),
            body=json.dumps({
                'success': True,
                'ads': [
                    {
                        'id': 'abcd',
                        'description': 'Five',
                        'campaign_id': 'b' * 24,
                    },
                ]
            })
        )

        res = self.client.get_ads(campaign_id='b' * 24)
        self.assertTrue(res['success'])
        self.assertIsInstance(res['ads'], list)
        self.assertEqual(len(res['ads']), 1)
        self.assertEqual(res['ads'][0]['campaign_id'], 'b' * 24)


if __name__ == '__main__':
    unittest.main()