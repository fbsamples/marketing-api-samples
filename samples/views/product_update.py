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
from samples.samplecode.product_update import ProductUpdateSample
from security.fbsample import fbads_sample
from components.component_form import ComponentForm
from components.business_manager_select import BusinessManagerSelect
from components.product_catalog_select import ProductCatalogSelect
from components.product_select import ProductSelect
import logging

logger = logging.getLogger(__name__)


class ProductUpdateForm(ComponentForm):

    business_id = BusinessManagerSelect()
    catalog_id = ProductCatalogSelect()
    retailer_id = ProductSelect()
    choices_availability = (
        ('IN_STOCK', 'in stock'),
        ('PREORDER', 'preorder'),
        ('AVAILABLE_FOR_ORDER', 'available for order'),
        ('OUT_OF_STOCK', 'out of stock')
    )
    availability = forms.ChoiceField(choices=choices_availability)


class ProductUpdateView(SampleBaseView):

    BUTTON_TEXT = "Update Product"

    @fbads_sample('samples.samplecode.product_update')
    def get(self, request, *args, **kwargs):
        form = ProductUpdateForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.product_update')
    def post(self, request, *args, **kwargs):
        form = ProductUpdateForm(request.POST, request.FILES)
        status = ''
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        # Get form parameters
        catalog_id = form.cleaned_data['catalog_id']
        retailer_id = form.cleaned_data['retailer_id']
        availability = form.cleaned_data['availability']

        product_update = ProductUpdateSample()
        result = product_update.update_product_item_by_retailer_id(
            catalog_id,
            retailer_id,
            {
                'availability': availability
            }
        )
        if result.is_success:
            status = 'SUCCESS'

        return self.render_form_with_status(request, form, status)
