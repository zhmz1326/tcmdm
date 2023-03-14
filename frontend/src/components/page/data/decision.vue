<template>
  <div class="datasetManager">
    <div class="search-con search-con-top">
      <Form ref="editData" :model="editData" :rules="ruleValidate" :label-width="100" >
        <FormItem label="病历数据" prop="datasetpath">
          <div class="import-file">
            <span>选择文件(csv或txt文件，病案与中药处方各一列)</span>
            <input type="file" @change="handleFileChange" ref="inputer" accept=".csv,.txt"/>
            <span>{{ uploadFileInfo.fileName }}</span>
          </div>
          <div class="import-file-error">{{uploadFileInfo.errmsg}}</div>
        </FormItem>
        <FormItem label="需分析的中药" prop="tcm">
          <Input v-model.trim="editData.tcm" placeholder="需分析的中药"></Input>
        </FormItem>
        
      </Form>
      <Button class="search-btn" style="margin-left:100px" @click="doAnalysis" type="primary">
        决策树分析
      </Button>
    </div>

    <div class="search-con search-con-top">
      中药决策树图
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
        mix_img: '',
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
      doAnalysis(){
        let formData = this.uploadFileInfo.formData;
        if(!formData){
            this.$Message.error("请先选择文件");
            return ;
        }     
        this.$refs['editData'].validate((valid) => {
          if(valid) {
            let obj = Object.assign({},this.editData);
              this.$http.decision(obj, formData).then(resp=>{
                  this.$Message.success("操作成功")
                  
                  this.mix_img = baseUrl + '/static/' + resp.mix_img
              })
            // }
          }
        });
      }
    },
    created() {
    }
  }
</script>
