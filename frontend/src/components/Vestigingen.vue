<template>
  <div>
    <div class="rij mode_input text rij_verplicht">
      <label for="formInput">Zoek een vestiging</label>
      <div class="invoer">
        <input v-model="filterText"
               type="text"
               id="formInput"
               class="input"
               placeholder="Zoektekst">
      </div>

      <button class="action primary" @click="clearFilter()">Clear</button>
    </div>

    <table v-if="filteredVestigingen.length" class="table table-sm table-striped table-bordered">
      <thead>
        <tr>
          <th scope="col">School</th>
          <th scope="col">BRIN6</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="vestiging in filteredVestigingen" :key="vestiging.brin6">
          <td>
            <router-link :to="{path: 'vestiging/' + vestiging.brin6}">{{vestiging.naam}}</router-link>
          </td>
          <td>
            {{vestiging.brin6}}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

/**
 * Filter on naam and brin
 * @param v
 * @returns {string}
 */
const vestigingText = v => ['naam', 'brin'].map(key => v[key].toLowerCase()).join('.')

/**
 * autofilter timeout
 */
let autoFilter

export default {
  computed: {
    ...mapGetters([
      'vestigingen'
    ])
  },
  data () {
    return {
      filteredVestigingen: [],
      filterText: ''
    }
  },
  methods: {
    clearFilter () {
      this.filterText = ''
      this.filteredVestigingen = this.vestigingen
    },

    filter () {
      this.filteredVestigingen = this.vestigingen.filter(v => vestigingText(v).includes(this.filterText.toLowerCase()))
    }
  },
  watch: {
    'vestigingen' () {
      this.clearFilter()
    },
    'filterText' () {
      if (autoFilter) {
        clearTimeout(autoFilter)
      }
      autoFilter = setTimeout(() => this.filter(), 250)
    }
  },
  created () {
    this.clearFilter()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
