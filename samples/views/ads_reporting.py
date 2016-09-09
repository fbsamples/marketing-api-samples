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

from samples.views.sample import SampleBaseView
from samples.samplecode import ads_reporting
from security.fbsample import fbads_sample
from components.component_form import ComponentForm
from components.datetime_picker import DatetimePicker
from components.ad_account_select import AdAccountSelect
import datetime


class AdsReportingForm(ComponentForm):

    ad_account = AdAccountSelect()
    LAST_90_DAYS = datetime.date.today() - datetime.timedelta(days=90)
    TODAY = datetime.date.today()

    report_date = DatetimePicker(
        id='id_reportdate',
        initial=TODAY.strftime('%Y-%m-%d'),
        datetime_format='YYYY-MM-DD',
        min_date=LAST_90_DAYS.strftime('%Y-%m-%d'),
        max_date=TODAY.strftime('%Y-%m-%d'),
        help_text='Date between last 90 days and today',
    )


class AdsReportingView(SampleBaseView):

    TEMPLATE = 'samples/ads_reporting_form.html'

    @fbads_sample('samples.samplecode.ads_reporting')
    def get(self, request, *args, **kwargs):
        form = AdsReportingForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.ads_reporting')
    def post(self, request, *args, **kwargs):
        form = AdsReportingForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        # Get form parameters
        account_id = form.cleaned_data['ad_account']
        report_date = form.cleaned_data['report_date'].strftime('%Y-%m-%d')

        # Get ads reporting
        ar_sample = ads_reporting.AdsReportingSample()
        ar = ar_sample.get_ads_insight(
            account_id,
            report_date,
        )
        status = ''
        if len(ar) <= 0:
            status = 'No data in the selected time span.'

        return self.render_form_with_status(
            request,
            form,
            status,
            {'ads_reports': ar})
