<template>
  <div v-if="vestiging">
    Vestiging {{ vestiging.brin6 }}
  </div>
  <div v-else>
    Loading...
  </div>
</template>

<script>
export default {
  data () {
    return {
      vestiging: null
    }
  },
  async created () {
    // Set this.vestiging
    this.vestiging = {
      brin6: this.$route.params.id
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
