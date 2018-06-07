<template>
  <div v-if="vestiging">
    <hr>
    <div>
      <router-link :to="{ name: 'Vestigingen' }"> &lt; Terug naar zoekpagina</router-link>
    </div>
    <hr>
    <div class="page-title-block">
      <h3 class="d-inline">
        {{ vestiging.naam }}
      </h3>
      <div class="float-right small">
        {{ vestiging.brin6 }},
        {{ vestiging.adres.adres }}, {{ vestiging.adres.postcode }} {{ vestiging.adres.plaats }}
        ({{ vestiging.gebiedscode}}, {{ vestiging.adres.stadsdeel }})
      </div>
    </div>

    <div class="zone-clear clear"></div>

    <div class="navigation">
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a :class="{ 'active': selected === 'algemeen', 'nav-link': true }" href="javascript:void(0)" @click="show('algemeen')">Algemene Informatie</a>
        </li>
        <li class="nav-item">
          <a :class="{ 'active': selected === 'vestiging', 'nav-link': true }" href="javascript:void(0)" @click="show('vestiging')">De vestiging</a>
        </li>
        <li class="nav-item">
          <a :class="{ 'active': selected === 'omgeving', 'nav-link': true }" href="javascript:void(0)" @click="show('omgeving')">De omgeving</a>
        </li>
      </ul>
    </div>

    <div class="zone-clear clear"></div>
    <div id="algemeen" v-show="selected === 'algemeen'">
      <algemene-informatie :vestiging="vestiging"></algemene-informatie>
    </div>

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
import algemeneInformatie from './AlgemeneInformatie'

export default {
  data () {
    return {
      id: this.$route.params.id,
      vestiging: null,
      gebiedscode: null,
      selected: 'algemeen'
    }
  },
  components: {
    'vestigingscijfers': vestigingscijfers,
    'gebiedscijfers': gebiedscijfers,
    'algemene-informatie': algemeneInformatie
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
    margin-bottom: 2rem;
    margin-top: 2rem;
  }
  * {
    border-radius: 0 !important;
  }
  hr {
    margin-top: 5px;
    margin-bottom: 5px
  }

  .page-title-block {
    margin-top: 2rem
  }
</style>
