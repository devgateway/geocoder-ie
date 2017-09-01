import PropTypes from 'prop-types'
import React, {Component} from 'react';
import ReactPaginate from 'react-paginate';
import {DropzoneComponent} from 'react-dropzone-component';
import {Messages} from './messages';
import './docsManager.scss'
import '../../../../node_modules/react-dropzone-component/styles/filepicker.css';
import '../../../../node_modules/dropzone/dist/min/dropzone.min.css';
import {Link} from 'react-router';


const dropzoneConfig = {
  iconFiletypes: ['.odt', '.xml', '.pdf'],
  showFiletypeIcon: true,
  postUrl: 'no-url'
};

const djsConfig = {
  autoProcessQueue: false,
  addRemoveLinks: true,
  acceptedFiles: '.xml, .pdf, .odt'
}



export default class DocsList extends Component {

  handleFileAdded(file) {
    let dzComp = this.refs.dzComp;
    let {filesToLoad} = this.props;
    let duplicated = false;
    filesToLoad.forEach(fl => {
      if (fl.name === file.name){
        duplicated = true;
      }
    });
    if (!duplicated) {
      if (file.type !== 'text/xml' && file.type !== 'application/pdf' && file.type !== 'application/vnd.oasis.opendocument.text') {
        this.props.onAddMessage(`File ${file.name} is not supported`, 'error');
        dzComp.dropzone.removeFile(file);
      } else {
        filesToLoad = dzComp.dropzone.files.slice();
        print('Set files to load');
        this.props.onFilesLoaded(filesToLoad)

      }
    } else {
      this.props.onAddMessage(`File ${file.name} is duplicatedd`, 'warning');
      dzComp.dropzone.removeFile(file);
    }
  }

  handleFileRemoved(file) {
    let dzComp = this.refs.dzComp;
    let currentFiles=dzComp.dropzone.files.slice()
    this.props.onFilesLoaded(currentFiles);
  }

  uploadFile() {
    let dzComp = this.refs.dzComp;
    const {filesToLoad, countryISO} = this.props;
    filesToLoad.forEach(file => {
      this.props.onUploadDoc({file, countryISO});
      dzComp.dropzone.removeFile(file);
    })
  }

  handleCountryChange(event) {
    this.props.onCountryChanged(event.target.value);
  }

  closeMessage(id) {
    this.props.onCloseMessage(id);
  }

  deleteDoc(id) {
    this.props.onDeleteDoc(id);
  }

  processDoc(id) {
    this.props.onProcessDoc(id);
  }

