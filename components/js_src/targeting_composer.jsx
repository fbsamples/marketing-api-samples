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
/*global define*/
define(
  ['react', 'react-selectize', 'fbutils'],
function(React, ReactSelectize, fbutils) {
  var RightColumn = React.createClass({
    render: function() {
      var reach_estimate = parseInt(this.props.reachestimate, 10);
      if (isNaN(reach_estimate)) {
        reach_estimate = this.props.reachestimate;
      } else {
        // Audience size number with comma
        reach_estimate = reach_estimate.toString().replace(
          /\B(?=(\d{3})+(?!\d))/g,
          ','
        );
      }

      var reach_estimate_link = (
        <a href=
          "https://developers.facebook.com/docs/marketing-api/reachestimate/"
          target="_blank">
          reach estimate
        </a>
      );
      return (
        <div>
          <label>Targeting Description:</label>
          <TargetingDescription
            targetingsentencelines={this.props.targetingsentencelines}
          />
          <label>Current Targeting Spec: </label>
          <div><pre style={{maxHeight:'300px', overflow:'scroll'}}>
            <code language="JavaScript">
              {JSON.stringify(this.props.spec, null, 2)}
            </code>
          </pre></div>
          <label>Estimated audience size:</label>
          <p>{reach_estimate}</p>
          <p>Data retrieved from the {reach_estimate_link} endpoint.</p>
        </div>
      );
    },
  });

  var TargetingDescription = React.createClass({
    render: function() {
      var sentences = this.props.targetingsentencelines;
      var items = [];
      if (!sentences.length) {
        items.push(
          <li key="all">
            <p>Everyone</p>
          </li>
        );
      } else {
        items = sentences.map(function(sentence, index) {
          if (!sentence.content) {
            return <li key={sentence}>{sentence}</li>;
          }
          return (
            <li key={sentence.content + '.' + index}>
              <div>
                {sentence.content}
              </div>
              <ul>
                {(sentence.children || []).map(function(child, childIndex) {
                  return (
                    <li key={child}>
                      {child}
                    </li>
                  );
                })}
              </ul>
            </li>
          );
        });
      }

      return (
        <pre style={{maxHeight:'300px', overflow:'scroll'}}>
          <ul className="list-unstyled">
            {items}
          </ul>
        </pre>
      );
    },
  });

  var AgeComponent = React.createClass({
    propTypes: {
      ageMin: React.PropTypes.string,
      ageMax: React.PropTypes.string,
      onAgeChange: React.PropTypes.func.isRequired,
    },

    getDefaultProps: function() {
      return {
        onAgeChange: function() {},
      };
    },

    getInitialState: function() {
      return {
        ageMin: '',
        ageMax: '',
      };
    },
    onAgeChange: function(e) {
      if (e.target.name === 'age_min') {
        this.setState({ageMin: e.target.value});
      } else if (e.target.name === 'age_max') {
        this.setState({ageMax: e.target.value});
      }

      this.props.onAgeChange(e);
    },
    // Hack: Use the props sent from parent to override the state. This happens
    // when you close the composer without saving and open the composer again,
    // the spec will be different from the previous age setting.
    componentWillReceiveProps: function(props) {
      this.setState({
        ageMin: props.ageMin,
        ageMax: props.ageMax,
      });
    },

    render: function() {
      return (
        <div id="age-form" className="row">
          <div className="col-md-6">
            <label htmlFor="age-min">Age min:</label>
            <input type="number" id="age-min" min="13" max="65" step="1"
              className="form-control" name="age_min"
              placeholder="default to 18, min is 13"
              onChange={this.onAgeChange}
              value={this.state.ageMin}
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="age-max">Age max:</label>
            <input type="number" id="age-max" min="13" max="65" step="1"
              className="form-control" name="age_max"
              placeholder="default to 65, max is 65"
              onChange={this.onAgeChange}
              value={this.state.ageMax}
            />
          </div>
        </div>
      );
    },
  });

  var ComposerBody = React.createClass({
    propTypes: {
      spec: React.PropTypes.object.isRequired,
      countryList: React.PropTypes.array.isRequired,
      customAudiences: React.PropTypes.array.isRequired,
      onCountryChange: React.PropTypes.func.isRequired,
      onExcludedCountryChange: React.PropTypes.func.isRequired,
      onCaChange: React.PropTypes.func.isRequired,
      onExcludedCaChange: React.PropTypes.func.isRequired,
      onAgeChange: React.PropTypes.func.isRequired,
      onGenderChange: React.PropTypes.func.isRequired,
      onOsChange: React.PropTypes.func.isRequired,
      onPublisherPlatformsChange: React.PropTypes.func.isRequired,
      onDevicePlatformsChange: React.PropTypes.func.isRequired,
      onFacebookPositionsChange: React.PropTypes.func.isRequired,
    },
    render: function() {
      // We need to translate the spec back to the option values for each child
      var spec = this.props.spec;

      var selectedCountries = [];
      if ('geo_locations' in spec) {
        if ('countries' in spec.geo_locations) {
          selectedCountries = spec.geo_locations.countries;
        }
      }
      var selectedExcludedCountries = [];
      if ('excluded_geo_locations' in spec) {
        if ('countries' in spec.excluded_geo_locations) {
          selectedExcludedCountries = spec.excluded_geo_locations.countries;
        }
      }

      var selectedCas = [];
      if ('custom_audiences' in spec) {
        spec.custom_audiences.map(function(ca) {
          selectedCas.push(ca.id);
        });
      }
      var selectedExcludedCas = [];
      if ('excluded_custom_audiences' in spec) {
        spec.excluded_custom_audiences.map(function(ca) {
          selectedExcludedCas.push(ca.id);
        });
      }

      var genders = [
        {id: '1', name: 'male'},
        {id: '2', name: 'female'},
      ];
      var selectedGenders = [];
      if ('genders' in spec) {
        selectedGenders = spec.genders;
      }

      var ageMin = '';
      if ('age_min' in spec) {
        ageMin = spec.age_min;
      }
      var ageMax = '';
      if ('age_max' in spec) {
        ageMax = spec.age_max;
      }

      var userOs = [
        {id: 'iOS', name: 'iOS'},
        {id: 'Android', name: 'Android'},
      ];
      var selectedOs = [];
      if ('user_os' in spec) {
        selectedOs = spec.user_os;
      }

      var device_platforms = [
        {id: 'mobile', name: 'mobile'},
        {id: 'desktop', name: 'desktop'}
      ];

      var publisher_platforms = [
        {id: 'facebook', name: 'facebook'},
        {id: 'instagram', name: 'instagram'},
        {id: 'audience_network', name: 'audience_network'}
      ];

      var facebook_positions = [
        {id: 'feed', name: 'feed'},
        {id: 'right_hand_column', name: 'right_hand_column'}
      ];

      var selectedDevicePlatforms = null;
      if ('device_platforms' in spec) {
        selectedDevicePlatforms = spec.device_platforms;
      }

      var selectedPublisherPlatforms = null;
      if ('publisher_platforms' in spec) {
        selectedPublisherPlatforms = spec.publisher_platforms;
      }

      var selectedFacebookPositions = null;
      if ('facebook_positions' in spec) {
        selectedFacebookPositions = spec.facebook_positions;
      }

      return (
        <div className="composer-body">
          <ReactSelectize
            items={this.props.countryList}
            value={selectedCountries}
            selectId="select-country"
            placeholder="- Select countries -"
            label="Countries:"
            multiple={true}
            onChange={this.props.onCountryChange}
          />
          <ReactSelectize
            items={this.props.countryList}
            value={selectedExcludedCountries}
            selectId="select-excluded-country"
            placeholder="- Select countries -"
            label="Excluded Countries:"
            multiple={true}
            onChange={this.props.onExcludedCountryChange}
          />
          <AgeComponent
            ageMin={ageMin}
            ageMax={ageMax}
            onAgeChange={this.props.onAgeChange}
          />
          <ReactSelectize
            items={genders}
            value={selectedGenders}
            selectId="select-gender"
            placeholder="- Select gender, default to all -"
            label="Genders:"
            multiple={true}
            onChange={this.props.onGenderChange}
          />
          <ReactSelectize
            items={userOs}
            value={selectedOs}
            selectId="select-os"
            placeholder="- Select device OS -"
            label="Device OS:"
            multiple={true}
            onChange={this.props.onOsChange}
          />
          <ReactSelectize
            items={device_platforms}
            value={selectedDevicePlatforms}
            selectId="select-device-platforms"
            placeholder={'- Select device platforms,' +
              ' default to both mobile and desktop -'}
            label="Device platforms:"
            multiple={true}
            onChange={this.props.onDevicePlatformsChange}
          />
          <ReactSelectize
            items={publisher_platforms}
            value={selectedPublisherPlatforms}
            selectId="select-publisher-platforms"
            placeholder={'- Select publisher platforms,' +
              ' default to all Facebook, Instagram and Audience Network -'}
            label="Publisher platforms:"
            multiple={true}
            onChange={this.props.onPublisherPlatformsChange}
          />
          <ReactSelectize
            items={facebook_positions}
            value={selectedFacebookPositions}
            selectId="select-facebook-positions"
            placeholder={'- Select Facebook positions,' +
              ' default to both feed and right hand column -'}
            label="Facebook positions:"
            multiple={true}
            onChange={this.props.onFacebookPositionsChange}
          />
          <ReactSelectize
            items={this.props.customAudiences}
            value={selectedCas}
            selectId="select-ca"
            placeholder="- Select custom audiences -"
            label="Custom audiences:"
            multiple={true}
            onChange={this.props.onCaChange}
          />
          <ReactSelectize
            items={this.props.customAudiences}
            value={selectedExcludedCas}
            selectId="select-excluded-ca"
            placeholder="- Select custom audiences -"
            label="Excluded Custom audiences:"
            multiple={true}
            onChange={this.props.onExcludedCaChange}
          />
        </div>
      );
    },
  });

  var TargetingComposer = React.createClass({
    propTypes: {
      accountId: React.PropTypes.string.isRequired,
      customAudiences: React.PropTypes.array.isRequired,
      countryList: React.PropTypes.array.isRequired,
      onChange: React.PropTypes.func.isRequired,
      initialValue: React.PropTypes.object.isRequired,
    },

    getDefaultProps: function() {
      return {
        onChange: function() {},
      };
    },

    getInitialState: function() {
      return {
        ca: [],
        spec: this.props.initialValue,
        reachestimate: 0,
        targetingsentencelines: [],
      };
    },

    // Verifies the current targeting setting by calling reach estimate
    estimate: function() {
      var spec = this.state.spec;
      var error_msg = 'Something went wrong, please try again...';

      // Ajax to the reach estimate endpoint to check on the audience size
      var apiQuery = fbutils.api(
        '/' + this.props.accountId + '/reachestimate',
        'GET',
        {
          'currency': 'USD',
          'optimize_for': 'IMPRESSIONS', // Default for impressions
          'targeting_spec': spec,
        }
      );
      apiQuery.then(function(result) {
        var estimate = result.data.users;
        this.setState({reachestimate: estimate});
      }.bind(this)).catch(function(message) {
        console.log(message);
        this.setState({reachestimate: message});
        this.setState({isDirty: false});
      }.bind(this));

      // Ajax to the targetingsentecelines endpoint to get description
      var descQuery = fbutils.api(
        '/' + this.props.accountId + '/targetingsentencelines',
        'GET',
        {
          'targeting_spec': spec,
        }
      );
      descQuery.then(function(response) {
        var description = response.targetingsentencelines;
        this.setState({targetingsentencelines: description});
      }.bind(this)).catch(function(reason) {
        console.log(reason);
        this.setState({targetingsentencelines: [error_msg]});
      }.bind(this));
    },

    handleSpecValueChange: function(key, value) {
      // Replace the key=>value in the spec, or remove the key if value is null
      var spec = this.state.spec;
      if (value === undefined || value === null || value.length === 0) {
        delete spec[key];
      } else {
        spec[key] = value;
      }
      this.setState({spec: spec});
      this.estimate();

      this.props.onChange(spec);
    },

    onCountryChange: function(value) {
      var countries = {'countries': value};
      if (value === null) {
        countries = null;
      }
      this.handleSpecValueChange('geo_locations', countries);
    },

    onExcludedCountryChange: function(value) {
      var countries = {'countries': value};
      if (value === null) {
        countries = null;
      }
      this.handleSpecValueChange('excluded_geo_locations', countries);
    },

    onAgeChange: function(e) {
      this.handleSpecValueChange(e.target.name, e.target.value);
    },

    onGenderChange: function(value) {
      this.handleSpecValueChange('genders', value);
    },

    onOsChange: function(value) {
      this.handleSpecValueChange('user_os', value);
    },

    onDevicePlatformsChange: function(value) {
      this.handleSpecValueChange('device_platforms', value);
    },

    onPublisherPlatformsChange: function(value) {
      this.handleSpecValueChange('publisher_platforms', value);
    },

    onFacebookPositionsChange: function(value) {
      this.handleSpecValueChange('facebook_positions', value);
    },

    onCaChange: function(value) {
      var caSpec = [];
      var customAudiences = this.props.customAudiences;

      if (value) {
        value.map(function(id) {
          // Search for the CA based on ID
          if (customAudiences !== undefined) {
            customAudiences.map(function(ca) {
              if (ca.id === id) {
                caSpec.push({id: ca.id});
              }
            });
          }
        });
      }
      this.handleSpecValueChange('custom_audiences', caSpec);
    },

    onExcludedCaChange: function(value) {
      var caSpec = [];
      var customAudiences = this.props.customAudiences;

      if (value) {
        value.map(function(id) {
          // Search for the CA based on ID
          if (customAudiences !== undefined) {
            customAudiences.map(function(ca) {
              if (ca.id === id) {
                caSpec.push({id: ca.id});
              }
            });
          }
        });
      }
      this.handleSpecValueChange('excluded_custom_audiences', caSpec);
    },

    // The modal dialog HTML boilerplate
    render: function() {
      return (
        <div className="row">
          <div className="col-md-8 col-sm-12">
            <ComposerBody
              spec={this.state.spec}
              customAudiences={this.props.customAudiences}
              countryList={this.props.countryList}
              onCountryChange={this.onCountryChange}
              onExcludedCountryChange={this.onExcludedCountryChange}
              onCaChange={this.onCaChange}
              onExcludedCaChange={this.onExcludedCaChange}
              onAgeChange={this.onAgeChange}
              onGenderChange={this.onGenderChange}
              onOsChange={this.onOsChange}
              onDevicePlatformsChange={this.onDevicePlatformsChange}
              onPublisherPlatformsChange={this.onPublisherPlatformsChange}
              onFacebookPositionsChange={this.onFacebookPositionsChange}
            />
          </div>
          <div className="col-md-4 col-sm-12">
            <RightColumn
              spec={this.state.spec}
              reachestimate={this.state.reachestimate}
              targetingsentencelines={this.state.targetingsentencelines}
            />
          </div>
        </div>
      );
    },
  });

  return TargetingComposer;
});
