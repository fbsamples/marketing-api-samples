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
from widgets import SelectizeWidget


class CTASelect(forms.CharField):
    """
    Call To Action select component that makes use of the selectize widget.
    It contains a dropdown list of CTA types.
    Find all CTA types at:
    https://developers.facebook.com/docs/marketing-api/unpublished-page-posts/v2.5#cta-spec
    """
    DEFAULT_CHOICES = [
        ('NO_BUTTON', 'NO BUTTON'),
        ('BOOK_TRAVEL', 'BOOK TRAVEL'),
        ('BUY_NOW', 'BUY NOW'),
        ('CALL_NOW', 'CALL NOW'),
        ('DOWNLOAD', 'DOWNLOAD'),
        ('GET_DIRECTIONS', 'GET DIRECTIONS'),
        ('GET_QUOTE', 'GET QUOTE'),
        ('INSTALL_APP', 'INSTALL APP'),
        ('LEARN_MORE', 'LEARN MORE'),
        ('LIKE_PAGE', 'LIKE PAGE'),
        ('PLAY_GAME', 'PLAY GAME'),
        ('SHOP_NOW', 'SHOP NOW'),
        ('SIGN_UP', 'SIGN UP'),
        ('SUBSCRIBE', 'SUBSCRIBE'),
        ('USE_APP', 'USE APP'),
        ('WATCH_VIDEO', 'WATCH VIDEO'),
    ]

    def __init__(
        self,
        id='cta_select',
        *args,
        **kwargs
    ):
        super(CTASelect, self).__init__(*args, **kwargs)
        self.id = id
        self.widget = SelectizeWidget(
            attrs={
                'id': self.id,
            },
            choices=self.DEFAULT_CHOICES,
        )
