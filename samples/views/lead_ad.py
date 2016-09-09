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
from samples.views.sample import SampleBaseView
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect
from components.page_select import PageSelect
from components.lead_form_create import LeadFormCreate
from components.targeting_spec import TargetingSpec
from components.image_input import ImageInput
from components.bid_component import BidComponent
from security.fbsample import fbads_sample
from samples.samplecode import lead_ad
from facebookads.objects import Campaign

targeting_info_initial = TargetingSpec.US_ANDROID_MOBILEFEED


class LeadAdForm(ComponentForm):

    ad_account = AdAccountSelect()
    page = PageSelect()
    lead_form = LeadFormCreate()
    name = forms.CharField(initial='My First Lead Ad')
    targeting = TargetingSpec(initial=targeting_info_initial)
    bid_info = BidComponent('bid_info',
                            Campaign.Objective.lead_generation)
    daily_budget = forms.DecimalField(
        min_value=1,
        initial='500',
    )
    image = ImageInput(
        allow_empty_file=False, required=True,
    )
    message = forms.CharField(initial='My First Lead Ad')
    link = forms.CharField()
    caption = forms.CharField()
    description = forms.CharField()


class LeadAdView(SampleBaseView):

    @fbads_sample('samples.samplecode.lead_ad')
    def get(self, request, *args, **kwargs):
        form = LeadAdForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.lead_ad')
    def post(self, request, *args, **kwargs):
        form = LeadAdForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        account_id = form.cleaned_data['ad_account']

        bid_info = form.cleaned_data['bid_info']
        optimization_goal = bid_info[BidComponent.ID_OPTIMIZATION_GOAL]
        billing_event = bid_info[BidComponent.ID_BILLING_EVENT]
        bid_amount = bid_info[BidComponent.ID_BID_AMOUNT]

        targeting = form.cleaned_data['targeting']

        image_path = self._handle_image_upload(request.FILES['image'])

        sample = lead_ad.LeadAdSample()

        try:
            result = sample.create_lead_ad(
                account_id=account_id,
                name=form.cleaned_data['name'],
                page_id=form.cleaned_data['page'],
                form_id=form.cleaned_data['lead_form'],
                optimization_goal=optimization_goal,
                billing_event=billing_event,
                bid_amount=bid_amount,
                daily_budget=form.cleaned_data['daily_budget'],
                targeting=targeting,
                image_path=image_path,
                message=form.cleaned_data['message'],
                link=form.cleaned_data['link'],
                caption=form.cleaned_data['caption'],
                description=form.cleaned_data['description'])

            adlink = (
                'https://www.facebook.com/ads/manager/' + result['campaign_id']
            )
            status = (
                'Campaign created: <a target="_blank" href="%s">%s</a>' %
                (adlink, result['campaign_id'])
            )
            data = {
                'ad_preview_dict': {
                    'ad_id': result['ad_id'],
                    'ad_format': 'MOBILE_FEED_STANDARD',
                }
            }
            return self.render_form_with_status(request, form, status, data)
        except:
            raise
        finally:
            """ Clean up the temp images """
            os.remove(image_path)
