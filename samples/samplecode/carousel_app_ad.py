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
# Carousel App Ad

## Creating carousel app install ads

***

<img class="title-img"
    src="/static/images/carouselappad_title.jpg" />


This sample shows how to use the Marketing API to create a new mobile app
install ad in the carousel format.

## References:

* [Carousel Ads][1]
* [Mobile App Ads][2]

[1]: https://developers.facebook.com/docs/marketing-api/guides/carousel-ads
[2]: https://developers.facebook.com/docs/marketing-api/mobile-app-ads
"""
from facebookads.objects import (
    AdImage,
    Campaign,
    AdSet,
    AdCreative,
    Ad
)
from facebookads.specs import ObjectStorySpec, LinkData, AttachmentData


class CarouselAppAdSample:
    """
    This class provides a funciton (`carousel_app_ad_create`) to create
    a mobile app install ad in the carousel format with Facebook Marketing API.
    """

    def carousel_app_ad_create(
        self,
        accountid,
        basename,
        message,
        imagefilepaths,
        linktitles,
        deeplinks,
        dailybudget,
        appinfo,
        optimization_goal,
        billing_event,
        bid_amount,
        targeting,
    ):
        """
        There are 5 steps in creating a carousel mobile app install ad.

        1. upload ad images for the carousel
        2. create a campaign
        3. create an ad set
        4. create an ad creative of the carousel format
        5. create an ad

        Please read each corresponding function's doc for further details.

        Params:

        * `accountid` is your Facebook AdAccount id
        * `basename` is a string of base name of your ads
        * `message` is the text message above the carousel
        * `imagefilepaths` is the list of image file paths
        * `linktitles` is the list of title messages for the carousel
        * `deeplinks` is the list of deep links for the carousel
        * `dailybudget` is integer number in your currency. E.g., if your
           currency is USD, dailybudget=1000 says your budget is 1000 USD.
        * `appinfo` is a dict with following keys: `app_name`, `app_store_url`,
           `fbapplication_id` and `fbpage_id`.
        * `optimization_goal` Which optimization goal to use for this adset
        * `billing_event` Billing event for this adset
        * `bid_amount` Bid amount for this adset, 100 says bid $1.00. See [Ad
          Set][1] for details on bidding.
        * `targeting` is a JSON string specifying targeting info of your ad.
          See [Targeting Specs][2]
          for details.

        [1]: https://developers.facebook.com/docs/marketing-api/adset
        [2]: https://developers.facebook.com/docs/marketing-api/targeting-specs

        """
        imagehashes = self.s1_upload_ad_images(accountid, imagefilepaths)

        campaignid = self.s2_create_campaign(
            accountid,
            '%s Campaign' % basename
        )

        adsetid = self.s3_create_ad_set(
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

        creativeid = self.s4_create_creative(
            accountid,
            '%s Creative' % basename,
            imagehashes,
            linktitles,
            deeplinks,
            message,
            appinfo
        )

        adid = self.s5_create_ad(
            accountid,
            '%s Ad' % basename,
            adsetid,
            creativeid,
            appinfo
        )

        return {
            'campaignid': campaignid,
            'adsetid': adsetid,
            'creativeid': creativeid,
            'adid': adid
        }

    def s1_upload_ad_images(self, accountid, imagefilepaths):
        """
        Step 1: upload an images for the carousel. See
        [Ad Image](https://developers.facebook.com/docs/marketing-api/adimage)
        for further details on the API used here.
        """
        result = []
        for imagefilepath in imagefilepaths:
            image = AdImage(parent_id=accountid)
            image[AdImage.Field.filename] = imagefilepath
            image.remote_create()
            result.append(image[AdImage.Field.hash])
        return result

    def s2_create_campaign(self, accountid, name):
        """
        Step 2: create a campaign. See
        [Ad Campaign](
        https://developers.facebook.com/docs/marketing-api/adcampaign)
        for further details on the API used here.
        """
        campaign = Campaign(parent_id=accountid)
        campaign[Campaign.Field.name] = name
        campaign[Campaign.Field.objective] = (
            Campaign.Objective.mobile_app_installs
        )

        campaign.remote_create(params={
            'status': Campaign.Status.paused
        })
        return campaign[Campaign.Field.id]

    def s3_create_ad_set(self, accountid, name, dailybudget, campaignid,
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

    def s4_create_creative(
        self,
        accountid,
        name,
        imagehashes,
        linktitles,
        deeplinks,
        message,
        appinfo
    ):
        """
        Step 4: create ad creative with call to action type to be
        'INSTALL_MOBILE_APP'. See
        [Ad Creative](
        https://developers.facebook.com/docs/marketing-api/adcreative)
        for further details on the API used here.
        """
        attachments = []
        for index, imagehash in enumerate(imagehashes):
            attachment = AttachmentData()
            attachment[AttachmentData.Field.link] = appinfo['appstore_link']
            attachment[AttachmentData.Field.image_hash] = imagehash
            call_to_action = {
                'type': 'INSTALL_MOBILE_APP',
                'value': {
                    'link_title': linktitles[index],
                },
            }
            if deeplinks and index in deeplinks:
                call_to_action['value']['app_link'] = deeplinks[index]

            attachment[AttachmentData.Field.call_to_action] = call_to_action
            attachments.append(attachment)

        link_data = LinkData()
        link_data[LinkData.Field.link] = appinfo['appstore_link']
        link_data[LinkData.Field.message] = message
        link_data[LinkData.Field.child_attachments] = attachments

        object_story_spec = ObjectStorySpec()
        object_story_spec[ObjectStorySpec.Field.page_id] = appinfo['fbpage_id']
        object_story_spec[ObjectStorySpec.Field.link_data] = link_data

        creative = AdCreative(parent_id=accountid)
        creative[AdCreative.Field.name] = name
        creative[AdCreative.Field.object_story_spec] = object_story_spec
        creative.remote_create()

        return creative[AdCreative.Field.id]

    def s5_create_ad(self, accountid, name, adsetid, creativeid, appinfo):
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

        ad[Ad.Field.tracking_specs] = tracking_specs

        ad.remote_create(params={
            'status': Ad.Status.paused
        })
        return ad[Ad.Field.id]
