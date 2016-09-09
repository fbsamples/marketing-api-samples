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
define(['jquery', 'react'],
function($, React) {

  var SpecSelectContainer = React.createClass({displayName: 'SpecSelectContainer',

    getInitialState: function() {
      return {
        selected: this.props.selected || 0
      };
    },

    change: function(event) {
      this.setState({ selected: event.target.value });
    },

    render: function() {
      var select_options = [];
      this.props.specs.forEach(function(spec, index) {
        select_options.push(
          React.createElement('option', {value: index, key: index},
            spec.name
          )
        );
      });

      $('#' + this.props.targetId).val(this.state.selected);

      return (
        React.createElement('div', null,
          React.createElement('p', null,
            React.createElement('select', {value: this.state.selected,
              onChange: this.change},
              select_options
            )
          ),
          React.createElement('p', null,
          'Current Selected:',
          React.createElement('pre', null,
            this.props.specs[this.state.selected].spec
          )
          )
        )
      );
    }
  });

  // Load the react JS component
  var initialize = function(specSelectId, value, specsdata) {
    React.render(
      React.createElement(SpecSelectContainer, {
        targetId: specSelectId,
        selected: value,
        specs: specsdata}),
      document.getElementById(specSelectId + '_react')
    );
  };

  return {
    initialize: initialize,
  };

});
