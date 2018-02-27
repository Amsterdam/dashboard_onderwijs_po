<template>
  <div id="gebiedscijfer-opleiding">
      <h3>placeholder opleiding</h3>
      <div class="vegaembed"></div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import vegaEmbed from 'vega-embed'
import util from '@/services/util'

const API_URL = 'https://api.data.amsterdam.nl'

const vegaEmbedOptions = {
  'actions': {
    'export': false,
    'source': false,
    'editor': true},
  'renderer': 'svg'
}

export default {
  props: [
    'gebiedscode'
  ],
  data () {
    return {
      opleidingData: []
    }
  },
  async mounted () {
    this.setOpleidingData()
  },
  methods: {
    async setOpleidingData () {
      // TODO: facet "order" (extra property on data to order by)
      let plotData = await this.downloadBbgaData(
        ['O_OPLPO_L_P', 'O_OPLPO_M_P', 'O_OPLPO_P'],
        [this.gebiedscode, 'STAD']
      )
      let mapping = new Map(
        [['O_OPLPO_L_P', 'L'], ['O_OPLPO_M_P', 'M'], ['O_OPLPO_P', 'H']]
      )
      plotData = plotData.map(function (d) {
        d.variabele = mapping.get(d.variabele)
        return d
      })
      this.opleidingData = plotData.filter(datum => datum.jaar === 2016)
    },
    createJsonDownload (element, data, filename) {
      // TODO: move to services
      let toDownload = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(data))
      d3.select(element).append('a')
        .attr('href', toDownload)
        .text('Download file: ' + filename)
        .attr('download', filename)
    },
    async downloadBbgaData (variables, gebiedcodes) {
      // TODO: move to services, add retry on failure.
      // construct URLS that need querying to retrieve our data
      let urls = []
      for (let v of variables) {
        for (let gc of gebiedcodes) {
          let url = API_URL + `/bbga/cijfers/?gebiedcode15=${gc}&variabele=${v}`
          urls.push(url)
        }
      }
      // download data (in parallel) -> failure of one promise will cause all to fail (retry?)
      let promisedResultsArrays = urls.map(
        url => util.readPaginatedHalJsonData(url)
      )
      let resultsArrays = await Promise.all(promisedResultsArrays)

      // flatten our array
      let out = [].concat.apply([], resultsArrays)
      return out
    },
    async draw () {
      let spec = await util.readData('/static/gebiedscijfers/gebiedscijfer-opleiding.vg.json')
      spec.data = {values: this.opleidingData}
      vegaEmbed(this.$el.querySelector('.vegaembed'), spec, vegaEmbedOptions)
    }
  },
  watch: {
    opleidingData (to, from) {
      if (to.length) {
        this.draw()
      }
    }
  }
}

</script>

<style scoped>
</style>
