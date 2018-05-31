<template>
  <div>
    <vega-spec-render v-if="hasData" :data="data" :vegaspec="vegaspec"></vega-spec-render>
    <div v-else class="missing-data">Data is niet beschikbaar.</div>
  </div>
</template>

<script>
import { readPaginatedData } from '@/services/datareader'

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
        this.data = await readPaginatedData(API_HOST + `/onderwijs/api/leerling-naar-gewicht/?vestiging=${this.id}`)
        this.hasData = this.data.length
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
