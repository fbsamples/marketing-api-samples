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
# Product Image Size Check

## Check the image sizes of products in a product catalog.

***

This sample checks the product images of a catalog to see whether the images
are over 600x600px, the recommended size for dynamic ads.

* It checks products of an existing prodoct catalog at product catalog level. It
is not restricted to certain product feeds.
* You can use it to check all products of your catalog, by copying the code
below and remove the limit checking.
* It checks "additional images" of each product also, to see whether a simple
swapping is feasible.

## References:

* [Dynamic Product Ads reference][1]

[1]: https://developers.facebook.com/docs/marketing-api/dynamic-product-ads/
"""
from facebookads.objects import (
    AdUser,
    Business,
    ProductCatalog
)
from PIL import ImageFile
import urllib
import urlparse
# to load the full image, the following libs are needed.
# from PIL import Image
# import requests
# from io import BytesIO


class DPAImageCheckSample:
    """
        This class provides a function (`check_product_images`)
        to check product image sizes in a product catalog with Facebook
        Marketing API.

        It returns a tuple, with 3 number: total products checked, number of
        products with images of recommended size, number of products with images
        below recommended size but having at least 1 big enough additional
        image, as well as an array of up to 5 small image samples for the last
        case.

        Set the limit to a number in huandreds or a little more. Only
        products of that number would be checked. We have this control as
        to check multiple images of each product in a catalog with millions of
        products will take too long. But if you run this script on your own
        machine, you can raise that limit more.
    """

    def check_product_images(
        self,
        catalog_id,
        limit
    ):
        """
            Check the first "limit" products of a product catalog
        """
        catalog = ProductCatalog(catalog_id)
        fields = [
            'additional_image_urls',
            'image_url',
            'url'
        ]
        products = catalog.get_products(fields)
        image_ok_count = 0
        additional_image_ok_count = 0
        total_count = 0
        small_images = []
        for product in products:
            total_count += 1
            if total_count > limit:
                total_count -= 1
                break
            if self.is_size_ok(product['image_url']):
                image_ok_count += 1
            else:
                if len(small_images) < 5:
                    small_images.append((
                        product['url'],
                        self.extract_from_safe_img(product['image_url'])
                    ))
                if 'additional_image_urls' in product.keys() and \
                        product['additional_image_urls']:
                    image_urls = product['additional_image_urls']
                    for url in image_urls:
                        if self.is_size_ok(url):
                            additional_image_ok_count += 1
                            break
        res = (total_count, image_ok_count, additional_image_ok_count,
               small_images)
        return res

    def extract_from_safe_img(self, image_url):
        """
            Get the original image url from the "safe image url" returned by
            API.
        """
        parsed = urlparse.urlparse(image_url)
        url = urlparse.parse_qs(parsed.query)['url']
        if url is not None:
            return url[0]
        else:
            return image_url

    def is_size_ok(
        self,
        image_url
    ):
        """
            Check whether the dimension of an image is 600px or more.
        """
        # This method reads in the whole image
        # img_resp = requests.get(image_url)
        # im = Image.open(BytesIO(img_resp.content))
        # width, height = im.size

        # This method reads in only usuallly 1k of data per image
        file = urllib.urlopen(image_url)
        (width, height) = (0, 0)
        p = ImageFile.Parser()
        while 1:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                (width, height) = p.image.size
                break
        file.close()

        if width >= 600 and height >= 600:
            return True
        return False

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
        catalogs = business.get_product_catalogs()
        return catalogs
