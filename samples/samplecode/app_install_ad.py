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
# Mobile App Install Ads

## Creating mobile app install ads

***

This sample shows how to use the Marketing API to create a new mobile app
install ad.

## References:

* [Mobile App Install Ads][1]

[1]: https://developers.facebook.com/docs/marketing-api/mobile-app-ads/
"""
from facebookads.objects import (
    AdImage,
    Campaign,
    AdSet,
    AdCreative,
    Ad
)
from facebookads.specs import ObjectStorySpec, LinkData


class AppInstallAdSample:
    """
    This class provides a function (`create_app_install_ad`) to create
    a mobile app install ad with Facebook Marketing API.
    """
    def create_app_install_ad(
        self,
        account_id,
        base_name,
        message,
        image_path,
        daily_budget,
        page_id,
        optimization_goal,
        billing_event,
        bid_amount,
        targeting,
        app_id,
        app_name,
        app_store_link,
        deferred_app_link=None,
    ):
        """
        There are 5 steps in creating a mobile app install ad.

        1. upload an ad image
        2. create a campaign
        3. create an ad set
        4. create an ad creative
        5. create an ad

        Please read each corresponding function's doc for further details.

        Params:

        * `account_id` is your Facebook AdAccount id
        * `base_name` is a string for the name of your campaign, ad set and ad.
        * `message` is the text in the ad.
        * `image_path` is the path of an image file to be used in your ad.
        * `daily_budget` is integer number in your currency. E.g., if your
           currency is USD, dailybudget=1000 says your budget is 1000 USD.
        * `page_id` is the page that the creative comes from.
        * `optimization_goal` Which optimization goal to use for this adset
        * `billing_event` Billing event for this adset
        * `bid_amount` Bid amount for this adset, 100 says bid $1.00. See [Ad
          Set][1] for details on bidding.
        * `targeting` is a JSON string specifying targeting info of your ad.
          See [Targeting Specs][2] for details.
        * `app_id` is the id of the app.
        * `app_name` is the name of the app.
        * `app_store_link` is the link to the store link, Google play store or
          iTunes.
        * `deferred_app_link` is a optional deferred app link.

        [1]: https://developers.facebook.com/docs/marketing-api/adset
        [2]: https://developers.facebook.com/docs/marketing-api/targeting-specs
        """
        image_hash = self.upload_ad_image(account_id, image_path)

        campaign_id = self.create_campaign(
            account_id,
            '%s Campaign' % base_name
        )

        adset_id = self.create_ad_set(
            account_id,
            '%s AdSet' % base_name,
            daily_budget,
            campaign_id,
            optimization_goal,
            billing_event,
            bid_amount,
            targeting,
            app_id,
            app_store_link,
        )

        creative_id = self.create_creative(
            account_id,
            '%s Creative' % base_name,
            image_hash,
            message,
            page_id,
            app_name,
            app_store_link,
            deferred_app_link,
        )

        ad_id = self.create_ad(
            account_id,
            '%s Ad' % base_name,
            adset_id,
            creative_id,
            app_id,
        )

        return {
            'image_hash': image_hash,
            'campaign_id': campaign_id,
            'adset_id': adset_id,
            'creative_id': creative_id,
            'ad_id': ad_id,
        }

    def upload_ad_image(self, account_id, image_path):
        """
        Step 1: upload an ad image. See
        [Ad Image](https://developers.facebook.com/docs/marketing-api/adimage)
        for further details on the API used here.
        """
        image = AdImage(parent_id=account_id)
        image[AdImage.Field.filename] = image_path
        image.remote_create()
        return image[AdImage.Field.hash]

    def create_campaign(self, account_id, name):
        """
        Step 2: create a campaign. See [Campaign][1] for further details on
        the API used here.
        [1]: https://developers.facebook.com/docs/marketing-api/adcampaign
        """
        campaign = Campaign(parent_id=account_id)
        campaign[Campaign.Field.name] = name
        campaign[Campaign.Field.objective] = (
            Campaign.Objective.mobile_app_installs
        )
        campaign.remote_create(params={
            'status': Campaign.Status.paused
        })
        return campaign[Campaign.Field.id]

    def create_ad_set(self, account_id, name, daily_budget, campaign_id,
                      optimization_goal, billing_event, bid_amount,
                      targeting, app_id, app_store_link):
        """
        Step 3: create an ad set in campaign we just created. See [Ad Set][1]
        for further details on the API used here.
        [1]: https://developers.facebook.com/docs/marketing-api/adset
        """
        pdata = {
            AdSet.Field.name: name,
            AdSet.Field.optimization_goal: optimization_goal,
            AdSet.Field.billing_event: billing_event,
            AdSet.Field.bid_amount: bid_amount,
            AdSet.Field.daily_budget: daily_budget,
            AdSet.Field.campaign_id: campaign_id,
            AdSet.Field.promoted_object: {
                'application_id': app_id,
                'object_store_url': app_store_link
            },
            AdSet.Field.targeting: targeting,
        }
        pdata['status'] = AdSet.Status.paused
        adset = AdSet(parent_id=account_id)
        adset.remote_create(params=pdata)
        return adset[AdSet.Field.id]

    def create_creative(self, account_id, name, image_hash, message, page_id,
                        app_name, app_store_link, deferred_app_link):
        """
        Step 4: create ad creative with call to action type to be
        'INSTALL_MOBILE_APP'. See [Ad Creative][1] for further details on the
        API used here.
        [1]: https://developers.facebook.com/docs/marketing-api/adcreative
        """
        link_data = LinkData()
        link_data[LinkData.Field.link] = app_store_link
        link_data[LinkData.Field.message] = message
        link_data[LinkData.Field.image_hash] = image_hash
        call_to_action = {'type': 'INSTALL_MOBILE_APP'}
        call_to_action['value'] = {
            'link': app_store_link,
            'link_title': app_name
        }
        if deferred_app_link:
            call_to_action['value']['app_link'] = deferred_app_link

        link_data[LinkData.Field.call_to_action] = call_to_action

        object_story_spec = ObjectStorySpec()
        object_story_spec[ObjectStorySpec.Field.page_id] = page_id
        object_story_spec[ObjectStorySpec.Field.link_data] = link_data

        creative = AdCreative(parent_id=account_id)
        creative[AdCreative.Field.name] = name
        creative[AdCreative.Field.object_story_spec] = object_story_spec
        creative.remote_create()

        return creative[AdCreative.Field.id]

    def create_ad(self, account_id, name, adset_id, creative_id, app_id):
        """
        Step 5: finally create the ad within our campaign, ad set and creative.
        See
        [Ad Group](https://developers.facebook.com/docs/marketing-api/adgroup)
        for further details on the API used here.
        """
        adgroup = Ad(parent_id=account_id)
        adgroup[Ad.Field.name] = name
        adgroup[Ad.Field.adset_id] = adset_id
        adgroup[Ad.Field.creative] = {'creative_id': str(creative_id)}
        tracking_specs = [
            {'action.type': ['mobile_app_install'],
             'application': [app_id]},
            {'action.type': ['app_custom_event'],
             'application': [app_id]}
        ]

        adgroup[Ad.Field.tracking_specs] = tracking_specs

        adgroup.remote_create(params={
            'status': Ad.Status.paused
        })
        return adgroup[Ad.Field.id]
