// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import iView from 'iview'
import './index.less'
import '@/assets/less/main.less'
import '@/assets/css/icon.css';
import store from './store'
import config from '@/config'
import http from './api/http'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUI)

Vue.config.productionTip = false

/**
 * @description 全局注册应用配置
 */
Vue.prototype.$config = config

Vue.prototype.$http = http

Vue.prototype.$bus = new Vue();

Vue.use(iView, {
  transfer: true
});

/* eslint-disable no-new */
let vue = new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})

export default vue


