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
from models import Role

# We will check user's fbid with a list of roles (role_list). User has to pass
# all single role checking to be identified as passed. This is flexible, e.g.,
#
#   role_check(['fbads_api_2.4', 'dpa_prospecting'], someuser)
#
# will only allow users who can access fbads api 2.4 and is whitelisted for dpa
# prospecting, while users who can access fbads api 2.4 can not pass.
#
# On the other side, we muse developers require lots of roles. Whenever someone
# adds a new role to muse, we developers should be assigned to it. This is
# convinient and efficient. So we also design some super roles here, which will
# shortcut the checking flow. However, if the user failed super role, we will
# just go on to checking other roles.

logger = logging.getLogger(__name__)

SUPER_ROLE = 'super_role'


def role_check(role_list, user):
    """
    User passes a role_list if:
    1. the role_list is empty, or
    2. he passes one of the super role, or
    3. he passes all role_name inside it.
    """
    logger.debug("role_check called for roles: %s, user: %s",
                 role_list, user)

    # empty role list to check => True, no matter what user
    if (isinstance(role_list, list) and
            len(role_list) == 0):
        return True

    rlist = role_list[:]

    # super role first
    if SUPER_ROLE in rlist:
        rlist.remove(SUPER_ROLE)
        if test_role_with_user(SUPER_ROLE, user):
            return True

    if len(rlist) <= 0:
        # super role is the only role, so failed means failed
        return False

    # if user failed super role, go on with left roles
    topass = len(rlist)
    passed = 0
    for role_name in rlist:
        if test_role_with_user(role_name, user):
            passed = passed + 1
    if passed == topass:
        return True

    # reach here? means nothing can help him
    return False


def test_role_with_user(role_name, user):
    if not user:
        return False

    try:
        role_count = Role.objects.filter(
            fbuserinrole__fb_userid__fb_userid=user.fb_userid,
            name=role_name
        ).count()
        if role_count == 1:
            return True
        else:
            return False
    except MultipleObjectsReturned as mor:
        logger.error(
            "role(%s) check with %s return weiredly: "
            "MultipleObjectsReturned",
            role_name, user.fb_userid)
        logger.exception(mor)
        return False
    except ObjectDoesNotExist as odne:
        logger.error("role(%s) check with %s failed: ObjectDoesNotExist",
                     role_name, user.fb_userid)
        logger.exception(odne)
        return False
