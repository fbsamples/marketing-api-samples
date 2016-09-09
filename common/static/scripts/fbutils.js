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

 // facebook utilities
//
//   initializes FB checks session status
//
//   utility functions for FB api, login, permission checking and session management

/*global define, window*/

'use strict';

define(['facebook'], function(FB) {

  var MAX_API_RETRIES = 5;
  var SESSION_EXPIRATION = 30 * 24 * 60 * 60 * 1000; // 30 days
  var currentPermissions = [];
  var sessionChangeSubscribers = [];
  // initialize Facebook
  //   window.fbAsyncInit not needed.  FB SDK loaded by requireJS and required by this module
  //   see https://developers.facebook.com/docs/javascript/howto/requirejs/
  FB.init({
    appId      : window.app_config.fbAppId, // Facebook App ID
    channelUrl : window.app_config.channelUrl,
    status     : true, // check login status
    cookie     : false,
    xfbml      : true,  // parse XFBML
    version    : 'v2.6',
  });

  function isUserConnected() {
    return new Promise(function(resolve, reject) {
      FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
          resolve('user is connected');
        } else {
          reject('user is not connected');
        }
      });
    });
  }



  /* Call FB.api() with basic session expiration error handling and return a Promise
   *   parameters:
   *     path (String): url path (eg: '/me')
   *     method (String): http method (default 'GET')
   *     params (Object): parameters for the query
   *   return:
   *     Promise
   */
  function api() {
    var retries = 0;
    var args = Array.prototype.slice.call(arguments, 0);

    return new Promise(function(resolve, reject) {
        // API response handler
        var cb = function (response) {
          if (response && response.error) {
            if (retries === 0 && FB.getAuthResponse() === null) {
              // some type of auth error. try to get a new access token
              FB.getLoginStatus(function (newResponse) {
                if (newResponse.status === 'connected') {
                  retries += 1;
                  FB.api.apply(FB, args.concat(cb));
                } else {
                  reject(newResponse.status);
                }
              });
            } else if (response.error.code === 1 || response.error.code === 2) {
              // FB guidance is to retry on these error codes:
              //   https://developers.facebook.com/docs/reference/api/errors/
              retries += 1;
              FB.api.apply(FB, args.concat(cb));
            } else {
              reject(response.error);
            }
          } else {
            resolve(response);
          }
        };
        // first API call
        isUserConnected().then(function() {
          FB.api.apply(FB, args.concat(cb));
        }, function() {
          console.log('Can\'t call API because user is not connected');
          reject();
        });
    });
  }

  function sessionChanged() {
    sessionChangeSubscribers.forEach(function (cb) {
      cb();
    });
  }

  // must be called via user-triggered function due to popup-blockers
  function login(scope) {
    return new Promise(function(resolve, reject) {
        FB.login(function (response) {
          if (response.authResponse) {
            getUser(response.authResponse).then(function (user) {
              resolve(user);
              sessionChanged();
            });
          } else {
            reject('user did not authorize the app');
            sessionChanged();
          }
        }, {scope: scope});
    });
  }

  // 'private'  check if I already have the permissions i need
  function hasPerms(perms) {
    for (var p in perms) {
      if (!currentPermissions[perms[p]]) {
        return false;
      }
    }
    return true;
  }

  // must be called via user-triggered function due to popup-blockers
  // Use this to login or requesting new permissions
  function checkPermissions(permsNeeded) {
    return new Promise(function(resolve, reject) {
        if (hasPerms(permsNeeded)) {
          resolve();
        } else {
          FB.login(function (response) {
            if (response && response.authResponse && response.authResponse.grantedScopes) {
              response.authResponse.grantedScopes.split(',').forEach(function (p) {
                currentPermissions[p] = 1;
              });
            }
            if (hasPerms(permsNeeded)) {
              resolve();
            } else {
              reject('The requested permission was not granted');
            }
          }, {scope: permsNeeded.join(','), return_scopes: true});
        }
    });
  }

  function getPicture(user, size) {
    var url = 'https://graph.facebook.com/' + user.get('userid') + '/picture?';
    url += size === 'large' ? 'width=200&height=200' : 'width=30&height=30';
    url += '&access_token=' +
      user.current().get('authData').facebook.access_token;
    return url;
  }

  // 'private' - get a parse user from the FB user
  function getUser(authResponse) {
    return new Promise(function(resolve, reject) {
        var fbAuthObject = {
          'id': authResponse.userID,
          'access_token': authResponse.accessToken,
          'expiration_date': new Date(
            Date.now() + (authResponse.expiresIn * 1000)
          ).toISOString(),
        };
        api('/me/permissions').then(function (response) {
          if (response && response.data) {
            currentPermissions = response.data[0];
            resolve(fbAuthObject);
          } else {
            reject('could not get current permissions');
          }
        });
    });
  }

  function logout() {
    FB.logout(function(response) {
      console.log(response);
    });
  }

  return {
    api: api,
    getPicture: getPicture,
    checkPermissions: checkPermissions,
    logout: logout,
  };

});
