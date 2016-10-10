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
# Audience Network
## Retrieve and opt-in eligible Ad Sets into Audience Network

This sample shows how to retrieve all eligible Ad Sets that can have Audience
Network enabled on them but don't have it enabled yet. Also explained is a
function to help enable Audience Network given a list of ad set ids.
"""

from facebookads.objects import (
    AdAccount,
    Campaign,
    AdSet,
    TargetingSpecsField,
)
from facebookads.exceptions import FacebookError
import copy


class AudienceNetworkOptinSample:
    """
    This class provides functions that help retrieve eligible ad sets that
    don't have audience network (an) enabled on them and also help enable
    the audience network on a given list of ad set ids.
    """
    def retrieve_eligible_adsets_for_an(
        self,
        accountid,
        includepaused=False,
    ):
        """
        This method returns all eligible ad sets that can have audience
        networked turned on for a given ad account id.

        Args:
            accountid: The ad account id (should be of the form act_<act_id>)
                for which you are running this exercise.
            inlcudepaused: Boolen parameter to make your method consider ad
                sets with paused states (PAUSED & CAMPAIGN_PAUSED). Checks
                only ACTIVE by default.

        Returns:
            List of ad set objects (if found satisfying the conditions) or
            an empty list.

        """
        # use accountid to retrieve all active adsets
        account = AdAccount(accountid)
        adsetfields = [
            AdSet.Field.id,
            AdSet.Field.name,
            AdSet.Field.campaign_id,
            AdSet.Field.targeting,
            AdSet.Field.effective_status,
        ]
        adsets = list(account.get_ad_sets(fields=adsetfields))

        # Filter ad sets received by desired status and placement types.
        # Further filter by campaign objectives listed in the criteria below.
        #
        # Ref: https://developers.facebook.com/docs/
        #               marketing-api/audience-network/v2.5

        desired_campaign_status = set(['ACTIVE'])

        # mostly useful in testing when you don't have active campaigns
        if includepaused is True:
            desired_campaign_status.update({'PAUSED', 'CAMPAIGN_PAUSED'})

        desired_campaign_objectives = set([
            'MOBILE_APP_INSTALLS',
            'MOBILE_APP_ENGAGEMENT',
            'LINK_CLICKS',
            'CONVERSIONS',
            'PRODUCT_CATALOG_SALES',
        ])

        # Hold the result set
        eligible_adsets = []

        for adset in adsets:
            if adset[AdSet.Field.effective_status] in desired_campaign_status:

                """
                'devide_platforms', 'publisher_platforms' and
                'facebook_positions' could be absent for the default of 'ALL'
                """
                device_platforms = None
                if TargetingSpecsField.device_platforms in \
                        adset[AdSet.Field.targeting]:
                    device_platforms = set(
                        adset[AdSet.Field.targeting][
                            TargetingSpecsField.device_platforms]
                    )

                publisher_platforms = None
                if TargetingSpecsField.publisher_platforms in \
                        adset[AdSet.Field.targeting]:
                    publisher_platforms = set(
                        adset[AdSet.Field.targeting][
                            TargetingSpecsField.publisher_platforms]
                    )

                facebook_positions = None
                if TargetingSpecsField.facebook_positions in \
                        adset[AdSet.Field.targeting]:
                    facebook_positions = set(
                        adset[AdSet.Field.targeting][
                            TargetingSpecsField.facebook_positions]
                    )

                if ((facebook_positions is None or
                        'feed' in facebook_positions) and
                    (device_platforms is None or
                        'mobile' in device_platforms)):

                    if (publisher_platforms is None or
                            'audience_network' in publisher_platforms):
                        # audience network already enabled, so just pass
                        continue
                    else:
                        campaign = Campaign(adset[AdSet.Field.campaign_id])
                        campaignfields = [
                            Campaign.Field.id,
                            Campaign.Field.name,
                            Campaign.Field.effective_status,
                            Campaign.Field.objective,
                        ]
                        campaign = campaign.remote_read(fields=campaignfields)
                        if (
                            campaign[Campaign.Field.objective] in
                            desired_campaign_objectives
                        ):
                            eligible_adsets.append(adset)

        return eligible_adsets

    def enable_an_on_adsets(
        self,
        adsetids
    ):
        """
        Method that takes a list of ad set ids and enables the audience network
        placement on them. Please note that this method does not perform any
        pre-validation check to see whether the ad set passed  satisfies the
        pre-requisites to have audience network enabled.

        Args:
            adsetids: List of ad set ids on which you want audience network
            enabled. Even if you have just one id, pass it as a list.
        Returns:
            A list of 'ad set id' vs. 'status' mapping with a further 'message'
            node whenever there was a failure to update the audience network.
            Returns an empty list when an empty list or non list element is
            passed.

            status 1 is a success.
            status 0 is a failure.

            Sample response format:
            [
                {'<ad_set_id_1>': {'status': 1}},
                {'<ad_set_id_2>': {'status': 0, 'message': '<exception_msg>'}},
                ...
            ]
        """
        results = []

        # check if adsets is a list
        if type(adsetids) is not list:
            return results

        # go over the list of adset ids
        for adsetid in adsetids:
                try:
                    # read ad set info
                    adset = AdSet(fbid=adsetid)
                    adsetobj = adset.remote_read(fields=[AdSet.Field.targeting])

                    # edit targeting spec info for placements
                    targetinginfo = copy.deepcopy(adsetobj[
                        AdSet.Field.targeting
                    ])
                    targetinginfo[TargetingSpecsField.publisher_platforms]. \
                        append('audience_network')

                    # update ad set info
                    adset.update({
                        AdSet.Field.targeting: targetinginfo
                    })
                    adset.remote_update()

                    # update result list along with status
                    results.append({adsetid: {'status': 1}})

                except FacebookError as e:

                    # update result list along with status & message
                    results.append({
                        adsetid: {'status': 0, 'message': e.message}
                    })

        return results
