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
  ['jquery', 'react', 'components/react_modal',
    'components/lead_form_select'],
function($, React, ReactModal, LeadFormSelect) {
  // Load the react JS component
  var initialize = function(leadFormId, initialValue, pageSelectId) {
    LeadFormSelect = React.createFactory(LeadFormSelect);
    ReactModal = React.createFactory(ReactModal);

    var reactElementId = leadFormId + '_react';
    var toggleButtonId = leadFormId + '_modal';

    var hasOldData = false;
    if (initialValue !== '') {
      hasOldData = true;
    }

    var form_select = $('#' + leadFormId);
    form_select.val(initialValue)
      .next('span.input-group-addon')
      .attr('id', leadFormId + '_toggle')
      .attr('data-target', '#' + leadFormId + '_modal');

    $('<div id="' + leadFormId + '_react"></div>')
      .insertAfter(form_select);

    var refresh = function() {
      var pageId = $('#' + pageSelectId).val();
      if (pageId) {
        $('#' + toggleButtonId).attr('data-toggle', 'modal');

        // Unmount previous component and render new one with loaded apps
        var element = document.getElementById(reactElementId);
        if (element) {
          React.unmountComponentAtNode(element);
        }
        var selectedFormId = $('#' + leadFormId).val();
        render(pageId, selectedFormId);
      } else {
        $('#' + toggleButtonId).removeAttr('data-toggle');
      }
    };

    var render = function(pageId, formId) {
      var formSelect = new LeadFormSelect({
        initialValue: formId,
        pageId: pageId,
        onChange: onChange,
      });
      React.render(
        new ReactModal({
          modalHeader: 'Select Lead Gen Form',
          modalBody: formSelect,
          targetId: leadFormId,
          onSave: onSave,
          onClose: onClose,
        }),
        document.getElementById(reactElementId)
      );
    };

    var currentFormId = initialValue;

    var onChange = function(value) {
      currentFormId = value;
    };
    var onSave = function() {
      console.log('Save! ' + currentFormId);
      // Write out the currently selected app
      $('#' + leadFormId).val(currentFormId);
    };

    var onClose = function() {
      refresh();
    };

    // Listen to the change event from page select, revert form id to null.
    $('#' + pageSelectId).change(function(event) {
      var formId = '';
      if (hasOldData) {
        formId = initialValue;
        hasOldData = false;
      }
      $('#' + leadFormId).val(formId);
      refresh();
    });
  };

  return {
    initialize: initialize,
  };
});
