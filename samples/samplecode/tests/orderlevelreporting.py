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

from samples.samplecode.orderlevelreporting import OrderLevelReportingSample
from samples.samplecode.tests.sampletestcase import SampleTestCase
from datetime import date, timedelta


class OrderLevelReportingTestCase(SampleTestCase):

    def setUp(self):
        super(OrderLevelReportingTestCase, self).setUp()

        self.TEST_BUSINESS = '722569367853065'
        self.sample = OrderLevelReportingSample()

    def test_normal(self):
        # get generator
        generator = self.sample.retrieve_order_level_report_data_parallel(
            from_date=date.today() - timedelta(days=8),
            to_date=date.today() - timedelta(days=7),
            business_id=self.TEST_BUSINESS,
            app_id='743337925789686',
            splits=3,
        )

        # enumerate and make sure that we don't throw any errors
        self.assertListEqual(list(generator), [])
