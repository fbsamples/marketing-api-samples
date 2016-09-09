# Copyright (c) 2016-present, Facebook, Inc. All rights reserved.
#
# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.
#
# As with any software that integrates with the Facebook platform, your use of
# this software is subject to the Facebook Developer Principles and Policies
# [http://developers.facebook.com/policy/]. This copyright notice shall be
# included in all copies or substantial portions of the software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import time
from django.test import TestCase
from django.conf import settings
from facebookads.session import FacebookSession
from facebookads.api import FacebookAdsApi


class SampleTestCase(TestCase):

    def setUp(self):
        fbads_session = FacebookSession(
            settings.SAMPLE_TEST['APP_ID'],
            settings.SAMPLE_TEST['APP_SECRET'],
            settings.SAMPLE_TEST['TOKEN'],
        )
        fbads_api = FacebookAdsApi(fbads_session)
        FacebookAdsApi.set_default_api(fbads_api)
        self.account_id = settings.SAMPLE_TEST['ACCOUNT_ID']
        self.page_id = settings.SAMPLE_TEST['PAGE_ID']
        self.form_id = '436706799859690'  # For Lead Ads
        image_files = [
            "adimage0.png",
            "adimage1.jpg",
            "adimage2.jpg",
            "adimage3.jpg"
        ]

        self.images = map(
            lambda image_path: os.path.abspath(
                os.path.join(os.path.dirname(__file__), image_path)
            ),
            image_files
        )
        self.app_info = {
            "app_name": "DiDiAds",
            "appstore_link": "https://play.google.com/store/apps/details?id=com.facebook.se.apac.example.liyuhk.didiadsa",
            "app_deep_link": "example://detail/1234",
            "fbapplication_id": "743337925789686",
            "fbpage_id": "1426815194312958",
            "fboffsitepixel_id": "null"
        }
        self.basic_targeting = {
            "geo_locations": {
                "countries": ["US"]
            },
        }

        self.mobile_targeting = {
            "geo_locations": {
                "countries": ["US"]
            },
            "user_os": ["Android"],
            "device_platforms": ["mobile"],
            "publisher_platforms": ["facebook"],
            "facebook_positions": ["feed"],
        }
        # Base custom audience id that can be used for creating LALs etc.
        self.ca_id = "6034234313285"

    def tearDown(self):
        time.sleep(5)
