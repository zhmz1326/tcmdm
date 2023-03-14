import API from './api'
import FETCH from './fetch'
import qs from 'Qs'

export default {
  apriori(requestForm, formData){
    formData.set('data', JSON.stringify(requestForm));
    return FETCH.post(API.API_Apriori, formData)
  },

  bk(requestForm, formData){
    formData.set('data', JSON.stringify(requestForm));
    return FETCH.post(API.API_Bk, formData)
  },

  cluster(requestForm, formData){
    formData.set('data', JSON.stringify(requestForm));
    return FETCH.post(API.API_Cluster, formData)
  },

  decision(requestForm, formData){
    formData.set('data', JSON.stringify(requestForm));
    return FETCH.post(API.API_Decision, formData)
  },
}