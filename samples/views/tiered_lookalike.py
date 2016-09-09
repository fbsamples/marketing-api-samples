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
from components.custom_audience_select import CustomAudienceSelect
from components.image_input import ImageInput
from components.country_select import CountrySelect
from components.bid_component import BidComponent
from components.budget_type_select import BudgetTypeSelect
from components.datetime_picker import DatetimePicker
from samples.samplecode import tiered_lookalike
from security.fbsample import fbads_sample
from facebookads.objects import Campaign, AdPreview
import datetime
import os


class TieredLookalikeForm(ComponentForm):

    TOMORROW = datetime.date.today() + datetime.timedelta(days=1)

    ad_account = AdAccountSelect()

    CA_NAME_HELP_TEXT = 'This name will be used to create ' + \
        'the lookalike audiences.'
    CA_HELP_TEXT = 'Choose a existing custom audience id as the seed ' + \
        'for the lookalike audiences.'

    """
        Information for the uploaded custom audience
    """
    lookalike_audience_name = forms.CharField(
        max_length=50,
        help_text=CA_NAME_HELP_TEXT,
    )
    """
        Choose to create based on existing custom audience
    """
    seed_id = CustomAudienceSelect()

    NAME_HELP_TEXT = 'Name for the campaign and ads.'

    """
        Created lookalike campaign information
    """
    name = forms.CharField(
        initial='Tiered lookalikes',
        max_length=50,
        help_text=NAME_HELP_TEXT,
    )
    country = CountrySelect()
    bid_info = BidComponent('bid_info', Campaign.Objective.link_clicks)

    help_text = (
        '5 bid amounts will be generated between min and max bid. This will ' +
        'replace the bid amount you chose in the bid component above.'
    )
    bid_min = forms.IntegerField(initial=100, help_text=help_text)
    bid_max = forms.IntegerField(initial=500, help_text=help_text)

    budget_type = BudgetTypeSelect()
    budget = forms.IntegerField(initial=1000)

    start_time = DatetimePicker(id='id_starttime', initial=TOMORROW)
    end_time = DatetimePicker(id='id_endtime', required=False)

    title = forms.CharField(initial='Ad title')
    body = forms.CharField(initial='Ad body.')
    url = forms.URLField()
    image = ImageInput()


class TieredLookalikeView(SampleBaseView):

    BUTTON_TEXT = "Create Ads"

    @fbads_sample('samples.samplecode.tiered_lookalike')
    def get(self, request, *args, **kwargs):
        form = TieredLookalikeForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.tiered_lookalike')
    def post(self, request, *args, **kwargs):
        form = TieredLookalikeForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        # Get form parameters
        accountid = form.cleaned_data['ad_account']

        lookalike_audience_name = form.cleaned_data['lookalike_audience_name']
        seed_id = form.cleaned_data['seed_id']

        name = form.cleaned_data['name']
        country = form.cleaned_data['country']

        bid_info = form.cleaned_data['bid_info']
        optimization_goal = bid_info[BidComponent.ID_OPTIMIZATION_GOAL]
        billing_event = bid_info[BidComponent.ID_BILLING_EVENT]
        bid_min = form.cleaned_data['bid_min']
        bid_max = form.cleaned_data['bid_max']

        daily_budget = None
        lifetime_budget = None
        if form.cleaned_data['budget_type'] == 'daily_budget':
            daily_budget = form.cleaned_data['budget']
        else:
            lifetime_budget = form.cleaned_data['budget']

        start_time = form.cleaned_data['start_time']
        end_time = None
        if form.cleaned_data['end_time']:
            end_time = form.cleaned_data['end_time'].strftime('%s')

        title = form.cleaned_data['title']
        body = form.cleaned_data['body']
        url = form.cleaned_data['url']
        image_path = self._handle_image_upload(form.cleaned_data['image'])

        # Create 5 tiers
        TIERS = 5
        caid = seed_id

        # Make corresponding bidding info objects
        bid_amounts = []
        bid_interval = (bid_max - bid_min) / (TIERS - 1)
        for tier in range(1, TIERS + 1):
            bid_amount = bid_max - bid_interval * (tier - 1)
            bid_amounts.append(bid_amount)

        """
            Lookalike audiences are ready, move on to ad creation
        """
        try:
            # Create lookalike audiences from the source
            tiered_sample = tiered_lookalike.TieredLookalikeSample()
            tiered_audiences = tiered_sample.create_tiered_lookalikes(
                accountid,
                lookalike_audience_name,
                caid,
                TIERS,
                country
            )

            # Create the ads
            results = tiered_sample.create_lookalike_ads(
                accountid,
                name,

                tiered_audiences,
                optimization_goal,
                billing_event,
                bid_amounts,

                title,
                body,
                url,
                image_path,

                daily_budget,
                lifetime_budget,
                start_time,
                end_time
            )
            # Success!
            campaign_id = str(results['adsets'][0]['campaign_id'])
            ad_id = results['ads'][0]['id']

            ads_manager_link = \
                'https://business.facebook.com/ads/manage/summary/' + \
                'campaign/?campaign_id={}'.format(campaign_id)
            status = 'Created {0} tiered ad sets. See the campaign at ' + \
                '<a target="_blank" href="{1}">{2}</a>. ' + \
                'Here is the preview for one of the ads:'
            status = status.format(
                len(results['adsets']),
                ads_manager_link,
                campaign_id,
            )
            data = {
                'ad_preview_dict': {
                    'ad_id': ad_id,
                    'ad_format': AdPreview.AdFormat.right_column_standard,
                }
            }
            return self.render_form_with_status(request, form, status, data)
        except:
            raise
        finally:
            """ Clean up the temp images """
            os.remove(image_path)
