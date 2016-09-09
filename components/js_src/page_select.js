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
  // Takes in the DOM id for the ad account select and page select.
  // Then it listens to the change event in ad account select and AJAX load the
  // page list from that account and populate in the page
  // select. Loaded pages will be cached here so no AJAX call should
  // be repeated.
    var initialize = function(
      pageSelectElementId,
      initialValue,
      accountSelectElementId
    ) {
      var pageSelectId = '#' + pageSelectElementId;
      var accountSelectId = '#' + accountSelectElementId;

      $(pageSelectId).ready(function() {
        $(pageSelectId).selectize();

        // Cache the page list
        var pages_data = {};

        var populate_options = function(pages) {
          clear_options();
          $(pageSelectId).append($('<option/>', {
            value: '',
            text: '- Choose a page -',
          }));

          var render_item = function(item, escape) {
            var img = '';
            if (item.picture.data.url) {
              img = '<img class="picture" src=' +
                escape(item.picture.data.url) + ' />';
            }
            return '<div>' + img +
              '<span>' + escape(item.name) +
              ' (' + escape(item.id) + ')</span>' +
              '</div>';
          };

          $(pageSelectId).selectize({
            valueField: 'id',
            labelField: 'id',
            searchField: ['name'],
            options: pages,
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
          $(pageSelectId)[0].selectize.destroy();

          // Clear previous options
          $(pageSelectId).empty();
        };

        // Listen to changes from ad account
        $(accountSelectId).change(function() {
          var act = $(accountSelectId).val();
          if (act === undefined || act === '') {
            return;
          }

          var pages = {};

          clear_options();
          $(pageSelectId).append($('<option/>', {
            value: '',
            text: '- Loading... -',
          })).selectize();

          if (act === '0') {
            // Nothing selected for act
            populate_options([]);
          } else if (pages_data[act] !== undefined) {
            pages = pages_data[act];
            // Remove the previous choices
            populate_options(pages);
          } else {
            // Ajax the custom audiences list for act
            var apiQuery = fbutils.api(
              '/me/accounts',
              'GET',
              {
                'fields': [
                  'id',
                  'name',
                  'picture',
                ],
                'limit': 100,
              }
            );
            apiQuery.then(function(result) {
              pages_data[act] = result.data;
              populate_options(pages_data[act]);

              // If the widget is initialized with a previous value, it shall be
              // a page refresh so we wait for the current act select load then
              // set with the value
              if (initialValue &&
                initialValue in $(pageSelectId)[0].selectize.options
              ) {
                $(pageSelectId)[0].selectize.setValue(initialValue);
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
  }
);
