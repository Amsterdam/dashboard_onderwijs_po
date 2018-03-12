<template>
  <div>
    <vega-spec-render :data="data" :vegaspec="vegaspec"></vega-spec-render>
    <data-download-link :data="data" text="Download inkomens cijfers JSON" filename="inkomen.json"></data-download-link>
  </div>
</template>

<script>
import { getBbgaVariables, annotate } from '@/services/bbgareader'

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
        let variables = ['IMINHH120_P', 'IWWB_P', 'PWERKLBBV_P', 'BEVEENOUDERHH_P']
        let labelMapping = [
          ['IMINHH120_P', 'Minima'],
          ['IWWB_P', 'Bijstand'],
          ['PWERKLBBV_P', 'Werkloos'],
          ['BEVEENOUDERHH_P', 'Éénouder']
        ]

        let data = await getBbgaVariables(variables, [this.gebiedcode, 'STAD'], years)
        data = annotate(data, 'variabele', '_label', labelMapping)
        // data = orderFacets(data, 'variabele', variables)
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
