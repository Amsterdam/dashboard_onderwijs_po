<template>
  <div>
    <vega-spec-render :data="data" :vegaspec="vegaspec"></vega-spec-render>
    <div v-if="data && data.length" class="text-right small">{{ yearsRange }}</div>
  </div>
</template>

<script>
import _ from 'lodash'

import { getBbgaVariables, annotate, translateAreaCodes } from '@/services/bbgareader'
import vegaSpecRenderer from '@/components/general/vegaSpecRenderer'
import vegaspec from './vega-spec.json'

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
      vegaspec
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      if (this.gebiedcode) {
        let variables = ['OSDQ10_P']
        let labelMapping = [
          ['OSDQ10_P', 'SDQ-10']
        ]

        let data = await getBbgaVariables(variables, [this.gebiedcode, 'STAD'], -1)
        data = await translateAreaCodes(data)
        this.data = annotate(data, 'variabele', '_label', labelMapping)
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
