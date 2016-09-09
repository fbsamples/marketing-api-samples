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
# Mobile App Engagement Ads

## Creating mobile app engagement ads

***

This sample shows how to use the Marketing API to create a new mobile app
engagement ad.

Mobile app ads help drive engagement and conversion for your app with ads that
take users to a customized location within your app.

## References:

* [Mobile App Ads for Engagement and Conversion][1]

[1]: https://developers.facebook.com/docs/ads-for-apps/mobile-app-ads-engagement
"""
from facebookads.objects import (
    AdImage,
    Campaign,
    AdSet,
    AdCreative,
    Ad
)
from facebookads.specs import ObjectStorySpec, LinkData


class AppEngagementSample:
    """
    This class provides a funciton (`app_engagement_ad_create`) to create
    a mobile app engagement ad with Facebook Marketing API.
    """

    def app_engagement_ad_create(
        self,
        accountid,
        basename,
        message,
        imagefilepath,
        dailybudget,
        appinfo,
        optimization_goal,
        billing_event,
        bid_amount,
        targeting
    ):
        """
        There are 5 steps in creating a mobile app engagement ad.

        1. upload an ad image
        2. create a campaign
        3. create an ad set
        4. create an ad creative
        5. create an ad

        Please read each corresponding function's doc for further details.

        Params:

        * `accountid` is your Facebook AdAccount id
        * `basename` is a string of basename of your ads.
        * `message` is the string of what user will see
        * `imagefilepath` is the path of an image file to be used in your ad.
        * `dailybudget` is integer number in your currency. E.g., if your
           currency is USD, dailybudget=1000 says your budget is 1000 USD.
        * `appinfo` is a dict with following keys: `app_store_url`,
           `app_dep_link`, `fbapplication_id` and `fbpage_id`.
        * `bidtype` is the bidding type.
        * `bidinfo` is a JSON string specifying bid info of your ad.
          See [Ad Set Parameters](https://developers.facebook.com/docs/marketing-api/adset)
          for details.
        * `optimization_goal` Which optimization goal to use for this adset
        * `billing_event` Billing event for this adset
        * `bid_amount` Bid amount for this adset, 100 says bid $1.00.
        * `targeting` is a JSON string specifying targeting info of your ad.
          See [Targeting Specs](https://developers.facebook.com/docs/marketing-api/targeting-specs)
          for details.

        """
        imagehash = self.upload_ad_image(accountid, imagefilepath)

        campaignid = self.create_campaign(
            accountid,
            '%s Campaign' % basename
        )

        adsetid = self.create_ad_set(
            accountid,
            '%s AdSet' % basename,
            dailybudget,
            campaignid,
            optimization_goal,
            billing_event,
            bid_amount,
            targeting,
            appinfo
        )

        creativeid = self.create_creative(
            accountid,
            '%s Creative' % basename,
            imagehash,
            message,
            appinfo
        )

        adid = self.create_ad(
            accountid,
            '%s Ad' % basename,
            adsetid,
            creativeid,
            appinfo
        )

        return {
            'imagehash': imagehash,
            'campaignid': campaignid,
            'adsetid': adsetid,
            'creativeid': creativeid,
            'adid': adid
        }

    def upload_ad_image(self, accountid, imagefilepath):
        """
        Step 1: upload an ad image. See
        [Ad Image](https://developers.facebook.com/docs/marketing-api/adimage)
        for further details on the API used here.
        """
        image = AdImage(parent_id=accountid)
        image[AdImage.Field.filename] = imagefilepath
        image.remote_create()
        return image[AdImage.Field.hash]

    def create_campaign(self, accountid, name):
        """
        Step 2: create a campaign. See
        [Ad Campaign](https://developers.facebook.com/docs/marketing-api/adcampaign)
        for further details on the API used here.
        """
        campaign = Campaign(parent_id=accountid)
        campaign[Campaign.Field.name] = name
        campaign[Campaign.Field.objective] = (
            Campaign.Objective.mobile_app_engagement
        )

        campaign.remote_create(params={
            'status': Campaign.Status.paused
        })
        return campaign[Campaign.Field.id]

    def create_ad_set(self, accountid, name, dailybudget, campaignid,
                      optimization_goal, billing_event, bid_amount,
                      targeting, appinfo):
        """
        Step 3: create an ad set in campaign we just created. See
        [Ad Set](https://developers.facebook.com/docs/marketing-api/adset)
        for further details on the API used here.
        """
        pdata = {
            AdSet.Field.name: name,
            AdSet.Field.optimization_goal: optimization_goal,
            AdSet.Field.billing_event: billing_event,
            AdSet.Field.bid_amount: bid_amount,
            AdSet.Field.daily_budget: dailybudget,
            AdSet.Field.campaign_id: campaignid,
            AdSet.Field.promoted_object: {
                'application_id': appinfo['fbapplication_id'],
                'object_store_url': appinfo['appstore_link']
            },
            AdSet.Field.targeting: targeting,
        }
        pdata['status'] = AdSet.Status.paused
        adset = AdSet(parent_id=accountid)
        adset.remote_create(params=pdata)
        return adset[AdSet.Field.id]

    def create_creative(self, accountid, name, imagehash, message, appinfo):
        """
        Step 4: create ad creative with call to action type to be
        'USE_MOBILE_APP'. See
        [Ad Creative](https://developers.facebook.com/docs/marketing-api/adcreative)
        for further details on the API used here.
        """
        link_data = LinkData()
        link_data[LinkData.Field.link] = appinfo['appstore_link']
        link_data[LinkData.Field.message] = message
        link_data[LinkData.Field.image_hash] = imagehash
        call_to_action = {'type': 'USE_MOBILE_APP'}
        call_to_action['value'] = {
            'link': appinfo['appstore_link'],
            'app_link': appinfo['app_deep_link'],
            'application': appinfo['fbapplication_id'],
            'link_title': appinfo['app_name']
        }
        link_data[LinkData.Field.call_to_action] = call_to_action

        object_story_spec = ObjectStorySpec()
        object_story_spec[ObjectStorySpec.Field.page_id] = appinfo['fbpage_id']
        object_story_spec[ObjectStorySpec.Field.link_data] = link_data

        creative = AdCreative(parent_id=accountid)
        creative[AdCreative.Field.name] = name
        creative[AdCreative.Field.object_story_spec] = object_story_spec
        creative.remote_create()

        return creative[AdCreative.Field.id]

    def create_ad(self, accountid, name, adsetid, creativeid, appinfo):
        """
        Step 5: finally create the ad within our campaign, ad set and creative.
        See
        [Ad Group](https://developers.facebook.com/docs/marketing-api/adgroup)
        for further details on the API used here.
        """
        ad = Ad(parent_id=accountid)
        ad[Ad.Field.name] = name
        ad[Ad.Field.adset_id] = adsetid
        ad[Ad.Field.creative] = {'creative_id': str(creativeid)}
        tracking_specs = [
            {'action.type': ['mobile_app_install'],
             'application': [appinfo['fbapplication_id']]},
            {'action.type': ['app_custom_event'],
             'application': [appinfo['fbapplication_id']]}
        ]
        if not (appinfo['fboffsitepixel_id'].strip() == 'null'):
            tracking_specs.append({
                'action.type': ['offsite_conversion'],
                'offsite_pixel': [appinfo['fboffsitepixel_id']]
            })
        ad[Ad.Field.tracking_specs] = tracking_specs

        ad.remote_create(params={
            'status': Ad.Status.paused
        })
        return ad[Ad.Field.id]
