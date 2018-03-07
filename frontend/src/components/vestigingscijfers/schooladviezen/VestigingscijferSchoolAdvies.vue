<template>
  <div>
    <vega-spec-render :data="data" :vegaspec="vegaspec"></vega-spec-render>
    <data-download-link :data="data" text="Download leerling naar gewicht JSON" filename="inkomen.json"></data-download-link>
  </div>
</template>

<script>
import { readData } from '@/services/datareader'

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
      vegaspec
    }
  },
  async mounted () {
    if (this.id) {
      this.getData()
    }
  },
  methods: {
    async getData () {
      let url = API_HOST + `/onderwijs/api/aggregated-advies/?vestiging=${this.id}`

      let data = await readData(url)
      this.data = data
    }
  },
  watch: {
    id (to, from) {
      if (to) {
        this.getData()
      }
    }
  }
}
</script>

<style scoped>
</style>
