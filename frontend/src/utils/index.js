import Cookies from 'js-cookie'
// cookie保存的天数
import config from '@/config'
const {cookieExpires} = config

let USERINFO_KEY = "USER_INFO";
let userinfo = null;
let currentFlag = '';

function getUserinfo(){
	if(!userinfo){
		userinfo = JSON.parse(localStorage.getItem(USERINFO_KEY + currentFlag));
	}
	return userinfo || {};
}

export const TOKEN_KEY = 'jwt-token'
	
export const setUserinfo = (userinfo,flag) =>{
  currentFlag = flag || 'admin';
  Cookies.set(TOKEN_KEY + currentFlag, 1, { expires: cookieExpires || 1});
	localStorage.setItem(USERINFO_KEY + currentFlag,JSON.stringify(userinfo));
}

export const getToken = (isMemberPage) => {
  if(isMemberPage !== undefined){
      currentFlag = isMemberPage; //isMemberPage ? 'member' : 'admin';
  }
  const token = Cookies.get(TOKEN_KEY + currentFlag);
  if(token){
	  return getUserinfo().token;
  }else {
	  return false;
  }
}

export const setToken = (token) =>{
	getUserinfo().token = token;
}

export const clearUserinfo = ()=>{
	Cookies.set(TOKEN_KEY + currentFlag, '', { expires: 0});
  userinfo = null;
  localStorage.removeItem(USERINFO_KEY + currentFlag);
}

export const getAuths = () =>{
	return getUserinfo().authList || [];
}

export const getRole = () =>{
	let userdetail = getUserinfo().userDetail;
	if(userdetail){
		return userdetail.roleid;
	}
	return null;
}

export const getUserDetail = () => {
  return getUserinfo().userDetail || {};
}

export const getHomeRoute = (routers, homeName = 'home') => {
  let i = -1
  let len = routers.length
  let homeRoute = {}
  while (++i < len) {
    let item = routers[i]
    if (item.children && item.children.length) {
      let res = getHomeRoute(item.children, homeName)
      if (res.name) return res
    } else {
      if (item.name === homeName) homeRoute = item
    }
  }
  return homeRoute
}

export const getBreadCrumbList = (route, homeRoute) => {
  let homeItem = { ...homeRoute, icon: homeRoute.meta.icon }
  let routeMetched = route.matched
  if (routeMetched.some(item => item.name === homeRoute.name)) return [homeItem]
  let res = routeMetched.filter(item => {
    return item.meta === undefined || !item.meta.hideInBread
  }).map(item => {
    let meta = { ...item.meta }
    if (meta.title && typeof meta.title === 'function') {
    meta.__titleIsFunction__ = true
    meta.title = meta.title(route)
  }
  let obj = {
    icon: (item.meta && item.meta.icon) || '',
    name: item.name,
    meta: meta
  }
  return obj
})
  res = res.filter(item => {
    return !item.meta.hideInMenu
  })
  return [{ ...homeItem, to: homeRoute.path }, ...res]
}

/**
 * @description 本地存储和获取标签导航列表
 */
export const setTagNavListInLocalstorage = list => {
  localStorage.tagNavList = JSON.stringify(list)
}
/**
 * @returns {Array} 其中的每个元素只包含路由原信息中的name, path, meta三项
 */
export const getTagNavListFromLocalstorage = () => {
  const list = localStorage.tagNavList
  return list ? JSON.parse(list) : []
}

/**
 * @param {Number} times 回调函数需要执行的次数
 * @param {Function} callback 回调函数
 */
export const doCustomTimes = (times, callback) => {
  let i = -1
  while (++i < times) {
    callback(i)
  }
}

/**
 * 判断打开的标签列表里是否已存在这个新添加的路由对象
 */
export const routeHasExist = (tagNavList, routeItem) => {
  let len = tagNavList.length
  let res = false
  doCustomTimes(len, (index) => {
    if (routeEqual(tagNavList[index], routeItem)) res = true
})
  return res
}

/**
 * @description 根据name/params/query判断两个路由对象是否相等
 * @param {*} route1 路由对象
 * @param {*} route2 路由对象
 */
export const routeEqual = (route1, route2) => {
  return (route1.name === route2.name)
}

/**
 * @param {*} list 现有标签导航列表
 * @param {*} newRoute 新添加的路由原信息对象
 * @description 如果该newRoute已经存在则不再添加
 */
export const getNewTagList = (list, newRoute) => {
  const { name, path, meta } = newRoute
  let newList = [...list]
  if (newList.findIndex(item => item.name === name) >= 0) return newList
else newList.push({ name, path, meta })
  return newList
}

export const showTitle = (item, vm) => {
  let { title, __titleIsFunction__ } = item.meta
  if (!title) return
  return title
}

/**
 * @param {Array} list 标签列表
 * @param {String} name 当前关闭的标签的name
 */
export const getNextRoute = (list, route) => {
  let res = {}
  if (list.length === 2) {
    res = getHomeRoute(list)
  } else {
    const index = list.findIndex(item => routeEqual(item, route))
    if (index === list.length - 1) res = list[list.length - 2]
    else res = list[index + 1]
  }
  return res
}

export const strToArr = (str,fg=',') =>{
	let arr = [];
	if(str){
		arr = str.split(fg);
	}
	return arr;
}
export const arrToStr = (arr,fg=",") =>{
	if(arr){
		return arr.join(fg);
	}
	return '';
}

export const inArray = (value,arr) =>{
   if(arr){
      for(let i in arr){
        if(value === arr[i]){
           return true;
        }
      }
   }
   return false;
}

export const getErrMsg = (error) =>{
   let errMsg = '';
   if(typeof error === 'object'){
       if(error.message){
          errMsg = errMsgObj[error.message];
       }
   }
   return errMsg || '请求失败';
}

let errMsgObj = {
   'Network Error': '网络错误'
}
