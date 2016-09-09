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

import re
import datetime
from django import forms
from django.http import StreamingHttpResponse
from django.template import loader, RequestContext
from samples.samplecode import orderlevelreporting
from security.fbsample import fbads_sample
from samples.views.sample import SampleBaseView
from components.component_form import ComponentForm
from components.datetime_picker import DatetimePicker
from components.business_manager_select import BusinessManagerSelect


class OrderLevelReportingForm(ComponentForm):

    YESTERDAY = datetime.date.today() + datetime.timedelta(days=-1)

    business_id = BusinessManagerSelect(
        required=True,
    )

    start_time = DatetimePicker(
        id='id_starttime',
        initial=YESTERDAY,
        required=True,
    )

    end_time = DatetimePicker(
        id='id_endtime',
        initial=datetime.date.today(),
        required=True,
    )

    pixel_id = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'number'}),
        required=False,
    )

    app_id = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'number'}),
        required=False,
    )

    format = forms.ChoiceField(initial='html', choices=(
        ('html', 'Preview (Opens in New Tab)', ),
        ('xls', 'Excel Report (.xls)', ),
        ('csv', 'Comma-Separated Values (.csv)', ),
    ),
    )


class OrderLevelReportingView(SampleBaseView):

    BUTTON_TEXT = "Get Report"
    BUTTON_TARGET = '_blank'

    @fbads_sample('samples.samplecode.orderlevelreporting')
    def get(self, request, *args, **kwargs):
        form = OrderLevelReportingForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.orderlevelreporting')
    def post(self, request, *args, **kwargs):

        form = OrderLevelReportingForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        format = re.sub("[^a-z]", "", form.cleaned_data['format'])
        download = format != 'html'

        business_id = re.sub("[^0-9]", "", form.cleaned_data['business_id'])

        pixel_id = re.sub("[^0-9]", "", form.cleaned_data['pixel_id'])
        app_id = re.sub("[^0-9]", "", form.cleaned_data['app_id'])

        from_date = form.cleaned_data['start_time']
        to_date = form.cleaned_data['end_time']

        sample = orderlevelreporting.OrderLevelReportingSample()

        # First try to call the API on this thread to check for errors
        # so that they can be bubbled up to the UI (invalid pixel_id etc.)
        list(sample.retrieve_order_level_report_data(
            from_date=from_date,
            to_date=to_date,
            business_id=business_id,
            pixel_id=pixel_id,
            app_id=app_id,
            limit=0,
        ))

        # And if we didn't raise an exception, start to stream it out
        rowsets_generator = sample.retrieve_order_level_report_data_parallel(
            from_date=from_date,
            to_date=to_date,
            business_id=business_id,
            pixel_id=pixel_id,
            app_id=app_id,
        )

        stream = self.stream_rowsets_to_templates(
            format=format,
            rowsets=rowsets_generator,
            context=RequestContext(request, {
                'pixel_id': pixel_id,
                'app_id': app_id,
                'business_id': business_id,
                'from_date': from_date,
                'to_date': to_date,
                'num_rows': 0,
                'num_outline_rows': 0,
                'cumulative_num_rows': 0,
                'cumulative_num_outline_rows': 0,
            }),
        )

        response = StreamingHttpResponse(
            stream,
            content_type={
                'html': 'text/html',
                'xls': 'application/xml',
                'csv': 'text/csv',
            }[format],
            )

        if download:
            response['Content-Disposition'] = (
                'attachment; filename="' +
                '_'.join(filter(None, (
                    'report',
                    business_id,
                    pixel_id,
                    app_id,
                ))) + '.' + format + '"'
            )
        return response

    def stream_rowsets_to_templates(
        self,
        format,
        context,
        rowsets,
        preview_limit=10,
    ):
        header_template = loader.get_template(
            'samples/order_level_report.header.' + format,
        )

        yield header_template.render(context)

        rows_template = loader.get_template(
            'samples/order_level_report.row.' + format,
        )

        for rowset in rowsets:

            total_num_rows = context['cumulative_num_rows']

            rows_left_in_preview = max(preview_limit - total_num_rows, 0)
            context['preview_slice'] = ':' + str(rows_left_in_preview)

            num_rows = len(rowset)

            context['data'] = rowset
            context['num_rows'] = num_rows
            context['cumulative_num_rows'] += num_rows

            num_outline_rows = reduce(
                lambda accum, x: accum + max(len(x['attributions']), 1),
                rowset,
                0,
            )

            context['num_outline_rows'] = num_outline_rows
            context['cumulative_num_outline_rows'] += num_outline_rows

            yield rows_template.render(context)

        footer_template = loader.get_template(
            'samples/order_level_report.footer.' + format,
        )

        yield footer_template.render(context)
