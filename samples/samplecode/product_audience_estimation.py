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
# Product Audience Estimation

## Estimate the size of your product audience

***

This sample demos how to use reach estimation API to estimate the size of
your product audience. In detail, in this sample we use ad account reach
estimate edge.

## References:
* [Reach estimate][1]

[1]: https://developers.facebook.com/docs/marketing-api/reachestimate
"""
from facebookads.objects import (
    AdAccount,
    ReachEstimate
)
import copy


class ProductAudienceEstimation:

    def estimate(
        self,
        account_id,
        product_set_id,
        targeting_spec,
    ):
        """
        This function will estimate product audience of `product_set_id`,
        defined with `targeting_spec`, in the context of ad account
        `account_id`. You need to ensure that ad account and product set
        are belong to same business, otherwise probably we will get invalid
        response or zero audience from Facebook.

        Params:

        * `account_id`: The ad account id to use in estimation, in
          format of `act_xxxxxx`.

        * `product_set_id`: The product set id to use in estimation.

        * `targeting_spec`: The product audience targeting spec without
          `product_set_id` as we will set it in code. Please check here for
          how to define product audience rules
          (https://developers.facebook.com/docs/marketing-api/dynamic-product-ads/product-audiences,
          step 3).
        """
        adaccount = AdAccount(account_id)

        ts = copy.deepcopy(targeting_spec)
        ts['product_set_id'] = product_set_id
        targeting_spec = {'product_audience_specs': [ts]}

        params = {
            'currency': 'USD',
            'optimize_for': ReachEstimate.OptimizeFor.link_clicks,
            'targeting_spec': targeting_spec,
        }
        reachestimates = adaccount.get_reach_estimate(params=params)
        return reachestimates.get_one()
