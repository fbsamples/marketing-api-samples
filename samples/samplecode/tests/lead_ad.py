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
from samples.samplecode.lead_ad import LeadAdSample
from samples.samplecode.tests.sampletestcase import SampleTestCase


class LeadAdTestCase(SampleTestCase):

    def setUp(self):
        super(LeadAdTestCase, self).setUp()
        self.sample = LeadAdSample()

    def test_normal(self):
        result = self.sample.create_lead_ad(
            account_id=self.account_id,
            name="My Awesome Lead Ad",
            page_id=self.page_id,
            form_id=self.form_id,
            optimization_goal='LEAD_GENERATION',
            billing_event='IMPRESSIONS',
            bid_amount=100,
            daily_budget=1000,
            targeting=self.mobile_targeting,
            image_path=self.images[0],
            message="My message",
            link="fb.me/fmd",
            caption="My Caption",
            description="My description",
            cta_type="SIGN_UP"
        )

        self.assertIn('image_hash', result)
        self.assertIn('campaign_id', result)
        self.assertIn('adset_id', result)
        self.assertIn('creative_id', result)
        self.assertIn('ad_id', result)

        self.campaign = Campaign()
        self.campaign[Campaign.Field.id] = result['campaign_id']
        self.campaign.remote_read()
        self.assertEqual(self.campaign.get_id(), result['campaign_id'])

    def tearDown(self):
        super(LeadAdTestCase, self).tearDown()
        if hasattr(self, 'campaign'):
            self.campaign.remote_delete()
