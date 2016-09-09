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
from samples.samplecode.tests.sampletestcase import SampleTestCase
from samples.samplecode.tiered_lookalike import TieredLookalikeSample


class TieredLookalikeTestCase(SampleTestCase):

    def setUp(self):
        super(TieredLookalikeTestCase, self).setUp()
        self.tiered_sample = TieredLookalikeSample()

    def test_normal(self):
        self.tiered_lookalikes = self.tiered_sample.create_tiered_lookalikes(
            self.account_id,
            "tiered_lookalike_test",  # lookalike_name
            self.ca_id,  # ca_id
            2,  # tiers
            "US"  # country
        )
        self.assertEqual(len(self.tiered_lookalikes), 2)

        self.results = self.tiered_sample.create_lookalike_ads(
            self.account_id,
            "tiered_adset_test",  # adset_name
            self.tiered_lookalikes,
            'IMPRESSIONS',  # optimization_goal
            'IMPRESSIONS',  # billing_event
            [
                200,
                100,
            ],  # tiered_bid_amounts
            "test title",  # title
            "test body",  # body
            "https://www.facebookmarketingdevelopers.com",  # url
            self.images[0],
            1000,  # daily_budget,
        )
        self.assertIn('adsets', self.results)
        self.assertIn('ads', self.results)
        self.assertEqual(len(self.results['adsets']), 2)
        self.assertEqual(len(self.results['ads']), 2)

    def tearDown(self):
        super(TieredLookalikeTestCase, self).tearDown()
        if hasattr(self, 'results'):
            campaign_id = str(self.results['adsets'][0]['campaign_id'])
            campaign = Campaign(campaign_id)
            campaign.remote_delete()
        if hasattr(self, 'tiered_lookalikes'):
            for lookalike in self.tiered_lookalikes:
                lookalike.remote_delete()
