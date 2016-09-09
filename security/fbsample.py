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

import importlib
import logging
import re
import sys
import traceback

import markdown
import pdoc
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.signals import got_request_exception
from django.core.signals import request_finished, request_started
from django.dispatch import receiver
from django.http import HttpRequest
from django.shortcuts import render
from facebookads.api import FacebookAdsApi
from facebookads.session import FacebookSession

from common.utils import clear_session_user
from dash.models import Sample
from common_templates.metatemplate import meta
from security.models import FBAuthBackend
from security.role import role_check

logger = logging.getLogger(__name__)


# gets user from session
def get_session_user(request):
    user = None
    # check the userid and access token in the session
    # if exists get the user and install on the request
    # if not exists, redirect to login page with next
    fb_userid = request.session.get('fbuserid', None)
    token = request.session.get('token', None)
    if (fb_userid is not None and token is not None):
        logger.debug("Found fb_userid in session. Getting User object")
        user = FBAuthBackend().get_user(fb_userid)
        if user is not None:
            logger.debug("Got the User object")
            # TODO we should move these lines to the sample code
            # to make samples more self-contained
            fbads_session = FacebookSession(
                settings.FACEBOOK_APP_ID,
                settings.FACEBOOK_APP_SECRET,
                token)
            fbads_api = FacebookAdsApi(fbads_session)

            # Set the user agent for the API requests from default
            # "fb-python-ads-api-sdk-%s" % SDK_VERSION, to
            # "fb-python-ads-muse-%s" % SDK_VERSION,
            fbads_api.HTTP_DEFAULT_HEADERS['User-Agent'] = \
                "fb-python-ads-muse-" + fbads_api.SDK_VERSION

            FacebookAdsApi.set_default_api(fbads_api)
            request.fbads_api = fbads_api
            logger.debug("Added fbads_api to request")
        else:
            logger.info("The fb_userid in session did not map to a valid user.")
            clear_session_user(request)
    else:
        logger.debug("fb_userid and/or token not found in session")
        FacebookAdsApi.set_default_api(None)

    return user


def gen_docs(sample_module_name):
    """
    Generates pdocs from sample module, and the template intentionally skip the
    module doc string because we use that for the sample description at top of
    the sample page. See gen_desc function below.
    """
    docs = None
    if sample_module_name is not None:
        logger.debug("Generating sample docs")
        pdoc.tpl_lookup.directories.insert(0, settings.DOC_TEMPLATE_DIR)
        try:
            docs = pdoc.html(sample_module_name)
            docs = docs.split('<article id="content">')
            docs = docs[1]
            docs = docs.split('</article>')
            docs = docs[0]
        except:
            e = sys.exc_info()[0]
            tb = traceback.format_exc()
            logger.error("Error generating docs: %s. Traceback: %s", e, tb)
            docs = "There was an error while generating the sample docs."

    return docs


def gen_desc(sample_module_name):
    """
    Generates description from sample module, which is the module doc string
    from the sample source code. This description will appear before the form,
    at the top of every sample page.
    """
    code_module = importlib.import_module(sample_module_name)
    desc = ''
    desc_summary = ''
    title = 'Marketing Automation Samples'
    one_line = 'Code samples for automation with Facebook Marketing API'
    if code_module.__doc__:
        desc = code_module.__doc__
        match = re.search('^# (.+)$', desc, re.MULTILINE)
        if match:
            title = match.group(1)
        match = re.search('^## (.+)$', desc, re.MULTILINE)
        if match:
            one_line = match.group(1)

        desc = markdown.markdown(code_module.__doc__)

        # Take the first Paragraph as summary <p> </p>
        match = re.search(r'<p>(.*?)</p>', desc, re.S)
        if match:
            desc_summary = match.group(1)

    desc_meta = '{0} | {1}'.format(title, one_line)
    return (desc, desc_meta, desc_summary)


def gen_sample_role_list(sample_module_name):
    """
    Generate sample's check role list.
    """
    # sample_module_name is in format samples.samplecode.abc123
    # sample's view_module name is in format samples.views.abc123
    # so here we generate view_module based on sample_module_name
    view_module_name = ("samples.views" +
                        sample_module_name[len("samples.samplecode"):])
    try:
        logger.error(view_module_name)
        sampleobj = Sample.objects.get(view_module=view_module_name)
        if sampleobj.roles_to_check:
            return sampleobj.roles_to_check.strip().split(',')
        else:
            return []
    except ObjectDoesNotExist:
        logger.error("Can not find sample metadata of %s.", sample_module_name)
        return []


def fbads_sample(sample_module_name):
    logger.debug("fbads_sample called for sample %s", sample_module_name)

    def wrap(f):

        def wrapped_f(*args, **kwargs):
            error_message = "Decorator applied to function that is not a view"

            assert len(args) > 1, error_message
            request = args[1]
            assert isinstance(request, HttpRequest), error_message
            # try to get the user
            user = get_session_user(request)

            # try to get the roles of this sample
            check_role_list = gen_sample_role_list(sample_module_name)
            # and check, if fail, redirect to http404
            if not role_check(check_role_list, user):
                return render(request, '404.html')

            if sample_module_name:
                sample_desc, sample_desc_meta, sample_desc_summary = \
                    gen_desc(sample_module_name)
                request.sample_desc = sample_desc
                request.sample_desc_meta = sample_desc_meta

                # set django-meta descriptions
                if hasattr(meta, 'title'):
                    meta.description = sample_desc_summary
                    meta.title = sample_desc_meta

                docs = gen_docs(sample_module_name)
                request.docs = docs

            # Set sample absolute path for the social plugins
            sample_url = request.build_absolute_uri().split('?')[0]
            request.sample_url = sample_url

            # if we have user, call the wrapped view function
            # else render the base form with just docs
            if user:
                response = f(*args, **kwargs)
            else:
                response = render(
                    request,
                    'common/sample_base.html',
                    {'meta': meta}
                )

            return response

        return wrapped_f

    return wrap


def fbads_auth(check_role_list=[]):
    logger.debug("fbads_auth called")

    def wrap(f):

        def wrapped_f(*args, **kwargs):
            error_message = "Decorator applied to function that is not a view"

            assert len(args) > 1, error_message
            request = args[1]
            assert isinstance(request, HttpRequest), error_message
            # try to get the user
            user = get_session_user(request)

            # check this view's role_list, if fail, redirect to http404
            if not role_check(check_role_list, user):
                return render(request, '404.html')

            if user:
                return f(*args, **kwargs)
            else:
                return render(request, 'common/login.html')

        return wrapped_f

    return wrap


def components_auth():
    # Auth decor used for the components pages that needed the login session and
    # login redirect back to the components overview page
    logger.debug("components_auth called")

    def wrap(f):

        def wrapped_f(*args, **kwargs):
            error_message = "Decorator applied to function that is not a view"

            assert len(args) > 1, error_message
            request = args[1]
            assert isinstance(request, HttpRequest), error_message
            # try to get the user
            user = get_session_user(request)

            if user:
                return f(*args, **kwargs)
            else:
                return render(request, 'components/overview.html')

        return wrapped_f

    return wrap


@receiver(request_started)
@receiver(request_finished)
@receiver(got_request_exception)
def reset_thread_state(**kwargs):
    '''
    Called to reset static variables for example the API instance after we are
    done with one request to prevent them from unintentionally lingering between
    requests.
    '''
    FacebookAdsApi.set_default_api(None)
