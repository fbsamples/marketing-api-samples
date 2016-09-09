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
define(['jquery', 'selectize', 'fbutils'],
function($, selectize, fbutils) {
  var initialize = function(
    psSelectElementId,
    initialValue,
    catalogSelectElementId
  ) {
    var psSelectId = '#' + psSelectElementId;
    var catalogSelectId = '#' + catalogSelectElementId;

    // product set picker
    $(psSelectId).ready(function() {

      $(psSelectId).selectize();

      // Cache the product set list
      var product_set_data = {};

      var populate_options = function(product_sets) {
        clear_options();
        $(psSelectId).append($('<option/>', {
          value: '',
          text: '- Choose a product set -'
        }));
        // Populate the product set selector
        $.map(product_sets, function(product_set) {
          $(psSelectId).append(
            $('<option/>', {
              value: product_set.id,
              text: (product_set.name.substr(0, 50) + '... (' +
                     product_set.id + ')')
            })
          );
        });
        $(psSelectId).selectize();
      };

      var clear_options = function() {
        // Destroy the previous select list
        $(psSelectId)[0].selectize.destroy();

        // Clear previous options
        $(psSelectId).empty();
      };

      // Listen to changes from catalog
      $(catalogSelectId).change(function() {
        var catalog_id = $(catalogSelectId).val();
        if (catalog_id === undefined || catalog_id === '') {
          return;
        }

        var product_sets = {};

        clear_options();
        $(psSelectId).append($('<option/>', {
          value: '',
          text: '- Loading... -'
        })).selectize();

        if (catalog_id === '0') {
          // Nothing selected for catalog_id
          populate_options([]);
        } else if (product_set_data[catalog_id] !== undefined) {
          product_sets = product_set_data[catalog_id];
          // Remove the previous choices
          populate_options(product_sets);
        } else {
          // Ajax the custom audiences list for act
          var apiQuery = fbutils.api(
            '/' + catalog_id + '/product_sets',
            'GET',
            {
              'fields': [
                'id',
                'name',
              ],
              'limit': 100
            }
          );
          apiQuery.then(function(result) {
            var loaded_product_sets = result.data;
            populate_options(loaded_product_sets);

            // If the widget is initialized with a previous value, it shall be
            // a page refresh so we wait for the current catalog_id select load
            // then set with the value
            if (initialValue &&
              initialValue in $(psSelectId)[0].selectize.options) {
              $(psSelectId)[0].selectize.setValue(initialValue);
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
    initialize: initialize
  };
});
