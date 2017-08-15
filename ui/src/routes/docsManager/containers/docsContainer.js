import {
  connect
} from 'react-redux'
import {
  loadDocsList,
  docsPageChange,
  uploadDoc
} from '../modules/docsModule'

import View from '../components/docsList'


const mapDispatchToProps = {
  onUploadDoc: uploadDoc,
  onLoadDocsList: loadDocsList,
  onDocsPageChange: docsPageChange
}

const mapStateToProps = (state) => {
  return {
    rows: state.getIn(['docsqueue','docs','rows']),
    limit: state.getIn(['docsqueue','docs','limit']),
    count: state.getIn(['docsqueue','docs','count']),
    page: state.getIn(['docsqueue','page'])
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(View)
