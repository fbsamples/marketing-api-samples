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
define(['jquery', 'react'], function($, React) {

  var ReactModal = React.createClass({
    propTypes: {
      modalHeader: React.PropTypes.string.isRequired,
      modalBody: React.PropTypes.element.isRequired,
      targetId: React.PropTypes.string.isRequired,
      onSave: React.PropTypes.func.isRequired,
      onClose: React.PropTypes.func.isRequired,
    },

    getDefaultProps: function() {
      return {
        onSave: function() {},
        onClose: function() {},
      };
    },

    componentDidMount: function() {
      var targetId = this.props.targetId;
      $('#' + targetId + '_modal').on('hidden.bs.modal', function() {
        this.close();
      }.bind(this));

      var toggle_button = targetId + '_toggle';
      $('#' + toggle_button).attr('data-toggle', 'modal');
    },

    close: function() {
      var targetId = this.props.targetId;
      $('#' + targetId + '_modal').modal('hide');
      // Closed without saving, callback to reload the modal body
      this.props.onClose();
    },

    // Save the current spec using the callback function
    save: function() {
      this.props.onSave();
    },

    saveAndClose: function() {
      this.save();
      var targetId = this.props.targetId;
      $('#' + targetId + '_modal').modal('hide');
    },

    render: function() {
      var targetId = this.props.targetId;
      return (
        <div>
          <div className="modal fade" id={targetId + '_modal'}
          tabIndex="-1" role="dialog"
          aria-labelledby={targetId + '_label'} aria-hidden="true">
            <div className="modal-dialog modal-lg">
              <div className="modal-content">
                <div className="modal-header">
                  <button type="button" className="close"
                    onClick={this.close} aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                  <h4 className="modal-title" id={targetId + '_label'}>
                    {this.props.modalHeader}
                  </h4>
                </div>
                <div className="modal-body">
                  {this.props.modalBody}
                </div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-success"
                    onClick={this.saveAndClose}>
                    Save
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      );
    },
  });

  return ReactModal;
});
