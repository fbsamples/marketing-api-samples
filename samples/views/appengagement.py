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
from components.bid_component import BidComponent
from components.page_select import PageSelect
from django.core.files.images import get_image_dimensions
from samples.samplecode import appengagement
from security.fbsample import fbads_sample
import os


targeting_info_initial = TargetingSpec.US_ANDROID_MOBILEFEED


class AppEngagementForm(ComponentForm):

    IMAGE_MIN_WIDTH = 1200
    IMAGE_MIN_HEIGHT = 627

    ad_account = AdAccountSelect()
    name = forms.CharField(
        label='Basename for your ads',
        max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'My App Engagement'}),
        help_text='''We will generate campaign name, adset name and ad name
        with basename.'''
    )
    page = PageSelect()
    image = ImageInput(
        allow_empty_file=False, required=True,
        help_text='PNG or JPG file with width=1200px, height=627px'
    )
    message = forms.CharField(
        label='Ad Message',
        max_length=90, required=True,
        initial='Try out this feature in our app!'
    )

    app = AppSelect()
    deep_link = forms.CharField(
        label='Deep link to your app action', min_length=4, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'example://detail/1234'})
    )
    pixel = forms.CharField(
        label='Facebook offsite pixel id of your app',
        min_length=1, required=True,
        initial='null',
        help_text='Fill `null` to skip.'
    )

    targeting = TargetingSpec(initial=targeting_info_initial)
    PLATFORMS = (
        ('Android', 'Android'),
        ('iOS', 'iOS'),
    )
    platform = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=PLATFORMS,
        help_text='Platform needs to match the platform in targeting above'
    )

    bid_info = BidComponent('bid_info', 'MOBILE_APP_ENGAGEMENT')
    daily_budget = forms.DecimalField(
        min_value=1,
        required=True,
        initial='500',
        help_text='to bid $5.00, set 500'
    )

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('Not an image!')
        else:
            w, h = get_image_dimensions(image)
            if w < AppEngagementForm.IMAGE_MIN_WIDTH:
                raise forms.ValidationError(
                    "The image is %i pixel wide. It's supposed to be >= %i." %
                    (w, AppEngagementForm.IMAGE_MIN_WIDTH)
                )
            if h < AppEngagementForm.IMAGE_MIN_HEIGHT:
                raise forms.ValidationError(
                    "The image is %i pixel high. It's supposed to be >= %i." %
                    (h, AppEngagementForm.IMAGE_MIN_HEIGHT)
                )
        return image

    def clean(self):
        self.cleaned_data = super(AppEngagementForm, self).clean()

        self.cleaned_data = \
            super(AppEngagementForm, self).validate_mobile_platform_targeting()

        return self.cleaned_data


class AppEngagementView(SampleBaseView):

    BUTTON_TEXT = "Create App Engagement Ad"

    @fbads_sample('samples.samplecode.appengagement')
    def get(self, request, *args, **kwargs):
        form = AppEngagementForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.appengagement')
    def post(self, request, *args, **kwargs):
        form = AppEngagementForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        imagefilepath = self._handle_image_upload(request.FILES['image'])

        accountid = form.cleaned_data['ad_account']
        basename = form.cleaned_data['name']
        message = form.cleaned_data['message']
        dailybudget = form.cleaned_data['daily_budget']

        platform = form.cleaned_data['platform']

        appinfo = {}

        appinfo['fbpage_id'] = form.cleaned_data['page']
        appinfo['app_deep_link'] = form.cleaned_data['deep_link']
        appinfo['fboffsitepixel_id'] = form.cleaned_data['pixel']

        # get data from BidComponet, it is list.
        bid_info = form.cleaned_data['bid_info']

        targeting = form.cleaned_data['targeting']

        app = form.cleaned_data['app']

        try:
            appinfo['fbapplication_id'] = app['id']
            appinfo['app_name'] = app['name']
            if platform == 'Android':
                appinfo['appstore_link'] = \
                    app['object_store_urls']['google_play']
            elif platform == 'iOS':
                appinfo['appstore_link'] = app['object_store_urls']['itunes']
            else:
                raise

            aesample = appengagement.AppEngagementSample()

            r = aesample.app_engagement_ad_create(
                accountid,
                basename,
                message,
                imagefilepath,
                dailybudget,
                appinfo,
                bid_info[BidComponent.ID_OPTIMIZATION_GOAL],
                bid_info[BidComponent.ID_BILLING_EVENT],
                bid_info[BidComponent.ID_BID_AMOUNT],
                targeting
            )
            adlink = (
                'https://www.facebook.com/ads/manager/' + r['campaignid']
            )
            status = (
                'Campaign created: <a href="%s">%s</a>' %
                (adlink, r['campaignid'])
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
            os.remove(imagefilepath)
