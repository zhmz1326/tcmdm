<template>
  <el-table-column :prop="columns.prop" :formatter="columns.formatter"
    :label="columns.label" 
    align="center" show-overflow-tooltip>
    <template v-if="columns.children">
      <my-column v-for="(item, index) in columns.children"
        :key="index"
        :columns="item"></my-column>
    </template>
  </el-table-column>
</template>
<script>
export default {
  name: 'MyColumn',
  props: {
    columns: {
      type: Object
    }
  }
}
</script>
<style>
.my-table .el-table thead.is-group th{
   background-color: #f8f8f9;
   border: 1px solid #e8eaec;
}
.my-table .el-table thead.is-group th>.cell{
   background-color: #f8f8f9;
   color: #515a6e;
   font-size: 12px;
}
</style>