import Immutable from 'immutable'
import {
  getSentences,
  deleteSentenceById,
  updateSentenceById
} from 'api'

// ------------------------------------
// Constants
// ------------------------------------

export const SENTENCES_LIST_LOADED = 'SENTENCES_LIST_LOADED'
export const SENTENCE_DELETED = 'SENTENCE_DELETED'
export const SENTENCE_UPDATED = 'SENTENCE_UPDATED'
export const TERM_UPDATED = 'TERM_UPDATED'
export const PAGE_CHANGED = 'PAGE_CHANGED'

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
      page:page + 1
    })
      const term = getState().getIn(['classifier', 'term'])
      dispatch(loadSentences({page:page+1,query:term}))
  }

}


export function search() {
  return (dispatch, getState) => {
    const term = getState().getIn(['classifier', 'term'])
    dispatch(loadSentences({query: term}))
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

export function updateSentence(id, category) {
  return (dispatch, getState) => {
      const term = getState().getIn(['classifier', 'term'])
      const page = getState().getIn(['classifier', 'page'])

    updateSentenceById(id, category).then((response) => {
        dispatch(loadSentences({page,query:term}))
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
  [TERM_UPDATED]: (state, action) => {
    return state.set('term', action.term)
  },
  [PAGE_CHANGED]: (state, action) => {
    return state.set('page', action.page)
  }
}

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = Immutable.Map({
  'term': ''
})

export default function counterReducer(state = initialState, action) {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}
