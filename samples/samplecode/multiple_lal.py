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
# Multiple Lookalike Audiences

## Creating lookalike audiences in multiple countries and similarity ratios

***

This sample shows how you can take a custom audience seed and quickly create
lookalike audiences in multiple countries at multiple similarity ratios.

## References:

* [Lookalike Audiences][1]

[1]: https://developers.facebook.com/docs/marketing-api/lookalike-audience-targeting
"""
import itertools
from facebookads.objects import (
    CustomAudience,
    LookalikeAudience,
)


class MultipleLalSample:
    """
    The sample that creates multiple lookalike audiences in different countries
    at different similarity ratios
    """
    def create_lals(
        self,
        account_id,
        seed_id,
        base_name,
        countries,
        ratios,
    ):
        """
        Function that creates the lookalike audiences
        Params:
        * `account_id` is your Facebook AdAccount id
        * `seed_id` is the source custom audience
        * `base_name` the lookalike audiences will have names in the format of
          `[base_name] [COUNTRY_CODE] [RATIO]`
        * `countries` array of country codes
        * `ratios` array of integers stating the lookalike ratio, from 1 to 10
           currency is USD, dailybudget=1000 says your budget is 1000 USD
        """
        lal_created = []

        for country, ratio in itertools.product(countries, ratios):
            # Create the lookalike audience
            lookalike = CustomAudience(parent_id=account_id)
            lookalike[LookalikeAudience.Field.name] = "{0} {1} {2}".format(
                base_name,
                country,
                ratio,
            )
            lookalike[LookalikeAudience.Field.origin_audience_id] = seed_id
            lookalike[LookalikeAudience.Field.lookalike_spec] = {
                LookalikeAudience.Field.LookalikeSpec.ratio: ratio / 100.0,
                LookalikeAudience.Field.LookalikeSpec.country: country,
            }
            lookalike[CustomAudience.Field.subtype] = \
                CustomAudience.Subtype.lookalike
            lookalike.remote_create()
            lal_created.append(lookalike)
        return lal_created
