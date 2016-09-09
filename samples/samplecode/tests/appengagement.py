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
from facebookads.objects import Campaign
from samples.samplecode.appengagement import AppEngagementSample
from samples.samplecode.tests.sampletestcase import SampleTestCase


class AppEngagementTestCase(SampleTestCase):

    def setUp(self):
        super(AppEngagementTestCase, self).setUp()
        self.appengagement_sample = AppEngagementSample()

    def test_normal(self):

        optimization_goal = 'LINK_CLICKS'
        billing_event = 'LINK_CLICKS'
        bid_amount = '100'  # stands for $1.00

        result = self.appengagement_sample.app_engagement_ad_create(
            self.account_id,
            "appengagement_test",  # basename
            "Try my app! Only 8 clicks you are done!",  # message
            self.images[0],
            "500",  # dailybudget stands for $5.00,
            self.app_info,
            optimization_goal,
            billing_event,
            bid_amount,
            self.mobile_targeting
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
        super(AppEngagementTestCase, self).tearDown()
        if hasattr(self, 'campaign'):
            self.campaign['adsets'] = None
            self.campaign.remote_delete()
