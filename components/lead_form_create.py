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
from django.forms import CharField


class LeadFormCreate(CharField):
    """
    Component for creating or selecting a lead gen form. This component is used
    for creating [Lead Ads][1] or downloading the lead data from a lead ad. The
    component will have a button to trigger a popup window where you can choose
    from a list of forms loaded via AJAX, or create a new one using the create
    flow available from [Facebook JS SDK][2].

    [1]: https://developers.facebook.com/docs/marketing-api/guides/lead-ads/
    [2]: https://developers.facebook.com/docs/javascript
    """

    def __init__(
        self,
        id='id_lead_form',
        id_page_select='id_page_select',
        *args,
        **kwargs
    ):
        super(LeadFormCreate, self).__init__(*args, **kwargs)

        self.id = id
        if not self.help_text:
            self.help_text = ("Choose a Page before using.")

        self.widget = ReactModalWidget(attrs={
            'id': self.id,
            'js_params': [id_page_select],
            'icon': "glyphicon glyphicon-list-alt",
            'js_module': 'lead_form',
            'js_class': 'LeadForm',
        })
