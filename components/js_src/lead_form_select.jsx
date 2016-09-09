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
/* global define, FB */
define(
  ['react', 'fbutils'],
function(React, fbutils) {
  var LeadFormSelect = React.createClass({
    propTypes: {
      initialValue: React.PropTypes.string.isRequired,
      pageId: React.PropTypes.string.isRequired,
      onChange: React.PropTypes.func.isRequired,
    },

    getDefaultProps: function() {
      return {
        onChange: function() {},
      };
    },

    getInitialState: function() {
      return {
        formId: this.props.initialValue,
        status: null,
      };
    },

    onFormIdInputChange: function(event) {
      this.handleChanges(event.target.value);
    },

    handleChanges: function(formId) {
      this.setState({formId: formId});
      this.props.onChange(formId);
    },

    onCreateForm: function() {
      FB.ui({
        method: 'lead_gen',
        page_id: this.props.pageId,
        display: 'popup',
      }, function(response) {
        if (response.status === 'success') {
          this.handleChanges(response.formID);
          this.setState({
            'status': 'Successfully created form: ' + response.name +
              ' (' + response.formID + ')' +
              ' for page: ' + response.pageID,
          });
        } else {
          console.log(response);
        }
      }.bind(this));
    },

    render: function() {
      return (
        <div className="composer-body">
          <div className="form-group">
            <label htmlFor="form-id">Input existing lead form id:</label>
            <input type="number" id="form-id"
              className="form-control" name="form_id"
              onChange={this.onFormIdInputChange}
              value={this.state.formId}
            />
          </div>
          <label className="control-label" htmlFor="">
            Or create a new form
          </label>
          <br/>
          <button type="button"
            className="btn btn-success"
            onClick={this.onCreateForm}>
            Create New Lead Form
          </button>
          <div>
            {this.state.status ?
              <div className="bs-callout bs-callout-success">
                <h4>Success</h4>
                {this.state.status}
              </div> : null}
          </div>
        </div>
      );
    },
  });

  return LeadFormSelect;
});
