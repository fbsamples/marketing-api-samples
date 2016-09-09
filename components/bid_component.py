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
from django.forms import widgets
from widgets import ReactModalWidget


class BidWidget(widgets.MultiWidget):

    def decompress(self, value):
        return ['', '', 100]


class BidComponent(forms.MultiValueField):
    """
    Component for setting your bids. The component will have a button to open a
    popup window where you can input your optimization goal, billing event and
    bid amount. The output of this component will be a JSON object.
    """

    # Constants for list access
    ID_OPTIMIZATION_GOAL = 0
    ID_BILLING_EVENT = 1
    ID_BID_AMOUNT = 2

    def __init__(
        self,
        field_name,
        objective='',
        id='id_bid_component',
        *args,
        **kwargs
    ):
        fields = [
            forms.CharField(),
            forms.CharField(),
            forms.CharField()
        ]
        super(BidComponent, self).__init__(fields=fields, *args, **kwargs)

        self.id = id
        if not self.help_text:
            self.help_text = ("Click to open dialog for bidding options.")

        optimization_goal = forms.HiddenInput()
        billing_event = forms.HiddenInput()
        bid_amount = forms.HiddenInput()
        widgets = [
            optimization_goal,
            billing_event,
            bid_amount,
            ReactModalWidget(attrs={
                'id': self.id,
                'js_params': [field_name, objective],
                'icon': "glyphicon glyphicon-plus",
                'js_module': 'bid_component',
                'js_class': 'BidComponent',
            })
        ]
        self.widget = BidWidget(widgets=widgets)

    def compress(self, values):
        return values
