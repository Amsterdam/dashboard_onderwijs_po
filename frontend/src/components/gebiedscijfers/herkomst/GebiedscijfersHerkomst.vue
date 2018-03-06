<template>
  <div>
    <data-download-link :data="data" text="Download afkomst cijfers JSON" filename="afkomst.json"></data-download-link>
    <vega-spec-render :data="data" :vegaspec="vegaspecAfkomst"></vega-spec-render>
  </div>
</template>

<script>
import { getBbgaVariables, annotate, orderFacets } from '@/services/bbgareader'

import dataDownloadLink from '@/components/general/dataDownloadLink'
import vegaSpecRenderer from '@/components/general/vegaSpecRenderer'
import vegaspecAfkomst from '@/components/gebiedscijfers/herkomst/vega-spec.json'

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
      vegaspecAfkomst
    }
  },
  async mounted () {
    if (this.gebiedcode) {
      this.getData()
    }
  },
  methods: {
    async getData () {
      let variables = ['BEVSUR_P', 'BEVANTIL_P', 'BEVTURK_P', 'BEVMAROK_P', 'BEVWEST_P', 'BEVOVNW_P', 'BEVAUTOCH_P']
      let labelMapping = [
        ['BEVSUR_P', 'Surinaams'],
        ['BEVANTIL_P', 'Antilliaans'],
        ['BEVTURK_P', 'Turks'],
        ['BEVMAROK_P', 'Marrokaans'],
        ['BEVOVNW_P', 'Niet-westers'],
        ['BEVWEST_P', 'Westers'],
        ['BEVAUTOCH_P', 'Autochtoon']
      ]

      let data = await getBbgaVariables(variables, [this.gebiedcode, 'STAD'], years)
      data = annotate(data, 'variabele', '_label', labelMapping)
      data = orderFacets(data, 'variabele', variables)
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
