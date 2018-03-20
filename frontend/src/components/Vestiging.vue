<template>
  <div v-if="vestiging">
    <h3>
      Vestiging:
      {{ vestiging.naam }}
      <span class="float-right small">
        {{ vestiging.brin6 }},
        {{ vestiging.adres.adres }}, {{ vestiging.adres.postcode }} {{ vestiging.adres.plaats }}
        ({{ vestiging.gebiedscode}}, {{ vestiging.adres.stadsdeel }})
      </span>
    </h3>
    <div class="clear"></div>

    <vestigingscijfers :id="id" :gebiedscode="gebiedscode"></vestigingscijfers>
    <gebiedscijfers :gebiedscode="gebiedscode"></gebiedscijfers>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import vestigingscijfers from './vestigingscijfers/Vestigingscijfers'
import gebiedscijfers from './gebiedscijfers/Gebiedscijfers'

export default {
  data () {
    return {
      id: this.$route.params.id,
      vestiging: null,
      gebiedscode: null
    }
  },
  components: {
    'vestigingscijfers': vestigingscijfers,
    'gebiedscijfers': gebiedscijfers
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
      if (this.vestiging) {
        this.gebiedscode = this.vestiging.gebiedscode
      }
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
