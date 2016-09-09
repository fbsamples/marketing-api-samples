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
  ['jquery', 'react', 'components/react_modal', 'components/bid_composer'],
function($, React, ReactModal, BidComposer) {
  // Load the react JS component
  var initialize = function(biddingInfoId, initialValue, fieldBaseName, objective) {
    BidComposer = React.createFactory(BidComposer);
    ReactModal = React.createFactory(ReactModal);

    var fieldName = {
      optimizationGoal: 'id_' + fieldBaseName + '_0',
      billingEvent: 'id_' + fieldBaseName + '_1',
      bidAmount: 'id_' + fieldBaseName + '_2',
      textBase: 'id_' + fieldBaseName + '_3',
    };

    var initialBidInfo = {
      optimizationGoal: $('#' + fieldName.optimizationGoal).val(),
      billingEvent: $('#' + fieldName.billingEvent).val(),
      bidAmount: $('#' + fieldName.bidAmount).val(),
    };

    // If empty
    if (initialBidInfo.optimizationGoal == '' &&
      initialBidInfo.billingEvent == '') {
      $('#' + fieldName.textBase).val('click to open dialog.');
    }

    var bid_setting = $('#' + fieldName.textBase);
    bid_setting.next('span.input-group-addon')
      .attr('id', biddingInfoId + '_toggle')
      .attr('data-target', '#' + biddingInfoId + '_modal');

    $('<div id="' + biddingInfoId + '_react"></div>')
      .insertAfter(bid_setting);

    var currentBidInfo = initialBidInfo;

    var onSave = function() {
      var value = currentBidInfo;

      $('#' + fieldName.billingEvent).val(
        value.billingEvent
      );
      $('#' + fieldName.optimizationGoal).val(
        value.optimizationGoal
      );
      $('#' + fieldName.bidAmount).val(
        value.bidAmount
      );

      $('#' + fieldName.textBase).val(
        'Opt. Goal: ' + value.optimizationGoal + ', ' +
        'Bill Event: ' + value.billingEvent + ', ' +
        'Amount: ' + value.bidAmount
      );
    };

    var onChange = function(value) {
      currentBidInfo = value;
    };

    var bid_composer = new BidComposer({
      optimizationGoal: initialBidInfo.optimizationGoal,
      billingEvent: initialBidInfo.billingEvent,
      bidAmount: initialBidInfo.bidAmount,
      objective: objective,
      onChange: onChange,
    });

    React.render(
      new ReactModal({
        modalBody: bid_composer,
        modalHeader: 'Bid Setting',
        targetId: biddingInfoId,
        onSave: onSave,
      }),
      document.getElementById(biddingInfoId + '_react')
    );
  };

  return {
    initialize: initialize,
  };
});
