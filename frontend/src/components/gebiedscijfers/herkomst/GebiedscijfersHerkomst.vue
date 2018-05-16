<template>
  <div>
    <vega-spec-render :data="data" :vegaspec="vegaspecAfkomst"></vega-spec-render>
    <data-download-link :data="data" text="Download afkomst cijfers JSON" filename="afkomst.json"></data-download-link>
  </div>
</template>

<script>
import { getBbgaVariables, annotate, order, translateAreaCodes } from '@/services/bbgareader'

import dataDownloadLink from '@/components/general/dataDownloadLink'
import vegaSpecRenderer from '@/components/general/vegaSpecRenderer'
import vegaspecAfkomst from '@/components/gebiedscijfers/herkomst/vega-spec.json'

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
      vegaspecAfkomst
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      if (this.gebiedcode) {
        let variables = ['BEVSUR_P', 'BEVANTIL_P', 'BEVTURK_P', 'BEVMAROK_P', 'BEVWEST_P', 'BEVOVNW_P', 'BEVAUTOCH_P']
        let labelMapping = [
          ['BEVSUR_P', 'Surinaams'],
          ['BEVANTIL_P', 'Antilliaans'],
          ['BEVTURK_P', 'Turks'],
          ['BEVMAROK_P', 'Marrokaans'],
          ['BEVOVNW_P', 'Niet West.'],
          ['BEVWEST_P', 'Westers'],
          ['BEVAUTOCH_P', 'Autochtoon']
        ]

        let data = await getBbgaVariables(variables, [this.gebiedcode, 'STAD'], years)
        data = annotate(data, 'variabele', '_label', labelMapping)
        data = await translateAreaCodes(data)
        this.data = order(data, 'variabele', variables)
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
