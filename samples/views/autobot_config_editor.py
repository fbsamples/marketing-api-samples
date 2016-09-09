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
from django.http import HttpResponse

from samples.views.sample import SampleBaseView
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect
from components.app_select import AppSelect
from components.page_select import PageSelect
from security.fbsample import fbads_sample
import json


class AutobotConfigEditorForm(ComponentForm):

    name = forms.CharField(
        label='Name',
        max_length=128, required=True,
        initial='My Autobot config'
    )

    ad_account = AdAccountSelect()

    app = AppSelect(help_text='Select your application in the pop up')

    page = PageSelect(help_text='Select your Page in the pop up')

    settings_file = forms.CharField(
        label='Settings file',
        max_length=128, required=True,
        initial="autobot_config.json"
    )

    PLATFORMS = (
        ('Android', 'Android'),
        ('iOS', 'iOS'),
        ('Canvas', 'Canvas'),
    )

    access_token = forms.CharField(
        label='System Token',
        max_length=201, required=True,
        initial='Paste system token here'
    )

    adset_life = forms.IntegerField(
        label='Ad Set Life',
        required=True,
        max_value=180,
        min_value=1,
        initial=14,
    )

    age_min = forms.IntegerField(
        label='Age min',
        required=True,
        max_value=65,
        min_value=13,
        initial=25,
    )

    margin_requirement = forms.DecimalField(
        label='Margin Requirement',
        required=True,
        max_value=2.00,
        min_value=0.00,
        decimal_places=2,
        initial=1.15,
    )

    min_purchase_percentage = forms.DecimalField(
        label='Minimum purchase (%)',
        required=True,
        max_value=1.00,
        min_value=0.00,
        decimal_places=2,
        initial=0.25,
    )

    platforms = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'id_platform_select'}),
        choices=PLATFORMS,
        initial=(PLATFORMS[0])
    )

    def clean(self):
        self.cleaned_data = super(AutobotConfigEditorForm, self).clean()

        return self.cleaned_data


class AutobotConfigEditorView(SampleBaseView):

    BUTTON_TEXT = "Save Autobot Config File"

    @fbads_sample('samples.samplecode.autobot_config_editor')
    def get(self, request, *args, **kwargs):
        form = AutobotConfigEditorForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.autobot_config_editor')
    def post(self, request, *args, **kwargs):
        form = AutobotConfigEditorForm(request.POST, request.FILES)

        if not form.is_valid():
            return self.render_invalid_form(request, form)

        # XXX,TODO: scrub out file name from potential path.
        output = form.cleaned_data['settings_file']

        config = {}
        config['app_id'] = form.cleaned_data['app']['id']
        config['page_id'] = form.cleaned_data['page']
        config['access_token'] = form.cleaned_data['access_token']
        config['name'] = form.cleaned_data['name']
        config['adset_life'] = form.cleaned_data['adset_life']
        config['create_ads'] = False
        config['age_min'] = form.cleaned_data['age_min']
        config['settings_file'] = form.cleaned_data['settings_file']
        config['lifetime_budget'] = {}
        config['lifetime_budget']['default'] = 0
        config['margin_requirement'] = \
            float(form.cleaned_data['margin_requirement'])
        config['min_purchase_percentage'] = \
            float(form.cleaned_data['min_purchase_percentage'])
        config['user_adclusters'] = []
        # XXX,TODO: Interests selection is in a separate diff.
        config['interests'] = []
        config['lal_ratio_by_country'] = {}
        config['lal_ratio_by_country']['default'] = 0.05
        config['lal_source_audience_by_country'] = {}
        config['lal_source_audience_by_country']['default'] = 25
        config['pltv_days'] = [0, 28, 90, 182, 365, 545]
        config['pltv_days_strings'] = \
            ['1d', '28d', '90d', '6mo', '1yr', '18 mo']
        config['scale_targeting_type'] = {}
        config['scale_targeting_type']['BROAD'] = 0
        config['scale_targeting_type']['LOOKALIKE'] = 1.0
        config['scale_targeting_type']['INTEREST'] = 0.7
        config['scale_targeting_type']['WIDE_LOOKALIKE'] = 0
        config['ad_accounts'] = {}
        config['ad_accounts']['default'] = form.cleaned_data['ad_account'][4:]

        response = HttpResponse(json.dumps(config, indent=2, sort_keys=False),
                                content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename=%s' % output

        return response
