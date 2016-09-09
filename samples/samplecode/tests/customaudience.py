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
from samples.samplecode.customaudience import CustomAudienceSample
import json


class CustomAudienceTestCase(SampleTestCase):

    SAMPLE_EMAILS = [
        "bruce.wayne@gmail.com",
        "clark.kent@gmail.com",
        "tony.stark@gmail.com",
        "bruce.banner@gmail.com",
        "steve.rogers@gmail.com",
    ]

    def setUp(self):
        super(CustomAudienceTestCase, self).setUp()
        self.ca_sample = CustomAudienceSample()

    def test_normal(self):
        self.caid = self.ca_sample.create_audience(
            self.account_id,
            "Testing custom audiences",  # ca name
            "Custom audience from MUSE test",  # description
            "https://www.facebookmarketingdevelopers.com",  # optout_link
        )
        self.assertIsNotNone(self.caid, "Failed creating custom audience")

        response = self.ca_sample.upload_users_to_audience(
            self.caid,
            self.SAMPLE_EMAILS,
        )
        # response.body() should give something like this:
        # {
        #   "audience_id":"6028779619485",
        #   "num_received":5,
        #   "num_invalid_entries":0,
        #   "invalid_entry_samples":{}
        # }
        response = json.loads(response.body())
        self.assertEqual(
            response['audience_id'],
            self.caid,
            "Failed updating custom audience",
        )
        self.assertEqual(
            response['num_received'],
            len(self.SAMPLE_EMAILS),
            "Failed to receive right number of data entries",
        )

    def tearDown(self):
        super(CustomAudienceTestCase, self).tearDown()
        if hasattr(self, 'caid'):
            ca = CustomAudience(self.caid)
            ca.remote_delete()
