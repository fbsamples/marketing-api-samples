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
from samples.samplecode.app_install_ad import AppInstallAdSample
from samples.samplecode.tests.sampletestcase import SampleTestCase


class AppInstallAdTestCase(SampleTestCase):

    def setUp(self):
        super(AppInstallAdTestCase, self).setUp()
        self.maia_sample = AppInstallAdSample()

    def test_normal(self):
        optimization_goal = 'APP_INSTALLS'
        billing_event = 'IMPRESSIONS'
        bid_amount = 100
        result = self.maia_sample.create_app_install_ad(
            self.account_id,
            "MAIA Test",  # basename
            "Try my app!",  # message
            self.images[0],
            "1000",  # dailybudget,
            self.page_id,
            optimization_goal,
            billing_event,
            bid_amount,
            self.mobile_targeting,
            self.app_info['fbapplication_id'],
            self.app_info['app_name'],
            self.app_info['appstore_link'],
            self.app_info['app_deep_link'],
        )

        self.assertIn('campaign_id', result)
        self.assertIn('adset_id', result)
        self.assertIn('creative_id', result)
        self.assertIn('ad_id', result)

        self.campaign = Campaign()
        self.campaign[Campaign.Field.id] = result['campaign_id']
        self.campaign.remote_read()
        self.assertEqual(self.campaign.get_id(), result['campaign_id'])

    def tearDown(self):
        super(AppInstallAdTestCase, self).tearDown()
        if hasattr(self, 'campaign'):
            self.campaign.remote_delete()
