<template>
  <div>
    <data-download-link :data="data" text="Download sociale problemen cijfers JSON" filename="sociale-problemen.json"></data-download-link>
    <vega-spec-render :data="data" :vegaspec="vegaspec"></vega-spec-render>
  </div>
</template>

<script>
import { getBbgaVariables, annotate } from '@/services/bbgareader'

import dataDownloadLink from '@/components/general/dataDownloadLink'
import vegaSpecRenderer from '@/components/general/vegaSpecRenderer'
import vegaspec from './vega-spec.json'

let years = [2015, 2014, 2016] // TODO: make configurable (dev/prod) or latest data

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
    if (this.gebiedcode) {
      this.getData()
    }
  },
  methods: {
    async getData () {
      // LBETROKKEN_R Betrokkenheid met de buurt is geen percentage, kan niet in dezelfde plot!
      let variables = ['LSOCKWAL_P', 'WZOKT_P', 'WZSAMEN_P']
      let labelMapping = [
        ['LSOCKWAL_P', 'Sociale cohesie'],
        ['WZOKT_P', 'Bij OKT'],
        ['WZSAMEN_P', 'Bij Samen doen']
      ]

      let data = await getBbgaVariables(variables, [this.gebiedcode, 'STAD'], years)
      data = annotate(data, 'variabele', '_label', labelMapping)
      // data = orderFacets(data, 'variabele', variables)
      this.data = data
    }
  },
  watch: {
    gebiedcode (to, from) {
      if (to) {
        this.getData()
      }
    }
  }
}
</script>

<style scoped>
</style>
