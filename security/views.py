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
import re
import sys
import urllib2
import uuid
from django.shortcuts import render
from django.http import HttpResponseRedirect, QueryDict
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login
from common.utils import (construct_url,
                          log_and_show_error,
                          set_session_user,
                          logout_user)
logger = logging.getLogger(__name__)


def _clean_url(url, fallback='/samples/'):
    # relative URLs only
    if url is not None and re.match("^/\w.*", url):
        return url
    return fallback


def _clean_url_for_sample_name(sample_name):
    clean = '/samples/'
    # relative URLs only
    if sample_name is not None and re.match("^[A-Za-z_0-9]+$", sample_name):
        clean += sample_name
    return clean


def get_next_url(request):
    # trust only next within csrf-protected form
    if request.method == 'POST' and request.POST.get('next'):
        return _clean_url(request.POST.get('next'))

    return _clean_url_for_sample_name(request.GET.get('sample'))


def do_login(request):
    next_url = get_next_url(request)
    return render(request, 'common/login.html', {'next': next_url})


def oauth(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/samples/')

    state = str(uuid.uuid4())
    request.session['next'] = get_next_url(request)
    request.session['state'] = state
    url = construct_url('https://www.facebook.com/v2.6/dialog/oauth', {
        'client_id': settings.FACEBOOK_APP_ID,
        'response_type': 'code',
        'scope': ['ads_management', 'pages_show_list'],
        'state': state,
        'redirect_uri':
            request.build_absolute_uri(reverse('auth:fbcallback'))})
    logger.debug('Redirecting to oauth dialog')
    return HttpResponseRedirect(url)


def auth_callback(request):
    next_url = request.session.pop('next', '/samples/')
    logger.debug("nex_url is %s", next_url)
    if ('code' not in request.GET or 'state' not in request.GET or
            request.GET['state'] != request.session['state']):
            return HttpResponseRedirect(settings.LOGIN_URL)

    code = request.GET['code']
    url = construct_url('https://graph.facebook.com/oauth/access_token', {
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'code': code,
        'redirect_uri':
            request.build_absolute_uri(reverse('auth:fbcallback'))})
    try:
        logger.debug('Exchanging code %s for access token', code)
        result = urllib2.urlopen(url).read()
    except urllib2.HTTPError as e:
        return log_and_show_error(request, 'Failed to get access token.')

    q = QueryDict(result)
    if 'access_token' not in q:
        return log_and_show_error(request, 'Did not get access token.')
    token = q['access_token']
    try:
        user = authenticate(token=token)
        logger.debug('Authenticated user.')
    except:
        e = sys.exc_info()[0]
        return log_and_show_error(
            request,
            ('Failed to authenticate access token. '
                'Please try again later.'),
            logger,
            e)

    if user is not None:
        login(request, user)
        logger.info('Successfully logged in user ' + user.get_short_name())
        set_session_user(request, user.fb_userid, token)
        return HttpResponseRedirect(next_url)
    else:
        return log_and_show_error(
            request,
            'Login failed, please try again later.'
        )


def do_logout(request):
    logout_user(request)
    return HttpResponseRedirect(settings.LOGIN_URL)
