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

/** @jsx React.DOM */
'use strict';
/*global define*/
define(['react', 'jquery', 'selectize'], function(React, $, selectize) {
  /* React selectize wrapper */
  var ReactSelectize = React.createClass({displayName: 'ReactSelectize',

    getDefaultProps: function() {
      return {
        valueField: 'id',
        labelField: 'name',
        searchField: 'name',
        sortField: 'id',
        create: false,
        items: []
      };
    },

    isMultiple: function(props) {
      // Selectize becomes 'multiple' when 'maxItems' is passed via settings
      return props.multiple || props.maxItems !== undefined;
    },

    buildOptions: function() {
      var o = {};

      o.valueField = this.props.valueField;
      o.labelField = this.props.labelField;
      o.searchField = this.props.searchField;
      o.sortField = this.props.sortField;
      if (this.isMultiple(this.props)) {
        o.maxItems = this.props.maxItems || null;
      }
      o.options = this.props.items;
      o.create = this.props.create;

      // Add support for custom render functions
      o.render = this.props.render;

      return o;
    },

    getSelectizeControl: function() {
      var selectId = '#' + this.props.selectId;
      var $select = $(selectId);
      var selectControl = $select[0] && $select[0].selectize;

      return selectControl;
    },

    handleChange: function(e) {

      // IF Selectize is not multiple
      if (!this.isMultiple(this.props)) {
        // THEN blur it before calling onChange to prevent dropdown reopening
        this.getSelectizeControl().blur();
      }

      if (this.props.onChange) {
        this.props.onChange(e);
      }
    },

    rebuildSelectize: function() {
      var $select = null;
      var selectControl = this.getSelectizeControl();
      var items = this.props.items;

      if (selectControl) {
        // rebuild
        selectControl.off();
        selectControl.clearOptions();
        selectControl.load(function(cb) { cb(items); });
      } else {
        // build new
        $select = $('#' + this.props.selectId).selectize(this.buildOptions());
        selectControl = $select[0].selectize;
      }

      selectControl.setValue(this.props.value);

      if (this.props.onChange) {
        selectControl.on('change', this.handleChange);
      }
    },

    componentDidMount: function() {
      this.rebuildSelectize();
    },

    componentDidUpdate: function() {
      this.rebuildSelectize();
    },

    render: function() {
      var classes = this.props.classes;
      return React.createElement('div', {className: classes && classes.length > 0 ? classes.join(' ') : ''},
        React.createElement('label', {htmlFor: this.props.selectId}, this.props.label),
        React.createElement('select', {id: this.props.selectId, placeholder: this.props.placeholder})
      );
    }
  });

  return ReactSelectize;
});
