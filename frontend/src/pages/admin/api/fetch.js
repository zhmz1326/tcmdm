import axios from 'axios'
import config from '@/config'
import {getToken,getErrMsg} from "@/utils"
import { Message } from 'iview'
import router from '@/pages/admin/router'
import context from '@/pages/admin/admin.js'

export const baseUrl = process.env.NODE_ENV === 'development' ? config.baseUrl.dev : config.baseUrl.pro


const service = axios.create({
  baseURL: baseUrl, // api的base_url
  timeout: 5000          // 请求超时时间
});

export default service

// request拦截器，实现loading加载
service.interceptors.request.use(config => {
  context.$bus.$emit('loading', true);
  const token = getToken();
  config.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
  config.headers.Authorization = 'Bearer '+token;
  // config.timeout = 60000;
  config.timeout = 1800000;
  /*
  if(!token && config.url.indexOf("login") == -1) {
     router.push({name:"login"})
     return Promise.reject("请先登录")
  }
  */
  return config
}, error => {
  context.$bus.$emit('loading', false);
  Message.error(getErrMsg(error))
  return Promise.reject(error)
})

// response拦截器，实现loading关闭
service.interceptors.response.use(resp => {
  context.$bus.$emit('loading', false);
  if(resp.headers['content-type'] == 'application/octet-stream'){
	  return resp;
  }
  const {code,msg,data} = resp.data
  if (code !=200) {
    Message.error(msg)
    return Promise.reject(msg)
  }
  return data
}, error => {
  context.$bus.$emit('loading', false);
  Message.error(getErrMsg(error))
  return Promise.reject(error)
})
