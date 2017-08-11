import PropTypes from 'prop-types'
import React, {Component} from 'react';
import ReactPaginate from 'react-paginate';
import {DropzoneComponent} from 'react-dropzone-component';

import './docsList.scss'
import '../../../../node_modules/react-dropzone-component/styles/filepicker.css';
import '../../../../node_modules/dropzone/dist/min/dropzone.min.css';

export default class DocsList extends Component {

  constructor() {
    super(); 
    this.state = {};
  }

  componentWillMount() {
    this.props.onLoadDocsList();
  }

  handleFileAdded(file) {
    debugger;
    this.setState({'fileToLoad': file});
    console.log(file);
  }

  uploadFile() {
    this.props.onUploadDoc({'file': this.state.fileToLoad, 'country': 'N/A'});
  }

  render() {
    const {rows, count, limit, page, onDocsPageChange} = this.props;
    const pageCount = count / limit;
    const dropzoneConfig = {
      iconFiletypes: ['.odt', '.xml', '.pdf'],
      showFiletypeIcon: true,
      postUrl: 'no-url' 
    };
    const djsConfig = { 
      autoProcessQueue: false, 
      addRemoveLinks: true,
      acceptedFiles: ".xml, .pdf, .odt"
    }
    const eventHandlers = { addedfile: this.handleFileAdded.bind(this) }

    return (
      <div className='docs-list' style={{ margin: '0 auto' }} >

        <h1>List of Coding Docs</h1>
        <h3>{count} Records  </h3>

        <ReactPaginate
          previousLabel={"previous"}
          nextLabel={"next"}
          breakLabel={<a href="">...</a>}
          breakClassName={"break-me"}
          pageCount={pageCount}
          onPageChange={(page, count, limit) => {
            onDocsPageChange(page.selected);
          }}
          containerClassName={"pagination"}
          subContainerClassName={"pages pagination"}
          activeClassName={"active"} />

        <table>
          <tbody>
            <tr>
              <td><b>ID</b></td>
              <td><b>FILE NAME</b></td>
              <td><b>TYPE</b></td>
              <td><b>STATUS</b></td>
            </tr>
            {(rows)?rows.map(l => 
              <tr className={l[2]} key={l[0]}>
                <td>{l[0]}</td>
                <td>{l[1]}</td>
                <td>{l[2]}</td>
                <td>{l[3]}</td>
              </tr>)
            : null}
          </tbody>
        </table>
        
        <ReactPaginate
          previousLabel={"previous"}
          nextLabel={"next"}
          breakLabel={<a href="">...</a>}
          breakClassName={"break-me"}
          pageCount={pageCount}
          onPageChange={(page, count, limit) => {
            onDocsPageChange(page.selected);
          }}
          containerClassName={"pagination"}
          subContainerClassName={"pages pagination"}
          activeClassName={"active"} />

          <DropzoneComponent config={dropzoneConfig}
                       eventHandlers={eventHandlers}
                       djsConfig={djsConfig} />

          <button onClick={this.uploadFile.bind(this)}>Send File</button>
      </div>
    );
  }
}
