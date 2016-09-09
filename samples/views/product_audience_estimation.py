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

from samples.views.sample import SampleBaseView
from components.component_form import ComponentForm
from components.business_manager_select import BusinessManagerSelect
from components.ad_account_select import AdAccountSelect
from components.product_catalog_select import ProductCatalogSelect
from components.product_set_select import ProductSetSelect
from components.spec_select import SpecSelect
from samples.samplecode import product_audience_estimation
from security.fbsample import fbads_sample
import json


TARGETING_SPECS = [
    {
        'id': '30-day-viewcontent',
        'name': 'who triggers ViewContent in past 30 days',
        'spec': '''
{
    "inclusions": [
        {
            "retention_seconds": "2592000",
            "rule": "{\\"event\\":{\\"eq\\":\\"ViewContent\\"}}"
        }
    ]
}'''
    },
    {
        'id': '60-day-purchase',
        'name': 'who triggers Purchase in past 60 days',
        'spec': '''
{
    "inclusions": [
        {
            "retention_seconds": "5184000",
            "rule": "{\\"event\\":{\\"eq\\":\\"Purchase\\"}}"
        }
    ]
}'''
    },
    {
        'id': '60-day-viewcontent-and-30-day-addtocart',
        'name': ('who triggers ViewContent in past 60 days ' +
                 'and AddToCart in past 30 days'),
        'spec': '''
{
    "inclusions": [
        {
            "retention_seconds": "5184000",
            "rule": "{\\"event\\":{\\"eq\\":\\"ViewContent\\"}}"
        },
        {
            "retention_seconds": "2592000",
            "rule": "{\\"event\\":{\\"eq\\":\\"AddToCart\\"}}"
        }
    ]
}'''
    },
    {
        'id': '60-day-viewcontent-but-no-purchase',
        'name': 'who triggers ViewContent in past 60 days but not yet purcahse',
        'spec': '''
{
    "inclusions": [
        {
            "retention_seconds": "5184000",
            "rule": "{\\"event\\":{\\"eq\\":\\"ViewContent\\"}}"
        }
    ],
    "exclusions": [
        {
            "retention_seconds": "5184000",
            "rule": "{\\"event\\":{\\"eq\\":\\"Purchase\\"}}"
        }
    ]
}'''
    }
]


class ProductAudienceEstimationForm(ComponentForm):

    ad_account = AdAccountSelect()
    business_manager = BusinessManagerSelect()
    product_catalog = ProductCatalogSelect()
    product_set = ProductSetSelect()
    targeting_spec = SpecSelect(specs=TARGETING_SPECS)

    def clean(self):
        self.cleaned_data = super(ProductAudienceEstimationForm, self).clean()

        self.cleaned_data = \
            super(ProductAudienceEstimationForm,
                  self).validate_mobile_platform_targeting()

        return self.cleaned_data


class ProductAudienceEstimationView(SampleBaseView):

    TEMPLATE = 'samples/product_audience_estimation_form.html'

    @fbads_sample('samples.samplecode.product_audience_estimation')
    def get(self, request, *args, **kwargs):
        form = ProductAudienceEstimationForm(request.last_error_post)
        return self.render_form(request, form)

    @fbads_sample('samples.samplecode.product_audience_estimation')
    def post(self, request, *args, **kwargs):
        form = ProductAudienceEstimationForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_invalid_form(request, form)

        accountid = form.cleaned_data['ad_account']
        productsetid = form.cleaned_data['product_set']
        targetingspec_index = form.cleaned_data['targeting_spec']
        targetingspec = json.loads(TARGETING_SPECS[targetingspec_index]['spec'])

        try:
            p = product_audience_estimation.ProductAudienceEstimation()

            r = p.estimate(
                accountid,
                productsetid,
                targetingspec
            )
            if (not r) or r['unsupported']:
                return self.render_form_with_status(request, form, (
                    'Got unsupported response. You probably has chosen ' +
                    'wrong combination of ad account and product set.'
                ))

            return self.render_form_with_status(request, form, '', {
                'ad_account_id': accountid,
                'product_set_id': productsetid,
                'reachestimate': r
            })
        except:
            raise