  render() {
    const {countryList,filesToLoad, countryISO, pendingRows, pendingCount = 0, pendingLimit, processedRows, processedLimit, processedCount = 0, onUpdateDocsList, messages} = this.props;
    const pendingPageCount = pendingCount / pendingLimit;
    const processedPageCount = processedCount / processedLimit;
    const eventHandlers = {addedfile: this.handleFileAdded.bind(this), removedfile: this.handleFileRemoved.bind(this)}

    let showCountrySelector = false;
    filesToLoad.forEach(fl => {
      if (fl.type === 'application/pdf' || fl.type === 'application/vnd.oasis.opendocument.text') {
        showCountrySelector = true;
      }
    });
    let sendDisabled = true;
    if (filesToLoad.length > 0 && (!showCountrySelector || countryISO !== 'none')){
      sendDisabled = false;
    }
    return (
      <div className="docs-manager">

        <h1>Documents Manager</h1>
        <div className="doc-loader">
          <DropzoneComponent ref="dzComp"
            config={dropzoneConfig}
            eventHandlers={eventHandlers}
            djsConfig={djsConfig}
          />

          {showCountrySelector ?
            <select value={countryISO} onChange={this.handleCountryChange.bind(this)}>
              <option value='none'>Select a country</option>
              {countryList.map(country => {
                return <option key={country.code} value={country.code}>{country.name}</option>
              })}
            </select>
          : null}

          <button className={sendDisabled? 'send-button-disabled' : 'send-button'} disabled={sendDisabled} onClick={this.uploadFile.bind(this)}>Send File</button>
        </div>
        <div className="documents-lists">
          <div className="pending-list">
            <h3>List of Pending Docs</h3>
            <h5>({pendingCount} Records)  </h5>
            <div className="list-paginator">
              <ReactPaginate
                previousLabel={"previous"}
                nextLabel={"next"}
                breakLabel={<a href="">...</a>}
                breakClassName={"break-me"}
                pageCount={pendingPageCount}
                initialPage={0}
                onPageChange={(page, count, limit) => {
                  onUpdateDocsList(page.selected + 1, 'PENDING');
                }}
                containerClassName={"pagination"}
                subContainerClassName={"pages pagination"}
                activeClassName={"active"} />
            </div>
            <table className="doc-list">
              <tbody>
                <tr>
                  <th>ID</th>
                  <th>FILE NAME</th>
                  <th>STATUS</th>
                  <th>COUNTRY</th>
                  <th>LOAD DATE</th>
                  <th>ACTIONS</th>
                </tr>
                {(pendingRows)?pendingRows.map(l =>
                  <tr className={l[2]} key={l[0]}>
                    <td>{l[0]}</td>
                    <td><a target='new' href={`${window.API_ROOT}/docqueue/download/${l[0]}`}>{l[1]}</a></td>
                    <td>{l[3]}</td>
                    <td>{countryList.find(country => {return country.code === l[6]})? countryList.find(country => {return country.code === l[6]}).name : 'N/A'}</td>
                    <td>{new Date(l[4]).toLocaleString() }</td>
                    <td>
                    {l[3]=='PROCESSING'?'':<a className="list-action" onClick={this.deleteDoc.bind(this, l[0])}> Delete Document </a>}
                    {l[3]=='PROCESSING'?'':<a className="list-action" onClick={this.processDoc.bind(this, l[0])}> Force Process </a>}


                    </td>
                  </tr>)
                : null}
              </tbody>
            </table>
          </div>
          <div className="processed-list">
            <h3>List of Processed Docs</h3>
            <h5>({processedCount} Records)  </h5>

            <div className="list-paginator">
              <ReactPaginate
                previousLabel={"previous"}
                nextLabel={"next"}
                breakLabel={<a href="">...</a>}
                breakClassName={"break-me"}
                pageCount={processedPageCount}
                initialPage={0}
                onPageChange={(page, count, limit) => {
                  onUpdateDocsList(page.selected + 1, 'PROCESSED');
                }}
                containerClassName={"pagination"}
                subContainerClassName={"pages pagination"}
                activeClassName={"active"} />
            </div>
            <table className="doc-list">
              <tbody>
                <tr>
                  <th>ID</th>
                  <th>FILE NAME</th>
                  <th>STATUS</th>
                  <th>COUNTRY</th>
                  <th>PROCESSED DATE</th>
                  <th>ACTIONS</th>
                </tr>
                {(processedRows)?processedRows.map(l =>
                  <tr className={l[2]} key={l[0]}>
                    <td>{l[0]}</td>
                    <td><a target='new' href={`${window.API_ROOT}/docqueue/download/${l[0]}`}>{l[1]}</a></td>
                    <td>{l[3]}</td>
                    <td>{countryList.find(country => {return country.code === l[6]})? countryList.find(country => {return country.code === l[6]}).name : 'N/A'}</td>
                    <td>{new Date(l[5]).toLocaleString() }</td>
                    <td>
                      <a className="list-action" target='new' href={`${window.API_ROOT}/geocoding/download/${l[0]}`}>Download result</a>
                      <Link className="list-action" to={`/geocodeDetails?documentId=${l[0]}&isXML=${l[2]=='text/xml'}`}>Geocode Details</Link>
                    </td>
                  </tr>)
                : null}
              </tbody>
            </table>
          </div>
        </div>
        <div className='messages-container'>
          {messages.map(message => {
            return(<div className={`message-${message.msgType}`}>
                <div className="message-text">{message.text}</div>
                <div className="message-close" onClick={this.closeMessage.bind(this, message.id)}>X</div>
              </div>)
            })
          }
        </div>
      </div>
    );
  }
}
