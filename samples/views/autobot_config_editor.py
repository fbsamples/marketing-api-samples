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
from django.core.exceptions import ValidationError
from django.shortcuts import render

from samples.views.sample import SampleBaseView
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect
from components.country_select import CountrySelect
from components.interest_select import InterestSelect
from components.autobot.asset_feed import AssetFeed
from components.app_select import AppSelect
from components.page_select import PageSelect
from common.utils import construct_url
from security.fbsample import fbads_sample
import json
import re
import urllib2

asset_feed_initial = AssetFeed.ASSET_FEED_DEFAULT


class AutobotConfigEditorForm(ComponentForm):

    ad_account = AdAccountSelect(
        help_text='* Only one ad account is supported through the config UI.'
    )

    app = AppSelect(help_text='Select your application in the pop up')

    name = forms.CharField(
        label='Name',
        max_length=128, required=True,
        initial='My Autobot config'
    )

    page = PageSelect(help_text='Select your Page in the pop up')

    PLATFORMS = (
        ('Android', 'Android'),
        ('iOS', 'iOS'),
        ('Canvas', 'Canvas'),
    )

    access_token = forms.CharField(
        label='System Token',
        max_length=201, required=True,
        initial='- system access token -',
        help_text="Paste system access token."
    )

    adset_life = forms.IntegerField(
        label='Ad Set Life',
        required=True,
        max_value=180,
        min_value=1,
        initial=14,
    )

    lifetime_budget = forms.IntegerField(
        label='Lifetime Budget',
        required=True,
        max_value=1000000,
        min_value=0,
        initial=7500,
    )

    age_min = forms.IntegerField(
        label='Age Minimum',
        required=True,
        max_value=65,
        min_value=13,
        initial=18,
    )

    interests = InterestSelect(
        required=False,
        help_text='Type interest to lookup or find suggestions.'
    )

    min_purchase_percentage = forms.DecimalField(
        label='Minimum purchase (%)',
        required=True,
        max_value=1.00,
        min_value=0.00,
        decimal_places=2,
        initial=0.25,
        help_text="""Autobot will automatically include all countries that have
        purchase values exceeding this percentage."""
    )

    forced_countries = CountrySelect(
        id='id_forced_countres_select',
        multiple=True,
        required=False,
    )

    ignored_countries = CountrySelect(
        id='id_ignore_countries_select',
        multiple=True,
        required=False,
    )

    margin_requirement = forms.DecimalField(
        label='Margin Requirement',
        required=True,
        max_value=2.00,
        min_value=0.00,
        decimal_places=2,
        initial=1.15,
        help_text="""Scales the bid Autobot creates; intended to account for
        any overhead incurred between purchase value and actual profit."""
    )

    scale_targeting_type = forms.CharField(
        label='Scale Targeting',
        initial='''{"INTEREST": 0.7, "LOOKALIKE": 1.0, \
"WIDE_LOOKALIKE": 0.9, "BROAD": 0}''',
        help_text="""
        Multiplies the bid Autobot creates based on the type of ad
        being run. INTEREST of 1 means full bid, while BROAD 0.25 means 1/4 for
        broad targeting.
        The options are INTEREST, LOOKALIKE, WIDE_LOOKALIKE, and BROAD"""
    )

    platforms = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'id_platform_select'}),
        choices=PLATFORMS,
        initial=(PLATFORMS[0])
    )

    # https://developers.facebook.com/docs/marketing-api/targeting-specs/v2.7
    ANDROID_VERSIONS = (
        (2.0, '2.0'),
        (2.1, '2.1'),
        (2.2, '2.2'),
        (2.3, '2.3'),
        (3.0, '3.0'),
        (3.1, '3.1'),
        (3.2, '3.2'),
        (4.0, '4.0'),
        (4.1, '4.1'),
        (4.2, '4.2'),
        (4.3, '4.3'),
        (4.4, '4.4'),
        (5.0, '5.0'),
        (5.1, '5.1'),
    )
    IOS_VERSIONS = (
        (2.0, '2.0'),
        (3.0, '3.0'),
        (4.0, '4.0'),
        (4.3, '4.3'),
        (5.0, '5.0'),
        (6.0, '6.0'),
        (7.0, '7.0'),
        (8.0, '8.0'),
        (9.0, '9.0'),
    )

    android_version = forms.ChoiceField(label='Android Minimum Version',
                                        choices=ANDROID_VERSIONS,
                                        initial=4.1,
                                        required=False)
    ios_version = forms.ChoiceField(label='iOS Minimum Version',
                                    choices=IOS_VERSIONS,
                                    initial=8.0,
                                    required=False)

    asset_feed = AssetFeed(initial=asset_feed_initial)

    MISC_JSON = '''
    {
        "create_ads": false,
        "user_adclusters": [],
        "pltv_days": [0, 28, 90, 182, 365, 545],
        "pltv_days_strings": ["1d", "28d", "90d", "6mo", "1yr", "18 mo"],
        "lal_ratio_by_country": { "default": 0.05 },
        "lal_source_audience_by_country": { "default": 25 }
    }
    '''

    misc = forms.CharField(label='Miscellaneous Settings',
                           widget=forms.Textarea,
                           initial=MISC_JSON,
                           )

    settings_file = forms.CharField(
        label='Output Logging File',
        max_length=128, required=True,
        initial="autobot_output.json",
        help_text="Where Autobot will trace output at runtime."
    )

    save_filename = forms.CharField(
        label='Save Config as',
        max_length=128, required=True,
        initial="autobot_config.json"
    )

    def __init__(self, *args, **kwargs):
        super(AutobotConfigEditorForm, self).__init__(*args, **kwargs)

        js = """
          const name = document.getElementById('id_name');
          const app = document.getElementById('id_app_select');
          if (name && app) {
            try {
                const info = JSON.parse(app.value);
                if (info.name != name.value)
                    name.value = info.name;
            } catch(err) {}
          }
        """
        self.fields['app'].widget.attrs.update({'onblur': js})

    def clean(self):
        self.cleaned_data = super(AutobotConfigEditorForm, self).clean()

        if 'access_token' in self.cleaned_data:
            access_token = self.cleaned_data['access_token']

            url = construct_url('https://graph.facebook.com/v2.7/me',
                                {'access_token': access_token})
            try:
                urllib2.urlopen(url).read()
            except urllib2.HTTPError:
                raise ValidationError('Invalid access token.')

        return self.cleaned_data


