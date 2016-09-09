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
/*global window*/
window.require = {
  baseUrl: '/static/scripts',
  paths: {
    // External libraries
    'facebook': '//connect.facebook.net/en_US/sdk',
    'jquery': '//ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min',
    'bootstrap': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min',
    'jasny-bootstrap': '//cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/js/jasny-bootstrap.min',
    'datetimepicker':
      '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.15.35/js/bootstrap-datetimepicker.min',
    'moment': '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.3/moment.min',
    'selectize': '//cdnjs.cloudflare.com/ajax/libs/selectize.js/0.12.2/js/standalone/selectize.min',
    'react': '//cdnjs.cloudflare.com/ajax/libs/react/0.13.3/react.min',
    // Paths
    'components': '/static/scripts/components',
    'samples': '/static/samples/scripts',
    // Local libraries
    'country_list': 'lib/country_list',
    'react-selectize': 'lib/react-selectize',
  },
  shim: {
    'facebook': {
      exports: 'FB'
    },
    'bootstrap': {
      deps: ['jquery']
    },
    'jasny-bootstrap': {
      deps: ['bootstrap']
    },
    'selectize': {
      deps: ['jquery']
    },
    'datetimepicker': {
      deps: ['moment', 'jquery']
    },
    'react-selectize': {
      deps: ['react', 'selectize']
    }
  },
  deps: ['main'],
};
