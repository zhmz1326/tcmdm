<template>
  <div class="datasetManager">
    <div class="search-con search-con-top">
      <Form ref="editData" :model="editData" :rules="ruleValidate" :label-width="150" >
        <FormItem label="病历数据" prop="datasetpath">
          <div class="import-file">
            <span>选择文件(csv或txt文件，病案与中药处方各一列)</span>
            <input type="file" @change="handleFileChange" ref="inputer" accept=".csv,.txt"/>
            <span>{{ uploadFileInfo.fileName }}</span>
          </div>
          <div class="import-file-error">{{uploadFileInfo.errmsg}}</div>
        </FormItem>
        <FormItem label="最小共现数" prop="threshold">
          <Input v-model.trim="editData.threshold" placeholder="请输入0以上的整数"></Input>
        </FormItem>
        <FormItem label="置信度（CBWN）" prop="cbwn">
          <Input v-model.trim="editData.cbwn" placeholder="请输入0-1以内的小数"></Input>
        </FormItem>
        <FormItem label="支持度的α水平值（SBCα）" prop="sbc">
          <Input v-model.trim="editData.sbc" placeholder="请输入0-1以内的小数"></Input>
        </FormItem>
        <FormItem label="绘制图形最小共现数" prop="draw_threshold">
          <Input v-model.trim="editData.draw_threshold" placeholder="请输入0以上的整数"></Input>
        </FormItem>
      </Form>
      <Button class="search-btn" style="margin-left:150px" @click="doBK" type="primary">
        BK分析
      </Button>
    </div>

    <div class="search-con search-con-top">
      核心药对
    </div>
    <Table :columns="cloumns" border :data="tcm_rules" stripe></Table>
    <div class="search-con search-con-top">
      核心症状
    </div>
    <Table :columns="cloumns" border :data="symptom_rules" stripe></Table>
    <div class="search-con search-con-top">
      症状中药混合
    </div>
    <Table :columns="cloumns" border :data="mix_rules" stripe></Table>
    
    
    <div class="search-con search-con-top">
      药对网络图
    </div>
    <img :src="tcm_img" v-if="tcm_img!=null && tcm_img!=''"></img>
    
    <div class="search-con search-con-top">
      症状网络图
    </div>
    <img :src="symptom_img" v-if="symptom_img!=null && symptom_img!=''"></img>

    <div class="search-con search-con-top">
      症状中药混合网络图
    </div>
    <img :src="mix_img" v-if="mix_img!=null && mix_img!=''"></img>

  </div>
</template>

<script>
  import {baseUrl} from "@/pages/admin/api/fetch";
  export default {
    name: 'datasetManager',
    data() {
      return {
        tcm_rules: [],
        symptom_rules: [],
        mix_rules: [],
        tcm_img: '',
        symptom_img: '',
        mix_img: '',
        cloumns:[
          {
            key: 'index',
            title: '序号',
            align: 'center'
          },
          {
            key: 'rule',
            title: '组合',
            align: 'center'
          },
          {
            key: 'count',
            title: '组合中元素个数',
            align: 'center'
          },
          {
            key: 'cbwn',
            title: '置信度（CBWN）',
            align: 'center'
          },
          {
            key: 'sbc',
            title: '支持度的α水平值（SBCα）',
            align: 'center'
          }
         ],
         editData: {
            // min_support: 0,
            // min_confidence: 0
         },
         ruleValidate: {
         },
         uploadFileInfo: {
            fileName: '',
            formData: null,
            errmsg: ''
         }
      }
    },
    methods: {
      resetForm(show) {
        if (!show) {
          this.isdisabledFn = false;
          this.editFlag = false;
          this.$refs.editData.resetFields();
          this.editData.id = 0;
          this.clearFileUpload();
        }
      },
      handleFileChange(e) {
        let file = this.$refs.inputer.files[0];
        let formData = new FormData();
        formData.append("file", file);
        this.uploadFileInfo.formData = formData;
        this.uploadFileInfo.fileName = file.name;
        this.uploadFileInfo.errmsg = '';
      },
      doBK(){
        let formData = this.uploadFileInfo.formData;
        if(!formData){
            this.$Message.error("请先选择文件");
            return ;
        }     
        this.$refs['editData'].validate((valid) => {
          if(valid) {
            let obj = Object.assign({},this.editData);
            this.$http.bk(obj, formData).then(resp=>{
                this.$Message.success("操作成功")
                
                this.tcm_rules = resp.tcm_rules
                this.symptom_rules = resp.symptom_rules
                this.mix_rules = resp.mix_rules
                
                this.tcm_img = baseUrl + '/static/' + resp.tcm_img
                this.symptom_img = baseUrl + '/static/' + resp.symptom_img
                this.mix_img = baseUrl + '/static/' + resp.mix_img
            })
          }
        });
      }
    },
    created() {
    }
  }
</script>
