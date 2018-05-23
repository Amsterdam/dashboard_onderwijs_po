<template>
  <div v-if="!MISSING_DATA">
    <template v-if="citoScoreData">
      <h1 class="single-figure">{{
          this.citoScoreData !== null // we want to show 0 if it is present in data
          ? this.citoScoreData.toLocaleString(
            'nl-DU', { maximumFractionDigits: 1 }
          )
          : '...'
        }}
      </h1>
      <div class="average">
        <div style="text-align: right">Amsterdams gemiddelde: {{
          this.citoScoreGem !== null
          ? this.citoScoreGem.toLocaleString(
              'nl-DU', { maximumFractionDigits: 1 }
          )
          : '...'
          }}
        </div>
      </div>
    </template>
  </div>
  <div v-else class="missing-data">
      Data is niet beschikbaar.
  </div>
</template>

<script>
import _ from 'lodash'

import { readPaginatedData } from '@/services/datareader'
import { getBbgaVariables } from '@/services/bbgareader'

const API_HOST = process.env.API_HOST

export default {
  props: [
    'id'
  ],
  data () {
    return {
      'citoScoreData': null,
      'citoScoreGem': null,
      'MISSING_DATA': false
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      this.citoScoreData = _.get(await readPaginatedData(API_HOST + `/onderwijs/api/cito-score/?vestiging=${this.id}&jaar=2016`), '[0].cet_gem', null)
      this.citoScoreGem = _.get(await getBbgaVariables(['OCITOSCH_GEM'], ['STAD'], [2016]), '[0].waarde', null)

      if (!this.citoScoreData) {
        this.MISSING_DATA = true
      }
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
