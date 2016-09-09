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
import inspect
import sys
from facebookads.exceptions import FacebookRequestError
from facebookads.api import FacebookAdsApi
from urllib import urlencode
from urlparse import urlparse, urlunparse
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib import messages
from django.middleware.csrf import rotate_token

logger = logging.getLogger(__name__)

user_error_panel = """
<div class="panel panel-default">
    <div class="panel-heading">
        <p>{0}</p>
    </div>
    <div class="panel-body">
        <p>{1}</p>
    </div>
</div>
"""


def log_and_return_error(request, message=None):
    caller_module_name = __name__
    # get caller module name
    stack = inspect.stack()
    if len(stack) > 1:
        parentframe = stack[1][0]
        caller_module = inspect.getmodule(parentframe)
        caller_module_name = caller_module.__name__
    # get logger for caller module
    mlogger = logging.getLogger(caller_module_name)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    request.exception = exc_value
    if message is None:
        if exc_type == FacebookRequestError:
            message = exc_value.api_error_message()
            error_user_title = None
            error_user_msg = None
            # Display more detailed information if this is an API error message
            if exc_value._error:
                if 'error_user_title' in exc_value._error:
                    error_user_title = exc_value._error['error_user_title']
                if 'error_user_msg' in exc_value._error:
                    error_user_msg = exc_value._error['error_user_msg']

            if error_user_title is not None:
                message += user_error_panel.format(
                    error_user_title,
                    error_user_msg)
        else:
            message = 'Oops. Something went wrong.'

    mlogger.error("Exception:", exc_info=(exc_type, exc_value, exc_traceback))

    return message


def log_and_show_error(request, message=None):
    message = log_and_return_error(request, message)
    return render(request, 'common/error.html', {'message': message})


def add_success_message(request, message):
    messages.add_message(request, messages.SUCCESS, message)


def add_error_message(request, message):
    messages.add_message(request, messages.ERROR, message)


def construct_url(url, params):
    parts = list(urlparse(url))
    parts[4] = urlencode(params)
    return urlunparse(parts)


def set_session_user(request, fb_userid, token):
    rotate_token(request)
    request.session['fbuserid'] = fb_userid
    request.session['token'] = token


def clear_session_user(request):
    rotate_token(request)
    request.session.flush()
    FacebookAdsApi.set_default_api(None)


def logout_user(request):
    logout(request)
    clear_session_user(request)
    logger.info('User logged out')
