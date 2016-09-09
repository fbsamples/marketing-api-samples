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

from facebookads.objects import Campaign
from samples.samplecode.carousel_app_ad import CarouselAppAdSample
from samples.samplecode.tests.sampletestcase import SampleTestCase


class CarouselAppAdTestCase(SampleTestCase):

    def setUp(self):
        super(CarouselAppAdTestCase, self).setUp()
        self.cmaia_sample = CarouselAppAdSample()

    def test_normal(self):
        images = self.images[-3:]  # Only three images needed
        linktitles = ['Title 1', 'Title 2', 'Title 3']
        deeplinks = None

        optimization_goal = 'APP_INSTALLS'
        billing_event = 'IMPRESSIONS'
        bid_amount = 100

        result = self.cmaia_sample.carousel_app_ad_create(
            self.account_id,
            "CMAIA test",  # basename
            "Try my app!",  # message
            images,
            linktitles,
            deeplinks,
            "1000",  # dailybudget,
            self.app_info,
            optimization_goal,
            billing_event,
            bid_amount,
            self.mobile_targeting,
        )

        self.assertIn('campaignid', result)
        self.assertIn('adsetid', result)
        self.assertIn('creativeid', result)
        self.assertIn('adid', result)

        self.campaign = Campaign()
        self.campaign[Campaign.Field.id] = result['campaignid']
        self.campaign.remote_read()
        self.assertEqual(self.campaign.get_id(), result['campaignid'])

    def tearDown(self):
        super(CarouselAppAdTestCase, self).tearDown()
        if hasattr(self, 'campaign'):
            self.campaign['adsets'] = None
            self.campaign.remote_delete()
