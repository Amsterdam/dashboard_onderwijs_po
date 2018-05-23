<template>
  <div v-bind:class="MISSING_DATA ? 'missing-data' : ''">
    <vega-spec-render v-if="!MISSING_DATA" :data="data" :vegaspec="vegaspec"></vega-spec-render>
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
      MISSING_DATA: false
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      if (this.id) {
        let url = API_HOST + `/onderwijs/api/aggregated-advies/?vestiging=${this.id}`
        let data = order(await readData(url), 'advies', ['pro', 'vmbo b / k', 'vmbo g / t', 'havo / vwo'])

        this.data = data

        if (!data.length) {
          this.MISSING_DATA = true
        }
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
