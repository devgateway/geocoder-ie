import React from 'react'
import ReactDOM from 'react-dom'
import createStore from './store/createStore'
import './styles/main.scss'

//window.API_ROOT = 'http://localhost:8080'
//window.API_ROOT = document.location.href.indexOf('localhost') > -1 ? 'http://localhost:9095' : 'http://autogeocoder.dgstg.org';
window.API_ROOT = document.location.href.indexOf('localhost') > -1 || document.location.href.indexOf('127.0.0.1') > -1 ? 'http://localhost:5000' : (document.location.href.indexOf('developmentgateway.org')>-1?'http://autogeocoder-afdb.developmentgateway.org':'http://autogeocoder.dgstg.org');
// Store Initialization
// ------------------------------------
const {store, history} = createStore(window.__INITIAL_STATE__)

// Render Setup
// ------------------------------------
const MOUNT_NODE = document.getElementById('root')

let render = () => {
  const App = require('./components/App').default
  const routes = require('./routes/index').default(store)

  ReactDOM.render(
    <App store={store} routes={routes} history={history}/>,
    MOUNT_NODE
  )
}

// Development Tools
// ------------------------------------
if (__DEV__) {
  if (module.hot) {
    const renderApp = render
    const renderError = (error) => {
      const RedBox = require('redbox-react').default

      ReactDOM.render(<RedBox error={error} />, MOUNT_NODE)
    }

    render = () => {
      try {
        renderApp()
      } catch (e) {
        console.error(e)
        renderError(e)
      }
    }

    // Setup hot module replacement
    module.hot.accept([
      './components/App',
      './routes/index',
    ], () =>
      setImmediate(() => {
        ReactDOM.unmountComponentAtNode(MOUNT_NODE)
        render()
      })
    )
  }
}

// Let's Go!
// ------------------------------------
if (!__TEST__) render()
