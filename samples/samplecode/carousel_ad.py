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
# Carousel Ads

## Creating carousel link ads

***

<img class="title-img"
    src="/static/images/carousel_title.png" />


This sample shows how to create carousel link ads with up to 10 different
products. The sample sets `multi_share_optimized` to
True so Facebook will automatically select the 5 best performing products to
show in the ad.

## References:

* [Carousel Ads][1]

[1]: https://developers.facebook.com/docs/marketing-api/guides/carousel-ads
"""
from facebookads.objects import (
    Campaign,
    AdSet,
    Ad,
    AdImage,
    AdCreative,
)
from facebookads.specs import ObjectStorySpec, LinkData, AttachmentData


class CarouselAdSample:
    """
    This class provides a function named create_carousel_ad that takes in
    the creative elements for up to 10 different products,
    optimization goal, billing event, bid amount and
    targeting and creates a carousel ad in a newly created campaign. It returns
    the campaign, adset and ad.
    """
    def create_carousel_ad(
        self,
        accountid,
        page_id,
        site_link,
        caption,
        message,
        optimization_goal,
        billing_event,
        bid_amount,
        name,
        targeting,
        products,
        call_to_action_type=None,
    ):
        """
        There are 5 steps in this sample:

        1. Create a campaign
        2. Create an ad set
        3. For each product:
          a. Upload the product's image and get an image hash
          b. Create a story attachment using the product's creative elements
        4. Prepare the ad creative
        5. Create the ad using the ad creative
        """

        daily_budget = 10000

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
            'status': Campaign.Status.paused
        })
        """
        Step 2: Create AdSet using specified optimization goal, billing event
        and bid.
        See
        [AdSet](https://developers.facebook.com/docs/marketing-api/reference/ad-campaign)
        for further details on the API used here.
        """
        ad_set = AdSet(parent_id=accountid)
        ad_set[AdSet.Field.campaign_id] = campaign.get_id_assured()
        ad_set[AdSet.Field.name] = name + ' AdSet'
        ad_set[AdSet.Field.optimization_goal] = optimization_goal
        ad_set[AdSet.Field.billing_event] = billing_event
        ad_set[AdSet.Field.bid_amount] = bid_amount
        ad_set[AdSet.Field.daily_budget] = daily_budget
        ad_set[AdSet.Field.targeting] = targeting
        ad_set.remote_create()

        story_attachments = []
        """
        Step 3: Upload images and get image hashes for use in ad creative.
        See
        [Ad Image](https://developers.facebook.com/docs/marketing-api/reference/ad-image#Creating)
        for further details on the API used here.
        Then create a new attachment with the product's creative
        """
        call_to_action = {
            'type': call_to_action_type,
            'value': {
                'link': site_link,
                'link_caption': call_to_action_type,
            }
        } if call_to_action_type else None

        for product in products:
            img = AdImage(parent_id=accountid)
            img[AdImage.Field.filename] = product['image_path']
            img.remote_create()
            image_hash = img.get_hash()
            attachment = AttachmentData()
            attachment[AttachmentData.Field.link] = product['link']
            attachment[AttachmentData.Field.name] = product['name']
            attachment[AttachmentData.Field.description] = product[
                'description']
            attachment[AttachmentData.Field.image_hash] = image_hash
            if call_to_action:
                attachment[
                    AttachmentData.Field.call_to_action] = call_to_action
            story_attachments.append(attachment)

        """
        Step 4: Prepare the ad creative including link information
        Note that here we specify multi_share_optimized = True
        this means you can add up to 10 products and Facebook will
        automatically select the best performing 5 to show in the ad. Facebook
        will also select the best ordering of those products.
        """
        link = LinkData()
        link[link.Field.link] = site_link
        link[link.Field.caption] = caption
        link[link.Field.child_attachments] = story_attachments
        link[link.Field.multi_share_optimized] = True
        link[link.Field.call_to_action] = call_to_action

        story = ObjectStorySpec()
        story[story.Field.page_id] = page_id
        story[story.Field.link_data] = link

        creative = AdCreative()
        creative[AdCreative.Field.name] = name + ' Creative'
        creative[AdCreative.Field.object_story_spec] = story

        """
        Step 5: Create the ad using the above creative
        """
        ad = Ad(parent_id=accountid)
        ad[Ad.Field.name] = name + ' Ad'
        ad[Ad.Field.adset_id] = ad_set.get_id_assured()
        ad[Ad.Field.creative] = creative

        ad.remote_create(params={
            'status': Ad.Status.paused
        })
        return (campaign, ad_set, ad)
