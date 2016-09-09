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
    'selectize',
    'fbutils',
    'components/react_modal',
    'components/app_info',
  ],
function($, React, selectize, fbutils, ReactModal, AppInfo) {
  /*
  AppData = {
    '<account_id>': [
      {<app_info_json>},
      {...},
      ...
    ],
    ...
  }
  */
  var AppData = {};

  // Load the apps of the selected account
  var loadApps = function(accountId) {
    return new Promise(function(resolve, reject) {
      if (accountId === undefined || accountId === null || accountId === '') {
        resolve([]);
      }
      if (accountId in AppData) {
        resolve(AppData[accountId]);
      } else {
        // Ajax the custom audiences list for act
        var apiQuery = fbutils.api(
          '/' + accountId + '/advertisable_applications',
          'GET',
          {
            'fields': [
              'id',
              'name',
              'url',
              'picture',
              'supported_platforms',
              'native_app_store_ids',
              'object_store_urls',
              'type',
            ],
            'limit': 100,
          }
        );
        apiQuery.then(function(result) {
          var loaded_apps = result.data;
          AppData[accountId] = loaded_apps;
          resolve(loaded_apps);
        }).catch(function(message) {
          reject(message);
        });
      }
    });
  };
  // Takes in the DOM id for the ad account select as extra parameter.
  var initialize = function(
    appSelectElementId,
    initialValue,
    accountSelectElementId
  ) {

    AppInfo = React.createFactory(AppInfo);
    ReactModal = React.createFactory(ReactModal);

    var reactElementId = appSelectElementId + '_react';
    var toggleButtonId = appSelectElementId + '_modal';

    // Default to none selected
    var initialSelectedApp = {};
    var initialJson = JSON.stringify(initialSelectedApp);

    var hasOldData = false;
    if (initialValue !== '') {
      initialJson = initialValue;
      hasOldData = true;
    }

    // Init extra elements for React
    var app_select = $('#' + appSelectElementId);
    app_select.val(initialJson)
      .next('span.input-group-addon')
      .attr('id', appSelectElementId + '_toggle')
      .attr('data-target', '#' + appSelectElementId + '_modal');

    $('<div id="' + appSelectElementId + '_react"></div>')
      .insertAfter(app_select);

    var currentApp = initialSelectedApp;

    var onChange = function(value) {
      currentApp = value;
    };
    var onSave = function() {
      // Write out the currently selected app
      $('#' + appSelectElementId).val(JSON.stringify(currentApp));
    };

    var onClose = function() {
      refresh();
    };

    var refresh = function() {
      var accountId = $('#' + accountSelectElementId).val();
      if (accountId) {
        $('#' + toggleButtonId).attr('data-toggle', 'modal');
        loadApps(accountId).then(function(apps) {
          // Unmount previous component and render new one with loaded apps
          var element = document.getElementById(reactElementId);
          if (element) {
            React.unmountComponentAtNode(element);
          }
          var currentValue = $('#' + appSelectElementId).val();
          var selectedApp = JSON.parse(currentValue);
          render(apps, selectedApp);
        }).catch(function(reason) {
          console.log(reason);
        });
      } else {
        $('#' + toggleButtonId).removeAttr('data-toggle');
      }
    };

    var render = function(apps, selectedApp) {
      var appInfo = new AppInfo({
        initialValue: selectedApp,
        apps: apps,
        onChange: onChange,
      });
      React.render(
        new ReactModal({
          modalHeader: 'Select Application',
          modalBody: appInfo,
          targetId: appSelectElementId,
          onSave: onSave,
          onClose: onClose,
        }),
        document.getElementById(reactElementId)
      );
    };

    // Listen to the change event from account select, revert app info to
    // empty on account change prevents problems like apps belonging to
    // another ad account is present in the selected app info.
    // When initializing from previous submission, the account select widget
    // will fire a change event once it's properly initialized so this will
    // also get called.
    $('#' + accountSelectElementId).change(function() {
      if (hasOldData) {
        try {
          currentApp = JSON.parse(initialValue);
        } catch (e) {
          console.log(e);
          currentApp = {};
        }
        hasOldData = false;
      } else {
        currentApp = {};
      }
      $('#' + appSelectElementId).val(
        JSON.stringify(currentApp)
      );
      refresh();
    });
  };

  return {
    initialize: initialize,
  };
});
