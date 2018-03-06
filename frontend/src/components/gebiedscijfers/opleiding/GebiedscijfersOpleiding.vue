<template>
  <div>
    <data-download-link :data="data" text="Download opleiding cijfers JSON" filename="opleiding.json"></data-download-link>
    <vega-spec-render :data="data" :vegaspec="vegaspecOpleiding"></vega-spec-render>
  </div>
</template>

<script>
import { getBbgaVariables, annotate } from '@/services/bbgareader'

import dataDownloadLink from '@/components/general/dataDownloadLink'
import vegaSpecRenderer from '@/components/general/vegaSpecRenderer'
import vegaspecOpleiding from '@/components/gebiedscijfers/opleiding/vega-spec.json'

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
      vegaspecOpleiding
    }
  },
  async mounted () {
    if (this.gebiedcode) {
      this.getData()
    }
  },
  methods: {
    async getData () {
      let variables = ['O_OPLPO_L_P', 'O_OPLPO_M_P', 'O_OPLPO_P']
      let labelMapping = [
        ['O_OPLPO_L_P', 'Laag'],
        ['O_OPLPO_M_P', 'Midden'],
        ['O_OPLPO_P', 'Hoog']
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
