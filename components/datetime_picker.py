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

from django.forms import DateTimeField
from widgets import DatetimePickerWidget


class DatetimePicker(DateTimeField):
    """
    A user friendly date time picker component, using the [bootstrap datetime
    picker plugin][1].
    You can specify your custom datetime format that the plugin shows by setting
    the `datetime_format` variable. For the datetime formats see the [custom
    formats][2]

    [1]: https://eonasdan.github.io/bootstrap-datetimepicker/
    [2]: https://eonasdan.github.io/bootstrap-datetimepicker/#custom-formats
    """

    def __init__(
        self,
        id='id_datetime',
        datetime_format='YYYY-MM-DD HH:mm',
        min_date=None,
        max_date=None,
        *args,
        **kwargs
    ):
        super(DatetimePicker, self).__init__(*args, **kwargs)

        js_params = [datetime_format]
        if min_date is not None:
            js_params.append(min_date)
        if max_date is not None:
            js_params.append(max_date)
        self.id = id
        self.widget = DatetimePickerWidget(attrs={
            'id': self.id,
            'js_params': js_params,
            'js_module': 'datetime_picker',
            'js_class': 'DatetimePicker',
        })
