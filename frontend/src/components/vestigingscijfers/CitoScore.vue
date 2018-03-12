<template>
  <div>
    <h1 style="text-align: center">{{
        this.citoScoreData !== null // we want to show 0 if it is present in data
        ? this.citoScoreData.toLocaleString(
          'nl-DU', { maximumFractionDigits: 1 }
        )
        : '...'
      }}</h1>
    <div style="text-align: right">A'dams gem = {{
      this.citoScoreGem !== null
      ? this.citoScoreGem.toLocaleString(
          'nl-DU', { maximumFractionDigits: 1 }
      )
      : '...'
      }}</div>
  </div>
</template>

<script>
import { readPaginatedData, nextAccessor } from '@/services/datareader'
import { getBbgaVariables } from '@/services/bbgareader'

const API_HOST = process.env.API_HOST

export default {
  props: [
    'id'
  ],
  data () {
    return {
      'citoScoreData': null,
      'citoScoreGem': null
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      let score = await readPaginatedData(API_HOST + `/onderwijs/api/cito-score/?vestiging=${this.id}&jaar=2016`, nextAccessor)
      this.citoScoreData = score[0].cet_gem
      let scoreGem = await getBbgaVariables(['OCITOSCH_GEM'], ['STAD'], [2016])
      this.citoScoreGem = scoreGem[0].waarde
    }
  }
}
</script>

<style scoped>
</style>
