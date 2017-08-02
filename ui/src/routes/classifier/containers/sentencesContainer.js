import {
  connect
} from 'react-redux'
import {
  loadSentences,
  pageClick,
  deleteSentence ,
  updateSentence,
  updateTerm,
  search,
  loadDocList,
  changeDocument
} from '../modules/sentences'

/*  This is a container component. Notice it does not contain any JSX,
    nor does it import React. This component is **only** responsible for
    wiring in the actions and state necessary to render a presentational
    component - in this case, the counter:   */

import View from '../components/sentences'

/*  Object of action creators (can also be function that returns object).
    Keys will be passed as props to presentational components. Here we are
    implementing our wrapper around increment; the component doesn't care   */

const mapDispatchToProps = {
  onChangeDocument:changeDocument,
  onDelete:deleteSentence,
  onUpdate:updateSentence,
  onLoad: loadSentences,
  onLoadDocs:loadDocList,
  onSearchChange:updateTerm,
  onSearch:search,
  onPageClick: pageClick
}

const mapStateToProps = (state) => {
  return {
    doc:state.getIn(['classifier','doc']),
    term:state.getIn(['classifier','term']),
    rows: state.getIn(['classifier', 'sentences','rows']),
    limit: state.getIn(['classifier', 'sentences','limit']),
    count: state.getIn(['classifier', 'sentences','count']),
    docs: state.getIn(['classifier', 'docs'])
  }
}

/*  Note: mapStateToProps is where you should use `reselect` to create selectors, ie:

    import { createSelector } from 'reselect'
    const counter = (state) => state.counter
    const tripleCount = createSelector(counter, (count) => count * 3)
    const mapStateToProps = (state) => ({
      counter: tripleCount(state)
    })

    Selectors can compute derived data, allowing Redux to store the minimal possible state.
    Selectors are efficient. A selector is not recomputed unless one of its arguments change.
    Selectors are composable. They can be used as input to other selectors.
    https://github.com/reactjs/reselect    */

export default connect(mapStateToProps, mapDispatchToProps)(View)
