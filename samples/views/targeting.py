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

from samples.views.sample import SampleBaseView
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect
from components.targeting_spec import TargetingSpec
from security.fbsample import fbads_sample


class TargetingForm(ComponentForm):

    ad_account = AdAccountSelect()
    targeting_spec = TargetingSpec()


class TargetingView(SampleBaseView):

    @fbads_sample('samples.samplecode.targeting')
    def get(self, request, *args, **kwargs):
        form = TargetingForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.targeting')
    def post(self, request, *args, **kwargs):
        form = TargetingForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        status = "OK"
        return self.render_form_with_status(request, form, status)
