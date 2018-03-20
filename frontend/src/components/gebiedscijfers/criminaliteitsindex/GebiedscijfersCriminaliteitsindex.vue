<template>
  <div>
    <h1 v-if="data" class="single-figure">{{data[0].waarde}}</h1>
    <data-download-link :data="data" text="Download veiligheidsindex cijfers JSON" filename="veiligheids-index.json"></data-download-link>
  </div>
</template>

<script>
import { getBbgaVariables } from '@/services/bbgareader'

import dataDownloadLink from '@/components/general/dataDownloadLink'

let years = [2016] // TODO: make configurable (dev/prod) or latest data

export default {
  components: {
    'data-download-link': dataDownloadLink
  },
  props: [
    'gebiedcode'
  ],
  data () {
    return {
      data: null
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      if (this.gebiedcode) {
        // LBETROKKEN_R Betrokkenheid met de buurt is geen percentage, kan niet in dezelfde plot!
        let variables = ['VCRIMIN_I']

        this.data = await getBbgaVariables(variables, [this.gebiedcode], years)
      }
    }
  },
  watch: {
    gebiedcode (to, from) {
      this.getData()
    }
  }
}
</script>

<style scoped>
</style>
