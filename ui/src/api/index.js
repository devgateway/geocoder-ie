import axios from 'axios'


const ROOT=window.API_ROOT
export function getSentences(params) {
  return axios.get(`${ROOT}/corpora`, {
    params: params
  })
}


export function deleteSentenceById(id) {
  return axios.delete(`${ROOT}/corpora/${id}`)
}

export function updateSentenceById(id, category) {
  debugger
  return axios.post(`${ROOT}/corpora/${id}`, {
    category: category
  })
}
