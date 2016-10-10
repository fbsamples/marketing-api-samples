'use strict';

/*global define*/
define([
  'jquery',
  'react',
  'react-selectize',
  'fbutils',
  'components/simple_modal',
  'components/image_asset_select',
],
function($, React, ReactSelectize, fbutils, Modal, ImageAssetSelect) {
  const RightColumn = React.createClass({
    render: function() {
      return (
        <div>
          <label>Current Asset Feed Spec: </label>
          <div>
            <pre style={{maxHeight:'900px', overflow:'scroll'}}>
              <code language="JavaScript">
                {JSON.stringify(this.props.spec, null, 2)}
              </code>
            </pre>
          </div>
        </div>
      );
    },
  });

  const isVideo = (format) => {
    return format === 'SINGLE_VIDEO' ||  format === 'CAROUSEL_VIDEO';
  };
  const isImage = (format) => { return !isVideo(format); };

  const Assets = React.createClass({
    propTypes: {
      account: React.PropTypes.string.isRequired,
      accountId: React.PropTypes.string.isRequired,
      formats: React.PropTypes.array.isRequired,
      platforms: React.PropTypes.array.isRequired,
      spec: React.PropTypes.object.isRequired,
      onAssetsChange: React.PropTypes.func.isRequired,
      showImageAssetSelect: React.PropTypes.func.isRequired,
      fields: React.PropTypes.array.isRequired,
    },

    getDefaultProps: function() {
      const any = (format) => { return true; };

      let fields = [
        {feed_id: 'titles', attachment_id: 'title', sub_id: 'text'},
        {feed_id: 'bodies', attachment_id: 'body', sub_id: 'text'},
        {feed_id: 'captions', attachment_id: 'caption', sub_id: 'text'},
        {feed_id: 'link_urls', attachment_id: 'link', sub_id: 'url'},
        {feed_id: 'call_to_action_types', attachment_id: 'call_to_action'},
        {feed_id: 'images', attachment_id: 'image_hash', sub_id: 'hash',
          format: isImage},
        {feed_id: 'videos', attachment_id: 'video_id', sub_id: 'id',
          format: isVideo},
      ];

      fields.forEach((field) => {
        if (!field.hasOwnProperty('format')) {
          field.format = any;
        }
      });

      return {fields: fields};
    },

    render: function() {
      const account = this.props.account;
      const accountId = this.props.accountId;
      const formats = this.props.formats;
      const assets = this.props.spec;
      const fields = this.props.fields;
      const onAssetsChange = this.props.onAssetsChange;

      const selected_format = assets.ad_formats[0];
      const video = isVideo(selected_format);

      const update = function(assets, field, index, spec) {
        const property = field.feed_id;
        const value = spec[field.attachment_id];

        if (!(property in assets)) {
          assets[property] = [];
        }

        if ('sub_id' in field) {
          assets[property][index] = {};
          assets[property][index][field.sub_id] = value;
        } else {
          assets[property][index] = value;
        }
      };

      const read = function(assets, field, index) {
        const property = field.feed_id;
        if (property in assets && index < assets[property].length) {
          const value = assets[property][index];
          return (value && 'sub_id' in field) ? value[field.sub_id] : value;
        }
        return null;
      };

      const onAttachmentChange = function(spec) {
        const index = spec.index;
        const ad_format = spec.ad_format;
        let feed = assets;
        fields.forEach(
          (field) => {
            if (field.attachment_id in spec && field.format(ad_format)) {
              update(feed, field, index, spec);
            }
          }
        );

        onAssetsChange(account, feed);
      };

      const removeAttachment = function() {
        const end = attachments.length - 1;
        let feed = assets;
        fields.forEach(
          (field) => {
            const property = field.feed_id;
            if (property in feed) {
              feed[property] = feed[property].slice(0, end);
            }
          }
        );

        onAssetsChange(account, feed);
      };

      const addAttachment = function() {
        let attachment = {
          index: attachments.length,
          ad_format: selected_format,
        };

        if (video) {
          attachment.video_id = null;
        } else {
          attachment.image_hash = null;
        }

        onAttachmentChange(attachment);
      };

      const onAdFormatSelected = function(format) {
        if (format !== selected_format) {
          let feed = {ad_formats: []};
          feed.ad_formats[0] = format;
          if (isVideo(format)) {
            feed.videos = [];
            feed.videos[0] = {id: null};
          } else {
            feed.images = [];
            feed.images[0] = {hash: null};
          }

          onAssetsChange(account, feed);
        }
      };

      const showImageAssetSelect = this.props.showImageAssetSelect;
      const createAttachment = (creative, i) => {
        let attachment = {
          index: i,
          ad_format: selected_format,
        };

        this.props.fields.forEach(
          (field) => {
            attachment[field.attachment_id] = read(assets, field, i);
          }
        );

        return (
          <div className="panel panel-default">
            <div className="panel-body">
              <Attachment
                accountId={accountId}
                spec={attachment}
                onAttachmentChange={onAttachmentChange}
                showImageAssetSelect={showImageAssetSelect}
              />
            </div>
          </div>
        );
      };

      let attachments = [];
      if (video && assets.hasOwnProperty('videos') && assets.videos) {
        attachments = attachments.concat(assets.videos.map(createAttachment));
      } else if (assets.hasOwnProperty('images') && assets.images) {
        attachments = attachments.concat(assets.images.map(createAttachment));
      }

      let minus = <span className="input-group-addon" onClick={removeAttachment}>
                  <i className="glyphicon glyphicon-minus"/>
              </span>;
      if (attachments.length === 1) {
        minus = null;
      }

      return (
        <div className="Assets">
          <ReactSelectize
            items={formats}
            value={selected_format}
            selectId="select-format"
            placeholder="- Select -"
            label="Ad Format:"
            multiple={false}
            onChange={onAdFormatSelected}
          />
          <div>
            <div className="input-group">
              <label>Attachments:</label>
            </div>
            {attachments}
            </div>
            <div className="input-group">
              <span/>
              {minus}
              <span className="input-group-addon" onClick={addAttachment}>
                  <i className="glyphicon glyphicon-plus"/>
              </span>
            </div>
          </div>
      );
    },
  });

  let Attachment = React.createClass({
    propTypes: {
      accountId: React.PropTypes.string.isRequired,
      spec: React.PropTypes.object.isRequired,
      onAttachmentChange: React.PropTypes.func.isRequired,
      showImageAssetSelect: React.PropTypes.func.isRequired,
      ctaTypes: React.PropTypes.array.isRequired,
    },

    getDefaultProps: function() {
      const actions = [
        'OPEN_LINK', 'LIKE_PAGE', 'SHOP_NOW', 'PLAY_GAME',
        'INSTALL_MOBILE_APP', 'USE_APP', 'USE_MOBILE_APP',
        'BOOK_TRAVEL', 'LISTEN_MUSIC', 'WATCH_VIDEO', 'LEARN_MORE',
        'SIGN_UP', 'DOWNLOAD', 'WATCH_MORE', 'NO_BUTTON', 'CALL_NOW',
        'BUY_NOW', 'GET_OFFER', 'GET_OFFER_VIEW', 'GET_DIRECTIONS',
        'MESSAGE_PAGE', 'SUBSCRIBE', 'SELL_NOW', 'DONATE_NOW', 'GET_QUOTE',
        'CONTACT_US', 'RECORD_NOW', 'VOTE_NOW', 'OPEN_MOVIES'];

      const selectList = actions.map(
        (callToAction) => {
          return {id: callToAction, name: callToAction};
        }
      );

      return {
        ctaTypes: selectList,
      };
    },

    onTextChange: function(property, value) {
      const spec = this.props.spec;
      spec[property] = value;
      this.props.onAttachmentChange(spec);
    },

    onCreativeChange: function(creative) {
      const format = this.props.spec.ad_format;
      (isVideo(format)) ?
        this.onTextChange('video_id', creative.id) :
        this.onTextChange('image_hash', creative.hash);

      this.setState({url: null});
    },

    openImageAssetSelect: function() {
      this.props.showImageAssetSelect(
        this.props.accountId,
        isVideo(this.props.spec.ad_format),
        this.onCreativeChange
      );
    },

    render: function() {
      const spec = this.props.spec;
      const format = this.props.spec.ad_format;
      const video = isVideo(format);
      const img = 'thumbnail_' + spec.index;

      let selectedCtaType = null;
      if ('call_to_action' in spec) {
        selectedCtaType = spec['call_to_action'];
      }

      if (video && spec.video_id) {
        const endpoint = '/' +  spec.video_id;
        const apiQuery = fbutils.api(
          endpoint,
          'GET',
          { fields: 'picture' }
        );

        apiQuery.then(function(result) {
          if (result) {
            $('#' + img).css({backgroundImage: `url(${result.picture})`});
          }
        }).catch(function(message) {
          console.log(message);
        });
      } else if (spec.image_hash) {
        const endpoint = '/' + this.props.accountId + '/adimages';
        const apiQuery = fbutils.api(
          endpoint,
          'GET',
          {
            fields: 'url',
            hashes: [spec.image_hash],
          }
        );

        apiQuery.then(function(result) {
          const data = result.data;
          if (data && Array.isArray(data) && data.length) {
            $('#' + img).css({backgroundImage: `url(${data[0].url})`});
          }
        }).catch(function(message) {
          console.log(message);
        });
      }

      return (
        <div className="Attachment">
          <div className="form-group">
            <label className="control-label" htmlFor={'image_' + spec.index}>
              {(video) ? 'Video ID' : 'Image Hash'}
            </label>
            <div className="assetThumbnail" id={'thumbnail_' + spec.index} />
            <div className="input-group">
              <span>
                <input className="form-control" id={'image_' + spec.index}
                  type="text"
                  placeholder="image hash or video id"
                  value={(video) ? spec.video_id : spec.image_hash}
                  onChange={(event) => {
                    this.onTextChange('image_hash', event.target.value);
                  }}
                />
              </span>
              <span className="input-group-addon" onClick={this.openImageAssetSelect}>
                <i className="glyphicon glyphicon-plus"/>
              </span>
            </div>
          </div>

          <TextInput
            label="Title"
            index={spec.index}
            placeholder="Title'"
            value={spec.title}
            onChange={(event) => {
              this.onTextChange('title', event.target.value);
            }}
          />
          <TextInput
            label="Body"
            index={spec.index}
            placeholder="Body message'"
            value={spec.body}
            onChange={(event) => {
              this.onTextChange('body', event.target.value);
            }}
          />
          <TextInput
            label="Caption"
            index={spec.index}
            placeholder="Caption'"
            value={spec.caption}
            onChange={(event) => {
              this.onTextChange('caption', event.target.value);
            }}
          />
          <TextInput
            label="Link"
            index={spec.index}
            placeholder="URL"
            value={spec.link}
            onChange={(event) => {
              this.onTextChange('link', event.target.value);
            }}
          />

          <div className="form-group">
            <ReactSelectize
              selectId={'select-cta_' + spec.index}
              items={this.props.ctaTypes}
              value={selectedCtaType}
              placeholder="- select -"
              label="Call to action:"
              multiple={false}
              onChange={this.onCTATypeChange}
              onChange={(value) => {
                this.onTextChange('call_to_action', value);
              }}
            />
          </div>
        </div>
      );
    },
  });

  let TextInput = React.createClass({
    propTypes: {
      label: React.PropTypes.string.isRequired,
      index: React.PropTypes.number.isRequired,
      value: React.PropTypes.string.isRequired,
      placeholder: React.PropTypes.string.isRequired,
      onChange: React.PropTypes.func.isRequired,
    },

    render: function() {
      const id = this.props.label + this.props.index;
      return (
          <div className="form-group">
            <label className="control-label" htmlFor={id}>
              {this.props.label}:
            </label>
            <div>
            <input className="form-control" id={id}
              type="text"
              placeholder={this.props.placeholder}
              value={this.props.value}
              onChange={this.props.onChange}
             />
             </div>
          </div>
      );
    },
  });


  let ComposerBody = React.createClass({
    propTypes: {
      defaultAccountId: React.PropTypes.string.isRequired,
      spec: React.PropTypes.object.isRequired,
      formats: React.PropTypes.array.isRequired,
      platforms: React.PropTypes.array.isRequired,
      onAssetsChange: React.PropTypes.func.isRequired,
      showImageAssetSelect: React.PropTypes.func.isRequired,
    },

    render: function() {
      const spec = this.props.spec;
      let accounts = [];
      for (let account in spec) { accounts.push(account); }

      accounts = accounts.map(
        (account) => {
          let accountId = account;
          if (account === 'default') {
            accountId = this.props.defaultAccountId;
          }

          return (
            <div>
              <label>Account id: {account}</label>
              <div className="panel panel-default">
                <div className="panel-body">
                  <Assets
                    account={account}
                    accountId={accountId}
                    formats={this.props.formats}
                    platforms={this.props.platforms}
                    spec={spec[account]}
                    onAssetsChange={this.props.onAssetsChange}
                    showImageAssetSelect={this.props.showImageAssetSelect}
                  />
                </div>
              </div>
            </div>
          );
        }
      );

      return (
        <div className="composer-body">
          {accounts}
        </div>
      );
    },
  });

  let AutobotAssetFeedComposer = React.createClass({
    propTypes: {
      accountId: React.PropTypes.string.isRequired,
      platforms: React.PropTypes.array.isRequired,
      onChange: React.PropTypes.func.isRequired,
      formats: React.PropTypes.array.isRequired,
      initialValue: React.PropTypes.object.isRequired,
    },

    getDefaultProps: function() {
      return {
        onChange: function() {},
        formats: [
          {id: 'SINGLE_IMAGE', name: 'Single Image'},
          {id: 'SINGLE_VIDEO', name: 'Single Video'},
          {id: 'CAROUSEL_IMAGE', name: 'Carousel Image'},
          {id: 'CAROUSEL_VIDEO', name: 'Carousel Video'},
        ],
      };
    },

    getInitialState: function() {
      return  {
        spec: this.props.initialValue,
        enableImageAssetSelectModal: false,
        onImageAssetSelect: function() {},
      };
    },

    showImageAssetSelect: function(accountId, video, onImageAssetSelect) {
      this.setState({
        enableImageAssetSelectModal: true,
        assetAccountId: accountId,
        video: video,
        onImageAssetSelect: onImageAssetSelect,
      });
    },

    onImageAssetSelect: function(image) {
      if (image) {
        this.state.onImageAssetSelect(image);
      }
      this.setState({
        enableImageAssetSelectModal: false,
        assetAccountId: null,
        onImageAssetSelect: function() {},
      });
    },

    onAssetsChange: function(account, value) {
      let spec = this.state.spec;

      if (value === undefined || value === null || value.length === 0) {
        delete spec[account];
      } else {
        spec[account] = value;
      }

      this.setState({spec: spec});
      this.props.onChange(spec);
    },

    // The modal dialog HTML boilerplate.
    render: function() {
      const onClose = function(event) {
        this.onImageAssetSelect(null);
      }.bind(this);

      return (
        <div className="row">
          <div className="col-md-8 col-sm-12">
            <ComposerBody
              defaultAccountId={this.props.accountId}
              formats={this.props.formats}
              platforms={this.props.platforms}
              spec={this.state.spec}
              onAssetsChange={this.onAssetsChange}
              showImageAssetSelect={this.showImageAssetSelect}
            />
          </div>
          <div className="col-md-4 col-sm-12">
            <RightColumn
              spec={this.state.spec}
            />
          </div>
          <Modal
            header="Select an asset from the library"
            targetId="ImageAssetSelect"
            show={this.state.enableImageAssetSelectModal}
            onClose={onClose}>
            <ImageAssetSelect
                accountId={this.state.assetAccountId}
                video={this.state.video}
                onImageAssetSelect={this.onImageAssetSelect}
              />
          </Modal>
        </div>
      );
    },
  });

  return AutobotAssetFeedComposer;
});
