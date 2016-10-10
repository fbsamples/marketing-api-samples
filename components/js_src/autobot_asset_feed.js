/**
 * Copyright (c) 2016-present, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

'use strict';
/*global define*/
define(
  [
    'jquery',
    'react',
    'country_list',
    'fbutils',
    'components/react_modal',
    'components/autobot_asset_feed_composer',
  ],
  function(
    $,
    React,
    CountryList,
    fbutils,
    ReactModal,
    AutobotAssetFeedComposer
  ) {

    // Load the react JS component
    let initialize = function(
      assetFeedSpecId,
      initialValue,
      accountSelectId,
      platformSelectId
    ) {

      AutobotAssetFeedComposer = React.createFactory(AutobotAssetFeedComposer);
      ReactModal = React.createFactory(ReactModal);
      let defaultSpec = {
        'default': {
          'ad_formats': ['SINGLE_IMAGE'],
          'descriptions': [{'text': 'Description'}, ],
          'titles': [{'text': 'Title'}, ],
          'bodies': [{'text': 'Body'}, ],
          'images': [{'hash': ''}, ]
        }
      };

      let defaultJson = JSON.stringify(defaultSpec);

      let initialSpec = defaultSpec;
      let initialJson = defaultJson;
      let hasOldData = false;

      if (initialValue !== '') {
        try {
          // Try to parse the value passed in
          initialSpec = JSON.parse(initialValue);
          initialJson = initialValue;
          hasOldData = true;
        } catch (e) {
          // Value passed in was invalid JSON, revert back to default
          console.log('Invalid value for targeting spec: ' + initialValue);
        }
      }

      let currentassetFeedSpec = initialSpec;

      let onChange = function(value) {
        currentassetFeedSpec = value;
      };
      let onSave = function() {
        // Write out the currently selected app
        $('#' + assetFeedSpecId).val(JSON.stringify(currentassetFeedSpec));
      };
      let onClose = function() {
        refresh();
      };

      let asset_feed_spec = $('#' + assetFeedSpecId);
      let reactElementId = assetFeedSpecId + '_react';
      let toggleButtonId = assetFeedSpecId + '_modal';

      // Tooltip
      asset_feed_spec
        .tooltip({
          'placement': 'bottom',
          'trigger': 'hover focus',
        })
        .on('show.bs.tooltip', function() {
          let accountId = $('#' + accountSelectId).val();
          if (accountId) {
            $(this).attr('data-original-title',
              'Click button on the right to open asset feed setting!');
          } else {
            $(this).attr('data-original-title',
              'Select an ad account before using!');
          }
        });

      asset_feed_spec.val(initialJson)
        .next('span.input-group-addon')
        .attr('id', assetFeedSpecId + '_toggle')
        .attr('data-target', '#' + assetFeedSpecId + '_modal');

      $('<div id="' + assetFeedSpecId + '_react"></div>')
        .insertAfter(asset_feed_spec);

      let countryList = CountryList.getCountries();

      let refresh = function() {
        let accountId = $('#' + accountSelectId).val();
        if (accountId) {
          $('#' + toggleButtonId).attr('data-toggle', 'modal');

          let platforms = [];
          let platformSelected = $('#' + platformSelectId).children();
          platformSelected.each(function() {
            let input = $(this).find('input');
            if (input && input.is(':checked')) {
              platforms.push(input.val());
            }
          });

          try {
            // Unmount previous component and render new one with loaded apps
            let element = document.getElementById(reactElementId);
            if (element) {
              React.unmountComponentAtNode(element);
            }
            let currentSpec = JSON.parse($('#' + assetFeedSpecId).val());
            render(accountId, platforms, currentSpec);
          } catch (reason) {
            console.log(reason);
          }

        } else {
          $('#' + toggleButtonId).removeAttr('data-toggle');
        }
      };

      let render = function(accountId, platforms, initialSpec) {
        let composer = new AutobotAssetFeedComposer({
          accountId: accountId,
          platforms: platforms,
          countryList: countryList,
          onChange: onChange,
          initialValue: initialSpec,
        });
        React.render(
          new ReactModal({
            modalHeader: 'Autobot Asset Feed Composer',
            modalBody: composer,
            targetId: assetFeedSpecId,
            onSave: onSave,
            onClose: onClose,
          }),
          document.getElementById(reactElementId)
        );
      };

      // Listen to the change event from account select, revert spec to
      // empty on account change prevents problems like custom audience
      // belonging to another ad account is present in the current targeting
      // spec.
      // When initializing from previous submission, the account select widget
      // will fire a change event once it's properly initialized so this will
      // also get called.
      $('#' + accountSelectId).change(function(event) {
        let assetFeedSpec = defaultSpec;
        if (hasOldData) {
          assetFeedSpec = initialSpec;
          hasOldData = false;
        } else {
          assetFeedSpec = defaultSpec;
        }

        // Set the selected app
        $('#' + assetFeedSpecId).val(
          JSON.stringify(assetFeedSpec)
        );
        refresh();
      });

      $('#' + platformSelectId).change(function(event) {
        refresh();
      });
    };

    return {
      initialize: initialize,
    };
  }
);
