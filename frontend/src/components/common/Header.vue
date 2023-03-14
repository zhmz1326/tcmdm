<template>
  <div class="header">
    <v-sider-trigger :collapsed="collapsed" @on-change="handleCollpasedChange"></v-sider-trigger>
    <v-bread-crumb style="margin-left: 30px;" :list="breadCrumbList"></v-bread-crumb>
  </div>
</template>

<script>
  import VSiderTrigger from './SiderTrigger'
  import VBreadCrumb from './BreadCrumb'
  import {clearUserinfo,getUserDetail} from "@/utils"
  import router from '@/pages/admin/router'
  export default {
    data() {
      return {
        modal:false,
        configmodal:false,
        pform:{
          oldpassword:'',
          newpassword:''
        },
        cform:{
          f1_threshold: 0.0,
        },
        userDetail: getUserDetail(),
        ruleValidate:{
          oldpassword:[{ required: true, message: '必须填密码', trigger: 'blur' }],
          newpassword:[{ required: true, message: '必须填密码', trigger: 'blur' }]   
        }
      }
    },
    computed: {
      breadCrumbList () {
        return this.$store.state.app.breadCrumbList
      }
    },
    props: {
      collapsed: Boolean
    },
    methods: {
      handleCollpasedChange (state) {
        this.$emit('on-coll-change', state)
      },
      handleSubmit(name){
        let that=this;
        this.$refs[name].validate((valid) => {
            if (valid) {
                this.$http.modifyPassword({newpassword:that.pform.newpassword,oldpassword:that.pform.oldpassword}).then(resp=>{
                  this.$Message.success("操作成功！");
                  this.modal = false;
                })
            }
        })
      },

      handleSubmitConfig(name){
        let that=this;
        this.$refs[name].validate((valid) => {
            if (valid) {
                this.$http.modifyConfig({f1_threshold:that.cform.f1_threshold}).then(resp=>{
                  this.$Message.success("操作成功！");
                  this.configmodal = false;
                })
            }
        })
      },
      handleClick (name) {
        let that=this;
        switch (name) {
          case 'logout':
            clearUserinfo()
            router.push('login')
            break;
          case 'modifypassword':
            that.modal=true;
            break;
          case 'modifyconfig':
            that.configmodal=true;
            break;
        }
      }
    },
    created() {
      // this.getF1Threshold();
    },
    components:{VSiderTrigger,VBreadCrumb}
  }
</script>

<style lang="less" scoped>
  .header {
    width: 100%;
    height: 100%;
    position: relative;
    .custom-content-con{
      float: right;
      height: auto;
      padding-right: 20px;
      line-height: 64px;
      & > *{
        float: right;
      }
    }
  }

  .user{
    &-avator-dropdown{
      cursor: pointer;
      display: inline-block;
      position:absolute;
      top:0;
      right: 20px;
      // height: 64px;
      vertical-align: middle;
      // line-height: 64px;
      .ivu-badge-dot{
        top: 16px;
      }
    }
  }
</style>
