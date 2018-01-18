<template>
  <div v-if="vestiging">
    Vestiging {{ vestiging.naam }} - {{ vestiging.brin6 }}
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
  created () {
    let brin6 = this.$route.params.id
    let vestigingen = this.$store.state.vestigingen
    this.vestiging = vestigingen.find(v => v.brin6 === brin6)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
