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

from django import forms
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt
from django.utils.html import escape
from django.utils.encoding import force_unicode as force_text
import json


class JsWidgetMixin:
    """
    Mixin for common JS function of our custom widgets that has JS initialize
    function. In the JS modules, the initialize function always takes the widget
    element ID as the first variable, the previous value as second variable, and
    the rest params listed in widget.attrs['js_params']
    """
    def get_js(self, value=''):
        attrs = self.attrs

        js_params = []
        if 'js_params' in attrs:
            # Do a copy to prevent modifying the original js_params
            js_params = attrs['js_params'][:]
        js_params.insert(0, attrs['id'])
        js_params.insert(1, value)

        def param_to_js(param):
            """
            Escape the param values before passing to HTML realm, for XSS
            protection. JSON values will be escaped then unescaped in the JS
            domain to get the actual value.
            """
            param_escaped = escape(param)
            return "'{}'".format(param_escaped)

        js_params = ', '.join(map(param_to_js, js_params))
        init_js = "components.initialize('{0}', {1});".format(
            'components/' + attrs['js_module'],
            js_params
        )
        js_code = """<script type='text/javascript'>
            require(['components/components'], function(components) {{
                {0}
            }});
        </script>"""
        js_code = js_code.format(init_js)

        return js_code

    def get_react_js(self, value=''):
        attrs = self.attrs

        js_params = []
        if 'js_params' in attrs:
            # Do a copy to prevent modifying the original js_params
            js_params = attrs['js_params'][:]
        js_params.insert(0, attrs['id'])
        js_params.insert(1, value)

        def param_to_js(param):
            return json.dumps(param)

        js_params = ', '.join(map(param_to_js, js_params))
        js_code = """<script type='text/javascript'>
            require(['{0}'], function(component) {{
                component.initialize({1});
            }});
        </script>"""
        return js_code.format(
            'components/' + attrs['js_module'],
            js_params
        )


class SelectizeWidget(forms.Select, JsWidgetMixin):
    """
    The most basic select widget improved by the selectjs JS library. Use this
    for select fields as much as possible to keep the UI consistent. If you
    don't need fancy things like dynamic loading etc, you don't have to specify
    your special js module and js code, it will use the basic selectize
    initialization and validation code by default.
    """
    def __init__(self, attrs=None, choices=()):
        """
        Initialize the widget. Since this widget will always depend on the
        javascript code to initialize the widget, default the js defines to the
        basic setup.
        """
        if 'js_module' not in attrs:
            attrs['js_module'] = 'basic_selectize'
        if 'js_class' not in attrs:
            attrs['js_class'] = 'BasicSelectize'

        super(SelectizeWidget, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None):
        """
        Where magic happens! Django supports Media classes to include JS source
        files but since we have 'dynamic' element IDs we need inline JS support
        which is not in the official package. So hijacking the render function
        here to attach the JS code.
        """
        html = super(SelectizeWidget, self).render(name, value, attrs)

        # Initialize with a value, this happens after the submit button is
        # clicked, whether form is valid or not.
        if value is None:
            value = ''

        js_code = self.get_js(value)
        return mark_safe(html + js_code)


class SelectizeMultiWidget(forms.SelectMultiple, JsWidgetMixin):
    """
    The same idea as SelectizeWidget but for multiple selections by inheriting
    from forms.SelectMultiple.
    """
    def __init__(self, attrs=None, choices=()):
        if 'js_module' not in attrs:
            attrs['js_module'] = 'basic_selectize'
        if 'js_class' not in attrs:
            attrs['js_class'] = 'BasicSelectize'

        super(SelectizeMultiWidget, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None):
        html = super(SelectizeMultiWidget, self).render(name, value, attrs)

        if value is None:
            value = ''

        js_code = self.get_js(value)
        return mark_safe(html + js_code)


