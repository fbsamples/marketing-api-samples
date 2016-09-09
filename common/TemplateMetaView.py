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

from django.views.generic import TemplateView
from seo_meta import meta


class TemplateMetaView(TemplateView):
    # override these parameters at urls.py
    seo_title = 'Facebook Marketing API Accelerator'
    seo_description = 'The Facebook Marketing API Accelerator is your path ' \
                      'to serious ads API skills and significant ' \
                      'technical developer support.'
    seo_image = '/static/images/fmd.jpg'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TemplateMetaView, self).get_context_data(**kwargs)

        meta.title = self.seo_title
        meta.description = self.seo_description
        meta.image = self.seo_image
        context['meta'] = meta

        return context
