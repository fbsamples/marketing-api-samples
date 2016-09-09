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

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from dash.models import Sample
from django.forms.models import modelform_factory
from dash.components.role_select import RoleSelect
from security.fbsample import fbads_auth


class SampleCreateView(CreateView):
    model = Sample
    template_name = 'dash/create_sample.html'
    form_class = modelform_factory(
        Sample,
        fields='__all__',
        exclude=None,
        widgets={'roles_to_check': RoleSelect}
    )

    def get_success_url(self):
        return reverse_lazy('dash:sample_list')

    @fbads_auth(check_role_list=['super_role'])
    def get(self, request, *args, **kwargs):
        return CreateView.get(self, request, args, kwargs)

    @fbads_auth(check_role_list=['super_role'])
    def post(self, request, *args, **kwargs):
        return CreateView.post(self, request, args, kwargs)


class SampleListView(ListView):
    model = Sample
    template_name = 'dash/list_sample.html'

    @fbads_auth(check_role_list=['super_role'])
    def get(self, request, *args, **kwargs):
        return ListView.get(self, request, args, kwargs)

    @fbads_auth(check_role_list=['super_role'])
    def post(self, request, *args, **kwargs):
        return ListView.post(self, request, args, kwargs)


class SampleDeleteView(DeleteView):
    model = Sample
    template_name = 'dash/delete_sample.html'
    success_url = reverse_lazy('dash:sample_list')

    @fbads_auth(check_role_list=['super_role'])
    def get(self, request, *args, **kwargs):
        return DeleteView.get(self, request, args, kwargs)

    @fbads_auth(check_role_list=['super_role'])
    def post(self, request, *args, **kwargs):
        return DeleteView.post(self, request, args, kwargs)


class SampleDetailView(DetailView):
    model = Sample
    template_name = 'dash/details_sample.html'

    @fbads_auth(check_role_list=['super_role'])
    def get(self, request, *args, **kwargs):
        return DetailView.get(self, request, args, kwargs)

    @fbads_auth(check_role_list=['super_role'])
    def post(self, request, *args, **kwargs):
        return DetailView.post(self, request, args, kwargs)


class SampleUpdateView(UpdateView):
    model = Sample
    template_name = 'dash/create_sample.html'
    success_url = reverse_lazy('dash:sample_list')
    form_class = modelform_factory(
        Sample,
        fields='__all__',
        exclude=None,
        widgets={'roles_to_check': RoleSelect}
    )

    @fbads_auth(check_role_list=['super_role'])
    def get(self, request, *args, **kwargs):
        return UpdateView.get(self, request, args, kwargs)

    @fbads_auth(check_role_list=['super_role'])
    def post(self, request, *args, **kwargs):
        return UpdateView.post(self, request, args, kwargs)
