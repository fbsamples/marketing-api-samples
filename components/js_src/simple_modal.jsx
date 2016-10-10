'use strict';
/* global define */
define(['jquery', 'react'], function($, React) {
  let Modal = React.createClass({
    propTypes: {
      targetId: React.PropTypes.string.isRequired,
      header: React.PropTypes.string.isRequired,
      show: React.PropTypes.bool.isRequired,
      onClose: React.PropTypes.func.isRequired,
    },

    getDefaultProps: function() {
      return {
        show: false,
        onClose: function(event) {}
      };
    },

    getInitialState: function() {
      return  {
      };
    },

    hideOnOuterClick: function(event) {
      if (event.target.dataset.modal) {
        this.props.onClose(event);
      }
    },

    render: function() {
      if (!this.props.show) {
        return null;
      }

      const targetId = this.props.targetId;
      return (
          <div className="modal" id={targetId + '_modal'}
            style={{display: 'block'}}
            data-model="true"
            tabIndex="-1" role="dialog"
            aria-labelledby={targetId + '_label'} aria-hidden="true">
            <div className="modal-dialog modal-mg">
              <div className="modal-content">
                <div className="modal-header">
                  <button type="button" className="close"
                    onClick={this.props.onClose} aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                  <h4 className="modal-title" id={targetId + '_label'}>
                    {this.props.header}
                  </h4>
                </div>
                <div className="modal-body">
                  {this.props.children}
                </div>
              </div>
            </div>
          </div>
      );
    },

  });

  return Modal;
});
