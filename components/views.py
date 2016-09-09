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


import textwrap
import markdown
import logging
import os
from django.shortcuts import render
from django.views.generic import View
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect
from components.custom_audience_select import CustomAudienceSelect
from components.app_select import AppSelect
from components.page_select import PageSelect
from components.bid_component import BidComponent
from components.business_manager_select import BusinessManagerSelect
from components.product_catalog_select import ProductCatalogSelect
from components.product_select import ProductSelect
from components.targeting_spec import TargetingSpec
from components.lead_form_create import LeadFormCreate
from security.fbsample import components_auth

logger = logging.getLogger(__name__)


def get_file_content(rel_path):
    """
    rel_path is the relative path of the script file to this file!
    """
    this_dir = os.path.dirname(__file__)
    file_path = os.path.realpath('{0}/{1}'.format(this_dir, rel_path))

    file_content = ''
    with open(file_path) as f:
        file_content = f.read()

    return file_content


class ComponentGalleryForm(ComponentForm):

    select_account = AdAccountSelect()
    select_account.JS_FILES = ['actselect.js']

    select_custom_audience = CustomAudienceSelect()
    select_custom_audience.JS_FILES = ['caselect.js']

    select_app = AppSelect()
    select_app.JS_FILES = ['app_select.js', 'app_info.jsx']

    targeting_setting = TargetingSpec()
    targeting_setting.JS_FILES = ['targeting_spec.js', 'targeting_composer.jsx']

    bid_setting = BidComponent('bid_setting')
    bid_setting.JS_FILES = ['bid_component.js', 'bid_composer.jsx']

    select_page = PageSelect()
    select_page.JS_FILES = ['page_select.js']

    select_lead_gen_form = LeadFormCreate()
    select_lead_gen_form.JS_FILES = ['lead_form.js', 'lead_form_select.jsx']

    select_business_manager = BusinessManagerSelect()
    select_business_manager.JS_FILES = ['business_select.js']

    select_product_catalog = ProductCatalogSelect()
    select_product_catalog.JS_FILES = ['product_catalog_select.js']

    select_product = ProductSelect()
    select_product.JS_FILES = ['product_select.js']

    def __init__(self):
        super(ComponentGalleryForm, self).__init__()

        for key, field in self.fields.items():
            field.desc = markdown.markdown(textwrap.dedent(field.__doc__))
            field.name = field.__class__.__name__
            js_modules = []
            if hasattr(field, 'JS_FILES'):
                for js_file in field.JS_FILES:
                    js_module_content = get_file_content(
                        './js_src/{0}'.format(
                            js_file
                        )
                    )
                    js_modules.append({
                        'name': js_file,
                        'content': js_module_content
                    })
            field.js_modules = js_modules


class ComponentGallery(View):

    TEMPLATE = 'components/gallery.html'

    @components_auth()
    def get(self, request, *args, **kwargs):
        form = ComponentGalleryForm()
        fbutils = get_file_content('../common/static/scripts/fbutils.js')
        return render(
            request,
            self.TEMPLATE,
            {
                'form': form,
                'fbutils': fbutils
            }
        )


class ComponentOverview(View):
    @components_auth()
    def get(self, request, *args, **kwargs):
        # Markdown content
        content = get_file_content('templates/components/overview.md')
        content = markdown.markdown(content,
                                    extensions=['markdown.extensions.extra'])
        return render(request, 'components/overview.html', {'content': content})
