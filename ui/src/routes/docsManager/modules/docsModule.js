import Immutable from 'immutable'
import {
  getDocsList,
  uploadDocToAPI
} from 'api'

// ------------------------------------
// Constants
// ------------------------------------

export const DOCS_LIST_LOADED = 'DOCS_LIST_LOADED';
export const DOCS_PAGE_CHANGED = 'DOCS_PAGE_CHANGED';
export const UPLOAD_DOC = 'UPLOAD_DOC';

// ------------------------------------
// Actions
// ------------------------------------

export function loadDocsList() {
  return (dispatch, getState) => {
    getDocsList().then((response) => {
        dispatch({
          type: DOCS_LIST_LOADED,
          data: response.data
        });
      })
      .catch((error) => {
        console.log(error)
      })
  }
}

export function docsPageChange(page) {
  return (dispatch, getState) => {
    dispatch({
      type: DOC_PAGE_CHANGED,
      page: page + 1
    })
    dispatch(getDocsList({'page': getState().getIn(['docqueue', 'page'])}))
  }

}

export function uploadDoc(data) {
  return (dispatch, getState) => {
    uploadDocToAPI(data);
    dispatch({
      type: UPLOAD_DOC,
      docName: data.file.name
    })
  }

}


// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
  [DOCS_LIST_LOADED]: (state, action) => {
    const newList = Immutable.Map(action.data)
    return state.set('docs', newList)
  },
  [DOCS_PAGE_CHANGED]: (state, action) => {
    return state.set('page', action.page)
  }
}


// ------------------------------------
// Reducer
// ------------------------------------
const initialState = Immutable.Map({
  'page': 1
})

export default function counterReducer(state = initialState, action) {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}
