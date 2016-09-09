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
/*global define, window, document*/
// bootstrap so every page and component doesn't have to load it
// also initialize Google Analytics and FB Pixel
define(['jquery', 'bootstrap', 'fbutils'], function($, fbutils) {
  // Google Analytics initialization
  (function(i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r;
    i[r] = i[r] || function() {
      (i[r].q = i[r].q || []).push(arguments);
    };
    i[r].l = 1 * new Date();
    a = s.createElement(o);
    m = s.getElementsByTagName(o)[0];
    a.async = 1;
    a.src = g;
    m.parentNode.insertBefore(a, m);
  })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');
  window.ga('create', 'UA-73045824-1', 'auto');
  window.ga('send', 'pageview');

  // Facebook Pixel Initialization
  (function(f, b, e, v, n, t, s) {
    if (f.fbq) {return;}
    n = f.fbq = function() {
      n.callMethod ?
        n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    if (!f._fbq) {f._fbq = n;}
    n.push = n;
    n.loaded = !0;
    n.version = '2.0';
    n.queue = [];
    t = b.createElement(e);
    t.async = !0;
    t.src = v;
    s = b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t, s);
  })(window, document, 'script', '//connect.facebook.net/en_US/fbevents.js');
  window.fbq('init', '1426637120987747');
  window.fbq('track', 'PageView');

  // adding a namespace-scoped variable to the window
  // to make it accessible to inline script that just wants to track events
  window.eventsUtil = window.eventsUtil || {};
  window.eventsUtil.trackEvent = function(gaEventParams, fbEventParams) {
    if (gaEventParams) {
      window.ga.apply(null, gaEventParams);
    }
    if (fbEventParams) {
      window.fbq.apply(null, fbEventParams);
    }
    return;
  };
  return {
    eventsUtil: window.eventsUtil,
  };
});
