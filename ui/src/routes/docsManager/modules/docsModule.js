import Immutable from 'immutable'
import {
  getDocsList,
  uploadDocToAPI,
  deleteDocById,
  forceProcessDoc,
  getCountries
} from 'api'



// ------------------------------------
// Constants
// ------------------------------------

const DOCS_LIST_LOADED = 'DOCS_LIST_LOADED';
const ADD_MESSAGE = 'ADD_MESSAGE';
const CLOSE_MESSAGE = 'CLOSE_MESSAGE';
const SET_FILES = 'SET_FILES';
const SET_COUNTRY = 'SET_COUNTRY';

// ------------------------------------
// Actions
// ------------------------------------

export function updateDocsList(page, state) {
  return (dispatch, getState) => {
    getDocsList({
        page,
        state
      }).then((response) => {
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

export function deleteDoc(id) {
  return (dispatch, getState) => {
    deleteDocById(id).then((response) => {
        dispatch(updateDocsList(1, 'PENDING'));
        dispatch(addMessage(`File ${data.file.name} deleted successfully`, 'success'));
      })
      .catch((error) => {
        dispatch(addMessage(`Error deleting file ${data.file.name}`));
      })
  }
}

export function processDoc(id) {
  return (dispatch, getState) => {
    dispatch(updateDocsList(1, 'PENDING'));
    forceProcessDoc(id).then((response) => {
        dispatch(updateDocsList(1, 'PENDING'));
        dispatch(updateDocsList(1, 'PROCESSED'));
        dispatch(addMessage(`File ${data.file.name} processed successfully`, 'success'));
      })
      .catch((error) => {
        dispatch(addMessage(`Error processing file ${data.file.name}`));
      })
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


export function setCountry(iso) {
  return {
    type: SET_COUNTRY,
    iso
  }
}


export function setFiles(files) {
  return {
    type: SET_FILES,
    files
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
    const {
      id,
      text,
      msgType
    } = action;
    newList.push({
      id,
      text,
      msgType
    });
    return state.set('messages', newList);
  },
  [CLOSE_MESSAGE]: (state, action) => {
    const newList = state.get('messages');
    return state.set('messages', newList.filter(msg => {
      return msg.id !== action.id
    }));
  },
  [SET_FILES]: (state, action) => {
    debugger;
    const {files} = action
    return state.setIn(['files'], files)
  },
  [SET_COUNTRY]: (state, action) => {
    debugger
    const {iso} = action
    return state.setIn(['countryISO'], iso)
  }
}


// ------------------------------------
// Reducer
// ------------------------------------
const initialState = Immutable.Map({
  'messages': [],
  'files': [],
  'countryISO':'' ,
  'countryList':getCountries()
})

debugger;

export default function counterReducer(state = initialState, action) {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}
