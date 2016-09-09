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

from django.http import HttpResponseRedirect
from django.conf import settings

class SslRedirect:
    def process_request(self, request):
        request_url = request.build_absolute_uri()
        original = request_url

        if not request.is_secure():
            # enforce https
            request_url = request_url.replace('http://', 'https://')

        if settings.IS_RELEASE():
            # only do this in release/production
            # replace non-www domain to www-domain
            if not request_url.startswith('https://www.'):
                request_url = request_url.replace(
                    'https://',
                    'https://www.', 1
                )

        if original == request_url:
            # do nothing when we did not change the url to avoid cycle
            # redirecting issue.
            return None
        else:
            return HttpResponseRedirect(request_url)
