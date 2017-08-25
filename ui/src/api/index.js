import axios from 'axios';
const ROOT=window.API_ROOT;


export function getSentences(params) {
  return axios.get(`${ROOT}/corpora`, {
    params: params
  })
}

export function deleteSentenceById(id) {
  return axios.delete(`${ROOT}/corpora/${id}`)
}

export function updateSentenceById(id, category) {
  return axios.post(`${ROOT}/corpora/${id}`, {
    category: category
  })
}

export function getCorporaDocList() {
  return axios.get(`${ROOT}/corpora/docs`)
}

export function getDocsList(params) {
  return axios.get(`${ROOT}/docqueue`, {params})
}

export function deleteDocById(id) {
  return axios.delete(`${ROOT}/docqueue/${id}`)
}

export function forceProcessDoc(id) {
  return axios.get(`${ROOT}/docqueue/process/${id}`)
}

export function uploadDocToAPI(fileData) {
  const {file, countryISO} = fileData;
  let data = new FormData();
  data.append('file', file, file.name);
  data.append('countryISO', countryISO);
  const config = {
    headers: { 'content-type': 'multipart/form-data' }
  };
  return new Promise(
      function(resolve, reject) {
        axios.post(`${ROOT}/docqueue/upload`, data, config)
        .then(function(response) {
          resolve(response);
        })
        .catch(function(response) {
          reject(response);
        });
      });
  //return axios.post(`${ROOT}/docqueue/upload`, data, config);
}

export function getGeocodingList(params) {
  return axios.get(`${ROOT}/geocoding`, {params})
}

export function getActivityList(params) {
  return axios.get(`${ROOT}/activity`, {params})
}

export function getExtractList(params) {
  return axios.get(`${ROOT}/extracted`, {params})
}

