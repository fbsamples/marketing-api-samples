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
# Lead Ads

## Creating lead ads

***

This sample shows how to use the Marketing API to create a new lead ad. Lead Ads
allow advertisers a mechanism to capture leads using native Facebook products.
The ads open a form that prompt advertisers with custom qualifiers or to confirm
contact information. The data is then collected and sent back to the advertiser.
The most important part of the lead ad is the lead form. In this sample, you can
use the lead form UI component to input an existing lead form you created before
, or create a new one.

## References:

* [Lead Ads Reference][1]

[1]: https://developers.facebook.com/docs/marketing-api/guides/lead-ads
"""
from facebookads.objects import (
    Campaign,
    AdSet,
    Ad,
    AdCreative,
    AdImage,
)
from facebookads.specs import ObjectStorySpec, LinkData


class LeadAdSample:
    """
    The flow of creating a lead ad is similar to creation of other ads, except
    for the following special settings:

    * The campaign must have its `objective` set to `LEAD_GENERATION`
    * The campaign should have its `buying_type` set to `AUCTION`
    * The ad set must have its `promoted_object` set to the corresponding
    `<PAGE_ID>`
    * The ad set's `optimization_goal` must be set to `LEAD_GENERATION`
    * The ad set's `billing_event` should be set to `IMPRESSIONS`
    * The targeting for the ad set can be either `mobilefeed` or `desktopfeed`
    """
    def create_lead_ad(
        self,
        account_id,
        name,
        page_id,
        form_id,
        optimization_goal,
        billing_event,
        bid_amount,
        daily_budget,
        targeting,
        image_path,
        message,
        link,
        caption,
        description,
        cta_type='SIGN_UP',
    ):
        """
        Create Campaign
        """
        campaign = Campaign(parent_id=account_id)
        campaign[Campaign.Field.name] = name + ' Campaign'
        campaign[Campaign.Field.objective] = \
            Campaign.Objective.lead_generation
        campaign[Campaign.Field.buying_type] = \
            Campaign.BuyingType.auction

        campaign.remote_create(params={
            'status': Campaign.Status.paused
        })

        """
        Create AdSet
        """
        adset = AdSet(parent_id=account_id)
        adset[AdSet.Field.campaign_id] = campaign.get_id_assured()
        adset[AdSet.Field.name] = name + ' AdSet'
        adset[AdSet.Field.promoted_object] = {
            'page_id': page_id,
        }
        adset[AdSet.Field.optimization_goal] = optimization_goal
        adset[AdSet.Field.billing_event] = billing_event
        adset[AdSet.Field.bid_amount] = bid_amount
        adset[AdSet.Field.daily_budget] = daily_budget
        adset[AdSet.Field.targeting] = targeting
        adset.remote_create()

        """
        Image
        """
        image = AdImage(parent_id=account_id)
        image[AdImage.Field.filename] = image_path
        image.remote_create()
        image_hash = image[AdImage.Field.hash]

        """
        Create Creative
        """
        link_data = LinkData()
        link_data[LinkData.Field.message] = message
        link_data[LinkData.Field.link] = link
        link_data[LinkData.Field.image_hash] = image_hash
        link_data[LinkData.Field.caption] = caption
        link_data[LinkData.Field.description] = description
        link_data[LinkData.Field.call_to_action] = {
            'type': cta_type,
            'value': {
                'lead_gen_form_id': form_id,
            },
        }

        object_story_spec = ObjectStorySpec()
        object_story_spec[ObjectStorySpec.Field.page_id] = page_id
        object_story_spec[ObjectStorySpec.Field.link_data] = link_data

        creative = AdCreative(parent_id=account_id)
        creative[AdCreative.Field.name] = name + ' Creative'
        creative[AdCreative.Field.object_story_spec] = object_story_spec
        creative.remote_create()

        """
        Create Ad
        """
        ad = Ad(parent_id=account_id)
        ad[Ad.Field.name] = name
        ad[Ad.Field.adset_id] = adset.get_id_assured()
        ad[Ad.Field.creative] = {'creative_id': str(creative.get_id_assured())}
        ad.remote_create()

        return {
            'image_hash': image_hash,
            'campaign_id': campaign['id'],
            'adset_id': adset['id'],
            'creative_id': creative['id'],
            'ad_id': ad['id'],
        }
