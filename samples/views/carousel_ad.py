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

import os
from django import forms
from facebookads.objects import Campaign
from security.fbsample import fbads_sample
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect
from components.image_input import ImageInput
from components.targeting_spec import TargetingSpec
from components.page_select import PageSelect
from components.cta_select import CTASelect
from components.bid_component import BidComponent
from samples.samplecode import carousel_ad
from samples.views.sample import SampleBaseView


class CarouselAdForm(ComponentForm):
    ad_account = AdAccountSelect()
    pageid = PageSelect()
    bid = BidComponent('bid',
                       Campaign.Objective.link_clicks)

    name = forms.CharField(
        initial='Carousel Ads',
        widget=forms.TextInput(attrs={'placeholder': 'Campaign name'}))
    targeting_spec = TargetingSpec()
    site_link = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Link to your site'}))
    caption = forms.CharField(initial='Caption')
    message = forms.CharField(initial='Message')
    call_to_action_type = CTASelect()
    title = forms.CharField(initial='Title 1')
    title2 = forms.CharField(initial='Title 2')
    title3 = forms.CharField(initial='Title 3')

    body = forms.CharField(initial='Body 1')
    body2 = forms.CharField(initial='Body 2')
    body3 = forms.CharField(initial='Body 3')

    url = forms.URLField(
        widget=forms.TextInput(attrs={'placeholder': 'Item 1 link'}))
    url2 = forms.URLField(
        widget=forms.TextInput(attrs={'placeholder': 'Item 2 link'}))
    url3 = forms.URLField(
        widget=forms.TextInput(attrs={'placeholder': 'Item 3 link'}))

    image = ImageInput()
    image2 = ImageInput(id='id_image2')
    image3 = ImageInput(id='id_image3')


class CarouselAdView(SampleBaseView):

    BUTTON_TEXT = "Create Carousel Ad"

    @fbads_sample('samples.samplecode.carousel_ad')
    def get(self, request, *args, **kwargs):
        form = CarouselAdForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.carousel_ad')
    def post(self, request, *args, **kwargs):
        form = CarouselAdForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        status = ''
        """
            Convert some of the parameters
        """
        titles = [form.cleaned_data['title']]
        if form.cleaned_data['title2']:
            titles.append(form.cleaned_data['title2'])
        if form.cleaned_data['title3']:
            titles.append(form.cleaned_data['title3'])

        bodies = [form.cleaned_data['body']]
        if form.cleaned_data['body2']:
            bodies.append(form.cleaned_data['body2'])
        if form.cleaned_data['body3']:
            bodies.append(form.cleaned_data['body3'])

        urls = [form.cleaned_data['url']]
        if form.cleaned_data['url2']:
            urls.append(form.cleaned_data['url2'])
        if form.cleaned_data['url3']:
            urls.append(form.cleaned_data['url3'])

        image = self._handle_image_upload(request.FILES['image'])
        image_paths = [image]
        if form.cleaned_data['image2']:
            image2 = self._handle_image_upload(request.FILES['image2'])
            image_paths.append(image2)
        if form.cleaned_data['image3']:
            image3 = self._handle_image_upload(request.FILES['image3'])
            image_paths.append(image3)

        bid = form.cleaned_data['bid']
        optimization_goal = bid[BidComponent.ID_OPTIMIZATION_GOAL]
        billing_event = bid[BidComponent.ID_BILLING_EVENT]
        bid_amount = bid[BidComponent.ID_BID_AMOUNT]

        products = []
        num = min(len(urls), len(titles), len(bodies), len(image_paths))
        for i in range(num):
            products.append({
                'link': urls[i],
                'name': titles[i],
                'description': bodies[i],
                'image_path': image_paths[i]
            })
        sample = carousel_ad.CarouselAdSample()
        try:
            result = sample.create_carousel_ad(
                accountid=form.cleaned_data['ad_account'],
                page_id=form.cleaned_data['pageid'],
                site_link=form.cleaned_data['site_link'],
                caption=form.cleaned_data['caption'],
                message=form.cleaned_data['message'],
                optimization_goal=optimization_goal,
                billing_event=billing_event,
                bid_amount=bid_amount,
                name=form.cleaned_data['name'],
                targeting=form.cleaned_data['targeting_spec'],
                products=products,
                call_to_action_type=form.cleaned_data['call_to_action_type'],
            )
            ad_set = result[1]
            ad = result[2]
            ad_link = \
                'https://business.facebook.com/ads/manage/summary/' + \
                'adset/?ad_set_id=' + ad_set.get_id_assured() + \
                '&show_adgroup_id=' + ad.get_id_assured()
            status = ('Success. <a target="_blank" href="' +
                      ad_link + '">See created ad</a>' +
                      'Below is the preview of the ad you created:')

            data = {
                'ad_preview_dict': {
                    'ad_id': ad.get_id_assured(),
                    'ad_format': 'DESKTOP_FEED_STANDARD',
                }
            }

            return self.render_form_with_status(request, form, status, data)
        except:
            raise
        finally:
            """ Clean up the temp images """
            for image_path in image_paths:
                os.remove(image_path)
