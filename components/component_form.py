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


class ComponentForm(forms.Form):
    """
    Holds the logic that should be used form wide, for example form wide
    validations etc.
    """
    def validate_mobile_platform_targeting(
        self,
        app='app',
        platform='platform',
        targeting='targeting'
    ):
        """
        Form wide validation to check if selected [mobile] app, platform and
        targeting (device OS and placement) are matched. Call this method if you
        are creating a mobile ad sample. Pass in the names for the AppSelect,
        platform select (value should be either 'iOS' or 'Android') and
        TargetingSpec. Call this method in your Form's clean method.
        """
        cleaned_data = super(ComponentForm, self).clean()

        platform_selected = cleaned_data.get(platform)
        app_data = cleaned_data.get(app)
        targeting_spec = cleaned_data.get(targeting)

        if not (platform_selected and app_data and targeting_spec):
            return cleaned_data

        if 'object_store_urls' not in app_data:
            raise ValidationError(u"Invalid app info: %s" % app_data)

        store_urls = app_data['object_store_urls']

        store_url = ''

        # Check if platform selected is valid against app platform
        if ((platform_selected == 'Android' and 'google_play' not in store_urls)
                or (platform_selected == 'iOS' and 'itunes' not in store_urls)):
            raise ValidationError(u"Your app doesn't support selected " +
                                  "platform: %s" % platform_selected)

        # Check if platform selected is matching with the targeting spec
        if 'user_os' not in targeting_spec:
            raise ValidationError(u'You need to specify mobile os in targeting')
        if len(targeting_spec['user_os']) > 1:
            raise ValidationError(u'You can only select one mobile os in ' +
                                  'targeting')
        if targeting_spec['user_os'][0] != platform_selected:
            raise ValidationError(u'Platform selected needs to match that in ' +
                                  'targeting setting')

        # Check if placement is mobile. This will default to 'mobile' if user_os
        # was specified so it's OK to be empty
        if (
            'device_platforms' in targeting_spec and
            'mobile' not in targeting_spec['device_platforms']
        ):
            raise ValidationError(u'You need to select mobile in ' +
                                  'device platforms')

        if platform_selected == 'Android':
            store_url = store_urls['google_play']
        elif platform_selected == 'iOS':
            store_url = store_urls['itunes']

        cleaned_data['store_url'] = store_url
        self.cleaned_data = cleaned_data

        return self.cleaned_data
