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

from django.forms import FileField
from widgets import ImageFileWidget


class ImageInput(FileField):
    """
    File upload component that's more consistent with the rest of bootstrap,
    using this [bootstrap file input plugin][1].
    The data file uploaded will be available at `form.cleaned_data[id]`

    [1]: http://www.jasny.net/bootstrap/javascript/#fileinput
    """

    def __init__(
        self,
        id='id_image_file',
        width='200px',
        height='130px',
        *args,
        **kwargs
    ):
        super(ImageInput, self).__init__(*args, **kwargs)

        self.id = id
        self.widget = ImageFileWidget(attrs={
            'id': self.id,
            'width': width,
            'height': height,
            'js_module': 'file_input',
            'js_class': 'ImageFileInput',
        })
