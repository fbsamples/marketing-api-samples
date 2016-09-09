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
# Creative Testing

## Creating ads with combination of creative elements

***

This sample shows how to create ads that use different combinations of
creative elements.
This is useful to test  multiple images, text, and landing pages and see
which performs best.
Suppose you have 1 link, 2 titles, 2 body, and 3 images, the result will
be 1 x 2 x 2 x 3 = 12 creatives in the result ad set. Instead of making 12
separate requests, the sample uses the batch API to send one request with all
12 creatives.

## References:

* Marketing API Guide: [Chapter 3 - Ad creative, placement, and previews][1]
* [Batch requests][2]

[1]: https://developers.facebook.com/docs/marketing-api/guides/chapter-3-ad-creative
[2]: https://developers.facebook.com/docs/marketing-api/batch-requests
"""
from facebookads.objects import (
    AdAccount,
    Campaign,
    AdSet,
    Ad,
    AdImage,
    AdCreative,
)
import itertools
from utils import generate_batches


class AdCreationSample:
    """
    This class provides a function named create_multiple_link_clicks_ads
    that takes in multiple creative elements (e.g. images, text, links) and
    creates ads using all combinations of those elements.
    """

    def create_multiple_link_clicks_ads(
        self,

        accountid,
        pageid,

        name,

        titles,
        bodies,
        urls,
        image_paths,

        targeting,

        optimization_goal,
        billing_event,
        bid_amount,
        daily_budget=None,
        lifetime_budget=None,

        start_time=None,
        end_time=None,
    ):
        """
        There are 7 steps in this sample:

        1. Create a campaign
        2. Create an ad set
        3. Upload images
        4. Make combinations of specified creative elements
        5. Prepare an API batch
        6. For each creative combination, add a call to the batch to create a
        new ad
        7. Execute API batch

        Params:

        * `accountid` is your Facebook AdAccount id
        * `name` is a string of basename of your ads.
        * `page` is the Facebook page used to publish the ads
        * `titles` array of strings of what user will see as ad title
        * `bodies` array of strings of what user will see as ad body
        * `image_paths` array of image file paths
        * `targeting` is a JSON string specifying targeting info of your ad
          See [Targeting Specs](https://developers.facebook.com/docs/marketing-api/targeting-specs)
          for details.
        * `optimization_goal` the optimization goal for the adsets
        * `billing_event` what you want to pay for
        * `bid_amount` how much you want to pay per billing event
        * `daily_budget` is integer number in your currency. E.g., if your
           currency is USD, dailybudget=1000 says your budget is 1000 USD
        * `lifetime_budget` lifetime budget for created ads
        * `start_time` when the campaign should start
        * `end_time` when the campaign should end


        """
        my_account = AdAccount(fbid=accountid)

        """
          Take different title body url and image paths, create a batch of
          ads based on the permutation of these elements
        """
        # Check for bad specs
        if daily_budget is None:
            if lifetime_budget is None:
                raise TypeError(
                    'One of daily_budget or lifetime_budget must be defined.'
                )
            elif end_time is None:
                raise TypeError(
                    'If lifetime_budget is defined, end_time must be defined.'
                )

        """
        Step 1: Create new campaign with WEBSITE_CLICKS objective
        See
        [Campaign Group](https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group)
        for further details on the API used here.
        """
        campaign = Campaign(parent_id=accountid)
        campaign[Campaign.Field.name] = name + ' Campaign'
        campaign[Campaign.Field.objective] = \
            Campaign.Objective.link_clicks

        campaign.remote_create(params={
            'status': Campaign.Status.paused,
        })

        """
        Step 2: Create AdSet using specified optimization goal, billing event
        and bid.
        See
        [AdSet](https://developers.facebook.com/docs/marketing-api/reference/ad-campaign)
        for further details on the API used here.
        """
        # Create ad set
        ad_set = AdSet(parent_id=accountid)
        ad_set[AdSet.Field.campaign_id] = campaign.get_id_assured()
        ad_set[AdSet.Field.name] = name + ' AdSet'
        ad_set[AdSet.Field.optimization_goal] = optimization_goal
        ad_set[AdSet.Field.billing_event] = billing_event
        ad_set[AdSet.Field.bid_amount] = bid_amount
        if daily_budget:
            ad_set[AdSet.Field.daily_budget] = daily_budget
        else:
            ad_set[AdSet.Field.lifetime_budget] = lifetime_budget
        if end_time:
            ad_set[AdSet.Field.end_time] = end_time
        if start_time:
            ad_set[AdSet.Field.start_time] = start_time

        ad_set[AdSet.Field.targeting] = targeting
        ad_set.remote_create()

        """
        Step 3: Upload images and get image hashes for use in ad creative.
        See
        [Ad Image](https://developers.facebook.com/docs/marketing-api/reference/ad-image#Creating)
        for further details on the API used here.
        """
        # Upload the images first one by one
        image_hashes = []
        for image_path in image_paths:
            img = AdImage(parent_id=accountid)
            img[AdImage.Field.filename] = image_path
            img.remote_create()
            image_hashes.append(img.get_hash())

        ADGROUP_BATCH_CREATE_LIMIT = 10
        ads_created = []

        def callback_failure(response):
            raise response.error()

        """
        Step 4: Using itertools.product get combinations of creative
        elements.
        """
        for creative_info_batch in generate_batches(
            itertools.product(titles, bodies, urls, image_hashes),
            ADGROUP_BATCH_CREATE_LIMIT
        ):
            """
            Step 5: Create an API batch so we can create all
            ad creatives with one HTTP request.
            See
            [Batch Requests](https://developers.facebook.com/docs/graph-api/making-multiple-requests#simple)
            for further details on batching API calls.
            """
            api_batch = my_account.get_api_assured().new_batch()

            for title, body, url, image_hash in creative_info_batch:
                # Create the ad
                """
                Step 6: For each combination of creative elements,
                add to the batch an API call to create a new Ad
                and specify the creative inline.
                See
                [AdGroup](https://developers.facebook.com/docs/marketing-api/adgroup/)
                for further details on creating Ads.
                """
                ad = Ad(parent_id=accountid)
                ad[Ad.Field.name] = name + ' Ad'
                ad[Ad.Field.adset_id] = ad_set.get_id_assured()
                ad[Ad.Field.creative] = {
                    AdCreative.Field.object_story_spec: {
                        "page_id": pageid,
                        "link_data": {
                            "message": body,
                            "link": url,
                            "caption": title,
                            "image_hash": image_hash
                        }
                    },
                }

                ad.remote_create(batch=api_batch, failure=callback_failure)
                ads_created.append(ad)
            """
            Step 7: Execute the batched API calls
            See
            [Batch Requests](https://developers.facebook.com/docs/graph-api/making-multiple-requests#simple)
            for further details on batching API calls.
            """
            api_batch.execute()

        return [campaign, ad_set, ads_created]
