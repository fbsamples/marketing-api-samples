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

from components.ad_account_select import AdAccountSelect
from components.adset_select import AdSetSelect
from components.component_form import ComponentForm
from django.http import JsonResponse
from samples.views.sample import SampleBaseView
from samples.samplecode import an_optin
from security.fbsample import fbads_sample
import logging

logger = logging.getLogger(__name__)


class AudienceNetworkOptInForm(ComponentForm):
    ad_account = AdAccountSelect()
    adset = AdSetSelect()


class AudienceNetworkOptInView(SampleBaseView):

    BUTTON_TEXT = "Opt into Audience Network"

    @fbads_sample('samples.samplecode.an_optin')
    def get(self, request, *args, **kwargs):

        if self.request.is_ajax():
            eligible_adsets = []
            sample = an_optin.AudienceNetworkOptinSample()
            # Get request parameter
            adaccount = request.GET.__getitem__('ad_ac')
            if not (adaccount is None):
                adsets = sample.retrieve_eligible_adsets_for_an(adaccount, True)
                for adset in adsets:
                    eligible_adset = {}
                    eligible_adset['id'] = adset[adset.Field.id]
                    eligible_adset['name'] = adset[adset.Field.name]
                    eligible_adsets.append(eligible_adset)

            result = JsonResponse(eligible_adsets, safe=False)
            return result

        form = AudienceNetworkOptInForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.an_optin')
    def post(self, request, *args, **kwargs):
        form = AudienceNetworkOptInForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        # Get form parameters
        adset_id = form.cleaned_data['adset']

        # Enable audience network on the adset
        adsets = [adset_id]
        sample = an_optin.AudienceNetworkOptinSample()
        result = sample.enable_an_on_adsets(adsets)
        if result and result[0][adset_id]['status'] == 1:
            status = ("Success. Successfully enabled audience network on \
                ad set " + adset_id + ".")
            data = {}
            return self.render_form_with_status(request, form, status, data)
        else:
            logger.debug("Error when trying to enable audience network for \
                ad set " + adset_id + ".")
            # actually nothing wrong with form but still throwing invalid
            # form to visually convey the action did not go through
            return self.render_invalid_form(request, form)
