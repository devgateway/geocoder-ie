import Immutable from 'immutable'
import {
  getDocsList,
  uploadDocToAPI
} from 'api'

// ------------------------------------
// Constants
// ------------------------------------

export const DOCS_LIST_LOADED = 'DOCS_LIST_LOADED';

// ------------------------------------
// Actions
// ------------------------------------

export function updateDocsList(page, state) {
  return (dispatch, getState) => {
    getDocsList({page, state}).then((response) => {
        dispatch({
          type: DOCS_LIST_LOADED,
          state,
          data: response.data
        });
      })
      .catch((error) => {
        console.log(error)
      })
  }
}

export function uploadDoc(data) {
  return (dispatch, getState) => {
    uploadDocToAPI(data).then(
      (results) => {
        dispatch(updateDocsList(1, 'PENDING'));
      });
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
    const newList = Immutable.Map(action.data);
    if (action.state === 'PENDING') {
      return state.set('pendingDocs', newList);
    } else {
      return state.set('processedDocs', newList);
    }
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
