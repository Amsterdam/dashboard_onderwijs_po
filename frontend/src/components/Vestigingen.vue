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
export default {
  data () {
    return {
      vestigingen: []
    }
  },
  created () {
    this.vestigingen = this.$store.state.vestigingen
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
