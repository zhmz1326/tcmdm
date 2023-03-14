<template>
  <div class="datamining">
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
        <FormItem label="最小支持度" prop="min_support">
          <Input v-model.trim="editData.min_support" placeholder="请输入0-1之间的小数"></Input>
        </FormItem>
        <FormItem label="最小置信度" prop="min_confidence">
          <Input v-model.trim="editData.min_confidence" placeholder="请输入0-1之间的小数"></Input>
        </FormItem>
        <FormItem label="去除的高频词" prop="stopWords">
          <Input v-model.trim="editData.stopWords" placeholder="不纳入分析的词汇，空格分隔，可选"></Input>
        </FormItem>
        
      </Form>
      <Button class="search-btn" style="margin-left:100px" @click="doApriori" type="primary">
        Apriori分析
      </Button>
    </div>

    <div class="search-con search-con-top">
      中药出现频次
    </div>
    <Table :columns="itemsets_columns" border :data="tcm_itemsets" stripe></Table>
    <div class="search-con search-con-top">
      中药关联规则
    </div>
    <Table :columns="rules_columns" border :data="tcm_rules" stripe></Table>
    
    <div class="search-con search-con-top">
      症状出现频次
    </div>
    <Table :columns="itemsets_columns" border :data="symptom_itemsets" stripe></Table>
    <div class="search-con search-con-top">
      症状关联规则
    </div>
    <Table :columns="rules_columns" border :data="symptom_rules" stripe></Table>

    <div class="search-con search-con-top">
      症状-中药关联规则
    </div>
    <Table :columns="rules_columns" border :data="symptom_tcm_rules" stripe></Table>
    <div class="search-con search-con-top">
      中药-症状关联规则
    </div>
    <Table :columns="rules_columns" border :data="tcm_symptom_rules" stripe></Table>
  </div>
</template>

<script>
  export default {
    name: 'datamining',
    data() {
      return {
        tcm_itemsets: [],
        tcm_rules: [],
        symptom_itemsets: [],
        symptom_rules: [],
        symptom_tcm_rules: [],
        tcm_symptom_rules: [],
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
      doApriori(){
        let formData = this.uploadFileInfo.formData;
        if(!formData){
            this.$Message.error("请先选择文件");
            return ;
        }     
        this.$refs['editData'].validate((valid) => {
          if(valid) {
            let obj = Object.assign({},this.editData);
              this.$http.apriori(obj, formData).then(resp=>{
                  this.$Message.success("操作成功")
                  
                  this.tcm_itemsets = resp.tcm_itemsets
                  this.tcm_rules = resp.tcm_rules
                  
                  this.symptom_itemsets = resp.symptom_itemsets
                  this.symptom_rules = resp.symptom_rules
                  
                  this.symptom_tcm_rules = resp.symptom_tcm_rules
                  this.tcm_symptom_rules = resp.tcm_symptom_rules
              })
          }
        });
      }
    },
    created() {
    }
  }
</script>
