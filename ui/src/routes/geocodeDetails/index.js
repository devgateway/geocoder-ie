import { injectReducer } from '../../store/reducers'

export default (store) => ({
  path : 'geocodeDetails',
  getComponent (nextState, cb) {
    require.ensure([], (require) => {
      const Comp = require('./containers/geocodeDetails').default
      const reducer = require('./modules/geocodeDetails').default
      injectReducer(store, { key: 'geocodeDetails', reducer })
      cb(null, Comp)
    }, 'geocodeDetails')
  }
})
