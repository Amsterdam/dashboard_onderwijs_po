<template>
  <div class="cito-score">
    <h1 class="single-figure">{{
        this.citoScoreData !== null // we want to show 0 if it is present in data
        ? this.citoScoreData.toLocaleString(
          'nl-DU', { maximumFractionDigits: 1 }
        )
        : '...'
      }}
    </h1>
    <div class="average">
      <div style="text-align: right">A'dams gem = {{
        this.citoScoreGem !== null
        ? this.citoScoreGem.toLocaleString(
            'nl-DU', { maximumFractionDigits: 1 }
        )
        : '...'
        }}
      </div>
    </div>
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
  .cito-score {
    position: relative;
    padding-top: 15%;
    height: 100%;
  }

  .average div {
    position: absolute;
    margin-right: 5px;
    bottom: 0;
    right: 0;
  }
</style>
