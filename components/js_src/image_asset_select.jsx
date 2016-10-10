'use strict';
/*global define*/
define(
  ['react', 'fbutils'],
function(React, fbutils) {
  let ImageAssetSelect = React.createClass({
    propTypes: {
      accountId: React.PropTypes.string.isRequired,
      video: React.PropTypes.boolean,
      columns: React.PropTypes.number,
      limits: React.PropTypes.number,
      onImageAssetSelect: React.PropTypes.func.isRequired,
    },

    getDefaultProps: function() {
      return {
        video: false,
        columns: 4,
        limits: 12,
        onImageAssetSelect: function() {},
      };
    },

    getInitialState: function() {
      return this.getCursors(this.props.accountId, this.props.video);
    },

    componentWillReceiveProps: function(props) {
      const cursor = this.getCursors(props.accountId, props.video);
      this.setState(cursor);
      this.page(cursor.next);
    },

    getCursors: function(accountId, video) {
      const endpoint = (accountId === undefined || accountId === null) ? null :
        (video) ?
          '/' + accountId + '/advideos' :
          '/' + accountId + '/adimages';

      return  {
        prev: null,
        next: endpoint,
        photos: [], /* { src, hash } */
      };
    },

    componentDidMount: function() {
      this.page(this.state.next);
    },

    page: function(endpoint) {
      if (endpoint === null) { return; }

      const video = this.props.video;

      console.log(endpoint);

      let fields = null;
      if (video) {
        fields = 'picture';
      } else {
        fields =  'url_128,hash';
      }

      let apiQuery = fbutils.api(
        endpoint,
        'GET',
        {
          fields: fields,
          limit: this.props.limits,
        }
      );

      apiQuery.then(function(result) {
        let paging = result.paging;

        if (paging === null) {
          return;
        }

        let data = result.data;
        let photos = data.map(photo => (
          (video) ?
          {src: photo.picture, hash: null, id: photo.id} :
          {src: photo.url_128, hash: photo.hash, id: null}
        ));

        let prev = null;
        let next = null;
        if (paging.hasOwnProperty('previous')) {
          prev = paging.previous;
        }
        if (paging.hasOwnProperty('next')) {
          next = paging.next;
        }

        this.setState({
          photos: photos,
          prev: prev,
          next: next,
        });

      }.bind(this)).catch(function(message) {
        console.log(message);
      });
    },

    render: function() {
      let next = null;
      let prev = null;

      if (this.state.next) {
        let onClick = function() {
          console.log('XXX');
          this.page(this.state.next);
        }.bind(this);

        next =
            <div style={{position: 'absolute', right: '20px'}}>
              <span className="glyphicon glyphicon-chevron-right"
                onClick={onClick}/>
            </div>;
      }

      if (this.state.prev) {
        let onClick = function() {
          this.page(this.state.prev);
        }.bind(this);

        prev =
            <div style={{position: 'absolute', left: '20px'}}>
              <span className="glyphicon glyphicon-chevron-left"
                onClick={onClick}/>
            </div>;
      }

      return (
          <div>
              <div className="imageGrid">
                {this.getGridElements()}
              </div>
              <div className="modal-footer">
                {prev} {next}
              </div>
          </div>
      );
    },

    getGridElements: function() {
      const {photos}  = this.state;
      const style = {width : this.getPercentWidth() + '%'};

      return photos.map(photo => (
        <div className="imageGridItem"
          style={style}
          key={photo.hash || photo.id}>
          {this.getImageElement(photo)}
        </div>
      ));
    },

    onImageSelect: function(photo) {
      return function() {
        this.props.onImageAssetSelect(photo);
      };
    },

    getImageElement: function(photo) {
      const style = {backgroundImage: `url(${photo.src})`};

      return (
        <div className="imageWrapper"
          style={style}
          onClick={this.onImageSelect(photo).bind(this)}
        />
      );
    },

    getPercentWidth: function() { return 100 / this.props.columns - 1; },
  });

  return ImageAssetSelect;
});
