<template>
  <div>
    <a v-if="linkdata && filename && text" v-bind:href="linkdata" v-bind:download="filename">{{text}}</a>
  </div>
</template>

<script>
export default {
  props: [
    'data',
    'text',
    'filename'
  ],
  data () {
    return {
      linkdata: ''
    }
  },
  watch: {
    data (to, from) {
      if (to.length) {
        this.linkdata = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(to))
      }
    }
  }
}
</script>

<style>

</style>
