import Immutable from 'immutable'
import {
  getDocsList,
  uploadDocToAPI
} from 'api'

// ------------------------------------
// Constants
// ------------------------------------

export const DOCS_LIST_LOADED = 'DOCS_LIST_LOADED';
export const ADD_MESSAGE = 'ADD_MESSAGE';
export const CLOSE_MESSAGE = 'CLOSE_MESSAGE';

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
        dispatch(addMessage(`File ${data.file.name} uploaded successfully`, 'success'));
      }).catch((failure) => {
        dispatch(addMessage(`Error on load file ${data.file.name}`));
      });
  }

}

export function addMessage(text, msgType) {
  return {
    type: ADD_MESSAGE,
    text,
    msgType,
    id: new Date().getTime()
  }
}

export function closeMessage(id) {
  return {
    type: CLOSE_MESSAGE,
    id
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
  },
  [ADD_MESSAGE]: (state, action) => {
    const newList = state.get('messages');
    const {id, text, msgType} = action;
    newList.push({id, text, msgType});
    return state.set('messages', newList);
  },
  [CLOSE_MESSAGE]: (state, action) => {
    const newList = state.get('messages');
    return state.set('messages', newList.filter(msg => {return msg.id !== action.id}));
  }
}


// ------------------------------------
// Reducer
// ------------------------------------
const initialState = Immutable.Map({
  'messages': []
})

export default function counterReducer(state = initialState, action) {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}
