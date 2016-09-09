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

from samples.samplecode.product_update import ProductUpdateSample
from samples.samplecode.tests.sampletestcase import SampleTestCase
from facebookads.objects import Product


class ProductUpdateTestCase(SampleTestCase):

    def setUp(self):
        super(ProductUpdateTestCase, self).setUp()
        self.TEST_BUSINESS = '722569367853065'
        self.TEST_CATALOG = '1625011544447134'
        self.TEST_RETAILER = 'ps4'

        self.sample = ProductUpdateSample()

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

        # get products for catalog
        products = self.sample.get_products_by_product_catalog_id(
            self.TEST_CATALOG
        )
        self.assertGreater(len(products), 0, 'get products')

        # check result contains test product
        retailer_ids = []
        for product in products:
            retailer_ids.append(product['retailer_id'])
        self.assertIn(self.TEST_RETAILER, retailer_ids)

        # update test product
        result = self.sample.update_product_item_by_retailer_id(
            self.TEST_CATALOG,
            self.TEST_RETAILER,
            {
                "availability": Product.Availability.in_stock
            }
        )
        self.assertTrue(result.json())
