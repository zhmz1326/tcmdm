<template>
  <div class="datasetManager">
    <div class="search-con search-con-top">
      <Form ref="editData" :model="editData" :rules="ruleValidate" :label-width="120" >
        <FormItem label="病历数据" prop="datasetpath">
          <div class="import-file">
            <span>选择文件(csv或txt文件，病案与中药处方各一列)</span>
            <input type="file" @change="handleFileChange" ref="inputer" accept=".csv,.txt"/>
            <span>{{ uploadFileInfo.fileName }}</span>
          </div>
          <div class="import-file-error">{{uploadFileInfo.errmsg}}</div>
        </FormItem>
        <FormItem label="中药最小纳入频次" prop="tcm_minimum_frequency ">
          <Input v-model.trim="editData.tcm_minimum_frequency" placeholder="请输入0以上的整数"></Input>
        </FormItem>
        <FormItem label="症状最小纳入频次" prop="symptom_minimum_frequency ">
          <Input v-model.trim="editData.symptom_minimum_frequency" placeholder="请输入0以上的整数"></Input>
        </FormItem>
        
      </Form>
      <Button class="search-btn" style="margin-left:120px" @click="doAnalysis" type="primary">
        层次聚类
      </Button>
    </div>

    <div class="search-con search-con-top">
      中药层次聚类结果
    </div>
    <img :src="tcm_img" v-if="tcm_img!=null && tcm_img!=''"></img>
    
    <div class="search-con search-con-top">
      症状层次聚类结果
    </div>
    <img :src="symptom_img" v-if="symptom_img!=null && symptom_img!=''"></img>
    
    <div class="search-con search-con-top">
      中药-症状层次聚类结果
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
        tcm_img: '',
        symptom_img: '',
        mix_img: '',
        itemsets_columns:[
          {
            key: 'count',
            title: '关键词数量',
            align: 'center'
          },
          {
            key: 'entity',
            title: '关键词',
            align: 'center'
          },
          {
            key: 'occurrence',
            title: '频次',
            align: 'center'
          },
          {
            key: 'frequency',
            title: '频率',
            align: 'center'
          }
         ],
        rules_columns:[
          {
            key: 'LHS',
            title: 'LHS',
            align: 'center'
          },
          {
            key: 'RHS',
            title: 'RHS',
            align: 'center'
          },
          {
            key: 'confidence',
            title: '置信度',
            align: 'center'
          },
          {
            key: 'support',
            title: '支持度',
            align: 'center'
          },
          {
            key: 'lift',
            title: '提升度',
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
      doAnalysis(){
        let formData = this.uploadFileInfo.formData;
        if(!formData){
            this.$Message.error("请先选择文件");
            return ;
        }     
        this.$refs['editData'].validate((valid) => {
          if(valid) {
            let obj = Object.assign({},this.editData);
              this.$http.cluster(obj, formData).then(resp=>{
                  this.$Message.success("操作成功")
                  
                  this.tcm_img = baseUrl + '/static/' + resp.tcm_img
                  this.symptom_img = baseUrl + '/static/' + resp.symptom_img
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
