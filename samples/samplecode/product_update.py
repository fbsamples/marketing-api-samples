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

"""
# DPA Product Update

## Update individual product by retailer id

***

This sample shows how to update individual products for Dynamic Product Ads.
 Updating products via API calls enables you to reflect stock status,
 description, price or other product information in a more real time manner than
 regular product data update via feed file uploading.

## References:

* [Dynamic Product Ads reference][1]

[1]: https://developers.facebook.com/docs/marketing-api/dynamic-product-ads/
"""
from facebookads.objects import (
    AdUser,
    Business,
    ProductCatalog
)


class ProductUpdateSample:
    """
        This class provides a function (`update_product_item_by_retailer_id`)
        to update a product item in product catalog with Facebook Marketing API.

        Use params to pass a dict of key-value pairs to update on the product,
        while key being the field name and value being the updated value.
        For example

        params={'availability': Product.Availability.out_of_stock}
    """

    def update_product_item_by_retailer_id(
        self,
        catalog_id,
        retailer_id,
        params
    ):
        """
            Update product item specified by retailer_id and catalog_id
        """
        catalog = ProductCatalog(catalog_id)
        result = catalog.update_product(
            retailer_id,
            **params
        )
        return result

    def get_businesses(self):
        """
            Retrieves business account of the user's ad accounts.
        """
        me = AdUser(fbid='me')
        businesses = me.remote_read(fields=['businesses'])
        return businesses['businesses']['data']

    def get_product_catalog_by_business_id(
        self,
        business_id
    ):
        """
            Retrieves product catalogs that belong to the specified business.
        """
        business = Business(business_id)
        return business.get_product_catalogs()

    def get_products_by_product_catalog_id(
        self,
        product_catalog_id,
        params=None
    ):
        """
            Retrieves products that belong to the specified product feed.
        """
        catalog = ProductCatalog(product_catalog_id)
        fields = [
            'availability',
            'brand',
            'category',
            'condition',
            'description',
            'id',
            'image_url',
            'name',
            'price',
            'retailer_id',
            'url'
        ]
        result = catalog.get_products(fields, params)
        return result
