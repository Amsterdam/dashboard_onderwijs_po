<template>
  <div :class="!hasData ? 'missing-data' : ''">
    <vega-spec-render v-if="hasData" :data="data" :vegaspec="vegaspec"></vega-spec-render>
    <template v-else>
      Data is niet beschikbaar.
    </template>
  </div>
</template>

<script>
import { readData } from '@/services/datareader'
import { order } from '@/services/bbgareader'

import dataDownloadLink from '@/components/general/dataDownloadLink'
import vegaSpecRenderer from '@/components/general/vegaSpecRenderer'
import vegaspec from './vega-spec.json'

let API_HOST = process.env.API_HOST

export default {
  components: {
    'data-download-link': dataDownloadLink,
    'vega-spec-render': vegaSpecRenderer
  },
  props: [
    'id'
  ],
  data () {
    return {
      data: null,
      vegaspec,
      hasData: true
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      if (this.id) {
        let data = await readData(API_HOST + `/onderwijs/api/aggregated-advies/?vestiging=${this.id}`)
        this.data = order(data, 'advies', ['pro', 'vmbo b / k', 'vmbo g / t', 'havo / vwo'])
        this.hasData = data.length
      }
    }
  },
  watch: {
    id (to, from) {
      this.getData()
    }
  }
}
</script>

<style scoped>
</style>