class AutobotConfigEditorLoadForm(ComponentForm):
    json_config = forms.FileField(label='Import Autobot Config file',
                                  help_text='Previously generated JSON')


class AutobotConfigEditorView(SampleBaseView):

    TEMPLATE = 'samples/autbot_config_editor_form.html'
    BUTTON_TEXT = "Save Autobot Config File"
    LOAD_BUTTON_TEXT = "Import"

    def render_form(self, request, form, load_form=None):
        return render(
            request,
            self.TEMPLATE,
            {
                'form': form,
                'button_text': self.BUTTON_TEXT,
                'load_form': load_form,
                'load_button_text': self.LOAD_BUTTON_TEXT,
                'target': self.BUTTON_TARGET,
            }
        )

    @fbads_sample('samples.samplecode.autobot_config_editor')
    def get(self, request, *args, **kwargs):
        form = AutobotConfigEditorForm(request.last_error_post)
        load_form = AutobotConfigEditorLoadForm(request.last_error_post)
        return self.render_form(request, form, load_form)

    @fbads_sample('samples.samplecode.autobot_config_editor')
    def post(self, request, *args, **kwargs):

        if self.LOAD_BUTTON_TEXT in request.POST:
            load_form = AutobotConfigEditorLoadForm(
                request.POST,
                request.FILES)

            if load_form.is_valid():
                try:
                    config = self.read_config(request.FILES['json_config'])
                    config['save_filename'] = request.FILES['json_config'].name
                    form = AutobotConfigEditorForm(config)
                    return self.render_form(request, form)
                except ValueError:
                    raise ValidationError('Invalid JSON file.')

            else:
                form = AutobotConfigEditorForm(request.last_error_post)
                return self.render_form(request, form, load_form)

        form = AutobotConfigEditorForm(request.POST, request.FILES)

        if not form.is_valid():
            return self.render_invalid_form(request, form)

        # XXX,TODO: scrub out file name from potential path.
        output = form.cleaned_data['save_filename']
        platforms = form.cleaned_data['platforms']
        android_version = form.cleaned_data['android_version']
        ios_version = form.cleaned_data['ios_version']

        # XXX,TODO: trap exception and render error msg.
        config = \
            json.loads(form.cleaned_data['misc'])

        config['app_id'] = int(form.cleaned_data['app']['id'])
        config['page_id'] = int(form.cleaned_data['page'])
        config['access_token'] = form.cleaned_data['access_token']
        config['name'] = form.cleaned_data['name']
        config['min_os_version'] = \
            self.min_os_version(platforms, android_version, ios_version)
        config['adset_life'] = form.cleaned_data['adset_life']
        config['forced_countries'] = \
            self.tokenize_multi_select(form.cleaned_data['forced_countries'])
        config['ignored_countries'] = \
            self.tokenize_multi_select(form.cleaned_data['ignored_countries'])
        config['age_min'] = form.cleaned_data['age_min']
        config['settings_file'] = form.cleaned_data['settings_file']
        config['lifetime_budget'] = \
            self.lifetime_budget(
                form.cleaned_data['lifetime_budget'], platforms)
        config['margin_requirement'] = \
            float(form.cleaned_data['margin_requirement'])
        config['min_purchase_percentage'] = \
            float(form.cleaned_data['min_purchase_percentage'])

        if (form.cleaned_data['interests']):
            interests = filter(lambda x: x.isdigit() or x == ',',
                               form.cleaned_data['interests']).split(',')
            config['interests'] = [int(x) for x in interests]

        config['scale_targeting_type'] = \
            json.loads(form.cleaned_data['scale_targeting_type'])
        config['ad_accounts'] = \
            self.ad_accounts(form.cleaned_data['ad_account'][4:], platforms)
        config['asset_feed'] = form.cleaned_data['asset_feed']

        response = HttpResponse(json.dumps(config, indent=2, sort_keys=True),
                                content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename=%s' % output

        return response

    def tokenize_multi_select(self, form_field):
        return re.sub("[u\[\]\'\s]", '', form_field).split(',')

    def lifetime_budget(self, budget, platforms, countries=[]):
        lifetime_budget = {}
        lifetime_budget['default'] = budget
        for platform in platforms:
            lifetime_budget[platform] = {}
            lifetime_budget[platform]['default'] = budget
            for country in countries:
                lifetime_budget[platform][country] = budget

        return lifetime_budget

    def ad_accounts(self, ad_account, platforms, countries=[]):
        ad_account = int(ad_account)
        ad_accounts = {}
        ad_accounts['default'] = ad_account
        for platform in platforms:
            ad_accounts[platform] = {}
            ad_accounts[platform]['default'] = ad_account
            for country in countries:
                ad_accounts[platform][country] = ad_account

        return ad_accounts

    def min_os_version(self, platforms, android, ios):
        versions = {}
        for platform in platforms:
            if platform == 'Android' and android is not None:
                versions[platform] = float(android)
            elif platform == 'iOS' and ios is not None:
                versions[platform] = float(ios)

        return versions

    def read_config(self, f):
        config = json.load(f)

        config['ad_account'] = 'act_' + str(config['ad_accounts']['default'])
        config['app'] = '{"id": %s}' % config['app_id']
        config['page'] = str(config['page_id'])
        if 'Android' in config['min_os_version']:
            config['android_version'] = config['min_os_version']['Android']
            config['android_version'] = \
                round(float(config['android_version']), 1)

        if 'iOS' in config['min_os_version']:
            config['ios_version'] = config['min_os_version']['iOS']
            config['ios_version'] = round(float(config['ios_version']), 1)
        config['lifetime_budget'] = config['lifetime_budget']['default']
        config['scale_targeting_type'] = \
            json.dumps(config['scale_targeting_type'], indent=2)
        config['platforms'] = list(config['min_os_version'].keys())
        if 'interests' in config:
            config['interests'] = '[' + \
                ','.join(str(i) for i in config['interests']) + ']'

        fields = ['ad_accounts', 'app_id', 'page_id', 'lifetime_budget',
                  'min_os_version', 'lifetime_budget', 'interests']
        form = AutobotConfigEditorForm()
        for field in form:
            fields.append(field.name)

        misc = {}
        for field in config:
            if field not in fields:
                misc[field] = config[field]

        config['misc'] = json.dumps(misc, indent=2, sort_keys=True)

        return config
