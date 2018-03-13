<template>
  <div>
    <vega-spec-render :data="data" :vegaspec="vegaspec"></vega-spec-render>
    <data-download-link :data="data" text="Download sociale problemen cijfers JSON" filename="sociale-problemen.json"></data-download-link>
  </div>
</template>

<script>
import { getBbgaVariables, annotate, translateAreaCodes } from '@/services/bbgareader'

import dataDownloadLink from '@/components/general/dataDownloadLink'
import vegaSpecRenderer from '@/components/general/vegaSpecRenderer'
import vegaspec from './vega-spec.json'

let years = [2016] // TODO: make configurable (dev/prod) or latest data

export default {
  components: {
    'data-download-link': dataDownloadLink,
    'vega-spec-render': vegaSpecRenderer
  },
  props: [
    'gebiedcode'
  ],
  data () {
    return {
      data: null,
      vegaspec
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      if (this.gebiedcode) {
        // LBETROKKEN_R Betrokkenheid met de buurt is geen percentage, kan niet in dezelfde plot!
        let variables = ['LSOCKWAL_P', 'WZOKT_P', 'WZSAMEN_P']
        let labelMapping = [
          ['LSOCKWAL_P', 'Cohesie'],
          ['WZOKT_P', 'Bij OKT'],
          ['WZSAMEN_P', 'Samen doe.']
        ]

        let data = await getBbgaVariables(variables, [this.gebiedcode, 'STAD'], years)
        data = annotate(data, 'variabele', '_label', labelMapping)
        data = await translateAreaCodes(data)
        this.data = data
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
