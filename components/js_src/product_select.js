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
  var initialize = function(
    rtSelectElementId,
    initialValue,
    catalogSelectElementId
  ) {
    var rtSelectId = '#' + rtSelectElementId;
    var catalogSelectId = '#' + catalogSelectElementId;

    // product picker
    $(rtSelectId).ready(function() {

      $(rtSelectId).selectize();

      // Cache the product list
      var product_data = {};

      var populate_options = function(products) {
        clear_options();
        $(rtSelectId).append($('<option/>', {
          value: '',
          text: '- Choose a product (showing up to 100) -',
        }));
        // Populate the product selector
        $.map(products, function(product) {
          $(rtSelectId).append(
            $('<option/>', {
              value: product.retailer_id,
              text: (product.name.substr(0, 50) + '... (' + product.id + ')'),
            })
          );
        });
        $(rtSelectId).selectize();
      };

      var clear_options = function() {
        // Destroy the previous select list
        $(rtSelectId)[0].selectize.destroy();

        // Clear previous options
        $(rtSelectId).empty();
      };

      // Listen to changes from ad account
      $(catalogSelectId).change(function() {
        var catalog_id = $(catalogSelectId).val();
        if (catalog_id === undefined || catalog_id === '') {
          return;
        }

        var products = {};

        clear_options();
        $(rtSelectId).append($('<option/>', {
          value: '',
          text: '- Loading... -',
        })).selectize();

        if (catalog_id === '0') {
          // Nothing selected for catalog_id
          populate_options([]);
        } else if (product_data[catalog_id] !== undefined) {
          products = product_data[catalog_id];
          // Remove the previous choices
          populate_options(products);
        } else {
          // Ajax the custom audiences list for act
          var apiQuery = fbutils.api(
            '/' + catalog_id + '/products',
            'GET',
            {
              'fields': [
                'id',
                'name',
                'retailer_id',
              ],
              'limit': 100,
            }
          );
          apiQuery.then(function(result) {
            var loaded_products = result.data;
            populate_options(loaded_products);

            // If the widget is initialized with a previous value, it shall be
            // a page refresh so we wait for the current catalog_id select load then
            // set with the value
            if (initialValue &&
              initialValue in $(rtSelectId)[0].selectize.options) {
              $(rtSelectId)[0].selectize.setValue(initialValue);
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
