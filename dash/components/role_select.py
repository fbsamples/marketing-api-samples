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

from components.widgets import SelectizeWidget
from security.models import Role


class RoleSelect(SelectizeWidget):
    """
    Role select widget based on selectize widget.
    """
    def __init__(self, attrs={}):
        attrs['id'] = attrs.id if hasattr(attrs, 'id') else 'id_role_select'
        attrs['multiple'] = attrs.multiple \
            if hasattr(attrs, 'multiple') else 'True'
        choices = self.get_choices()
        super(RoleSelect, self).__init__(attrs, choices)

    def get_choices(self):
        choices = [('', '- Choose Roles -')]
        # liyuhk: currently simply select all roles into memory.
        # This could be a problem when we have thousands of thousands roles
        # in muse production, but in longer enough time, I expect the total
        # numnber of roles can be handled in memory.
        roles = Role.objects.all()
        for role in roles:
            choices.append((role.name, role.name))
        return choices

    def value_from_datadict(self, data, files, name):
        return ','.join(data.getlist(name, []))
