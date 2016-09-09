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

//   Sample JS module
//
//   initializes other modules needed by samples
//
//   tracks sample view and sample run events

/*global define, window, document*/

'use strict';

define(['main', 'jquery'], function(main, $) {

  function _getFbEventParams() {
    return {
      'content_ids': [window.app_config.sample_id],
      'content_type': 'product',
    };
  }

  function _getGAEventParams(action) {
    return {
      hitType: 'event',
      eventCategory: 'Sample',
      eventAction: action,
      eventLabel: window.app_config.sample_id,
    };
  }
  // hook the form submit
  // to track when a sample runs
  $(document).ready(function() {
    // track the view sample event
    // using GA and FB Pixel
    main.eventsUtil.trackEvent([
      'send',
      _getGAEventParams('view'),
    ], [
      'track',
      'ViewContent',
      _getFbEventParams(),
    ]);
    // hook form submit to track sample run
    $('form').submit(function() {
      // track the run sample event
      main.eventsUtil.trackEvent([
        'send',
        _getGAEventParams('run'),
      ], [
        'track',
        'InitiateCheckout',
        _getFbEventParams(), // will use Purchase for sample code download
      ]);
    });
  });

  return {
    // expose any common sample utils here
  };
});
