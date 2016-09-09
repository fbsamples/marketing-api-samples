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

import time
from samples.samplecode.adcreation import AdCreationSample
from samples.samplecode.tests.sampletestcase import SampleTestCase
from facebookads.objects import AdSet


class AdCreationTestCase(SampleTestCase):

    def setUp(self):
        super(AdCreationTestCase, self).setUp()
        self.sample = AdCreationSample()

    def test_normal(self):
        start = int(time.time()) + 86400  # start tomorrow
        end = start + (2 * 86400)  # end after 2 days

        result = self.sample.create_multiple_link_clicks_ads(
            self.account_id,
            self.page_id,
            "sample_test",
            ["title1", "title2"],
            ["body1", "body2"],
            ["http://www.gaishen.org", "http://www.example.com"],
            self.images,
            self.basic_targeting,
            AdSet.OptimizationGoal.link_clicks,
            AdSet.BillingEvent.link_clicks,
            100,    # bid
            1000,   # daily budget
            10000,  # lifetime budget
            start,
            end
        )
        self.assertEqual(len(result), 3)
        campaign = result[0]
        ad_set = result[1]
        ads_created = result[2]
        self.assertIsNotNone(campaign)
        self.assertIsNotNone(ad_set)
        self.assertIsNotNone(ads_created)
        self.assertTrue(len(ads_created) > 0)
        self.campaign = campaign

    def tearDown(self):
        super(AdCreationTestCase, self).tearDown()
        if hasattr(self, 'campaign'):
            self.campaign.remote_delete()
