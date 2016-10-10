/**
 * Copyright (c) 2016-present, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

'use strict';
/* global define */
define(
  ['jquery', 'selectize', 'fbutils'],
function($, selectize, fbutils) {
  const querySearch = function(endpoint) {
          const apiQuery = fbutils.api(
            '/search',
            'GET',
            endpoint.param
          );

          apiQuery.then(function(result) {
            const interests= result.data;

            const munged = interests.map(
              (interest) => {
                return {
                  id: interest.id,
                  name: interest.name,
                  value: interest.name,
                  opt: endpoint.opt,
                  query: endpoint.query,
                };
              }
            );

            endpoint.callback(munged);

          }).catch(function(message) {
            console.log(message);
          });
  };

  // Takes in the DOM id for the interest select element.
  var initialize = function(
    interestSelectElementId, initialValue, appSelectElementId) {

    const appSelectId = '#' + appSelectElementId;
    const interestSelectId = '#' + interestSelectElementId;

    $(interestSelectId).ready(function() {

      $(appSelectId).ready(function() {
        $(appSelectId).blur(function() {
          try {
            const info = JSON.parse($(appSelectId).val());
            if (!initialValue || initialValue === '') {
              let list = info.name.split(' ');
              list.push(info.name);
              querySearch({
                param:
                {
                  'type': 'adinterestsuggestion',
                  'interest_list': list,
                },
                opt: 'Suggested',
                query: info.name,
                callback: (interests) => {
                  let suggestions = ['none'];
                  if (interests.length) {
                    suggestions = interests.slice(0, 3).map(
                      (interest) => {
                        return interest.name;
                      }
                    );
                  }
                  $(interestSelectId)[0].selectize.settings.placeholder =
                    'Suggested for ' + info.name  +': ' + suggestions.join(', ');
                  $(interestSelectId)[0].selectize.updatePlaceholder();
                }
              });
            }
          } catch(err) {}
        });
      });


      $(interestSelectId).selectize({
        persist: false,
        valueField: 'id',
        labelField: 'name',
        searchField: ['value', 'query'],
        preload: true,
        create: false,
        addPrecedence: false,
        lockOptgroupOrder: true,
        loadThrottle: 75,
        optgroups: [
          {value: 'Interests', label: 'Interests'},
          {value: 'Suggested', label: 'Suggested'},
        ],
        optgroupField: 'opt',
        load: function(query, callback) {

          const endpoints = [
            {param:
              {
                'type': 'adTargetingCategory',
                'class': 'interests',
               },
              opt: 'Interests',
              query: query,
              callback: (interests) => {
                callback(interests);

                if (initialValue) {
                  const interests = eval(initialValue);
                  $(interestSelectId)[0].selectize.setValue(interests, false);
                }
              },
            },
            {param:
              {
                'type': 'adinterestsuggestion',
                'interest_list': [query],
              },
              opt: 'Suggested',
              query: query,
              callback: (interests) => { callback(interests); },
            },
            {param:
              {
                'type': 'adinterest',
                'q': query,
              },
              opt: 'Interests',
              query: query,
              callback: (interests) => { callback(interests); },
            },
          ];

          if (query.length) {
            querySearch(endpoints[2]);
            querySearch(endpoints[1]);
          } else {
            querySearch(endpoints[0]);
          }
        }
      });

    });
  };

  return {
    initialize: initialize,
  };
});