class FileWidget(forms.FileInput, JsWidgetMixin):
    """
    File upload widget that's more consistent with the rest of bootstrap. From a
    bootstrap extension here:
    http://www.jasny.net/bootstrap/javascript/#fileinput
    """
    html_template = '''
        <div %(div_attrs)s class="fileinput fileinput-new input-group"
            data-provides="fileinput">
            <div class="form-control" data-trigger="fileinput">
                <i class="glyphicon glyphicon-file fileinput-exists"></i>
                <span class="fileinput-filename"></span>
            </div>
            <span class="input-group-addon btn btn-default btn-file">
                <span class="fileinput-new">Select file</span>
                <span class="fileinput-exists">Change</span>
                <input type="file" name="%(name)s" />
            </span>
            <a href="#" class="input-group-addon btn btn-default
                fileinput-exists" data-dismiss="fileinput">
                Remove
            </a>
        </div>'''

    def __init__(self, attrs=None):
        self.div_attrs = {
            'id': attrs.get('id') + '_container'
        }
        super(FileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        div_attrs = self.div_attrs
        html = self.html_template % dict(
            div_attrs=flatatt(div_attrs),
            name=name,
        )
        js_code = self.get_js()
        return mark_safe(html + js_code)


class ImageFileWidget(forms.FileInput, JsWidgetMixin):
    """
    Image file upload widget that's more consistent with the rest of bootstrap.
    From a bootstrap extension here:
    http://www.jasny.net/bootstrap/javascript/#fileinput
    """
    html_template = '''
        <div %(div_attrs)s class="fileinput fileinput-new"
            data-provides="fileinput">
            <div class="fileinput-preview thumbnail" data-trigger="fileinput"
                style="width: %(width)s; height: %(height)s;">
            </div>
            <div>
                <span class="btn btn-default btn-file">
                    <span class="fileinput-new">Select image</span>
                    <span class="fileinput-exists">Change</span>
                    <input type="file" name="%(name)s" />
                </span>
                <a href="#" class="btn btn-default fileinput-exists"
                    data-dismiss="fileinput">
                    Remove
                </a>
            </div>
        </div>'''

    def __init__(self, attrs=None):
        self.div_attrs = {
            'id': attrs.get('id') + '_container'
        }
        self.width = attrs.get('width', '200px')
        self.height = attrs.get('height', '130px')
        super(ImageFileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        div_attrs = self.div_attrs
        html = self.html_template % dict(
            div_attrs=flatatt(div_attrs),
            width=self.width,
            height=self.height,
            name=name,
        )
        js_code = self.get_js()
        return mark_safe(html + js_code)


class DatetimePickerWidget(forms.DateTimeInput, JsWidgetMixin):
    """
    The widget customizes the default DateTimeInput widget so that the datetime
    picker JS library can apply the magic to it.
    """
    html_template = '''
        <div%(div_attrs)s>
            <input%(input_attrs)s/>
            <span class="input-group-addon">
                <span class="glyphicon glyphicon-calendar"></span>
            </span>
        </div>'''

    def __init__(self, attrs=None, format=None):
        if 'js_module' not in attrs:
            raise KeyError("You need to define your own JS module!")
        if 'js_class' not in attrs:
            raise KeyError("You need to define your own JS class!")

        self.div_attrs = {
            'class': 'input-group date',
            'id': attrs.get('id') + '_pickers'
        }

        super(DatetimePickerWidget, self).__init__(attrs, format)

        if 'class' not in self.attrs:
            self.attrs['class'] = 'form-control'

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        input_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            input_attrs['value'] = force_text(self._format_value(value))

        div_attrs = self.div_attrs

        html = self.html_template % dict(div_attrs=flatatt(div_attrs),
                                         input_attrs=flatatt(input_attrs))

        js_code = self.get_js(force_text(self._format_value(value)))
        return mark_safe(html + js_code)


class ReactModalWidget(forms.TextInput, JsWidgetMixin):
    """
    This widget will output a text input field, with a glyphicon button to
    toggle the modal pop up, and a place holder for the react JS component to
    kick in. You still need to make sure that you render the modal pop up page
    in your react component.
    """
    html_template = '''
        <div %(div_attrs)s>
            <input %(input_attrs)s/>
            <span class="input-group-addon">
                <i class="%(icon)s"></i>
            </span>
        </div>'''

    def __init__(self, attrs=None):
        if 'js_module' not in attrs:
            raise KeyError("You need to define your own JS module!")
        if 'js_class' not in attrs:
            raise KeyError("You need to define your own JS class!")

        self.id = attrs.get('id')
        self.div_attrs = {
            'class': 'input-group',
            'id': self.id + '_container'
        }

        super(ReactModalWidget, self).__init__(attrs)

        if 'class' not in self.attrs:
            self.attrs['class'] = 'form-control'

    def render(self, name, value, attrs=None):
        icon = 'glyphicon glyphicon-list-alt'
        if 'icon' in self.attrs:
            icon = self.attrs['icon']

        if value is None:
            value = ''

        input_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            input_attrs['value'] = force_text(self._format_value(value))
        input_attrs['readonly'] = 'readonly'

        div_attrs = self.div_attrs

        html = self.html_template % dict(
            div_attrs=flatatt(div_attrs),
            input_attrs=flatatt(input_attrs),
            icon=icon
        )

        js_code = self.get_js(value)
        return mark_safe(html + js_code)


class ReactWidget(forms.TextInput, JsWidgetMixin):
    """
    This widget will output a text input field, with a glyphicon button to
    toggle the modal pop up, and a place holder for the react JS component to
    kick in. You still need to make sure that you render the modal pop up page
    in your react component.
    """
    html_template = '''
        <div %(div_attrs)s>
            <input style="display:none" %(input_attrs)s/>
            <div id="%(react_placeholder)s"></div>
        </div>
    '''

    def __init__(self, attrs=None):
        if 'js_module' not in attrs:
            raise KeyError("You need to define your own JS module!")
        if 'js_class' not in attrs:
            raise KeyError("You need to define your own JS class!")

        self.id = attrs.get('id')
        self.div_attrs = {
            'class': 'input-group',
            'id': self.id + '_container'
        }

        super(ReactWidget, self).__init__(attrs)

        if 'class' not in self.attrs:
            self.attrs['class'] = 'form-control'

    def render(self, name, value, attrs=None):
        react_placeholder = self.id + '_react'

        if value is None:
            value = ''

        input_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        div_attrs = self.div_attrs

        html = self.html_template % dict(
            div_attrs=flatatt(div_attrs),
            input_attrs=flatatt(input_attrs),
            react_placeholder=react_placeholder,
        )

        js_code = self.get_react_js(value)
        return mark_safe(html + js_code)
