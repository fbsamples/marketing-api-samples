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


class AppSelect(JsonCharField):
    """
    Component for selecting application. It renders a button on the input that
    triggers a pop up window to let user select an application that they own,
    and return a JSON string about the selected app that goes like this:

        {
            "id": "12345",
            "name": "My Android App",
            "url": "https://www.facebook.com/games/?app_id=12345",
            "picture": "https://someimagehost.com/your.png",
            "supported_platforms": [6],
            "native_app_store_ids": {
                "6": "com.my.app"
            },
            "object_store_urls": {
                "google_play":
                    "http://play.google.com/store/apps/details?id=com.my.app"
            }
        }
    """

    def __init__(
        self,
        id='id_app_select',
        id_act_select='id_act_select',
        *args,
        **kwargs
    ):
        super(AppSelect, self).__init__(*args, **kwargs)

        if not self.help_text:
            self.help_text = ("Choose an ad account before using. Changing " +
                              "ad account will reset the selection.")

        self.id = id
        self.widget = ReactModalWidget(attrs={
            'id': self.id,
            'js_module': 'app_select',
            'js_class': 'AppSelect',
            'js_params': [id_act_select],
            'icon': "glyphicon glyphicon-plus"
        })
