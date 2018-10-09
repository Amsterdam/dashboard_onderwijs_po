<template>
  <div>
    <hr>
    <h3>Overzicht scholen Amsterdam</h3>
    <div class="input-group mb-5">
        <div class="invoer">
          <input
            v-model="filterText"
            type="text"
            id="formInput"
            class="input form-control"
            placeholder="Typ hier vestiging of BRIN"
          >
          <button
            type="button"
            class="embed-search__clear"
            title="Wis zoektekst"
            @click="clearFilter()"
            v-if="filterText.length"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M12 13.527l4.848 4.848 1.527-1.527L13.527 12l4.848-4.848-1.527-1.527-4.859 4.859-4.837-4.859-1.527 1.527L10.474 12l-4.849 4.848 1.527 1.527z"/>
            </svg>
          </button>
        </div>
    </div>

    <table v-if="filteredVestigingen.length" class="table table-sm">
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
            <div class="small">
            {{ vestiging.adres.adres }}, {{ vestiging.adres.postcode }} {{ vestiging.adres.plaats }}
            ({{ vestiging.adres.stadsdeel }})
            </div>

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
  * {
    border-radius: 0 !important;
  }

  .visually-hidden {
    display: none;
  }

  .form-control {
    height: 44px;
  }

  .invoer {
    width: 100%;
  }
</style>
