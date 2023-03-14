<style scoped>
  .menu-icon{
    transition: all .3s;
  }
  .menu-item span{
    display: inline-block;
    overflow: hidden;
    width: 69px;
    text-overflow: ellipsis;
    white-space: nowrap;
    vertical-align: bottom;
    transition: width .2s ease .2s;
  }
  .menu-item i{
    transform: translateX(0px);
    transition: font-size .2s ease, transform .2s ease;
    vertical-align: middle;
    font-size: 16px;
  }
  .collapsed-menu span{
    width: 0px;
    transition: width .2s ease;
  }
  .collapsed-menu i{
    transform: translateX(5px);
    transition: font-size .2s ease .2s, transform .2s ease .2s;
    vertical-align: middle;
    font-size: 22px;
  }
</style>
<template>
  <div class="side-menu-wrapper">
  <Menu v-show="!isCollapsed" :active-name="$route.name" width="auto" ref="menu" :open-names="openNames" :accordion="accordion" theme="dark" :class="menuitemClasses" @on-select="handleSelect">
    <template v-for="item in menus">
      <template v-if="item.children && !item.meta.isIndex && !item.meta.hideInMenu">
        <Submenu :name="item.name">
          <template slot="title">
            <Icon :type="item.meta.icon" :size="14"/>
            {{item.meta.title}}
          </template>
          <template v-for="subItem in item.children">
            <v-side-menu-item :parent-item="item" :item="subItem"></v-side-menu-item>
          </template>
        </Submenu>
      </template>
      <template v-else>
        <v-side-menu-item  v-if="!item.meta.hideInMenu" :item="item"></v-side-menu-item>
      </template>
    </template>
  </Menu>
  <div class="menu-collapsed" v-show="isCollapsed" >
    <template v-for="item in menus">
        <Dropdown v-if="item.children" placement="right-end" @on-click="handleClick">
          <a class="drop-menu-a">
            <Icon :type="item.meta.icon" :size="20" color="#fff"></Icon>
          </a>
          <DropdownMenu slot="list">
            <template v-for="subItem in item.children">
              <DropdownItem :name="subItem.name"><Icon :type="subItem.meta.icon"/><span style="padding-left: 6px">{{subItem.meta.title}}</span></DropdownItem>
            </template>
          </DropdownMenu>
        </Dropdown>
      <Tooltip v-else :content="item.meta.title" placement="right">
        <a v-if="!item.meta.hideInMenu" class="drop-menu-a" @click="handleSelect(item.name)">
          <Icon :type="item.meta.icon" :size="20" color="#fff"></Icon>
        </a>
      </Tooltip>
    </template>
  </div>
  </div>
</template>

<script>
  import VSideMenuItem from "./SideMenuItem"
  import Menus from "@/pages/admin/router/router"
  export default {
    data() {
      return {
        menus:Menus,
        openNames: [],
        accordion: true
      }
    },
    computed: {
      menuitemClasses() {
        return [
          'menu-item',
          this.isCollapsed ? 'collapsed-menu' : ''
        ]
      }
    },
    methods: {
      getOpenedNamesByActiveName (name) {
        return this.$route.matched.map(item => item.name).filter(item => item !== name)
      },
      updateOpenName (name) {
        if (name === "home") this.openNames = []
        else this.openNames = this.getOpenedNamesByActiveName(name)
        this.$nextTick(() => {
          this.$refs.menu.updateOpened()
        })
      },
      handleSelect(name){
        this.$emit('on-select', name)
      },
      handleClick(name){
        this.$router.push({
          name,
        })
      },
    },
    watch:{
      activeName (name) {
        this.openNames = this.getOpenedNamesByActiveName(name)
      }
    },
    props: {
      isCollapsed: false
    },
    components: {VSideMenuItem}
  }
</script>


