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

import logging
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.views.generic import DetailView, ListView
from security.models import Role, FBUser, FBUserInRole
from security.fbsample import fbads_auth

logger = logging.getLogger(__name__)


class RoleListView(ListView):
    model = Role
    template_name = 'dash/list_role.html'

    @fbads_auth(check_role_list=['super_role'])
    def get(self, request, *args, **kwargs):
        return ListView.get(self, request, args, kwargs)


class RoleDetailsView(DetailView):
    model = Role
    template_name = 'dash/details_role.html'

    def get_object(self, queryset=None):
        obj = DetailView.get_object(self, queryset)
        fbuserinroles = FBUserInRole.objects.filter(role__name=obj.name)
        obj.current_fbusers = []
        for f in fbuserinroles:
            try:
                u = FBUser.objects.get(fb_userid=f.fb_userid)
                obj.current_fbusers.append(u)
            except MultipleObjectsReturned as mor:
                logger.error(
                    "Multi objets returned for fb_userid: %s.",
                    f.fb_userid
                )
                logger.exception(mor)
                continue
            except ObjectDoesNotExist:
                obj.current_fbusers.append({
                    'fb_userid': f.fb_userid,
                    'unknown': True
                })
        return obj

    @fbads_auth(check_role_list=['super_role'])
    def get(self, request, *args, **kwargs):
        return DetailView.get(self, request, args, kwargs)
