<template>
  <div class="custom-bread-crumb">
    <Breadcrumb >
      <BreadcrumbItem v-for="item in list" :to="item.to" :key="`bread-crumb-${item.name}`">
        <Icon style="margin-right: 4px;" :type="item.icon || ''"/>
        {{ item.meta.title }}
      </BreadcrumbItem>
    </Breadcrumb>
  </div>
</template>

<style scoped>
  .custom-bread-crumb{
    display: inline-block;
    vertical-align: top;
  }
</style>

<script>
  export default {
    props: {
      list: {
        type: Array,
        default: () => []
      }
    }
  }
</script>
