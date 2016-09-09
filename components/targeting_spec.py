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

from widgets import ReactModalWidget
from json_char_field import JsonCharField
import json


class TargetingSpec(JsonCharField):
    """
    Component for setting [Targeting Specs][1]. This component will render
    a button that will toggle the targeting spec composer popup window.
    The output is the targeting spec JSON data.

    [1]: https://developers.facebook.com/docs/marketing-api/targeting-specs/
    """

    """
    Some sample targeting specs
    """
    US_ANDROID_MOBILEFEED = {
        'geo_locations': {
            'countries': ['US'],
        },
        'user_os': ['Android'],
        'device_platforms': ['mobile'],
        'publisher_platforms': ['facebook', 'audience_network']
    }

    def __init__(
        self,
        id='id_targeting_spec',
        id_act_select='id_act_select',
        *args,
        **kwargs
    ):
        super(TargetingSpec, self).__init__(*args, **kwargs)

        self.id = id
        if not self.help_text:
            self.help_text = ("Choose an ad account before using. Changing " +
                              "ad account will reset the current spec.")

        self.widget = ReactModalWidget(attrs={
            'id': self.id,
            'js_params': [id_act_select],
            'icon': "glyphicon glyphicon-plus",
            'js_module': 'targeting_spec',
            'js_class': 'TargetingSpec',
            'data-toggle': 'tooltip',
            'title': 'Choose an ad account before using.',
        })
