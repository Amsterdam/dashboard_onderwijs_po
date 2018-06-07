<template>
  <div>
    <vega-spec-render :data="data" :vegaspec="vegaspecOpleiding"></vega-spec-render>
    <div v-if="data && data.length" class="text-right small">{{ yearsRange }}</div>
  </div>
</template>

<script>
import _ from 'lodash'

import { getBbgaVariables, annotate, translateAreaCodes } from '@/services/bbgareader'
import vegaSpecRenderer from '@/components/general/vegaSpecRenderer'
import vegaspecOpleiding from '@/components/gebiedscijfers/opleiding/vega-spec.json'

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
          ['O_OPLPO_L_P', '0: Laag'],
          ['O_OPLPO_M_P', '1: Midden'],
          ['O_OPLPO_P', '2: Hoog']
        ]

        let data = await getBbgaVariables(variables, [this.gebiedcode, 'STAD'], -1)
        data = annotate(data, 'variabele', '_label', labelMapping)
        data = await translateAreaCodes(data)
        this.data = data
      }
    }
  },
  computed: {
    yearsRange () {
      const begin = _.min(this.data.map(d => d.jaar))
      const end = _.max(this.data.map(d => d.jaar))

      return (begin === end) ? `Bron: BBGA peiljaar ${begin}` : `Bron: BBGA peiljaar ${begin} ${end}`
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
