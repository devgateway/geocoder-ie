import {
  connect
} from 'react-redux'
import {
  updateDocsList,
  uploadDoc,
  addMessage,
  deleteDoc,
  closeMessage,
  processDoc
} from '../modules/docsModule'

import View from '../components/docsManager'


const mapDispatchToProps = {
  onUploadDoc: uploadDoc,
  onUpdateDocsList: updateDocsList,
  onCloseMessage: closeMessage,
  onAddMessage: addMessage,
  onDeleteDoc: deleteDoc,
  onProcessDoc: processDoc,
}

const mapStateToProps = (state) => {
  return {
    pendingRows: state.getIn(['docsmanager','pendingDocs','rows']),
    pendingLimit: state.getIn(['docsmanager','pendingDocs','limit']),
    pendingCount: state.getIn(['docsmanager','pendingDocs','count']),

    processedRows: state.getIn(['docsmanager','processedDocs','rows']),
    processedLimit: state.getIn(['docsmanager','processedDocs','limit']),
    processedCount: state.getIn(['docsmanager','processedDocs','count']),

    messages: state.getIn(['docsmanager','messages']),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(View)
