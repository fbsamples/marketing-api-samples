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
# Ads Reporting

## Getting Ad Reports

***

This sample is to use the new Insights edge to pull insights and to
simulate inserting into DB.

## References:
* [Ads Insights doc][1]

[1]: https://developers.facebook.com/docs/marketing-api/insights-api
"""
from facebookads.objects import (
    AdAccount,
)


class AdsReportingSample:
    """
    This class provides 3 funciton (`get_ads_insight`,
    `get_insights_value`, `get_values`) to pull the insights
    from the Insight edge with Facebook Marketing API
    """

    def get_ads_insight(
        self,
        account_id,
        report_date
    ):
        """
        Pull insights from the Insight edge and return an array of
        insight report

        Params:

        * `account_id` is your Facebook AdAccount id
        * `report_date` is the date for the insight report

        For more information see the [Ads Insights doc](
        https://developers.facebook.com/docs/marketing-api/insights-api)
        """
        ad_account = AdAccount(fbid=account_id)
        limit = 10
        fields = [
            'campaign_name',
            'adset_name',
            'adset_id',
            'impressions',
            'website_clicks',
            'app_store_clicks',
            'deeplink_clicks',
            'spend',
            'reach',
            'actions',
            'action_values'
        ]
        params = {
            'time_range': {
                'since': report_date,
                'until': report_date
            },
            'action_attribution_windows': ['28d_click'],
            'breakdowns': ['impression_device', 'placement'],
            'level': 'adset',
            'limit': limit if limit > 0 else None
        }

        insights = ad_account.get_insights(fields, params)
        insights_value = self.get_insights_value(insights, report_date, limit)

        return insights_value

    def get_insights_value(
        self,
        insights,
        report_date,
        limit=-1
    ):
        """
        Construct an array of insight report from insights object

        Params:

        * `insights` is the object from insights edge
        * `report_date` is the date for the insight report
        * `limit` is the limit of records to be returned
        """
        count = 0
        data = []
        key_value = None
        for insight in insights:
            key_value = self.get_values(insight, report_date)
            if count == 0:
                data.append(key_value.keys())
            data.append(key_value.values())
            count += 1
            if limit > 0 and limit == count:
                break

        return data

    def get_values(
        self,
        insight,
        report_date
    ):
        """
        Get the values from an insight object

        Params:

        * `insight` is a single insights object
        * `report_date` is the date for the insight report

        For more information see the [Insights doc](
        https://developers.facebook.com/docs/marketing-api/insights)
        """
        # action types that we want to get from insight
        # format is action_type_returned_from_api: db_column_name
        action_type_columns = {
            'link_click': 'website_clicks',
            'offsite_conversion.checkout': 'checkouts',
            'offsite_conversion.add_to_cart': 'adds_to_cart',
            'offsite_conversion.key_page_view': 'key_web_page_views',
            'offsite_conversion.lead': 'leads',
            'offsite_conversion.other': 'other_website_conversions',
            'offsite_conversion.registration': 'registrations',
            'app_custom_event.fb_mobile_purchase': 'mobile_purchase',
            'app_custom_event.fb_mobile_add_to_cart': 'mobile_add_to_cart',
            'mobile_app_install': 'mobile_app_install',
            'app_custom_event.fb_mobile_activate_app': 'mobile_activate_app',
        }

        # action values that we want to get from insight
        # format is action_value_returned_from_api: db_column_name
        action_value_columns = {
            'offsite_conversion': 'website_action_value',
            'app_custom_event.fb_mobile_purchase': 'mobile_purchase_value',
        }

        # general columns that we want to get from insight
        general_columns = {
            'impression_device': 'impression_device',
            'action_device': 'action_device',
            'campaign_name': 'campaign',
            'adset_name': 'adset',
            'adset_id': 'adset_id',
            'impressions': 'impressions',
            'website_clicks': 'website_clicks',
            'app_store_clicks': 'app_store_clicks',
            'deeplink_clicks': 'deeplink_clicks',
            'spend': 'spend',
            'reach': 'reach'
        }

        key_value = {'start_date': report_date, 'end_date': report_date}
        d1 = dict.fromkeys(action_type_columns.values())
        key_value.update(d1)
        d2 = dict.fromkeys(action_value_columns.values())
        key_value.update(d2)
        d3 = dict.fromkeys(general_columns.values())
        key_value.update(d3)

        # get values for general columns
        for k in general_columns.keys():
            if k in insight:
                key_value[general_columns[k]] = \
                    str(insight[k]).replace("'", r"\'")

        # get values for actions
        if 'actions' in insight:
            actions = insight['actions']
            for action in actions:
                t = action['action_type']
                if t in action_type_columns and '28d_click' in action:
                    key_value[action_type_columns[t]] = \
                        str(action['28d_click'])

        # get values for action values
        if 'action_values' in insight:
            action_values = insight['action_values']
            for action_value in action_values:
                t = action_value['action_type']
                if t in action_value_columns and '28d_click' in action_value:
                    key_value[action_value_columns[t]] = \
                        str(action_value['28d_click'])

        return key_value
