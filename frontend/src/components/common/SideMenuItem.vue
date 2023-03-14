<template>
  <MenuItem :name="item.meta.isIndex?$config.homeName:item.name">
    <template>
      <Icon :type="item.meta.icon" :size="14"/>
      {{item.meta.title}}
    </template>
  </MenuItem>
</template>

<script>
  export default {
    props: {
      item: {},
      parentItem: {}
    }
  }
</script>
