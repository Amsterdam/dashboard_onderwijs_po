<template>
  <div>
    <vega-spec-render :data="data" :vegaspec="vegaspecOpleiding"></vega-spec-render>
    <data-download-link :data="data" text="Download opleiding cijfers JSON" filename="opleiding.json"></data-download-link>
  </div>
</template>

<script>
import { getBbgaVariables, annotate, translateAreaCodes } from '@/services/bbgareader'

import dataDownloadLink from '@/components/general/dataDownloadLink'
import vegaSpecRenderer from '@/components/general/vegaSpecRenderer'
import vegaspecOpleiding from '@/components/gebiedscijfers/opleiding/vega-spec.json'

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
      vegaspecOpleiding
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      if (this.gebiedcode) {
        let variables = ['O_OPLPO_L_P', 'O_OPLPO_M_P', 'O_OPLPO_P']
        let labelMapping = [
          ['O_OPLPO_L_P', 'Laag'],
          ['O_OPLPO_M_P', 'Midden'],
          ['O_OPLPO_P', 'Hoog']
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
