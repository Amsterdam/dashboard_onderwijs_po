<template>
  <div>
    <vega-spec-render :data="data" :vegaspec="vegaspec"></vega-spec-render>
    <data-download-link :data="data" text="Download inkomens cijfers JSON" filename="inkomen.json"></data-download-link>
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
        let variables = ['IMINHH120_P', 'IWWB_P', 'PWERKLBBV_P', 'BEVEENOUDERHH_P']
        let labelMapping = [
          ['IMINHH120_P', '0: Minima'],
          ['IWWB_P', '1: Bijstand'],
          ['BEVEENOUDERHH_P', '2: Éénouder'],
          ['PWERKLBBV_P', '3: Werkloos']
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
