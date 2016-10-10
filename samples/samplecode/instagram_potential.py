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
# Instagram Ads

## Instagram Ad Analyzer

***

This code checks the current ads of a selected ad account, and gives suggestion
about which ads should be considered to have a campaign on Instagram.

## References:

* [Instagram Ads document][1]

[1]: https://developers.facebook.com/docs/marketing-api/guides/instagramads/
"""
import locale
from facebookads.objects import (
    AdAccount,
    Campaign,
    AdSet,
    AdCreative,
    AdPreview,
)
from facebookads import FacebookAdsApi
from facebookads.exceptions import FacebookRequestError
import logging
logger = logging.getLogger(__name__)


class InstagramAdsPotential:
    def get_ad_sets(self, account_id, include_archived, limit):
        """
        Retrieves and displays a list of ad sets of a given account,
        and analyze how likely a similar ad for Instagram can be created.

        Params:

        * `account_id` is your Facebook Ad Account id.
        * `include_archived` specifies whether archived ad sets should be
          analyzed.
        * `limit` is how many ad sets to analyze. This script will analyze the
          first `limit` ad sets as in the response, not including those which
          use Instagram placement already. The more this limit is, the longer
          it takes to run. If you run the script directly and are willing
          to wait for a while, you can drop the lines of code around it.

        For more information see the [Instagram Ads document](
        https://developers.facebook.com/docs/marketing-api/guides/instagramads/)
        """
        locale.setlocale(locale.LC_ALL, '')
        if include_archived:
            params = {
                'limit': limit,
                AdSet.Field.configured_status: [
                    'PENDING', 'ACTIVE', 'PAUSED', 'PENDING_REVIEW',
                    'DISAPPROVED', 'PREAPPROVED', 'PENDING_BILLING_INFO',
                    'CAMPAIGN_PAUSED', 'CAMPAIGN_GROUP_PAUSED', 'ARCHIVED'
                ],
            }
        else:
            params = {'limit': limit}
        account = AdAccount(account_id)
        ad_sets = account.get_ad_sets(
            fields=[
                AdSet.Field.id,
                AdSet.Field.campaign_id,
                AdSet.Field.name,
                AdSet.Field.configured_status,
                AdSet.Field.targeting,
            ],
            params=params
        )
        cache = {}
        count = 0
        results = []
        for ad_set in ad_sets:
            if count >= limit:
                break
            count += 1

            result = {}
            result['id'] = ad_set['id']
            result['name'] = ad_set['name']
            logger.error(ad_set)

            # Get targeting from ad set
            targeting = ad_set.get(AdSet.Field.targeting, None)
            logger.error(targeting)
            if targeting is not None:
                publisher_platforms = targeting.get('publisher_platforms', None)
                pp_str = ''
                if publisher_platforms is None:
                    result['publisher_platforms'] = '<li>DEFAULT</li>'
                else:
                    for pp in publisher_platforms:
                        pp_str += ('<li>' +
                                   self.translate_placement_publisher(str(pp)) +
                                   '</li>')
                    result['publisher_platforms'] = pp_str

                params = {
                    'currency': 'USD',
                    'targeting_spec': targeting,
                    'optimize_for': AdSet.OptimizationGoal.impressions,
                }

                if publisher_platforms is not None and "instagram" in \
                        publisher_platforms:
                    count -= 1
                    continue

                reach_fb = account.get_reach_estimate(
                    params=params)[0].get('users', 0)

                targeting['publisher_platforms'] = ["instagram"]
                targeting['facebook_positions'] = None
                params = {
                    'currency': 'USD',
                    'targeting_spec': targeting,
                    'optimize_for': AdSet.OptimizationGoal.impressions,
                }
                reach_ig = account.get_reach_estimate(
                    params=params)[0].get('users', 0)

                self.add_check_result(
                    result,
                    self.check_audience(reach_fb, reach_ig))
                result["audience"] = reach_ig * 100 / reach_fb
                result["ig_audience"] = locale.format(
                    "%d", reach_ig, grouping=True)
            # Get objective and status from Campaign
            campaign_id = ad_set[AdSet.Field.campaign_id]
            campaign = self.get_ad_campaign(cache, campaign_id)
            result["c_objective"] = \
                campaign[Campaign.Field.objective].replace("_", " ")
            result["c_status"] = campaign[Campaign.Field.configured_status]
            check = self.check_objective(result["c_objective"])
            if check['eligibility'] == 5:
                result['objective_supported'] = 1
            elif check['eligibility'] == 1:
                result['objective_supported'] = 0
            else:
                result['objective_supported'] = 2

            self.add_check_result(result, check)

            # Get creative and check the media
            if campaign[Campaign.Field.objective] == 'PRODUCT_CATALOG_SALES':
                result['preview_url'] = \
                    'Images from product catalog are not supported.'
                results.append(result)
                result['creative_ready'] = False
                continue

            creatives = ad_set.get_ad_creatives([
                AdCreative.Field.object_story_id,
            ])
            result['creative_ready'] = False
            if not creatives:
                comment = 'No creative found in this ad set.'
                self.add_check_result(
                    result,
                    {
                        "eligibility": 3,
                    }
                )
                result['preview_url'] = comment
                results.append(result)
                continue
            creative = creatives[0]
            story_id = creative.get(AdCreative.Field.object_story_id, 0)
            if story_id == 0:
                comment = 'No post fround in the first creative of this ad set.'
                self.add_check_result(
                    result,
                    {
                        "eligibility": 3,
                    }
                )
                result['preview_url'] = comment
                results.append(result)
                continue

            # Check whether the creative's post is IG ready
            try:
                # This Graph API call is not a part of Ads API thus no SDK
                post = FacebookAdsApi.get_default_api().call(
                    'GET',
                    (story_id,),
                    params={
                        'fields': 'is_instagram_eligible,child_attachments'
                    },
                )
                post_ig_eligible = post.json()['is_instagram_eligible']
            except FacebookRequestError:
                post_ig_eligible = False
            result['creative_ready'] = post_ig_eligible
            if post_ig_eligible:
                self.add_check_result(
                    result,
                    {
                        "eligibility": 5,
                    }
                )

                # Generate preview
                # As we do not know which IG account you will use,
                # just use a hardcoded one for preview.
                jasper_ig_account = "1023317097692584"
                ad_format = 'INSTAGRAM_STANDARD'
                creative_spec = {
                    'instagram_actor_id': jasper_ig_account,
                    'object_story_id': story_id,
                }
                params = {
                    AdPreview.Field.creative: creative_spec,
                    AdPreview.Field.ad_format: ad_format,
                }
                preview = account.get_generate_previews(params=params)
                result['preview_url'] = preview[0].get_html() \
                    .replace('width="320"', 'width="340"', 1)
            else:
                comment = 'The creative needs to be modified for Instagram.'
                self.add_check_result(
                    result,
                    {
                        "eligibility": 3,
                    }
                )
                result['preview_url'] = comment
            results.append(result)
        return list(sorted(
            results,
            key=lambda result: result['eligibility'],
            reverse=True))

    def check_audience(self, reach_fb, reach_ig):
        """
        Compare the estimate audience size of the same targeting option on
        Instagram vs. on Facebook.

        Params:

        * `reach_fb` the estimated audience size of the existing ad set.
        * `reach_ig` the estimated audience size of an ad set with the same
          targeting but on Instagram only.
        """
        if reach_ig <= reach_fb * 0.05:
            return {
                "eligibility": 1,
                "comment": 'The target audience is not on Instagram.'}
        elif reach_ig <= reach_fb * 0.15:
            return {
                "eligibility": 2,
                "comment": 'The target audience may not be well represented' +
                ' on Instagram.'}
        elif reach_ig <= reach_fb * 0.25:
            return {
                "eligibility": 3,
                "comment": 'The target audience is partially on Instagram.'}
        elif reach_ig <= reach_fb * 0.40:
            return {
                "eligibility": 4,
                "comment": 'The target audience can be represented on ' +
                'Instagram.'}
        else:
            return {
                "eligibility": 5,
                "comment": 'The target audience is well represented on ' +
                'Instagram.'}

    def add_check_result(self, result, check):
        """
        Accumulate a check result into the overall result

        Params:

        * `result` the accumulated analysis result of the current ad set.
        * `check` the result of one analysis item.
        """
        if result.get('eligibility') is None:
            result['eligibility'] = check['eligibility']
            result['suggestion'] = '<li>' + check.get('comment', '')
        else:
            result['eligibility'] = min(
                result['eligibility'],
                check['eligibility'])
            if check.get('comment', None) is not None:
                result['suggestion'] += '<li>' + check['comment']

    def get_ad_campaign(self, cache, campaign_id):
        """
        Get the ad campaign. As some ad sets being analyzed belong to the
        same ad campaign, a caching is used to reduce the API calls.

        Params:

        * `cache` ad campaigns obtained already.
        * `campaign_id` the id of the ad campaign to be queried out.
        """

        if (cache.get(campaign_id) is None):
            campaign = Campaign(fbid=campaign_id)
            campaign.remote_read(fields=[
                Campaign.Field.name,
                Campaign.Field.configured_status,
                Campaign.Field.objective,
            ])
            cache[campaign_id] = campaign
        return cache.get(campaign_id)

    def check_objective(self, objective):
        """
        Compare the objective of the ad campaign to see whether it is
        supported by Instagram already.

        Params:

        * `objective` the objective to be checked.
        """
        return {
            'WEBSITE CLICKS': {"eligibility": 5},
            'LINK CLICKS': {"eligibility": 5},
            'VIDEO VIEWS': {"eligibility": 5},
            'MOBILE APP INSTALLS': {"eligibility": 5},
            'WEBSITE CONVERSIONS': {"eligibility": 5},
            'CONVERSIONS': {"eligibility": 5},
            'POST ENGAGEMENT': {"eligibility": 5},
            'MOBILE APP ENGAGEMENT': {"eligibility": 5},
            'BRAND AWARENESS': {"eligibility": 5},
        }.get(objective, {
            "eligibility": 1,
            "comment": objective + ' objective is not supported yet.'})

    def translate_placement_publisher(self, code):
        """
        Translate the placement publisher to their known names.

        Params:

        * `code` the page_type used as in API.
        """
        return {
            'instagram': 'Instagram',
            'facebook': 'Facebook',
            'audience_network': 'Audience Network',
        }.get(code, code)
