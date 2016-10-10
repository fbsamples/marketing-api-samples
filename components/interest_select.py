# Copyright (c) 2016, Facebook, Inc.
#
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from django import forms
from widgets import SelectizeWidget, SelectizeMultiWidget


class InterestSelect(forms.CharField):
    """
    Interest targeting select component. It loads the interests via AJAX
    and populates the select options.
    """

    DEFAULT_CHOICES = [('', '- Choose interest(s) -')]

    def __init__(
        self,
        id='id_interest_select',
        id_app_select='id_app_select',
        multiple=True,
        *args,
        **kwargs
    ):
        super(InterestSelect, self).__init__(*args, **kwargs)

        self.id = id

        args = {'attrs': {
                'id': self.id,
                'js_params': [id_app_select],
                'js_module': 'interest_select',
                'js_class': 'InterestSelect',
                },
                'choices': self.DEFAULT_CHOICES
                }

        self.widget = SelectizeMultiWidget(**args) if multiple \
            else SelectizeWidget(**args)
