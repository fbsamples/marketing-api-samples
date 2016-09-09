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

import os
import time
from django.http import Http404
from django.views.generic import View, ListView
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from dash.models import Sample
from facebookads.objects import Ad
from facebookads.exceptions import FacebookRequestError
from common_templates.metatemplate import meta
from common.utils import (log_and_return_error,
                          log_and_show_error,
                          logout_user,
                          add_success_message,
                          add_error_message)


class SampleCatalog(ListView):
    model = Sample
    template_name = 'samples/index.html'

    seo_title = 'Facebook Marketing API Samples.'
    seo_description = 'A library of code for developers that features ' \
                      'solutions to common tasks using Facebook Marketing ' \
                      'API. These code samples allow you to use the power ' \
                      'of the Marketing API to automation ad creation and ' \
                      'management.'
    seo_image = '/static/images/fmd.jpg'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ListView, self).get_context_data(**kwargs)

        if hasattr(meta, 'title'):
            meta.title = self.seo_title
            meta.description = self.seo_description
            meta.image = self.seo_image
            context['meta'] = meta

        return context


class SampleBaseView(View):

    TEMPLATE = 'samples/sample_form.html'
    BUTTON_TEXT = 'Submit'
    BUTTON_TARGET = '_self'

    def _handle_image_upload(self, upload):
        TEMP_PATH = '/tmp'
        if not os.path.exists(TEMP_PATH):
            os.mkdir(TEMP_PATH)

        """ Get an unique file name to save the image temporarily """
        file_name = str(int(round(time.time() * 1000))) + upload.name
        file_path = os.path.join(TEMP_PATH, file_name)
        while os.path.exists(file_path):
            file_name = str(int(round(time.time() * 1000))) + upload.name
            file_path = os.path.join(TEMP_PATH, file_name)

        with open(file_path, 'wb') as dest:
            for chunk in upload.chunks():
                dest.write(chunk)

        return file_path

    def render_form(self, request, form, data=None):
        return render(
            request,
            self.TEMPLATE,
            {
                'form': form,
                'button_text': self.BUTTON_TEXT,
                'data': data,
                'target': self.BUTTON_TARGET,
            }
        )

    def render_form_with_status(
        self,
        request,
        form,
        status,
        data=None
    ):
        if(
            data and
            'ad_preview_dict' in data and
            'ad_id' in data['ad_preview_dict'] and
            'ad_format' in data['ad_preview_dict']
        ):
            status += '<br />' + self.gen_ad_preview(
                data['ad_preview_dict']['ad_id'],
                data['ad_preview_dict']['ad_format'])

        add_success_message(request, status)
        return self.render_form(request, form, data)

    def render_form_with_error(self, request, form, error):
        add_error_message(request, error)
        return self.render_form(request, form)

    def render_invalid_form(self, request, form):
        return self.render_form_with_error(request, form, "Invalid form data")

    # ad_format options:
    # https://developers.facebook.com/docs/marketing-api/generatepreview
    def gen_ad_preview(
        self,
        ad_id,
        ad_format='MOBILE_FEED_STANDARD'
    ):  # ?string
        if not ad_id:
            return None
        if ad_format is None:
            ad_format = 'MOBILE_FEED_STANDARD'
        ad = Ad(ad_id)
        params = {
            'ad_format': ad_format
        }
        preview = ad.get_ad_preview(None, params)
        return preview.get_html()


class SampleView(View):

    """
    Show the selected sample
    by delegating to the sample's view class
    """
    def dispatch(self, request, *args, **kwargs):
        # errors that require a new token
        # see https://developers.facebook.com/docs/marketing-api/error-reference
        token_error_codes = set([102, 190, 200])
        try:
            """
            Use request.last_error_post to initialize your sample form to
            recover the form values.
            """
            if (request.method == 'GET'):
                request.last_error_post = self._recover_last_error_post(request)
            # get sample object
            sample_id = kwargs['sid']
            sample = Sample.objects.get(pk=sample_id)
            view = self.__get_sample_view(sample, kwargs)
            # sample metadata is needed for meta tags
            # and sample id is needed to track for GA and FB Pixel events
            request.sample = sample
            return view(request, args, kwargs)
        except ObjectDoesNotExist:
            raise Http404
        except:
            """
            If error came from post, remember the error and redirect to GET
            This will show the sample's view again but with the error message.
            Also the data from the error post will be cached in session to be
            recovered.
            """
            if (request.method == 'POST'):
                messages.add_message(
                    request,
                    messages.ERROR,
                    log_and_return_error(request)
                )
                request.session['last_error_post'] = request.POST
                response = redirect(request.path)
            else:
                response = log_and_show_error(request)

            if (isinstance(request.exception, FacebookRequestError) and
                    request.exception.api_error_code() in token_error_codes):
                logout_user(request)

            return response

    def _recover_last_error_post(self, request):
        """
        Recover the post data from a previous request that triggered exception
        at the SDK level. Called every time because we need to make sure that
        the session set by an exception is always consumed and destroyed.
        """
        data = None
        if request.session.get('last_error_post', None):
            data = request.session['last_error_post']
            del request.session['last_error_post']
        return data

    def __get_sample_view(self, sample, kwargs):
        view_module = __import__(
            sample.view_module,
            globals(),
            locals(),
            [sample.view_class],
            -1)
        view_class = getattr(view_module, sample.view_class)
        view = view_class.as_view()
        return view
