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

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from views import about


urlpatterns = patterns(
    '',
    url(r'^$', about, name='about'),
    url(r'^auth/', include('security.urls', namespace="auth")),
    url(r'^common/', include('common.urls', namespace="common")),
    url(r'^components/', include('components.urls', namespace="components")),
    url(r'^samples/', include('samples.urls', namespace="samples")),
    url(r'^dash/', include('dash.urls', namespace="dash")),
    url(r'^license/',
        TemplateView.as_view(template_name='common/license.html'),
        name='license'),
)

# Enable testing 404 pages by calling their urls in DEBUG mode
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^404/$', TemplateView.as_view(template_name="404.html")),
        (r'^500/$', TemplateView.as_view(template_name="500.html"))
    )
