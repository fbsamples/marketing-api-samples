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

from django.core.management.base import BaseCommand, CommandError
import sys
import os.path
import shutil
import time
import sqlite3

entry_tpl = '''
    Sample.objects.create(
        {0})
'''

param_tpl = ''',
        '''

autogen_section_start = ">>> AUTO GENERATED SAMPLE OBJECTS"
autogen_section_end = "<<< AUTO GENERATED SAMPLE OBJECTS"

caution_text = '''    # Regenerate with python manage.py gensamplemetadata'''


class Command(BaseCommand):
    help = '''Dump table dash_samples in muse/db.sqlite3 to
migrations/9999_auto_samples_metadata.py, so that the the sample registry can
be committed into our repo.'''

    def handle(self, *args, **options):
        # we are in dash/management/commands, and want to read ./db.sqlite3
        # and dash/migrations/0002_auto_20150114_2204.py
        dbpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              '..', '..', '..',
                              'db.sqlite3')
        mpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '..', '..',
                             'migrations', '9999_auto_samples_metadata.py')

        # read table dash_sample of db.sqlite3 and format
        conn = sqlite3.connect(dbpath)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        code_snippet = ''
        for row in c.execute('select * from dash_sample'):
            # each row should be (id, name, description, view_module,
            # view_class, hide_in_gallery)
            params = dict(row).items()
            code_snippet += entry_tpl.format(
                param_tpl.join(
                    ['%s=%s' %
                     # sqlite stores booleans as ints
                     # but we need to write them out as True/False
                     (k, bool(v) if k == 'hide_in_gallery' else self.escape(v))
                     for (k, v) in params],
                ),
            )
        if not code_snippet.strip():
            self.stdout.write('dash_sample is empty, stop generation.')
            # when no sample records found, exit peacefully
            sys.exit(0)

        # read migration file and generate
        with open(mpath) as f:
            lines = f.read().splitlines()

        generated = []
        autogen_section_start_index = -1
        autogen_section_end_index = -1
        for index, line in enumerate(lines):
            if autogen_section_start in line:
                autogen_section_start_index = index
            if autogen_section_end in line:
                autogen_section_end_index = index
            if (autogen_section_start_index >= 0 and
                    autogen_section_end_index >= 0):
                break
        if autogen_section_start_index < 0 or autogen_section_end_index < 0:
            raise CommandError(
                'Can not find autogen section start or end in ' + mpath
            )

        generated = (
            lines[0:autogen_section_start_index + 1]
            + [caution_text, code_snippet]
            + lines[autogen_section_end_index:]
        )

        # backup & rewrite
        bakfile = os.path.join(
            '/', 'tmp',
            os.path.basename(mpath) + '.bak.' + str(time.time())
        )
        shutil.copyfile(mpath, bakfile)
        with open(mpath, 'w') as f:
            f.write('\n'.join(generated))
        self.stdout.write('Done. Bak file write to \n  ' + bakfile)

    def escape(self, value):
        if isinstance(value, basestring):
            return '"' + value.encode('unicode_escape') + '"'
        return str(value)
