import { applyMiddleware, compose, createStore as createReduxStore } from 'redux'
import thunkMiddleware from 'redux-thunk'
import { hashHistory  } from 'react-router'
import makeRootReducer from './reducers'
import { updateLocation } from './location'
import Immutable from 'immutable'
import {
  browserHistory
} from 'react-router';
import {
  syncHistoryWithStore, routerMiddleware
} from 'react-router-redux';



  const createStore = (initialState = Immutable.Map()) => {
  // ======================================================
  // Middleware Configuration
  // ======================================================
  //const middleware = [thunk]
  const historyMiddleware = routerMiddleware(browserHistory);

  // ======================================================
  // Store Enhancers
  // ======================================================
  const enhancers = []
  let composeEnhancers = compose

  if (__DEV__) {
    if (typeof window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ === 'function') {
      composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
    }
  }

  // ======================================================
  // Store Instantiation and HMR Setup
  // ======================================================
  const store = createReduxStore(
    makeRootReducer(),
    initialState,
      composeEnhancers(
      applyMiddleware(thunkMiddleware, historyMiddleware),
      ...enhancers
    )
  )
  store.asyncReducers = {}

  // To unsubscribe, invoke `store.unsubscribeHistory()` anytime
  //store.unsubscribeHistory = hashHistory.listen(updateLocation(store))
  const history = syncHistoryWithStore(browserHistory, store, {
    selectLocationState (state) {
        return state.get('location').toJS();
    }
  });


  if (module.hot) {
    module.hot.accept('./reducers', () => {
      const reducers = require('./reducers').default
      store.replaceReducer(reducers(store.asyncReducers))
    })
  }

  return store
}

export default createStore
