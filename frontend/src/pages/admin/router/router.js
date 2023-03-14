import Home from '@/components/common/Home'
import HelloWorld from "@/components/HelloWorld";

export default [
{
  path: '/',
  name: 'index',
  component: Home,
  redirect: '/home',
  meta: {
    title: '首页',
    icon: 'md-home',
    isIndex: true
  },
  children: [{
    path: '/home',
    name: 'home',
    meta: {
      title: '首页',
      icon: 'md-home'
    },
    component: HelloWorld
  }]
},
{
  path: '/data',
  name: 'data',
  meta: {
    title: '数据挖掘',
    icon: 'md-laptop'
  },
  component: Home,
  children: [
    {
      path: 'apriori',
      name: 'apriori',
      meta: {
        icon: 'md-clipboard',
        title: 'Apriori关联规则分析'
      },
      component: () => import('@/components/page/data/apriori')
    },
    {
      path: 'bk',
      name: 'bk',
      meta: {
        icon: 'md-clipboard',
        title: 'Bron-Kerbosch极大团分析'
      },
      component: () => import('@/components/page/data/bk')
    },
    {
      path: 'clustering',
      name: 'clustering',
      meta: {
        icon: 'md-clipboard',
        title: 'Clustering聚类分析'
      },
      component: () => import('@/components/page/data/clustering')
    },
    {
      path: 'decision',
      name: 'decision',
      meta: {
        icon: 'md-clipboard',
        title: 'Decision Tree决策树分析'
      },
      component: () => import('@/components/page/data/decision')
    }
  ]
}]
