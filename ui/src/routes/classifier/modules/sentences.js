import Immutable from 'immutable'
import {
  getSentences,
  deleteSentenceById,
  updateSentenceById,
  getDocList
} from 'api'

// ------------------------------------
// Constants
// ------------------------------------

export const SENTENCES_LIST_LOADED = 'SENTENCES_LIST_LOADED'
export const SENTENCE_DELETED = 'SENTENCE_DELETED'
export const SENTENCE_UPDATED = 'SENTENCE_UPDATED'
export const TERM_UPDATED = 'TERM_UPDATED'
export const PAGE_CHANGED = 'PAGE_CHANGED'
export const DOC_LIST_LOADED = 'DOC_LIST_LOADED'
export const DOCUMENT_CHANGED = 'DOCUMENT_CHANGED'

// ------------------------------------
// Actions
// ------------------------------------


export function updateTerm(term) {
  return {
    type: TERM_UPDATED,
    term
  }
}

export function pageClick(page) {
  return (dispatch, getState) => {
    dispatch({
      type: PAGE_CHANGED,
      page: page + 1
    })

    dispatch(loadSentences(getParams(getState)))
  }

}


export function changeDocument(doc) {
  debugger
  return (dispatch, getState) => {
    dispatch({
      type: DOCUMENT_CHANGED,
      doc: doc
    })

    dispatch(loadSentences(getParams(getState)))
  }

}

export function search() {
  return (dispatch, getState) => {

    dispatch({
      type: PAGE_CHANGED,
      page: 1
    })
    dispatch(loadSentences(getParams(getState, 1)))
  }
}

export function loadDocList() {
  return (dispatch, getState) => {
    getDocList().then((response) => {
        dispatch({
          type: DOC_LIST_LOADED,
          data: response.data
        });
      })
      .catch((error) => {
        console.log(error)
      })
  }
}

export function loadSentences(params) {
  return (dispatch, getState) => {

    getSentences(params).then((response) => {
        dispatch({
          type: SENTENCES_LIST_LOADED,
          data: response.data
        });
      })
      .catch((error) => {
        console.log(error)
      })
  }
}

export function deleteSentence(id) {
  return (dispatch, getState) => {
    deleteSentenceById(id).then((response) => {
        dispatch(loadSentences())
      })
      .catch((error) => {
        console.log(error)
      })
  }
}

function getParams(getState, page) {
  let term = getState().getIn(['classifier', 'term'])
  page = (page) ? page : getState().getIn(['classifier', 'page'])
  let doc = getState().getIn(['classifier', 'doc'])

  if (doc == 'All') {
    doc = null
  }
  return {
    page,
    query: term,
    doc
  }
}
export function updateSentence(id, category) {
  return (dispatch, getState) => {


    updateSentenceById(id, category).then((response) => {
        dispatch(loadSentences(getParams(getState)))
      })
      .catch((error) => {
        console.log(error)
      })
  }
}

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
  [SENTENCES_LIST_LOADED]: (state, action) => {
    const newList = Immutable.Map(action.data)
    return state.set('sentences', newList)
  },
  [DOC_LIST_LOADED]: (state, action) => {
    debugger
    const newList = Immutable.List(action.data)
    return state.set('docs', newList)
  },
  [TERM_UPDATED]: (state, action) => {
    return state.set('term', action.term)
  },
  [PAGE_CHANGED]: (state, action) => {
    return state.set('page', action.page)
  },
  [DOCUMENT_CHANGED]: (state, action) => {
    return state.set('doc', action.doc)
  }
}

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = Immutable.Map({
  'term': '',
  'doc': 'All'
})

export default function counterReducer(state = initialState, action) {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}
