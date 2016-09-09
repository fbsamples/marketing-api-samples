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
# Tiered Lookalike Strategy

## Creating Ad Sets with tiered lookalike targeting

***

This sample first takes a data file to create a custom audience, then it
creates 5 lookalike audiences with different similarity level. With the new
tiered lookalike API, the lookalike audiences are created in the way that each
tier is excluding all the previous tiers. You can also specify a custom audience
ID as the seed audience. Then, it creates 5 ad sets that target to the tiered
lookalike audiences with different bidding settings: bid more on higher
similarity and less with lower similarity level.

## References:

* [Lookalike audiences doc][1]

[1]: https://developers.facebook.com/docs/marketing-api/lookalike-audience-targeting
"""
from facebookads.objects import (
    AdImage,
    AdCreative,
    Ad,
    AdSet,
    Campaign,
    TargetingSpecsField,
    CustomAudience,
    LookalikeAudience,
)


class TieredLookalikeSample:
    """
    The sample code for creating different lookalike audiences, and create
    tiered targeting ad sets. The tiered lookalike audiences are created with
    the `ratio` and `starting_ratio` parameters. For more information see
    [Lookalike Audiences doc](
    https://developers.facebook.com/docs/
    marketing-api/lookalike-audience-targeting/).
    """
    def create_tiered_lookalikes(
        self,
        account_id,
        name,
        seed_id,
        tiers,
        country
    ):
        """
        Take a seed custom audiences ID and create tiered lookalike audiences
        """
        tiered_audiences = []
        for tier in range(1, tiers + 1):
            lookalike = CustomAudience(parent_id=account_id)
            lookalike[LookalikeAudience.Field.name] = \
                '{0} LAL {1}'.format(name, tier)
            lookalike[LookalikeAudience.Field.origin_audience_id] = seed_id

            lal_spec = {
                LookalikeAudience.Field.LookalikeSpec.ratio: tier / 100.0,
                LookalikeAudience.Field.LookalikeSpec.country: country,
            }
            if (tier > 1):
                lal_spec[
                    # LookalikeAudience.Field.LookalikeSpec.starting_ratio
                    'starting_ratio'
                ] = (tier - 1) / 100.0

            lookalike[LookalikeAudience.Field.lookalike_spec] = lal_spec
            lookalike[CustomAudience.Field.subtype] = \
                CustomAudience.Subtype.lookalike
            lookalike.remote_create()

            tiered_audiences.append(lookalike)

        return tiered_audiences

    def create_lookalike_ads(
        self,
        account_id,
        name,

        tiered_lookalikes,
        optimization_goal,
        billing_event,
        tiered_bid_amounts,

        title,
        body,
        url,
        image_path,

        daily_budget=None,
        lifetime_budget=None,
        start_time=None,
        end_time=None,

        campaign=None,
    ):
        """
        Take the tiered lookalike audiences and create the ads
        """
        results = {
            'adsets': [],
            'ads': [],
        }

        tiers = len(tiered_lookalikes)
        if tiers != len(tiered_bid_amounts):
            raise TypeError('Audience and bid amount number mismatch.')

        # Create campaign
        if not campaign:
            campaign = Campaign(parent_id=account_id)
            campaign[Campaign.Field.name] = '{} Campaign'.format(name)
            campaign[Campaign.Field.objective] = \
                Campaign.Objective.link_clicks

            campaign.remote_create(params={
                'status': Campaign.Status.paused,
            })

        # Upload image
        img = AdImage(parent_id=account_id)
        img[AdImage.Field.filename] = image_path
        img.remote_create()
        image_hash = img.get_hash()

        # Inline creative for ads
        inline_creative = {
            AdCreative.Field.title: title,
            AdCreative.Field.body: body,
            AdCreative.Field.object_url: url,
            AdCreative.Field.image_hash: image_hash,
        }

        for tier in range(1, tiers + 1):
            # Create ad set
            ad_set = AdSet(parent_id=account_id)
            ad_set[AdSet.Field.campaign_id] = campaign.get_id_assured()
            ad_set[AdSet.Field.name] = '{0} AdSet tier {1}'.format(name, tier)
            ad_set[AdSet.Field.optimization_goal] = optimization_goal
            ad_set[AdSet.Field.billing_event] = billing_event
            ad_set[AdSet.Field.bid_amount] = tiered_bid_amounts[tier - 1]
            if daily_budget:
                ad_set[AdSet.Field.daily_budget] = daily_budget
            else:
                ad_set[AdSet.Field.lifetime_budget] = lifetime_budget
            if end_time:
                ad_set[AdSet.Field.end_time] = end_time
            if start_time:
                ad_set[AdSet.Field.start_time] = start_time

            audience = tiered_lookalikes[tier - 1]

            targeting = {
                TargetingSpecsField.custom_audiences: [{
                    'id': audience[CustomAudience.Field.id],
                    'name': audience[CustomAudience.Field.name],
                }]
            }

            ad_set[AdSet.Field.targeting] = targeting

            ad_set.remote_create(params={
                'status': AdSet.Status.paused,
            })

            # Create ad
            ad = Ad(parent_id=account_id)
            ad[Ad.Field.name] = '{0} Ad tier {1}'.format(name, tier)
            ad[Ad.Field.adset_id] = ad_set['id']
            ad[Ad.Field.creative] = inline_creative

            ad.remote_create(params={
                'status': Ad.Status.paused,
            })

            results['adsets'].append(ad_set)
            results['ads'].append(ad)

        return results
