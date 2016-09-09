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
# Custom Audiences

## Creating custom audiences and uploading data

***

This sample shows how to use the Custom Audiences API to create a new custom
audience and upload data to it.

Using data from your CRM system, you can find your existing customers on
Facebook. You can then run campaigns to re-target those customers and/or
campaigns that target new customers and exclude existing ones.

## References:

* [Custom Audiences API doc][1]

[1]: https://developers.facebook.com/docs/reference/ads-api/custom-audience-api
"""
from facebookads.objects import CustomAudience


class CustomAudienceSample:
    """
    The main sample class.
    """
    def create_audience(self, accountid, name, description, optoutlink):
        """
          Creates a new custom audience and returns the id.
        """
        audience = CustomAudience(parent_id=accountid)
        audience.update({
            CustomAudience.Field.name: name,
            CustomAudience.Field.description: description,
            CustomAudience.Field.opt_out_link: optoutlink,
            CustomAudience.Field.subtype: CustomAudience.Subtype.custom,
        })
        audience.remote_create()
        caid = audience[CustomAudience.Field.id]
        return caid

    def upload_users_to_audience(
            self,
            audienceid,
            users,
            schema=CustomAudience.Schema.email_hash):
        """
          Adds user emails to an existing audience. The SDK automatically hashes
          the emails. Only the hash is sent to Facebook.
        """
        audience = CustomAudience(audienceid)
        return audience.add_users(schema, users)
