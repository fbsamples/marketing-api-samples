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

import datetime
import os
from django import forms
from facebookads.objects import Campaign
from samples.samplecode import adcreation
from security.fbsample import fbads_sample
from samples.views.sample import SampleBaseView
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect
from components.bid_component import BidComponent
from components.datetime_picker import DatetimePicker
from components.image_input import ImageInput
from components.page_select import PageSelect
from components.targeting_spec import TargetingSpec


class AdCreationForm(ComponentForm):

    ad_account = AdAccountSelect()
    page = PageSelect()
    name = forms.CharField(initial='Creative Testing')

    GENDERS_CHOICES = (
        ('0', 'All'),
        ('1', 'Male'),
        ('2', 'Female'),
    )

    bid = BidComponent('bid',
                       Campaign.Objective.link_clicks)

    targeting = TargetingSpec()

    TOMORROW = datetime.date.today() + datetime.timedelta(days=1)

    start_time = DatetimePicker(
        id='id_starttime',
        initial=TOMORROW,
        required=False,
    )
    end_time = DatetimePicker(id='id_endtime', required=False)

    url = forms.URLField(
        widget=forms.TextInput(attrs={'placeholder': 'Link'}))
    title = forms.CharField(initial='Title 1')
    title2 = forms.CharField(initial='Title 2')
    body = forms.CharField(initial='Body 1')
    body2 = forms.CharField(initial='Body 2')
    image = ImageInput()
    image2 = ImageInput(id="id_image2")
    image3 = ImageInput(id="id_image3")


class AdCreationView(SampleBaseView):

    BUTTON_TEXT = "Create Ads"

    @fbads_sample('samples.samplecode.adcreation')
    def get(self, request, *args, **kwargs):
        form = AdCreationForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.adcreation')
    def post(self, request, *args, **kwargs):
        form = AdCreationForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        status = ''

        """
            Convert some of the parameters
        """
        bid = form.cleaned_data['bid']
        optimization_goal = bid[BidComponent.ID_OPTIMIZATION_GOAL]
        billing_event = bid[BidComponent.ID_BILLING_EVENT]
        bid_amount = bid[BidComponent.ID_BID_AMOUNT]
        end_time = None
        if form.cleaned_data['end_time']:
            end_time = form.cleaned_data['end_time'].strftime('%s')

        targeting = form.cleaned_data['targeting']

        titles = [form.cleaned_data['title']]
        if form.cleaned_data['title2']:
            titles.append(form.cleaned_data['title2'])
        bodies = [form.cleaned_data['body']]
        if form.cleaned_data['body2']:
            bodies.append(form.cleaned_data['body2'])

        urls = [form.cleaned_data['url']]

        image = self._handle_image_upload(request.FILES['image'])
        image_paths = [image]
        if form.cleaned_data['image2']:
            image2 = self._handle_image_upload(request.FILES['image2'])
            image_paths.append(image2)
        if form.cleaned_data['image3']:
            image3 = self._handle_image_upload(request.FILES['image3'])
            image_paths.append(image3)

        sample = adcreation.AdCreationSample()
        try:
            result = sample.create_multiple_link_clicks_ads(
                accountid=form.cleaned_data['ad_account'],
                pageid=form.cleaned_data['page'],
                name=form.cleaned_data['name'],
                titles=titles,
                bodies=bodies,
                urls=urls,
                image_paths=image_paths,
                targeting=targeting,
                optimization_goal=optimization_goal,
                billing_event=billing_event,
                bid_amount=bid_amount,
                daily_budget=(int(bid_amount) * 10),
                lifetime_budget=None,
                start_time=form.cleaned_data['start_time'].strftime('%s'),
                end_time=end_time,
            )
        except:
            raise
        else:
            adset = result[1]
            ads_created = result[2]
            adset_id = adset.get_id_assured()
            ad_id = ads_created[0]['id']
            adset_link = \
                'https://business.facebook.com/ads/manager/adset/' + \
                'ads/?ids=' + adset_id
            ad_link = \
                'https://business.facebook.com/ads/manager/ad/' + \
                'ads/?ids=' + ad_id
            status = \
                'Created ' + str(len(ads_created)) + ' ads for Ad Set ' + \
                '<a href="' + adset_link + '">' + adset_id + '</a>. ' + \
                'Below is the preview for one of them (' + \
                '<a href="' + ad_link + '">' + ad_id + '</a>)'
            data = {
                'ad_preview_dict': {
                    'ad_id': ad_id,
                    'ad_format': 'DESKTOP_FEED_STANDARD',
                }
            }
            return self.render_form_with_status(request, form, status, data)
        finally:
            """ Clean up the temp images """
            for image_path in image_paths:
                os.remove(image_path)
