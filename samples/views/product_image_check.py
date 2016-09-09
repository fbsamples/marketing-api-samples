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
from samples.views.sample import SampleBaseView
from samples.samplecode.product_image_check import DPAImageCheckSample
from security.fbsample import fbads_sample
from components.component_form import ComponentForm
from components.business_manager_select import BusinessManagerSelect
from components.product_catalog_select import ProductCatalogSelect
import logging

logger = logging.getLogger(__name__)


class ProductImageCheckForm(ComponentForm):

    business_id = BusinessManagerSelect()
    catalog_id = ProductCatalogSelect()
    limit = forms.DecimalField(
        label="How many products to check. The more you pick, the longer it " +
        "will take.",
        min_value=1,
        max_value=100,
        required=True,
        initial=10
    )


class ProductImageCheckView(SampleBaseView):

    BUTTON_TEXT = "Check Product Images"

    @fbads_sample('samples.samplecode.product_image_check')
    def get(self, request, *args, **kwargs):
        form = ProductImageCheckForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.product_image_check')
    def post(self, request, *args, **kwargs):
        form = ProductImageCheckForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        # Get form parameters
        catalog_id = form.cleaned_data['catalog_id']
        limit = form.cleaned_data['limit']
        image_check = DPAImageCheckSample()
        result = image_check.check_product_images(
            catalog_id,
            limit
        )
        total_count = result[0]
        image_ok_count = result[1]
        image_not_ok_count = total_count - image_ok_count
        additional_image_ok_count = result[2]
        small_images = result[3]

        self.TEMPLATE = 'samples/product_image_check.html'
        data = {
            'total_count': total_count,
            'image_ok_count': image_ok_count,
            'image_not_ok_count': image_not_ok_count,
            'additional_image_ok_count': additional_image_ok_count,
            'small_images_count': len(small_images),
            'small_images': small_images,
        }
        if total_count > 0:
            data.update({
                'image_ok_percent':
                round(image_ok_count * 100.0 / total_count, 1),
                'image_not_ok_percent':
                round(image_not_ok_count * 100.0 / total_count, 1),
            })
        return self.render_form_with_status(
            request,
            form,
            'msg',
            data
        )
