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
from components.targeting_spec import TargetingSpec
from components.page_select import PageSelect
from components.app_select import AppSelect
from components.image_input import ImageInput
from components.bid_component import BidComponent
from samples.samplecode import carousel_app_ad
from security.fbsample import fbads_sample
from facebookads.objects import Campaign
import os


targeting_info_initial = TargetingSpec.US_ANDROID_MOBILEFEED


class CarouselAppAdForm(ComponentForm):

    ad_account = AdAccountSelect()
    name = forms.CharField(
        label='Basename for your ads',
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Carousel App Install Ad'}
        ),
        help_text='''We will generate campaign name, adset name and ad name
        with basename.'''
    )
    message = forms.CharField(
        label='Ad Message',
        max_length=90, required=True,
        initial='Try out this new app!'
    )
    daily_budget = forms.DecimalField(min_value=1, required=True, initial=1000)
    bid_info = BidComponent('bid_info',
                            Campaign.Objective.mobile_app_installs)
    targeting = TargetingSpec(
        initial=targeting_info_initial,
        help_text='You need to choose mobile platform and a placement type' +
                  ' that has mobile, and the platform should match with below'
    )

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

    appinfo_fbpage_id = PageSelect(
        help_text='The page from which the ad is posted'
    )

    app = AppSelect(help_text='Select your application in the pop up')

    # The carousel contains 3 images
    image_1 = ImageInput(
        label='Image 1',
        allow_empty_file=False, required=True,
        help_text='PNG or JPG file with width=1200px, height=627px'
    )
    link_title_1 = forms.CharField(
        help_text='Title message for image 1',
        widget=forms.TextInput(attrs={'placeholder': 'My App Name'})
    )
    deep_link_1 = forms.CharField(
        help_text='Deep link for image 1',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example://product/123'})
    )
    image_2 = ImageInput(
        id='id_image_2', label='Image 2',
        allow_empty_file=False, required=True,
        help_text='PNG or JPG file with width=1200px, height=627px'
    )
    link_title_2 = forms.CharField(
        help_text='Title message for image 2',
        widget=forms.TextInput(attrs={'placeholder': 'My App Name'})
    )
    deep_link_2 = forms.CharField(
        help_text='Deep link for image 2',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example://product/123'})
    )
    image_3 = ImageInput(
        id='id_image_3', label='Image 3',
        allow_empty_file=False, required=True,
        help_text='PNG or JPG file with width=1200px, height=627px'
    )
    link_title_3 = forms.CharField(
        help_text='Title message for image 3',
        widget=forms.TextInput(attrs={'placeholder': 'My App Name'})
    )
    deep_link_3 = forms.CharField(
        help_text='Deep link for image 3',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'example://product/123'})
    )

    def clean(self):
        self.cleaned_data = super(CarouselAppAdForm, self).clean()

        self.cleaned_data = \
            super(CarouselAppAdForm, self).validate_mobile_platform_targeting()

        return self.cleaned_data


class CarouselAppAdView(SampleBaseView):

    BUTTON_TEXT = "Create Carousel App Install Ad"

    @fbads_sample('samples.samplecode.carousel_app_ad')
    def get(self, request, *args, **kwargs):
        form = CarouselAppAdForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.carousel_app_ad')
    def post(self, request, *args, **kwargs):
        form = CarouselAppAdForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        imagefilepaths = []
        imagefilepaths.append(
            self._handle_image_upload(request.FILES['image_1'])
        )
        imagefilepaths.append(
            self._handle_image_upload(request.FILES['image_2'])
        )
        imagefilepaths.append(
            self._handle_image_upload(request.FILES['image_3'])
        )

        linktitles = []
        linktitles.append(form.cleaned_data['link_title_1'])
        linktitles.append(form.cleaned_data['link_title_2'])
        linktitles.append(form.cleaned_data['link_title_3'])

        deeplinks = []
        deeplinks.append(form.cleaned_data['deep_link_1'])
        deeplinks.append(form.cleaned_data['deep_link_2'])
        deeplinks.append(form.cleaned_data['deep_link_3'])

        accountid = form.cleaned_data['ad_account']
        basename = form.cleaned_data['name']
        message = form.cleaned_data['message']
        dailybudget = form.cleaned_data['daily_budget']

        appinfo = {}

        app_data = form.cleaned_data['app']
        appinfo['app_name'] = app_data['name']
        appinfo['fbapplication_id'] = app_data['id']
        appinfo['fbpage_id'] = form.cleaned_data['appinfo_fbpage_id']
        appinfo['appstore_link'] = form.cleaned_data['store_url']

        bid_info = form.cleaned_data['bid_info']
        optimization_goal = bid_info[BidComponent.ID_OPTIMIZATION_GOAL]
        billing_event = bid_info[BidComponent.ID_BILLING_EVENT]
        bid_amount = bid_info[BidComponent.ID_BID_AMOUNT]

        targeting = form.cleaned_data['targeting']

        sample = carousel_app_ad.CarouselAppAdSample()
        try:
            r = sample.carousel_app_ad_create(
                accountid=accountid,
                basename=basename,
                message=message,
                imagefilepaths=imagefilepaths,
                linktitles=linktitles,
                deeplinks=deeplinks,
                dailybudget=dailybudget,
                appinfo=appinfo,
                optimization_goal=optimization_goal,
                billing_event=billing_event,
                bid_amount=bid_amount,
                targeting=targeting,
            )
            adlink = (
                '<a href="https://www.facebook.com/ads/manager/' +
                r['campaignid'] + '" target="_blank">ads manager</a>'
            )
            status = (
                'Campaign created %s. View it at %s' %
                (r['campaignid'], adlink)
            )
            data = {
                'ad_preview_dict': {
                    'ad_id': r['adid'],
                    'ad_format': 'MOBILE_FEED_STANDARD',
                }
            }
            return self.render_form_with_status(request, form, status, data)
        except:
            raise
        finally:
            """ Clean up the temp images """
            for image_path in imagefilepaths:
                os.remove(image_path)
