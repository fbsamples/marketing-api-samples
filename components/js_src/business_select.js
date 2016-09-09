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
/* global define */
define(
  ['jquery', 'selectize', 'fbutils'],
function($, selectize, fbutils) {
  var initialize = function(bizSelectElementId, initialValue) {
    var bizSelectId = '#' + bizSelectElementId;
    $(bizSelectId).ready(function() {

      $(bizSelectId).selectize();
      var populate_options = function(accounts) {
        clear_options();
        $(bizSelectId).append($('<option/>', {
          value: '',
          text: '- Choose a business manager -',
        }));

        // Populate the business selector
        $.map(accounts, function(account) {
          $(bizSelectId).append(
            $('<option/>', {
              value: account.id,
              text: (account.name + ' (' + account.id + ')'),
            })
          );
        });
        $(bizSelectId).selectize();
      };

      var clear_options = function() {
        // Destroy the previous select list
        $(bizSelectId)[0].selectize.destroy();

        // Clear previous options
        $(bizSelectId).empty();
      };

      clear_options();
      // Show some loading text
      $(bizSelectId).append($('<option/>', {
        value: '',
        text: '- Loading... -',
      })).selectize();

      // Ajax the custom audiences list for act
      var apiQuery = fbutils.api(
        '/me/businesses',
        'GET'
      );
      apiQuery.then(function(result) {
        var loaded_businesses = result.data;
        populate_options(loaded_businesses);

        if (initialValue &&
          initialValue in $(bizSelectId)[0].selectize.options) {
          // Important: sending silent=false to setValue will fire an change()
          // event from this element so those listening will react properly
          $(bizSelectId)[0].selectize.setValue(initialValue, false);
        }
      }).catch(function(message) {
        console.log(message);
      });
    });
  };

  return {
    initialize: initialize,
  };
});
