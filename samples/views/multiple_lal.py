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
from samples.views.sample import SampleBaseView
from samples.samplecode import multiple_lal
from security.fbsample import fbads_sample
from components.component_form import ComponentForm
from components.custom_audience_select import CustomAudienceSelect
from components.country_select import CountrySelect
from components.ad_account_select import AdAccountSelect


class MultipleLalForm(ComponentForm):

    ad_account = AdAccountSelect()
    base_name = forms.CharField(max_length=50)
    seed_id = CustomAudienceSelect()
    country = CountrySelect()
    country_2 = CountrySelect(id='country_2', required=False)
    country_3 = CountrySelect(id='country_3', required=False)

    ratio = forms.IntegerField(
        min_value=1,
        max_value=10,
        help_text='Lookalike percentage value, from 1 to 10')
    ratio_2 = forms.IntegerField(min_value=1, max_value=10, required=False)
    ratio_3 = forms.IntegerField(min_value=1, max_value=10, required=False)


class MultipleLalView(SampleBaseView):

    BUTTON_TEXT = "Create Lookalike Audiences"

    @fbads_sample('samples.samplecode.multiple_lal')
    def get(self, request, *args, **kwargs):
        form = MultipleLalForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.multiple_lal')
    def post(self, request, *args, **kwargs):
        form = MultipleLalForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        # Get form parameters
        account_id = form.cleaned_data['ad_account']
        base_name = form.cleaned_data['base_name']
        seed_id = form.cleaned_data['seed_id']
        countries = [form.cleaned_data['country']]
        country_2 = form.cleaned_data['country_2']
        if country_2 and country_2 not in countries:
            countries.append(form.cleaned_data['country_2'])
        country_3 = form.cleaned_data['country_3']
        if country_3 and country_3 not in countries:
            countries.append(form.cleaned_data['country_3'])

        ratios = [form.cleaned_data['ratio']]
        ratio_2 = form.cleaned_data['ratio_2']
        if ratio_2 and ratio_2 not in ratios:
            ratios.append(form.cleaned_data['ratio_2'])
        ratio_3 = form.cleaned_data['ratio_3']
        if ratio_3 and ratio_3 not in ratios:
            ratios.append(form.cleaned_data['ratio_3'])

        sample = multiple_lal.MultipleLalSample()
        lals = sample.create_lals(
            account_id,
            seed_id,
            base_name,
            countries,
            ratios,
        )

        act_number = account_id[4:]
        status = '{0} lookalike audiences created:<br/>'.format(len(lals))
        for lal in lals:
            lal_link = ('https://business.facebook.com/ads/manager/audiences/' +
                        'detail/?act={0}&ids={1}'.format(act_number, lal['id']))
            lal_link = ('<a target="_blank" href={0}>' + lal['name'] +
                        '</a><br/>').format(lal_link)
            status = status + lal_link

        # account_id is in the format of act_12345
        audience_manager_link = ('https://business.facebook.com/ads/manager/' +
                                 'audiences/manage/?act={0}'.format(act_number))

        status = status + ('Check at your <a target="_blank" href="{0}">' +
                           'audience manager</a>').format(audience_manager_link)

        return self.render_form_with_status(request, form, status)
