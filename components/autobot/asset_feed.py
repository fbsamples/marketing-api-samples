# Copyright (c) 2015, Facebook, Inc.
#
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from components.widgets import ReactModalWidget
from components.json_char_field import JsonCharField


class AssetFeed(JsonCharField):
    """
    AssetFeed subsection
    """

    """
    Some sample asset feed specs
    """
    ASSET_FEED_DEFAULT = {
        "default": {
            "descriptions": [{"text": "Description"}, ],
            "titles": [{"text": "Title"}, ],
            "ad_formats": ["SINGLE_IMAGE"],
            "bodies": [{"text": "Body"}, ],
            "images": [{"hash": "6c97ef2c81b383ae3624301b0b126a5a"}, ]
        }
    }

    def __init__(
        self,
        id='id_creative',
        id_act_select='id_act_select',
        id_platform_select='id_platform_select',
        *args,
        **kwargs
    ):
        super(AssetFeed, self).__init__(*args, **kwargs)

        self.id = id
        if not self.help_text:
            self.help_text = ("Choose an ad account before using. Changing " +
                              "ad account will reset the current spec.")

        self.widget = ReactModalWidget(attrs={
            'id': self.id,
            'js_params': [id_act_select, id_platform_select],
            'icon': "glyphicon glyphicon-plus",
            'js_module': 'autobot_asset_feed',
            'js_class': 'AssetFeed',
            'data-toggle': 'tooltip',
            'title': 'Choose an ad account before using.',
        })
