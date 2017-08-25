import {
  connect
} from 'react-redux'
import {
  loadGeocodingList,
  loadActivityList,
  loadExtractList
} from '../modules/geocodeDetails'

import View from '../components/geocodeDetails'

const mapDispatchToProps = {
  onLoadGeocodingList: loadGeocodingList,
  onLoadActivityList: loadActivityList,
  onLoadExtractList: loadExtractList
}

const mapStateToProps = (state) => {
  return {
    geocodingList: state.getIn(['geocodeDetails','geocodingList']),
    activityList: state.getIn(['geocodeDetails','activityList']),
    extractList: state.getIn(['geocodeDetails','extractList']),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(View)
