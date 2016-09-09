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

from samples.samplecode.carousel_ad import CarouselAdSample
from samples.samplecode.tests.sampletestcase import SampleTestCase
from facebookads.objects import AdSet


class CarouselAdTestCase(SampleTestCase):

    def setUp(self):
        super(CarouselAdTestCase, self).setUp()
        self.sample = CarouselAdSample()

    def test_normal(self):
        products = [{
            "link": "https://www.gaishen.org/img/photo/skypark_night.jpg",
            "name": "Skypark at night",
            "description": "Singapore Marina Bay Sky Park at night",
            "image_path": self.images[2],
        }, {
            "link": "https://www.gaishen.org/img/photo/garden_day.jpg",
            "name": "Garden by the Bay",
            "description": "Singapore Garden By The Bay",
            "image_path": self.images[3],
        }]

        result = self.sample.create_carousel_ad(
            self.account_id,
            self.page_id,
            "http://www.gaishen.org",
            "Some caption",
            "Some message",
            AdSet.OptimizationGoal.link_clicks,
            AdSet.BillingEvent.link_clicks,
            100,    # bid
            "Ad name",
            self.basic_targeting,
            products,
        )
        self.assertEqual(len(result), 3)
        campaign = result[0]
        ad_set = result[1]
        ad = result[2]
        self.assertIsNotNone(campaign)
        self.assertIsNotNone(ad_set)
        self.assertIsNotNone(ad)
        self.campaign = campaign

    def tearDown(self):
        super(CarouselAdTestCase, self).tearDown()
        if hasattr(self, 'campaign'):
            self.campaign.remote_delete()
