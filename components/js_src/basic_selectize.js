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

/*
Use this module if you just need the look and feel of selectize. Use it together
with SelectizeWidget to make your life easier. Define you own JS module and code
the behavior if you need dynamic loading of options or more complex stuff. Refer
to caselect.js module is a good start.
*/
'use strict';
/* global define */
define(['jquery', 'selectize'], function($, selectize) {

  // Takes in the DOM id for the target select element.
  var initialize = function(targetElementId, initialValues) {
    var targetId = '#' + targetElementId;
    var initValues = [];
    if (typeof initialValues === 'string') {
      if (initialValues.indexOf(',') > 0) {
        initValues = initialValues.split(',');
      } else {
        initValues = [initialValues];
      }
    }
    $(targetId).ready(function() {
      $(targetId).selectize();
      initValues.forEach(function(value) {
        if (value in $(targetId)[0].selectize.options) {
          $(targetId)[0].selectize.addItem(value);
        }
      });
    });
  };

  return {
    initialize: initialize,
  };
});
