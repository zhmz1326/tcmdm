<style scoped>
  .layout{
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
  }
  .layout-header-bar{
    background: #fff;
    box-shadow: 0 1px 1px rgba(0,0,0,.1);
  }
  .layout-logo-left{
    width: 90%;
    height: 30px;
    background: #5b6270;
    border-radius: 3px;
    margin: 15px auto;
  }
  .rotate-icon{
    transform: rotate(-90deg);
  }
</style>
<template>
    <Layout style="height: 100%" class="main">
      <Sider ref="side1" hide-trigger collapsible :width="256" class="left-sider" :collapsed-width="64" v-model="isCollapsed" >
        <v-side-bar @on-select="handleSelect" ref="sideMenu" :isCollapsed="isCollapsed"></v-side-bar>
      </Sider>
      <Layout>
        <Header :style="{padding: 0}" class="layout-header-bar" >
          <v-header @on-coll-change="handleCollapsedChange" :collapsed="isCollapsed"></v-header>
        </Header>
        <Content :style="{background: '#f5f7f9', minHeight: '260px'}" class="main-content-con">
          <Layout class="main-layout-con">
          <div class="tag-nav-wrapper">
            <v-tags-nav :value="$route" @input="handleClick" :list="tagNavList" @on-close="handleCloseTag"></v-tags-nav>
          </div>
          <Content class="content-wrapper">
          <transition name="move">
            <keep-alive :include="cacheList">
              <router-view v-if="isRouterAlice"></router-view>
            </keep-alive>
          </transition>
          </Content>
          </Layout>
        </Content>
      </Layout>
    </Layout>
</template>
<script>
  import VSideBar from "./SideBar"
  import VHeader from "./Header"
  import VTagsNav from "./TagsNav"
  import routers from '@/pages/admin/router/router.js'
  import { mapMutations, mapActions, mapGetters } from 'vuex'
  import { getNewTagList,routeEqual} from '@/utils'
  export default {
    name:'home',
    components:{VSideBar,VHeader,VTagsNav},
    data () {
      return {
        isCollapsed: false,
        isRouterAlice: true
      }
    },
    computed: {
      rotateIcon () {
        return [
          'menu-icon',
          this.isCollapsed ? 'rotate-icon' : ''
        ];
      },
      tagNavList () {
        return this.$store.state.app.tagNavList
      },
      cacheList () {
        //const list = [...this.tagNavList.length ? this.tagNavList.filter(item => !(item.meta && item.meta.notCache)).map(item => item.name) : []]
        return [];
      }
    },
    methods: {
      ...mapMutations([
        'setHomeRoute',
        'setBreadCrumb',
        'setTagNavList',
        'addTag',
        'closeTag'
      ]),
      handleCollapsedChange (state) {
        this.isCollapsed = state
      },
      handleSelect(name){
        if(name){
           let currRoute = this.queryCurrentRoute();
           this.$router.push({name});
           if(currRoute && currRoute.name === name){
              this.refreshRoute();
           }
        }
      },
      handleClick(item) {
        this.handleSelect(item.name)
      },
      handleCloseTag (res, type, route) {
        if (type !== 'others') {
          if (type === 'all') {
            this.handleSelect(this.$config.homeName)
          } else {
            if (routeEqual(this.$route, route)) {
              this.closeTag(route)
            }
          }
        }
        this.setTagNavList(res)
      },
      queryCurrentRoute(){
        let router = this.$router;
        return router && router.app && router.app._route;
      },
      refreshRoute(){
        this.isRouterAlice = false
        this.$nextTick(()=>{
           this.isRouterAlice = true
        })
      }
    },
    watch: {
      '$route' (newRoute) {
        const { name, path,meta} = newRoute
        this.addTag({
          router: { name, path, meta },
          type: 'push'
        })
        this.setBreadCrumb(newRoute)
        this.setTagNavList(getNewTagList(this.tagNavList, newRoute))
      }
    },
    mounted() {
      this.setHomeRoute(routers)
      this.setTagNavList()
      this.setHomeRoute(routers)
      const { name, path, meta} = this.$route

      this.addTag({
        router: { name, path, meta }
      })
      this.setBreadCrumb(this.$route)
      this.$refs.sideMenu.updateOpenName(this.$route.name)
    }
  }
</script>
