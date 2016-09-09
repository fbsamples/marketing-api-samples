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

from facebookads.objects import CustomAudience
from samples.samplecode.tests.sampletestcase import SampleTestCase
from samples.samplecode.maca_cumulative import MacaCumulativeSample


class MacaCumulativeTestCase(SampleTestCase):

    def setUp(self):
        super(MacaCumulativeTestCase, self).setUp()
        self.ca_sample = MacaCumulativeSample()

    def test_normal(self):
        self.caid = self.ca_sample.create_audience(
            self.account_id,
            app_id=self.app_info['fbapplication_id'],
            name='Test MACA',
            retention_days=180,
            event='fb_mobile_purchase',
            period='28d',
            greater_than=20,
            less_than=500,
        )
        self.assertIsNotNone(self.caid, "Failed creating custom audience")

    def tearDown(self):
        super(MacaCumulativeTestCase, self).tearDown()
        if hasattr(self, 'caid'):
            ca = CustomAudience(self.caid)
            ca.remote_delete()
