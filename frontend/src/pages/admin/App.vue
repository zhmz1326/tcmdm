<template>
  <div id="app">
    <v-loading></v-loading>
    <router-view></router-view>
  </div>
</template>

<script>
  import VLoading from "@/components/common/Loading"
  export default {
    name: 'app',
    components:{VLoading}
  }
</script>

<style lang="less">
  .size{
    width: 100%;
    height: 100%;
  }
  html,body{
    .size;
    overflow: hidden;
    margin: 0;
    padding: 0;
  }
  #app {
    .size;
  }
</style>
