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

from samples.samplecode.tests.sampletestcase import SampleTestCase
from samples.samplecode.multiple_lal import MultipleLalSample


class MultipleLalTestCase(SampleTestCase):

    def setUp(self):
        super(MultipleLalTestCase, self).setUp()
        self.sample = MultipleLalSample()

    def test_normal(self):
        self.created_lals = self.sample.create_lals(
            self.account_id,
            self.ca_id,
            "Multiple LAL Test",  # lookalike_name
            ["US"],  # country
            [1, 2],  # ratio
        )
        self.assertEqual(len(self.created_lals), 2)

    def tearDown(self):
        super(MultipleLalTestCase, self).tearDown()
        if hasattr(self, 'created_lals'):
            for lookalike in self.created_lals:
                lookalike.remote_delete()
