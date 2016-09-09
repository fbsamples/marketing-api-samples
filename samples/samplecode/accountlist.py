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
# Ad Account List

## Getting user's ad accounts

***

This is a simple sample that shows how to get a list of the user's ad accounts.
A first test after you get an access token with ads management/insights
permission you should do is to try to get the user's list of ad accounts.

## References:

* [Ad Account document][1]

[1]: https://developers.facebook.com/docs/reference/ads-api/adaccount
"""
from facebookads.objects import AdUser


class AdAccountsList:

    def get_accounts(self):
        """
          Retrieves and displays a list of the user's ad accounts.
         """
        me = AdUser(fbid='me')
        return list(me.get_ad_accounts(fields=[
                    'id',
                    'name',
                    'timezone_name',
                    'amount_spent',
                    'currency']))
