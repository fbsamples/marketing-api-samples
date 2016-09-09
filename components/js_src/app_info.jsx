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
  ['jquery', 'react', 'react-selectize', 'fbutils'],
  function($, React, ReactSelectize, fbutils) {

    var JsonResult = React.createClass({
      render: function() {
        var co_ref =
          <a href={'https://developers.facebook.com/docs/marketing-api/' +
          'connectionobjects/'}>connection objects</a>;

        return (
          <div>
            <label htmlFor="spec-panel">Result App Info:</label>
            <div id="spec-panel" className="panel panel-default">
              <div className="panel-body">
                <p>Current app:</p>
                <div>
                  <pre>{JSON.stringify(this.props.appInfo, null, 2)}</pre>
                </div>
                <br/>
                <p>Data retrived from the {co_ref} endpoint.</p>
              </div>
            </div>
          </div>
        );
      },
    });

    var _renderAppOption = function(item, escape) {
      return '<div>' +
        '<img class="picture" src=' + escape(item.picture.data.url) + ' />' +
        '<span>' + escape(item.name) +
        ' (' + escape(item.id) + ')</span>' +
        '</div>';
    };
    var _appRenderFunctions = {
      option: _renderAppOption,
      item: _renderAppOption,
    };

    var AppInfo = React.createClass({
      propTypes: {
        initialValue: React.PropTypes.object,
        onChange: React.PropTypes.func.isRequired,
        apps: React.PropTypes.array.isRequired,
      },

      getDefaultProps: function() {
        return {
          onChange: function() {},
        };
      },

      getInitialState: function() {
        return {
          // AppInfo JSON for the current selected app
          appInfo: this.props.initialValue,
        };
      },

      onAppChange: function(value) {
        var id = value;
        var apps = this.props.apps;
        var selectedAppInfo = null;

        if (value) {
          // Search for the CA based on ID
          apps.map(function(app) {
            if (app.id === id) {
              selectedAppInfo = app;
            }
          });
        }
        this.setState({appInfo: selectedAppInfo}, function() {
          this.props.onChange(selectedAppInfo);
        });
      },

      // The modal dialog HTML boilerplate
      render: function() {
        var selectedAppId = null;
        if (typeof this.state.appInfo.id !== 'undefined') {
          selectedAppId = this.state.appInfo.id;
        }

        return (
          <div>
            <ReactSelectize
              selectId="app-info-app-select"
              items={this.props.apps}
              value={selectedAppId}
              placeholder="- Select an application -"
              label="Application:"
              onChange={this.onAppChange}
              render={_appRenderFunctions}
            />
            <JsonResult
              appInfo={this.state.appInfo}
            />
          </div>
        );
      },
    });

    return AppInfo;
  }
);
