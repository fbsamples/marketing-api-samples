/**
 * Copyright (c) 2016-present, Facebook, Inc. All rights reserved.
 *
 * You are hereby granted a non-exclusive, worldwide, royalty-free license to
 * use, copy, modify, and distribute this software in source code or binary
 * form for use in connection with the web services and APIs provided by
 * Facebook.
 *
 * As with any software that integrates with the Facebook platform, your use
 * of this software is subject to the Facebook Developer Principles and
 * Policies [http://developers.facebook.com/policy/]. This copyright notice
 * shall be included in all copies or substantial portions of the software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE
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
    'components/targeting_composer',
  ],
  function(
    $,
    React,
    CountryList,
    fbutils,
    ReactModal,
    TargetingComposer
  ) {
    /*
    CaData = {
      '<account_id>': [
        {<custom_audience_json>},
        {...},
        ...
      ],
      ...
    }
    */
    var CaData = {};

    // Load the custom audiences of the selected account
    var loadCustomAudiences = function(accountId) {
      return new Promise(function(resolve, reject) {
        if (accountId === undefined || accountId === null || accountId === '') {
          resolve([]);
        }
        if (accountId in CaData) {
          resolve(CaData[accountId]);
        } else {
          // Ajax the custom audiences list for act
          var apiQuery = fbutils.api(
            '/' + accountId + '/customaudiences',
            'GET',
            {
              'fields': [
                'id',
                'name',
              ],
              'limit': 100,
            }
          );
          apiQuery.then(function(result) {
            CaData[accountId] = result.data;
            resolve(CaData[accountId]);
          }).catch(function(message) {
            reject(message);
          });
        }
      });
    };

    // Load the react JS component
    var initialize = function(targetingSpecId, initialValue, accountSelectId) {
      TargetingComposer = React.createFactory(TargetingComposer);
      ReactModal = React.createFactory(ReactModal);
      // Default to Singapore because it's HOT
      var defaultSpec = {
        'geo_locations': {
          'countries': ['SG'],
        },
        'publisher_platforms': ['facebook', 'audience_network'],
      };
      var defaultJson = JSON.stringify(defaultSpec);

      var initialSpec = defaultSpec;
      var initialJson = defaultJson;
      var hasOldData = false;

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

      var currentTargetingSpec = initialSpec;

      var onChange = function(value) {
        currentTargetingSpec = value;
      };
      var onSave = function() {
        // Write out the currently selected app
        $('#' + targetingSpecId).val(JSON.stringify(currentTargetingSpec));
      };
      var onClose = function() {
        refresh();
      };

      var targeting_spec = $('#' + targetingSpecId);
      var reactElementId = targetingSpecId + '_react';
      var toggleButtonId = targetingSpecId + '_modal';

      // Tooltip
      targeting_spec
        .tooltip({
          'placement': 'bottom',
          'trigger': 'hover focus',
        })
        .on('show.bs.tooltip', function() {
          var accountId = $('#' + accountSelectId).val();
          if (accountId) {
            $(this).attr('data-original-title',
              'Click button on the right to open targeting setting!');
          } else {
            $(this).attr('data-original-title',
              'Select an ad account before using!');
          }
        });

      targeting_spec.val(initialJson)
        .next('span.input-group-addon')
        .attr('id', targetingSpecId + '_toggle')
        .attr('data-target', '#' + targetingSpecId + '_modal');

      $('<div id="' + targetingSpecId + '_react"></div>')
        .insertAfter(targeting_spec);

      var countryList = CountryList.getCountries();

      var refresh = function() {
        var accountId = $('#' + accountSelectId).val();
        if (accountId) {
          $('#' + toggleButtonId).attr('data-toggle', 'modal');
          loadCustomAudiences(accountId).then(function(cas) {
            // Unmount previous component and render new one with loaded apps
            var element = document.getElementById(reactElementId);
            if (element) {
              React.unmountComponentAtNode(element);
            }
            var currentSpec = JSON.parse($('#' + targetingSpecId).val());
            render(accountId, cas, currentSpec);
          }).catch(function(reason) {
            console.log(reason);
          });
        } else {
          $('#' + toggleButtonId).removeAttr('data-toggle');
        }
      };

      var render = function(accountId, customAudiences, initialSpec) {
        var targetingComposer = new TargetingComposer({
          accountId: accountId,
          customAudiences: customAudiences,
          countryList: countryList,
          onChange: onChange,
          initialValue: initialSpec,
        });
        React.render(
          new ReactModal({
            modalHeader: 'Targeting Specs Composer',
            modalBody: targetingComposer,

            targetId: targetingSpecId,
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
        var targetingSpec = defaultSpec;
        if (hasOldData) {
          targetingSpec = initialSpec;
          hasOldData = false;
        } else {
          targetingSpec = defaultSpec;
        }

        // Set the selected app
        $('#' + targetingSpecId).val(
          JSON.stringify(targetingSpec)
        );
        refresh();
      });
    };

    return {
      initialize: initialize,
    };
  }
);
