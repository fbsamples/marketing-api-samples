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

import json
import logging
import urllib2
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from common import utils

logger = logging.getLogger(__name__)


class FBAuthBackend(object):
    def authenticate(self, token=None):
        if token is None:
            return None
        else:
            fbu = FBUserManager()
            user = fbu.get_or_create_user(token)
            return user

    def get_user(self, user_id):
        try:
            return FBUser.objects.get(fb_userid=user_id)
        except FBUser.DoesNotExist:
            return None


class FBUser(AbstractBaseUser):
    fb_userid = models.CharField(max_length=20, primary_key=True)
    fb_username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=61, unique=False)

    # can't use fb_username
    # because USERNAME max length is 30
    USERNAME_FIELD = 'fb_userid'
    REQUIRED_FIELDS = ['fb_username']

    def __init__(self, *args, **kwargs):
        super(FBUser, self).__init__(*args, **kwargs)
        self.token = None

    def get_short_name(self):
        return self.fb_username

    def get_full_name(self):
        return self.full_name


class FBUserManager(BaseUserManager):
    def get_or_create_user(self, token):
        (user_id, full_name, user_name) = self.get_userinfo_from_fb(token)
        user = None
        try:
            user = FBUser.objects.get(fb_userid=user_id)
        except FBUser.DoesNotExist:
            user = self.create_user(user_id, user_name, full_name)

        user.backend = settings.AUTH_BACKEND
        user.token = token

        return user

    def create_user(self, user_id, user_name, full_name):
        user = FBUser(
            fb_userid=user_id,
            fb_username=user_name,
            full_name=full_name
        )
        user.save()
        return user

    def get_userinfo_from_fb(self, token):
        url = utils.construct_url('https://graph.facebook.com/me', {
            'fields': 'id,name',
            'access_token': token})
        try:
            response = urllib2.urlopen(url).read()
            data = json.loads(response)
        except urllib2.HTTPError as e:
            logger.exception(e)
            logger.error('Failed to get user info from Facebook.')
            raise e
        # username is deprecated so using id in its place
        return (data['id'], data['name'], data['id'])


# Comments on the design of Role, FBUserInRole and their relationships:
#
# Entity: Role
#   This is the entity for each Role, which is a simple (name, description)
#   tuple. Name is the primary_key.
#
# Entity: FBUserInRole
#   This is the entity for which Facebook user is assigned which role. It is
#   (fb_userid, role_name) tuple, where fb_userid refs to FBUser, and role_name
#   refs to Role..
#
# Relations between Role and FBUserInRole
#   Role (1)<--(many) FBUserInRole,
#


class Role(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=200)


class FBUserInRole(models.Model):
    fb_userid = models.ForeignKey(FBUser)
    role = models.ForeignKey(Role)
