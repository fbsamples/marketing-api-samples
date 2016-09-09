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
from django.core.exceptions import ValidationError
from security.fbsample import fbads_sample
from components.app_select import AppSelect
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect
from samples.samplecode import maca_cumulative
from samples.views.sample import SampleBaseView


PERIOD_CHOICES = (
    ('1d', '1 day'),
    ('7d', '7 days'),
    ('28d', '28 days'),
)

EVENT_CHOICES = (
    ('fb_mobile_add_to_cart', 'Add to Cart'),
    ('fb_mobile_purchase', 'Purchase'),
)

GREATER_THAN_HELP = 'Specify the minimal value, default to negative infinity'
LESS_THAN_HELP = 'Specify the maximal value, default to positive infinity'
PERIOD_HELP = 'The time period you want to calculate the cumulative value'
RETENTION_HELP = 'How long do you want to keep people in the audience, 180 max'


def validate_retention_days(value):
    if value < 1 or value > 180:
        raise ValidationError('Retention days should be between 1 to 180 days')


class MacaCumulativeForm(ComponentForm):
    ad_account = AdAccountSelect()
    app = AppSelect()
    name = forms.CharField(initial='Test Mobile App Custom Audience')
    retention_days = forms.IntegerField(
        help_text=RETENTION_HELP,
        initial=180,
        validators=[validate_retention_days])
    event = forms.ChoiceField(choices=EVENT_CHOICES)
    period = forms.ChoiceField(choices=PERIOD_CHOICES, help_text=PERIOD_HELP)
    greater_than = forms.IntegerField(
        help_text=GREATER_THAN_HELP,
        required=False)
    less_than = forms.IntegerField(
        help_text=LESS_THAN_HELP,
        required=False)


class MacaCumulativeView(SampleBaseView):

    BUTTON_TEXT = "Create Mobile App Custom Audience"

    @fbads_sample('samples.samplecode.maca_cumulative')
    def get(self, request, *args, **kwargs):
        form = MacaCumulativeForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.maca_cumulative')
    def post(self, request, *args, **kwargs):
        form = MacaCumulativeForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        status = ''
        """
        Convert some of the parameters
        """
        accountid = form.cleaned_data['ad_account']
        app = form.cleaned_data['app']
        app_id = app['id']

        sample = maca_cumulative.MacaCumulativeSample()

        result = sample.create_audience(
            accountid=accountid,
            app_id=app_id,
            name=form.cleaned_data['name'],
            retention_days=form.cleaned_data['retention_days'],
            event=form.cleaned_data['event'],
            period=form.cleaned_data['period'],
            greater_than=form.cleaned_data['greater_than'],
            less_than=form.cleaned_data['less_than'],
        )
        ca_link = (
            'https://business.facebook.com/ads/manager/audiences/detail/' +
            '?act={0}&ids={1}'
        ).format(accountid.replace('act_', ''), result)

        status = ('Success. Created custom audience: <a target="_blank" ' +
                  'href={0}>{1}</a>').format(ca_link, result)

        return self.render_form_with_status(request, form, status)
