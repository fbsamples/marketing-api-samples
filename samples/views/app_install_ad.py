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
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect
from components.image_input import ImageInput
from components.targeting_spec import TargetingSpec
from components.app_select import AppSelect
from components.page_select import PageSelect
from components.bid_component import BidComponent
from samples.samplecode import app_install_ad
from security.fbsample import fbads_sample
from facebookads.objects import Campaign
import os


targeting_info_initial = TargetingSpec.US_ANDROID_MOBILEFEED


class AppInstallAdForm(ComponentForm):

    """
    We need these parameters for the sample script:
        account_id: AdAccountSelect
        base_name: TextInput
        message: TextInput
        image_path: ImageInput
        daily_budget: DecimalField
        page_id: PageSelect
        app_id: AppSelect
        app_name: AppSelect
        app_store_link: AppSelect
        deferred_app_link: TextInput
        bid_info: BidComponent
        targeting: TargetingSpec
    """
    ad_account = AdAccountSelect()
    name = forms.CharField(
        label='Basename for your ad',
        widget=forms.TextInput(attrs={'placeholder': 'App Install'}),
        help_text='''We will generate campaign name, adset name and ad name
        with basename.'''
    )

    page = PageSelect(help_text='Your ad will be published from this page.')
    app = AppSelect()
    image = ImageInput(allow_empty_file=False, required=True)
    message = forms.CharField(
        label='Ad Message',
        initial='Try out this awesome app!'
    )
    app_link = forms.CharField(
        label='Deferred app link to your app', min_length=4, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example://detail/1234'})
    )

    targeting = TargetingSpec(initial=targeting_info_initial)
    PLATFORMS = (
        ('Android', 'Android'),
        ('iOS', 'iOS'),
    )
    platform = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=PLATFORMS,
        initial='Android',
        help_text='Platform needs to match the platform in targeting above'
    )

    bid_info = BidComponent('bid_info',
                            Campaign.Objective.mobile_app_installs)
    daily_budget = forms.DecimalField(min_value=1, initial=1000)

    def clean(self):
        self.cleaned_data = super(AppInstallAdForm, self).clean()

        self.cleaned_data = \
            super(AppInstallAdForm, self).validate_mobile_platform_targeting()

        return self.cleaned_data


class AppInstallAdView(SampleBaseView):

    BUTTON_TEXT = "Create App Install Ad"

    @fbads_sample('samples.samplecode.app_install_ad')
    def get(self, request, *args, **kwargs):
        form = AppInstallAdForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.app_install_ad')
    def post(self, request, *args, **kwargs):
        form = AppInstallAdForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        image_path = self._handle_image_upload(request.FILES['image'])

        account_id = form.cleaned_data['ad_account']
        base_name = form.cleaned_data['name']
        message = form.cleaned_data['message']
        daily_budget = form.cleaned_data['daily_budget']
        page_id = form.cleaned_data['page']

        platform = form.cleaned_data['platform']

        deferred_app_link = None
        if 'app_link' in form.cleaned_data:
            deferred_app_link = form.cleaned_data['app_link']

        bid_info = form.cleaned_data['bid_info']
        optimization_goal = bid_info[BidComponent.ID_OPTIMIZATION_GOAL]
        billing_event = bid_info[BidComponent.ID_BILLING_EVENT]
        bid_amount = bid_info[BidComponent.ID_BID_AMOUNT]

        targeting = form.cleaned_data['targeting']
        app = form.cleaned_data['app']

        try:
            app_id = app['id']
            app_name = app['name']
            if platform == 'Android':
                app_store_link = \
                    app['object_store_urls']['google_play']
            elif platform == 'iOS':
                app_store_link = app['object_store_urls']['itunes']
            else:
                raise

            maia_sample = app_install_ad.AppInstallAdSample()

            r = maia_sample.create_app_install_ad(
                account_id,
                base_name,
                message,
                image_path,
                daily_budget,
                page_id,
                optimization_goal,
                billing_event,
                bid_amount,
                targeting,
                app_id,
                app_name,
                app_store_link,
                deferred_app_link,
            )
            adlink = (
                'https://www.facebook.com/ads/manager/' + r['campaign_id']
            )
            status = (
                'Campaign created: <a href="%s">%s</a>' %
                (adlink, r['campaign_id'])
            )
            data = {
                'ad_preview_dict': {
                    'ad_id': r['ad_id'],
                    'ad_format': 'MOBILE_FEED_STANDARD',
                }
            }
            return self.render_form_with_status(request, form, status, data)
        except:
            raise
        finally:
            """ Clean up the temp images """
            os.remove(image_path)
