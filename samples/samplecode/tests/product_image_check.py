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

from samples.samplecode.product_image_check import DPAImageCheckSample
from samples.samplecode.tests.sampletestcase import SampleTestCase


class ProductImageCheckTestCase(SampleTestCase):

    def setUp(self):
        super(ProductImageCheckTestCase, self).setUp()
        self.TEST_BUSINESS = '722569367853065'
        self.TEST_CATALOG = '1625011544447134'
        self.TEST_RETAILER = 'ps4'

        self.sample = DPAImageCheckSample()

    def test_normal(self):
        # get catalogs for business
        catalogs = self.sample.get_product_catalog_by_business_id(
            self.TEST_BUSINESS
        )
        self.assertGreater(len(catalogs), 0, 'get catalogs')

        # check catalogs contain a catalog for testing.
        catalog_ids = []
        for catalog in catalogs:
            catalog_ids.append(catalog['id'])
        self.assertIn(self.TEST_CATALOG, catalog_ids)

        # check result contains correct results
        check_result = self.sample.check_product_images(
            self.TEST_CATALOG,
            5
        )

        self.assertEqual(check_result[0], 5)
        self.assertEqual(check_result[1], 2)
        self.assertEqual(check_result[2], 0)
