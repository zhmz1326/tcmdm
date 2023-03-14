<template>
  <div @click="handleChange" :class="['siderTrigger', collapsed ? 'collapsed' : '']">
    <Icon :style="{margin: '0 20px'}" type="md-menu" size="24"></Icon>
  </div>
</template>

<script>
  export default {
    props: {
      collapsed: Boolean,
    },
    methods: {
      handleChange () {
        this.$emit('on-change', !this.collapsed)
      }
    }
  }
</script>

<style lang="less" scoped>
  .trans{
    transition: transform .2s ease;
  }
  @size: 40px;
  .siderTrigger {
    padding: 6px;
    width: @size;
    height: @size;
    display: inline-block;
    text-align: center;
    color: #5c6b77;
    margin-top: 12px;
    i{
      .trans;
      vertical-align: top;
    }
    &.collapsed i{
      transform: rotateZ(90deg);
      .trans;
    }
  }
</style>

