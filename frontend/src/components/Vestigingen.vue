<template>
  <table v-if="vestigingen.length" class="table table-sm table-striped table-bordered">
    <thead>
      <tr>
        <th scope="col">School</th>
        <th scope="col">BRIN6</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="vestiging in vestigingen" :key="vestiging.brin6">
        <td>
          <router-link :to="{path: 'vestiging/' + vestiging.brin6}">{{vestiging.naam}}</router-link>
        </td>
        <td>
          {{vestiging.brin6}}
        </td>
      </tr>
    </tbody>
  </table>
  <div v-else>
    Loading...
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  data () {
    return {
      vestigingen: []
    }
  },
  async created () {
    let next = 'https://data.amsterdam.nl/onderwijs/api/vestigingen/'
    this.vestigingen = []

    while (next) {
      try {
        let response = await Vue.axios.get(next)
        next = response.data.next
        response.data.results.forEach(result => {
          this.vestigingen.push({
            naam: result.naam,
            brin6: result.brin6
          })
        })
      } catch (e) {
        next = null
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
