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
define(['jquery', 'selectize', 'fbutils'],
function($, selectize, fbutils) {
  // Takes in the DOM id for the ad account select and adset select.
  // Then it listens to the change event in ad account select and AJAX load the
  // adset list from that account and populate in the adset select.
  // Loaded adsets will be cached here so no AJAX call should be repeated.
  var initialize = function(
    adsetSelectElementId,
    initialValue,
    accountSelectElementId
  ) {
    var adsetSelectId = '#' + adsetSelectElementId;
    var accountSelectId = '#' + accountSelectElementId;

    $(adsetSelectId).ready(function() {

      $(adsetSelectId).selectize();

      // Cache the ad sets list
      var adsets_data = {};
      var populate_options = function(adsets) {
        clear_options();
        $(adsetSelectId).append($('<option/>', {
          value: '',
          text: '- Choose an Ad Set -',
        }));

        var render_item = function(item, escape) {
          return '<div>' +
            '<span>' + escape(item.name) +
            ' (' + escape(item.id) + ')</span>' +
            '</div>';
        };

        $(adsetSelectId).selectize({
          valueField: 'id',
          labelField: 'id',
          searchField: ['name'],
          options: adsets,
          render: {
            option: function(item, escape) {
              return render_item(item, escape);
            },
            item: function(item, escape) {
              return render_item(item, escape);
            },
          },
        });
      };

      var clear_options = function() {
        // Destroy the previous select list
        $(adsetSelectId)[0].selectize.destroy();

        // Clear previous options
        $(adsetSelectId).empty();
      };

      // Listen to changes from ad account
      $(accountSelectId).change(function() {
        var act = $(accountSelectId).val();
        if (act === undefined || act === '') {
          return;
        }
        var adsets = {};

        clear_options();
        $(adsetSelectId).append($('<option/>', {
          value: '',
          text: '- Loading... -',
        })).selectize();

        if (act === '0') {
          // Nothing selected for act
          populate_options([]);
        } else if (adsets_data[act] !== undefined) {
          adsets = adsets_data[act];
          populate_options(adsets);
        } else {
          // Fetch eligible Ad Sets list for ad account
          $.ajax({
            url:'/samples/an_optin',
            dataType: 'json',
            data:'ad_ac='+act,
            success: function(data) {
              console.log(data);
              //If no data returned simply show the message
              if (data.length === 0) {
                clear_options();
                $(adsetSelectId).append($('<option/>', {
                  value: '',
                  text: '- No eligible Ad Sets found. Try another Ad Account -',
                })).selectize();
                return;
              }
              adsets_data[act] = data;
              populate_options(data);

              // If the widget is initialized with a previous
              // value, it shall be a page refresh so we wait for the
              // current act select load then set with the value
              if (initialValue &&
                initialValue in $(adsetSelectId)[0].selectize.options) {
                $(adsetSelectId)[0].selectize.setValue(initialValue);
                initialValue = null;
              }
            },
            error: function() {
              console.log('ajax failed');
            },
          });
        }
      });
    });
  };

  return {
    initialize: initialize,
  };
});
