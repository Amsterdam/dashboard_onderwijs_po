<template>
  <div v-if="vestiging">
    <h3>
      {{ vestiging.naam }}
      <span class="float-right small">
        {{ vestiging.brin6 }},
        {{ vestiging.adres.adres }}, {{ vestiging.adres.postcode }} {{ vestiging.adres.plaats }}
        ({{ vestiging.gebiedscode}}, {{ vestiging.adres.stadsdeel }})
      </span>
    </h3>

    <div class="zone-clear clear"></div>

    <div class="navigation">
      <ul class="tabs">
        <li :class="{ 'selected': selected === 'vestiging'}">
          <a href="javascript:void(0)" @click="show('vestiging')">De vestiging</a>
        </li>
        <li :class="{ 'selected': selected === 'omgeving'}">
          <a href="javascript:void(0)" @click="show('omgeving')">De omgeving</a>
        </li>
      </ul>
    </div>

    <div class="zone-clear clear"></div>

    <div id="vestiging" v-show="selected === 'vestiging'">
      <vestigingscijfers :id="id" :gebiedscode="gebiedscode"></vestigingscijfers>
    </div>

    <div id="omgeving" v-show="selected === 'omgeving'">
      <gebiedscijfers :gebiedscode="gebiedscode"></gebiedscijfers>
    </div>
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
      gebiedscode: null,
      selected: 'vestiging'
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
    },
    show (item) {
      this.selected = item
    }
  },
  created () {
    this.setVestiging()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .navigation {
    margin-left: -40px;
  }
</style>
