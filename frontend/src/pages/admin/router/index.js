import Vue from 'vue'
import Router from 'vue-router'
import routes from './router'
Vue.use(Router)
import { getToken,inArray} from '@/utils'
import config from '@/config'
const { homeName } = config

const base = '';

const router = new Router({
  routes,
  mode: 'hash',
  base
})

export default router;
