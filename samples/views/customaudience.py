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

from django import forms
from samples.samplecode import customaudience
from samples.views.sample import SampleBaseView
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect
from components.file_input import FileInput
from security.fbsample import fbads_sample


class CustomAudienceForm(ComponentForm):

    ad_account = AdAccountSelect()
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=100, required=False)
    optout_link = forms.URLField()
    data_file = FileInput(
        max_length=5242880,
        allow_empty_file=False,
        help_text='''Data format: one hash per line.''',
    )


class CustomAudienceView(SampleBaseView):

    BUTTON_TEXT = "Create Custom Audience"

    @fbads_sample('samples.samplecode.customaudience')
    def get(self, request, *args, **kwargs):
        form = CustomAudienceForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.customaudience')
    def post(self, request, *args, **kwargs):
        form = CustomAudienceForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        schema = customaudience.CustomAudience.Schema.email_hash
        casample = customaudience.CustomAudienceSample()
        caid = casample.create_audience(
            form.cleaned_data['ad_account'],
            form.cleaned_data['name'],
            form.cleaned_data['description'],
            form.cleaned_data['optout_link'])
        cadata = []
        for line in form.cleaned_data['data_file']:
            cadata.append(line)

        result = casample.upload_users_to_audience(caid, cadata, schema)
        status = result.body()

        return self.render_form_with_status(request, form, status)
