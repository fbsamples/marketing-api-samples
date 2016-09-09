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

from meta.views import Meta
from django.conf import settings

meta = Meta(
    title="Facebook Marketing API Code Samples",
    description="The Facebook Marketing API Accelerator is your path to "
                "serious ads API skills and significant technical developer "
                "support.",
    keywords=[
        'facebook marketing api',
        'facebook ads api',
        'ads api',
        'marketing automation',
        'ads api samples',
        'marketing api samples'
    ],
    use_og=True,
    use_twitter=True,
    use_facebook=True,
    facebook_app_id=settings.FACEBOOK_APP_ID,
    site_name="Facebook Marketing Developers",
    twitter_site='@fbplatform',
    twitter_card='summary_large_image',
    image='/static/images/fmd.jpg',
)
