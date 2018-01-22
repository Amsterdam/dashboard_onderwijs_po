<template>
  <div v-if="vestiging">
    Vestiging {{ vestiging.naam }} - {{ vestiging.brin6 }}

    <leerlingen-naar-gewicht :id="id"></leerlingen-naar-gewicht>
    <school-advies :id="id"></school-advies>
  </div>
  <div v-else>
    Loading... {{id}}
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import leerlingenNaarGewicht from './LeerlingenNaarGewicht'
import schoolAdvies from './SchoolAdvies'

export default {
  data () {
    return {
      id: this.$route.params.id,
      vestiging: null
    }
  },
  components: {
    'leerlingen-naar-gewicht': leerlingenNaarGewicht,
    'school-advies': schoolAdvies
  },
  computed: {
    ...mapGetters([
      'vestigingen'
    ])
  },
  watch: {
    '$route' (to, from) {
      this.id = to.params.id
      this.setVestiging()
    },
    vestigingen () {
      if (!this.vestiging) {
        this.setVestiging()
      }
    }
  },
  methods: {
    setVestiging () {
      this.vestiging = this.vestigingen.find(v => v.brin6 === this.id)
    }
  },
  created () {
    this.setVestiging()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
