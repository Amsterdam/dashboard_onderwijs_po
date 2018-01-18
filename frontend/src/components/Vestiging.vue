<template>
  <div v-if="vestiging">
    Vestiging {{ vestiging.naam }} - {{ vestiging.brin6 }}
  </div>
  <div v-else>
    Loading... {{brin6}}
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data () {
    return {
      brin6: null,
      vestiging: null
    }
  },
  computed: {
    ...mapGetters([
      'vestigingen'
    ])
  },
  watch: {
    vestigingen: function (vestigingen) {
      if (!this.vestiging) {
        this.vestiging = vestigingen.find(v => v.brin6 === this.brin6)
      }
    }
  },
  created () {
    this.brin6 = this.$route.params.id
    let vestigingen = this.$store.state.vestigingen
    this.vestiging = vestigingen.find(v => v.brin6 === this.brin6)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
