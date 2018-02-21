<template>
  <div id="gebiedscijfer-opleiding">
      <h3>placeholder opleiding</h3>
  </div>
</template>

<script>
import util from '@/services/util'

export default {
  props: [
    'gebiedscode'
  ],
  async created () {
    let url = `https://api.data.amsterdam.nl/bbga/cijfers/?gebiedcode15=${this.gebiedscode}&variabele=OSDQ10_P`
    let data = await util.readPaginatedHalJsonData(url)
    console.log('Opleiding', data)
  }
}

</script>

<style scoped>
</style>
