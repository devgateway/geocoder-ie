import PropTypes from 'prop-types';
import React, {Component} from 'react';
import Modal from 'react-modal';
import './geocodeDetails.scss';

export default class GeocodeDetails extends Component {

  constructor() {
    super();
    this.state = {extractVisible: false};
  }

  componentWillMount() {
    const documentId = this.props.location.query.documentId;
    const isXML = this.props.location.query.isXML;

    if (isXML === 'true') {
      this.props.onLoadActivityList(documentId);
    }
    this.props.onLoadGeocodingList(documentId);
  }

  renderGeocodingList(list) {
    debugger;
    return (
      <table className="details-list">
        <tbody>
          <tr>
            <th>GEONAME_ID</th>
            <th>LOCATION NAME</th>
            <th>LATITUD</th>
            <th>LONGITUD</th>
            <th>COUNTRY</th>
            <th>ACTIONS</th>
          </tr>
          {list.map(geocode =>
            <tr className="" key={geocode[0]}>
              <td>{geocode.geoname_id}</td>
              <td>{geocode.name}</td>
              <td>{geocode.lat}</td>
              <td>{geocode.lng}</td>
              <td>{geocode.country_name}</td>
              <td><a className="list-action" onClick={this.showTexts.bind(this, geocode[0])}> Show texts </a></td>
            </tr>)
          }
        </tbody>
      </table>
    );
  }

  showTexts(gecodeId) {
    this.props.onLoadExtractList(gecodeId);
    this.setState({extractVisible: true});
  }

  closeTexts() {
    this.setState({extractVisible: false});
  }

  render() {
    const {geocodingList, activityList, extractList} = this.props;
    const isXML = this.props.location.query.isXML;
    const customStyles = {
      content : {
        top                   : '50%',
        left                  : '50%',
        right                 : 'auto',
        bottom                : 'auto',
        marginRight           : '-50%',
        transform             : 'translate(-50%, -50%)',
        maxHeight             : '90vh',
        overflow              : 'auto',
        fontSize              : '13px',
      }
    };

    debugger;

    return (
      <div className="geocoding-details">

        <h1>Geocoding Details</h1>

        {isXML === 'true'?
          (activityList)? activityList.map(activity => {
            return (
              <div className="" key={activity[0]}>
                <div className="activity-header"><h2><b>Activity: </b> {activity[1]}</h2></div>
                {this.renderGeocodingList(geocodingList.filter(gc => gc[23]==activity[0]))}
              </div>
            );
          }) : null
        :
          (geocodingList)? this.renderGeocodingList(geocodingList) : null
        }

        <Modal
          isOpen={this.state.extractVisible}
          onRequestClose={this.closeTexts.bind(this)}
          contentLabel="Extracted Texts"
          style={customStyles}>

          <table className="details-list">
            <tbody>
              <tr>
                <th>SENTENCE ANALIZED</th>
                <th>ENTITIES EXTRACTED</th>
              </tr>
              {(extractList)? extractList.map(text =>
                <tr className="" key={text[0]}>
                  <td>{text.text}</td>
                  <td>{text.entities}</td>
                </tr>)
              : null}
            </tbody>
          </table>
          <button onClick={this.closeTexts.bind(this)}>Close</button>
        </Modal>
      </div>
    );
  }
}
