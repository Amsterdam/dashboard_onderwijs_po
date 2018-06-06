<template>
  <div>
    <vega-spec-render :data="data" :vegaspec="vegaspecAfkomst"></vega-spec-render>
    <div v-if="data && data.length" class="text-right small">{{ yearsRange }}</div>
  </div>
</template>

<script>
import _ from 'lodash'

import { getBbgaVariables, annotate, order, translateAreaCodes } from '@/services/bbgareader'
import vegaSpecRenderer from '@/components/general/vegaSpecRenderer'
import vegaspecAfkomst from '@/components/gebiedscijfers/herkomst/vega-spec.json'

export default {
  components: {
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
          ['BEVSUR_P', '1: Surinaams'],
          ['BEVANTIL_P', '2: Antilliaans'],
          ['BEVTURK_P', '3: Turks'],
          ['BEVMAROK_P', '4: Marrokaans'],
          ['BEVOVNW_P', '5: Niet West.'],
          ['BEVWEST_P', '6: Westers'],
          ['BEVAUTOCH_P', '7: Autochtoon']
        ]

        let data = await getBbgaVariables(variables, [this.gebiedcode, 'STAD'], -1)
        data = annotate(data, 'variabele', '_label', labelMapping)
        data = await translateAreaCodes(data)
        this.data = order(data, 'variabele', variables)
      }
    }
  },
  computed: {
    yearsRange () {
      const begin = _.min(this.data.map(d => d.jaar))
      const end = _.max(this.data.map(d => d.jaar))

      return (begin === end) ? `Data uit ${begin}` : `Data uit ${begin}-${end}`
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
