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
  // Takes in the DOM id for the ad account select and custom audiences select.
  // Then it listens to the change event in ad account select and AJAX load the
  // custom audience list from that account and populate in the custom audiences
  // select. Loaded custom audiences will be cached here so no AJAX call should
  // be repeated.
  var initialize = function(
    caSelectElementId,
    initialValue,
    accountSelectElementId
  ) {
    var caSelectId = '#' + caSelectElementId;
    var accountSelectId = '#' + accountSelectElementId;

    // Custom Audience picker
    $(caSelectId).ready(function() {

      $(caSelectId).selectize();

      // Cache the custom audiences list
      var custom_audiences_data = {};

      var populate_options = function(audiences) {
        clear_options();
        $(caSelectId).append($('<option/>', {
          value: '',
          text: '- Choose a custom audience -',
        }));
        // Populate the custom audience selector
        $.map(audiences, function(audience) {
          $(caSelectId).append(
            $('<option/>', {
              value: audience.id,
              text: (
                audience.name +
                ' (' + audience.subtype + ')' +
                ' (' + audience.id + ')'
              ),
            })
          );
        });
        $(caSelectId).selectize();
      };

      var clear_options = function() {
        // Destroy the previous select list
        $(caSelectId)[0].selectize.destroy();

        // Clear previous options
        $(caSelectId).empty();
      };

      // Listen to changes from ad account
      $(accountSelectId).change(function() {
        var act = $(accountSelectId).val();
        if (act === undefined || act === '') {
          return;
        }

        var custom_audiences = {};

        clear_options();
        $(caSelectId).append($('<option/>', {
          value: '',
          text: '- Loading... -',
        })).selectize();

        if (act === '0') {
          // Nothing selected for act
          populate_options([]);
        } else if (custom_audiences_data[act] !== undefined) {
          custom_audiences = custom_audiences_data[act];
          // Remove the previous choices
          populate_options(custom_audiences);
        } else {
          // Ajax the custom audiences list for act
          var apiQuery = fbutils.api(
            '/' + act + '/customaudiences',
            'GET',
            {
              'fields': [
                'id',
                'name',
                'subtype',
              ],
              'limit': 100,
            }
          );
          apiQuery.then(function(result) {
            var loaded_custom_audiences = result.data;
            loaded_custom_audiences = loaded_custom_audiences.filter(
              function(ca) {
                return ca.subtype !== 'LOOKALIKE';
              }
            );
            custom_audiences_data[act] = loaded_custom_audiences;
            populate_options(loaded_custom_audiences);

            // If the widget is initialized with a previous value, it shall be
            // a page refresh so we wait for the current act select load then
            // set with the value
            if (initialValue &&
              initialValue in $(caSelectId)[0].selectize.options) {
              $(caSelectId)[0].selectize.setValue(initialValue);
              initialValue = null; // Just use it once
            }
          }).catch(function(message) {
            console.log(message);
          });
        }
      });
    });
  };

  return {
    initialize: initialize,
  };
});
