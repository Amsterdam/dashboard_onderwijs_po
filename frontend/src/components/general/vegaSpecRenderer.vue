<template>
  <div>
    <div :ref="chartRef"></div>
  </div>
</template>

<script>
import vegaEmbed from 'vega-embed'

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
      // console.log('Rendering vega spec', this.data, this.vegaspec)
      if (this.data && this.vegaspec) {
        // we modify the bound vegaSpec (overwrite the data property), then render it
        this.vegaspec.data = {values: this.data}
        let element = this.$refs[this.chartRef]
        vegaEmbed(element, this.vegaspec, vegaEmbedOptions)
      }
    }
  },
  watch: {
    data (to, from) {
      if (to.length) {
        this.renderSpec()
      }
    }
  }
}
</script>

<style scoped>
</style>
