<template>
  <div class="loading" v-show="loading">
    <!--<img src="./loading.gif">-->
    <Spin fix>
      <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
      <div>加载中</div>
    </Spin>
  </div>
</template>
<script>
  export default {
    name: 'loading',
    data() {
      return {
        loading: false
      }
    },
    created() {
      let that = this;
      this.$bus.$on('loading', function(data) {
        that.loading = !!data;
      })
    }
  }
</script>
<style scoped lang="less">
  .loading {
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    position: fixed;
    left: calc(50% - 50px);
    top:  calc(50% - 50px);
    z-index: 9999999;
    width: 100px;
    height: 100px;
    border-radius: 10px;
    color: #fff;
    background-color: rgba(0, 0, 0, 0.8);
    p {
      padding: .15rem .15rem .2rem;
      color: #fff;
      font-size: .16rem;
    }
    img {
      width: .4rem;
      height: .4rem;
    }
  }
  .demo-spin-icon-load{
    animation: ani-demo-spin 1s linear infinite;
  }
</style>
