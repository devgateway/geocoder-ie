import Immutable from 'immutable'
import {
  getGeocodingList,
  getActivityList,
  getExtractList
} from 'api'

// ------------------------------------
// Constants
// ------------------------------------

export const GEOCODING_LIST_LOADED = 'GEOCODING_LIST_LOADED';
export const ACTIVITY_LIST_LOADED = 'ACTIVITY_LIST_LOADED';
export const EXTRACT_LIST_LOADED = 'EXTRACT_LIST_LOADED';

// ------------------------------------
// Actions
// ------------------------------------

export function loadGeocodingList(queueId) {
  debugger;
  return (dispatch, getState) => {
    getGeocodingList({queue_id:queueId}).then((response) => {
        dispatch({
          type: GEOCODING_LIST_LOADED,
          data: response.data
        });
      })
      .catch((error) => {
        console.log(error)
      })
  }
}

export function loadActivityList(queueId) {
  return (dispatch, getState) => {
    getActivityList({queueId}).then((response) => {
        dispatch({
          type: ACTIVITY_LIST_LOADED,
          data: response.data
        });
      })
      .catch((error) => {
        console.log(error)
      })
  }
}

export function loadExtractList(geocoding_id) {
  debugger;
  return (dispatch, getState) => {
    getExtractList({geocoding_id}).then((response) => {
        dispatch({
          type: EXTRACT_LIST_LOADED,
          data: response.data
        });
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
  [GEOCODING_LIST_LOADED]: (state, action) => {
    const newList = Immutable.List(action.data);
    return state.set('geocodingList', newList);
  },
  [ACTIVITY_LIST_LOADED]: (state, action) => {
    const newList = Immutable.List(action.data);
    return state.set('activityList', newList);
  },
  [EXTRACT_LIST_LOADED]: (state, action) => {
    const newList = Immutable.List(action.data);
    return state.set('extractList', newList);
  }
}


// ------------------------------------
// Reducer
// ------------------------------------
const initialState = Immutable.Map({
  'geocodingList': [],
  'activityList': [],
  'extractList': [],
})

export default function counterReducer(state = initialState, action) {
  const handler = ACTION_HANDLERS[action.type]
  return handler ? handler(state, action) : state
}
