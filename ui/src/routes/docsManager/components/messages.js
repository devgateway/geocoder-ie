import PropTypes from 'prop-types'
import React, {Component} from 'react';
import './messages.scss';

export default class Messages extends Component {

  constructor() {
    super(); 
    debugger;
    
    this.state = {};
  }

  closeMessage(id){
    this.props.onCloseMessage(id);
  }

  render() {
    const {messageList} = this.props;
    debugger;
    return (
      <div className='messages-container'>
        {messageList.map(message => {
          return(<div className={`message-${message.msgType}`}>
              <div className="message-text">{message.text}</div>
              <div className="message-close" onClick={this.closeMessage.bind(this, message.id)}>X</div>
            </div>)
          })
        }
      </div>
    );
  }
}
