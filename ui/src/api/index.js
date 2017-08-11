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

export function uploadDocToAPI(fileData) {
  const {file, country} = fileData;
  let data = new FormData();
  data.append('file', file, file.name);
  data.append('country', country);
  const config = {
    headers: { 'content-type': 'multipart/form-data' }
  };
  return axios.post(`${ROOT}/docqueue/upload`, data, config);
}
