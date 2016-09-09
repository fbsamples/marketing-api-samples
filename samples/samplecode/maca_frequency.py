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
# Mobile App Custom Audiences

## Creating custom audiences based on frequency of mobile app events

***

This sample shows how to use the Custom Audiences API to create a custom
audience based on frequency of mobile app events. You can create MACAs quite
easily via the native tools like ads manager or power editor, this sample will
demonstrate how to create ones based on the frequency of app events for example
how many times the user opened the app or made purchases, which is only possible
through the API at the moment.

## References:

* [Mobile App Custom Audiences][1]
* [Mobile App Custom Audiences API reference][2]

[1]: https://developers.facebook.com/docs/marketing-api/audiences-api/mobile-apps
[2]: https://developers.facebook.com/docs/marketing-api/custom-audience-mobile/

"""
from facebookads.objects import CustomAudience
import json


class MacaFrequencySample:
    """
    The main sample class.
    """
    def create_audience(
        self,
        accountid,
        app_id,
        name,
        retention_days,
        event,
        period,
        greater_than=None,
        less_than=None,
    ):
        """
        Creates a new custom audience and returns the id. The custom audience
        is created based on the cumulative values of the events (add to cart
        or purchase) during the selected period, provided that app is logging
        the selected app event and passing the right value with them.
        """
        audience = CustomAudience(parent_id=accountid)
        technique = {
            'technique_name': 'absolute',
        }
        if greater_than is not None:
            technique['lower_bound'] = greater_than
        if less_than is not None:
            technique['upper_bound'] = less_than
        rule = {
            '_application': app_id,
            '_eventName': event,
            '_cumulativeRule': {
                'metric': 'count',
                'period': period,
                'technique': technique,
            },
        }
        audience.update({
            CustomAudience.Field.name: name,
            CustomAudience.Field.subtype: CustomAudience.Subtype.app,
            CustomAudience.Field.retention_days: retention_days,
            CustomAudience.Field.rule: json.dumps(rule),
        })
        audience.remote_create()
        caid = audience[CustomAudience.Field.id]
        return caid
