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
  // Takes in the DOM id for the ad account select.
  var initialize = function(actSelectElementId, initialValue) {
    var actSelectId = '#' + actSelectElementId;
    $(actSelectId).ready(function() {

      $(actSelectId).selectize();
      var populate_options = function(accounts) {
        clear_options();
        $(actSelectId).append($('<option/>', {
          value: '',
          text: '- Choose an ad account -',
        }));

        // Populate the account selector
        $.map(accounts, function(account) {
          if (account.name === '') {
            account.name = account.id;
          }
          $(actSelectId).append(
            $('<option/>', {
              value: account.id,
              text: (account.name + ' (' + account.currency +
                ') (' + account.id + ')'),
            })
          );
        });
        $(actSelectId).selectize();
      };

      var clear_options = function() {
        // Destroy the previous select list
        var selectize_old = $(actSelectId)[0].selectize;
        selectize_old.destroy();

        // Clear previous options
        $(actSelectId).empty();
      };

      clear_options();
      // Show some loading text
      $(actSelectId).append($('<option/>', {
        value: '',
        text: '- Loading... -',
      })).selectize();

      // Ajax the account list for act
      var apiQuery = fbutils.api(
        '/me/adaccounts',
        'GET',
        {
          'fields': [
            'id',
            'name',
            'account_status',
            'timezone_name',
            'amount_spent',
            'currency',
          ],
        }
      );
      apiQuery.then(function(result) {
        var accounts = result.data;
        populate_options(accounts);

        if (initialValue &&
          initialValue in $(actSelectId)[0].selectize.options) {
          // Important: sending silent=false to setValue will fire an change()
          // event from this element so those listening will react properly
          $(actSelectId)[0].selectize.setValue(initialValue, false);
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
