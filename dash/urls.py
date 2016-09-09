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

import logging
from django.conf.urls import patterns, url
from dash.views.sample import SampleCreateView, SampleUpdateView
from dash.views.sample import SampleDetailView, SampleListView
from dash.views.sample import SampleDeleteView
from dash.views.role import RoleListView, RoleDetailsView
from django.conf import settings

logger = logging.getLogger(__name__)

urlpatterns = []
# enable dash only if not in prod/test and dash explicitly enabled
if hasattr(settings, 'ENABLE_DASH') \
   and settings.ENABLE_DASH \
   and not settings.IS_RELEASE() \
   and not settings.IS_TEST():
    urlpatterns = patterns(
        '',
        url(r'^sample/add/$', SampleCreateView.as_view(), name='sample_add'),
        url(r'^sample/list/$', SampleListView.as_view(), name='sample_list'),
        url(r'^sample/details/(?P<pk>\w+)/$',
            SampleDetailView.as_view(),
            name='sample_details'),
        url(r'^sample/delete/(?P<pk>\w+)$',
            SampleDeleteView.as_view(),
            name='sample_delete'),
        url(r'^sample/edit/(?P<pk>\w+)$',
            SampleUpdateView.as_view(),
            name='sample_edit'),
        url(r'^role/list/$', RoleListView.as_view(), name='role_list'),
        url(r'^role/details/(?P<pk>\w+)/$', RoleDetailsView.as_view(),
            name='role_details')
    )
else:
    logger.info('Dash disabled')
