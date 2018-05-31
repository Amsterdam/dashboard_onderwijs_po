<template>
  <div :ref="chartRef"></div>
</template>

<script>
import * as vegaEmbed from 'vega-embed'

const vegaEmbedOptions = {
  'actions': {
    'export': false,
    'source': false,
    'editor': false},
  'renderer': 'svg'
}

export default {
  props: [
    'data',
    'vegaspec'
  ],
  data () {
    return {
      chartRef: `${this._uid}.vegaembed`
    }
  },
  methods: {
    renderSpec () {
      if (this.data && this.data.length && this.vegaspec) {
        // we modify the bound vegaSpec (overwrite the data property), then render it
        this.vegaspec.data = {values: this.data}
        let element = this.$refs[this.chartRef]

        // https://gist.github.com/domoritz/a5707e5d9430c173019583ea8bc5707a (by vega / vega-lite co-author)
        vegaEmbed.vega.formatLocale({
          decimal: ',',
          thousands: '.',
          grouping: [3],
          currency: ['', '\u00a0€']
        })
        vegaEmbed.default(element, this.vegaspec, vegaEmbedOptions)
      }
    }
  },
  watch: {
    data (to, from) {
      this.renderSpec()
    }
  }
}
</script>

<style scoped>
</style>
