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
    pcSelectElementId,
    initialValue,
    businessSelectElementId,
    limitCatalogs = 300
  ) {
    var pcSelectId = '#' + pcSelectElementId;
    var businessSelectId = '#' + businessSelectElementId;

    // product catalog picker
    $(pcSelectId).ready(function() {

      $(pcSelectId).selectize();

      // Cache the product catalogs list
      var product_catalog_data = {};

      var populate_options = function(catalogs) {
        clear_options();
        $(pcSelectId).append($('<option/>', {
          value: '',
          text: '- Choose a product catalog -',
        }));
        // Populate the product catalog selector
        $.map(catalogs, function(catalog) {
          $(pcSelectId).append(
            $('<option/>', {
              value: catalog.id,
              text: (catalog.name + ' (' + catalog.id + ')'),
            })
          );
        });
        $(pcSelectId).selectize();
      };

      var clear_options = function() {
        // Destroy the previous select list
        $(pcSelectId)[0].selectize.destroy();

        // Clear previous options
        $(pcSelectId).empty();
      };

      $(businessSelectId).change(function() {
        var business = $(businessSelectId).val();
        if (business === undefined || business === '') {
          return;
        }

        var product_catalogs = {};

        clear_options();
        $(pcSelectId).append($('<option/>', {
          value: '',
          text: '- Loading... -',
        })).selectize();

        if (business === '0') {
          // Nothing selected for business
          populate_options([]);
        } else if (product_catalog_data[business] !== undefined) {
          product_catalogs = product_catalog_data[business];
          // Remove the previous choices
          populate_options(product_catalogs);
        } else {
          // Ajax the custom audiences list for act
          var apiQuery = fbutils.api(
            '/' + business + '/product_catalogs',
            'GET',
            {
              'fields': [
                'id',
                'name',
              ],
              'limit': limitCatalogs,
            }
          );
          apiQuery.then(function(result) {
            var loaded_catalogs = result.data;
            populate_options(loaded_catalogs);

            // If the widget is initialized with a previous value, it shall be
            // a page refresh so we wait for the current business select load then
            // set with the value
            if (initialValue &&
              initialValue in $(pcSelectId)[0].selectize.options) {
              $(pcSelectId)[0].selectize.setValue(initialValue);
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
