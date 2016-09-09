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
from django.shortcuts import render
from samples.samplecode import instagram_potential
from security.fbsample import fbads_sample
from samples.views.sample import SampleBaseView
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect


class AccountForm(ComponentForm):

    ad_account = AdAccountSelect()
    # STATUSES = (
    #     ('False', 'Do not include ARCHIVED ad sets'),
    #     ('True', 'Include ARCHIVED ad sets'),
    # )
    # include_archived = forms.ChoiceField(
    #     widget=forms.RadioSelect,
    #     choices=PLATFORMS,
    #     initial='Android',
    #     help_text='Platform needs to match the platform in targeting above'
    # )
    include_archived = forms.BooleanField(
        label="Include archived ad sets?",
        initial=False,
        required=False,
    )
    limit = forms.DecimalField(
        label="How many ad sets to check. The more you pick, the longer it " +
        "will take.",
        min_value=1,
        max_value=50,
        required=True,
        initial=10
    )


class InstagramPotentialView(SampleBaseView):

    @fbads_sample('samples.samplecode.instagram_potential')
    def get(self, request, *args, **kwargs):
        form = AccountForm()
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.instagram_potential')
    def post(self, request, *args, **kwargs):
        form = AccountForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        account_id = form.cleaned_data['ad_account']
        include_archived = form.cleaned_data['include_archived']
        limit = form.cleaned_data['limit']

        analyzer = instagram_potential.InstagramAdsPotential()
        ad_sets = analyzer.get_ad_sets(account_id, include_archived, limit)
        return render(
            request,
            'samples/ad_set_list.html',
            {'ad_sets': ad_sets, 'account_id': account_id})
