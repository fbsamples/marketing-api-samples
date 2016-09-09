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

from samples.samplecode.product_audience_estimation import (
    ProductAudienceEstimation
)
from samples.samplecode.tests.sampletestcase import SampleTestCase


class ProductAudienceEstimationTestCase(SampleTestCase):

    def setUp(self):
        super(ProductAudienceEstimationTestCase, self).setUp()

        self.sample = ProductAudienceEstimation()

    def test_normal_1(self):
        self._test_normal({
            "inclusions": [
                {
                    "retention_seconds": "5184000",
                    "rule": "{\"event\":{\"eq\":\"ViewContent\"}}"
                },
                {
                    "retention_seconds": "2592000",
                    "rule": "{\"event\":{\"eq\":\"AddToCart\"}}"
                }
            ]
        })

    def test_normal_2(self):
        self._test_normal({
            "inclusions": [
                {
                    "retention_seconds": "2592000",
                    "rule": "{\"event\":{\"eq\":\"ViewContent\"}}"
                }
            ]
        })

    def test_normal_3(self):
        self._test_normal({
            "inclusions": [
                {
                    "retention_seconds": "5184000",
                    "rule": "{\"event\":{\"eq\":\"Purchase\"}}"
                }
            ]
        })

    def test_normal_4(self):
        self._test_normal({
            "inclusions": [
                {
                    "retention_seconds": "5184000",
                    "rule": "{\"event\":{\"eq\":\"ViewContent\"}}"
                }
            ],
            "exclusions": [
                {
                    "retention_seconds": "5184000",
                    "rule": "{\"event\":{\"eq\":\"Purchase\"}}"
                }
            ]
        })

    def _test_normal(self, targeting_spec):
        product_set_id = 534350336722155
        r = self.sample.estimate(
            self.account_id,
            product_set_id,
            targeting_spec
        )
        self.assertTrue(r)
        self.assertIn('users', r)
        self.assertIn('bid_estimations', r)
        self.assertIn('estimate_ready', r)
