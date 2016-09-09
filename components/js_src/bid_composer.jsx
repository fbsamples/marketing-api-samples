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
  ['react', 'react-selectize'],
function(React, ReactSelectize) {
  var BidAmountComponent = React.createClass({
    propTypes: {
      bidAmount: React.PropTypes.string.isRequired,
      onBidAmountChange: React.PropTypes.func.isRequired,
    },

    getDefaultProps: function() {
      return {
        onBidAmountChange: function() {},
      };
    },

    onBidAmountChange: function(e) {
      var bidAmount = e.target.value;
      this.props.onBidAmountChange(bidAmount);
    },

    render: function() {
      return (
        <div id="bid-amount" className="row">
          <div className="col-md-12">
          <label htmlFor="bid-amount">Bid amount:</label>
          <input type="number" id="bid-amount-text" step="1"
            className="form-control" name="bid-amount"
            placeholder="to bid $1.00, set 100"
            onChange={this.onBidAmountChange}
            value={this.props.bidAmount}
          />
          </div>
        </div>
      );
    },
  });

  var BidComposer = React.createClass({
    propTypes: {
      objective: React.PropTypes.string,
      optimizationGoal: React.PropTypes.string,
      billingEvent: React.PropTypes.string,
      bidAmount: React.PropTypes.string,
      onChange: React.PropTypes.func.isRequired,
    },

    getDefaultProps: function() {
      return {
        onChange: function() {},
      };
    },

    getInitialState: function() {

      // refresh optimization goal bases on objective
      var optimizationGoals = this.filterOptimizationGoal(
        this.props.objective
      );

      // determine default value.
      var selectedOptimizationGoal = optimizationGoals[0].id;
      if (
        this.props.optimizationGoal !== undefined &&
        this.props.optimizationGoal !== ''
      ) {
        selectedOptimizationGoal = this.props.optimizationGoal;
      }

      // refresh billing events based on optimization goal
      var billingEvents = this.filterBillingEvents(selectedOptimizationGoal);
      var selectedBillingEvent = billingEvents[0].id;
      if (
        this.props.billingEvent !== undefined &&
        this.props.billingEvent !== ''
      ) {
        selectedBillingEvent = this.props.billingEvent;
      }

      var bidAmount = this.props.bidAmount;

      return {
        optimizationGoals: optimizationGoals,
        optimizationGoal: selectedOptimizationGoal,
        billingEvents: billingEvents,
        billingEvent: selectedBillingEvent,
        bidAmount: bidAmount,
      };
    },

    componentDidMount: function() {
      // Write out default values if nothing was passed
      this.handleChanges();
    },

    onOptimizationGoalChange: function(optimizationGoal) {
      var billingEvents = this.filterBillingEvents(optimizationGoal);
      this.setState({
        billingEvents: billingEvents,
        optimizationGoal: optimizationGoal,
      }, function() {
        this.handleChanges();
      }.bind(this));
    },

    onBillingEventChange: function(billingEvent) {
      this.setState({
        billingEvent: billingEvent,
      }, function() {
        this.handleChanges();
      }.bind(this));
    },

    onBidAmountChange: function(bidAmount) {
      // Controlled input works slightly differently
      this.setState({
        bidAmount: bidAmount,
      }, function() {
        this.handleChanges();
      }.bind(this));
    },

    handleChanges: function() {
      this.props.onChange({
        optimizationGoal: this.state.optimizationGoal,
        billingEvent: this.state.billingEvent,
        bidAmount: this.state.bidAmount,
      });
    },

    filterOptimizationGoal: function(objective) {
      // this block corresponds to:
      // https://developers.facebook.com/docs/marketing-api/validation/v2.6
      var availableOptimizationGoals = {
        'BRAND_AWARENESS':
          [
            'BRAND_AWARENESS',
            'REACH',
          ],

        'CANVAS_APP_ENGAGEMENT':
          [
            'ENGAGED_USERS',
            'APP_INSTALLS',
            'IMPRESSIONS',
            'POST_ENGAGEMENT',
            'REACH',
          ],

        'CANVAS_APP_INSTALLS':
          [
            'APP_INSTALLS',
            'IMPRESSIONS',
            'POST_ENGAGEMENT',
          ],

        'CONVERSIONS':
          [
            'OFFSITE_CONVERSIONS',
            'IMPRESSIONS',
            'LINK_CLICKS',
            'POST_ENGAGEMENT',
            'REACH',
            'SOCIAL_IMPRESSIONS',
          ],

        'EVENT_RESPONSES':
          [
            'EVENT_RESPONSES',
            'IMPRESSIONS',
            'REACH',
            'POST_ENGAGEMENT',
          ],

        'LEAD_GENERATION':
          [
            'LEAD_GENERATION',
            'LINK_CLICKS',
          ],

        'LINK_CLICKS':
          [
            'LINK_CLICKS',
            'IMPRESSIONS',
            'POST_ENGAGEMENT',
            'REACH',
          ],

        'LOCAL_AWARENESS':
          [
            'REACH',
          ],

        'MOBILE_APP_ENGAGEMENT':
          [
            'LINK_CLICKS',
            'IMPRESSIONS',
            'REACH',
            'OFFSITE_CONVERSIONS',
          ],

        'MOBILE_APP_INSTALLS':
          [
            'APP_INSTALLS',
            'LINK_CLICKS',
            'IMPRESSIONS',
            'REACH',
          ],

        'OFFER_CLAIMS':
          [
            'OFFER_CLAIMS',
            'IMPRESSIONS',
            'POST_ENGAGEMENT',
          ],

        'PAGE_LIKES':
          [
            'PAGE_LIKES',
            'IMPRESSIONS',
            'PAGE_ENGAGEMENT',
            'POST_ENGAGEMENT',
            'REACH',
          ],

        'POST_ENGAGEMENT':
          [
            'POST_ENGAGEMENT',
            'IMPRESSIONS',
            'LINK_CLICKS',
            'PAGE_ENGAGEMENT',
            'REACH',
            'VIDEO_VIEWS',
          ],

        'PRODUCT_CATALOG_SALES':
          [
            'LINK_CLICKS',
            'IMPRESSIONS',
            'POST_ENGAGEMENT',
            'OFFSITE_CONVERSIONS',
            'REACH',
          ],

        'VIDEO_VIEWS':
          [
            'VIDEO_VIEWS',
            'REACH',
          ],

        'NONE':
          [
            'APP_INSTALLS',
            'BRAND_AWARENESS',
            'ENGAGED_USERS',
            'EVENT_RESPONSES',
            'IMPRESSIONS',
            'LEAD_GENERATION',
            'LINK_CLICKS',
            'OFFER_CLAIMS',
            'OFFSITE_CONVERSIONS',
            'PAGE_ENGAGEMENT',
            'PAGE_LIKES',
            'POST_ENGAGEMENT',
            'REACH',
            'SOCIAL_IMPRESSIONS',
            'VIDEO_VIEWS',
          ],

      };

      var result = [];
      if (availableOptimizationGoals.hasOwnProperty(objective)) {
        result = availableOptimizationGoals[objective];
      } else {
        result = availableOptimizationGoals['NONE'];
      }
      var idNameObjArray = result.map(function(element) {
        return {id: element, name: element};
      });
      return idNameObjArray;
    },

    filterBillingEvents: function(optimizationGoal) {
      // this block corresponds to:
      // https://developers.facebook.com/docs/marketing-api/validation/v2.6

      // Extra billing events for specific optimization goal:
      var availableBillingEvents = {
        'APP_INSTALLS': ['APP_INSTALLS'],
        'LEAD_GENERATION': ['LINK_CLICKS'],
        'LINK_CLICKS': ['LINK_CLICKS'],
        'OFFER_CLAIMS': ['OFFER_CLAIMS'],
        'PAGE_LIKES': ['PAGE_LIKES'],
        'POST_ENGAGEMENT': ['POST_ENGAGEMENT'],
        'VIDEO_VIEWS': ['VIDEO_VIEWS'],
      };
      // IMPRESSIONS is available for all
      var result = ['IMPRESSIONS'];
      if (availableBillingEvents.hasOwnProperty(optimizationGoal)) {
        result = result.concat(availableBillingEvents[optimizationGoal]);
      }

      var idNameObjArray = result.map(function(element) {
        return {id: element, name: element};
      });
      return idNameObjArray;
    },

    render: function() {
      return (
        <div>
          <ReactSelectize
            items={this.state.optimizationGoals}
            value={this.state.optimizationGoal}
            selectId="select-optimization-goal"
            placeholder="- Select optimization goal -"
            label="Optimization goal:"
            multiple={false}
            onChange={this.onOptimizationGoalChange}
          />
          <ReactSelectize
            items={this.state.billingEvents}
            value={this.state.billingEvent}
            selectId="select-billing-event"
            placeholder="- Select billing event -"
            label="Billing event:"
            multiple={false}
            onChange={this.onBillingEventChange}
          />
          <BidAmountComponent
            onBidAmountChange={this.onBidAmountChange}
            bidAmount={this.state.bidAmount}
          />
        </div>
      );
    },
  });

  return BidComposer;
});
