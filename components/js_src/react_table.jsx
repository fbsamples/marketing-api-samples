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
define(['react'], function(React) {

  var ReactTable = React.createClass({
    propTypes: {
      header: React.PropTypes.array.isRequired,
      data: React.PropTypes.array.isRequired,
      tableClasses: React.PropTypes.array,
    },

    render: function() {
      var extraClasses = '';
      if (this.props.tableClasses.length > 0) {
        extraClasses = this.props.tableClasses.join(' ');
      }
      return (
        <table className={'table ' + extraClasses}>
          <thead>
            <tr>{
              this.props.header.map(function(value, i) {
                return (<td key={i}>{value}</td>);
              })
            }</tr>
          </thead>
          <tbody>
            {
              this.props.data.map(function(row, rowIndex) {
                return (
                  <tr key={rowIndex}>{
                    Object.keys(row).map(function(key, colIndex) {
                      return (
                        <td key={'' + rowIndex + colIndex}>
                          {row[key]}
                        </td>
                      );
                    })
                  }</tr>
                );
              })
            }
          </tbody>
        </table>
      );
    },
  });

  return ReactTable;
});
