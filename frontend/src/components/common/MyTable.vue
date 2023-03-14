<template>
  <div class="my-table">
    <el-table :data="data" :row-class-name="rowClass" :span-method="spanMethod">
      <my-column v-for="(item,index) in columns" :key="index" :columns="item"></my-column>
    </el-table>
  </div>
</template>
<script>
import MyColumn from './MyColumn'
export default {
  components: {
    MyColumn
  },
  props: {
    columns: {
      type: Array
    },
    data: {
      type: Array
    },
    rowClass: {
      type: Function
    },
    spanMethod: {
      type: Function
    }
  }
}
</script>
<style scoped>
</style>