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


function DocsTable(props){
  const {rows,actions,countryList,docFilter,pageCount,onUpdateDocsList}=props
  return (
    <div>
      <div className="list-paginator">
        <ReactPaginate
          previousLabel={"previous"}
          nextLabel={"next"}
          breakLabel={<a href="">...</a>}
          breakClassName={"break-me"}
          pageCount={pageCount}
          initialPage={0}
          onPageChange={(page, count, limit) => {
            onUpdateDocsList(page.selected + 1, docFilter);
          }}
          containerClassName={"pagination"}
          subContainerClassName={"pages pagination"}
          activeClassName={"active"} />
      </div>

      <table className="doc-list">
      <tbody>
        <tr>
          <th>TYPE</th>
          <th>ID</th>
          <th>DATE</th>
          <th>PROCESSED</th>
          <th>DOC / ACTIVITY </th>
          <th>STATUS</th>
          <th>MESSAGE</th>
          <th>COUNTRY</th>
          <th>ACTIONS</th>
        </tr>
        {(rows)?rows.map(l =>
          <tr className={l.id} key={l.id}>
            <td>{l.queue_type}</td>
            <td>{l.id}</td>
            <td>{new Date(l.create_date).toLocaleString() }</td>
             <td>{l.processed_date?new Date(l.processed_date).toLocaleString():null}</td>
            <td><a target='new' href={`${window.API_ROOT}/docqueue/download/${l.file_name}`}>{l.file_name}</a> {l.identifier}</td>
            <td>{l.state}</td>
            <td>{l.message}</td>
            <td>{countryList.find(country => {return country.code === l.country_iso})? countryList.find(country => {return country.code === l.country_iso}).name : 'N/A'}</td>
            <td>
              {(l.queue_type=='ACTIVITY_QUEUE')?null:actions.indexOf('DELETE')>-1?l.state=='PROCESSING'?null:<a key='delete' className="list-action" onClick={e=>props.onDeleteDoc(l.id)}> Delete </a>:null}
              {actions.indexOf('FORCE')>-1?l.state=='PROCESSING'?'':<a key='force' className="list-action" onClick={e=>props.onProcessDoc(l.id)}>Process </a>:null}
              {(l.queue_type=='ACTIVITY_QUEUE')?null:actions.indexOf('DOWNLOAD')>-1?<a className="list-action" key='download' target='new' href={`${window.API_ROOT}/geocoding/download/${l.id}`}>Result</a>:null}
              {actions.indexOf('DETAILS')>-1? <Link className="list-action" key='details' to={`/geocodeDetails?queueId=${l.id}&isXML=${l.type=='text/xml'}`}>Details</Link>:null}
            </td>
          </tr>)
        : null}
      </tbody>
    </table>
    </div>)
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

  componentDidMount() {

    const {onUpdateDocsList}=this.props
    this.timer = setInterval(()=>{
        console.log('Updating')
        onUpdateDocsList(1,'PENDING')
        onUpdateDocsList(1,'PROCESSED')
    }, 10000);
  }
componentWillUnmount() {
  clearInterval(this.timer);
  }

  render() {
    const {countryList,filesToLoad, countryISO, pendingRows, pendingCount = 0,
      pendingLimit, processedRows, processedLimit, processedCount = 0, onUpdateDocsList, messages,onProcessDoc,onDeleteDoc,onCloseMessage,onCountryChanged} = this.props;
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
        <h1>Autogeocoder</h1>
        <div className="doc-loader">
          <DropzoneComponent ref="dzComp" config={dropzoneConfig} eventHandlers={eventHandlers} djsConfig={djsConfig}/>

          {showCountrySelector ?
            <select value={countryISO} onChange={e=> onCountryChanged(e.target.value)}>
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
          <h5>({pendingCount} Records)</h5>
            <DocsTable key='pending-docs' rows={pendingRows}
            onDeleteDoc={onDeleteDoc}
            onProcessDoc={onProcessDoc}
            actions={['DELETE']}
            countryList={countryList}
            docFilter='PENDING' pageCount={pendingPageCount}
            onUpdateDocsList={onUpdateDocsList}/>
        </div>
        <div className="processed-list">
          <h3>List of Processed Docs</h3>
          <h5>({processedCount} Records)  </h5>
          <DocsTable key='processed-docs' rows={processedRows}
          onDeleteDoc={onDeleteDoc}
          onProcessDoc={onProcessDoc}
          actions={['DELETE','DETAILS','DOWNLOAD']} countryList={countryList}
          docFilter='PROCESSED'
          pageCount={processedPageCount}
          onUpdateDocsList={onUpdateDocsList}/>
        </div>
        </div>
        <div className='messages-container'>
          {messages.map(message => {
            return(<div className={`message-${message.msgType}`}>
                <div className="message-text">{message.text}</div>
                <div className="message-close" onClick={e=>onCloseMessage(message.id)}>X</div>
              </div>)
            })
          }
        </div>
      </div>
    );
  }
}
