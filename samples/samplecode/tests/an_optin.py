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

from samples.samplecode.an_optin import AudienceNetworkOptinSample
from samples.samplecode.tests.sampletestcase import SampleTestCase
from facebookads.adobjects.adset import AdSet
from facebookads.objects import TargetingSpecsField
import copy


class AudienceNetworkOptinTestCase(SampleTestCase):

    def setUp(self):
        super(AudienceNetworkOptinTestCase, self).setUp()
        self.sample = AudienceNetworkOptinSample()

    def test_normal(self):

        # test data
        SAMPLE_ADSET_ID = "6035543090685"
        SAMPLE_ADSET_LIST = [SAMPLE_ADSET_ID]

        # test class method retrieve_eligible_adsets_for_an()
        result = self.sample.retrieve_eligible_adsets_for_an(
            self.account_id,
            True,
        )

        # assertions

        # should always be a list even if empty; cannot be None
        self.assertIsNotNone(result, "The result cannot be None. "
                                     "Should return an empty list.")

        # we know there was atleast one ad set 6035543090685 under the test
        # Muse ad account so atleast that should have been returned
        self.assertGreaterEqual(
            len(result),
            1,
            "The result list should atleast contain one element, "
            "the ad set we were looking for.")

        # the returned list should have objects of type AdSet
        # and in particular it should have the ad set we are
        # looking for
        passed = False
        for adset in result:
            self.assertIsInstance(
                adset,
                AdSet,
                "The result list returned should only have elements "
                "of type AdSet")
            if adset[AdSet.Field.id] == SAMPLE_ADSET_ID:
                passed = True

        if passed is False:
            # throw an assertion failure
            self.fail("The ad set %s should have been part of the returned "
                      "response." % SAMPLE_ADSET_ID)

        # test class method enable_an_on_adsets()
        result = self.sample.enable_an_on_adsets(
            SAMPLE_ADSET_LIST
        )

        # assertions

        # should always be a list even if empty; cannot be None
        self.assertIsNotNone(result, "The result cannot be None. "
                                     "Should return an empty list.")

        # size of returned list is same as size of the list we passed
        self.assertEquals(
            len(SAMPLE_ADSET_LIST),
            len(result),
            "The result list should be of the same size of the "
            "list we passed as input.")

        # the list should have the ad set id that we expect and
        # status against should be 1
        passed = False
        for adset in result:
            if SAMPLE_ADSET_ID in adset.keys():
                if adset[SAMPLE_ADSET_ID]['status'] == 1:
                    passed = True

        if passed is False:
            self.fail("Method was not successfull in enabling the audience "
                      "network flag for our sample ad set with id %s"
                      % SAMPLE_ADSET_ID)

    def tearDown(self):
        if hasattr(self, 'campaign'):
            self.campaign.remote_delete()

        # rest the audience network flag on the ad set 6035543090685
        # so the the next test runs pass

        # read ad set info
        adset = AdSet(fbid="6035543090685")
        adsetobj = adset.remote_read(fields=[AdSet.Field.targeting])

        # edit targeting spec info for placements
        targetinginfo = copy.deepcopy(adsetobj[AdSet.Field.targeting])
        targetinginfo[TargetingSpecsField.publisher_platforms].remove('audience_network')

        # update ad set info
        adset.update({
            AdSet.Field.targeting: targetinginfo
        })
        adset.remote_update()
