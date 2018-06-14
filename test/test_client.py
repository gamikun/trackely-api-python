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


if __name__ == '__main__':
    unittest.main()