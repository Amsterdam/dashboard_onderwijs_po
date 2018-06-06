<template>
  <div v-if="hasData">
    <h1 class="single-figure">{{
        this.citoScoreData !== null // we want to show 0 if it is present in data
        ? this.citoScoreData.toLocaleString(
          'nl-DU', { maximumFractionDigits: 1 }
        )
        : '...'
      }}
    </h1>
    <div class="average">
      <div style="text-align: right">Amsterdams gemiddelde{{
        this.citoScoreGem !== null
        ? ' (' + bbgaYear + '): ' + this.citoScoreGem.toLocaleString(
            'nl-DU', { maximumFractionDigits: 1 }
        )
        : ': ...'
        }}
      </div>
    </div>
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
      'isBusy': true,
      'hasData': true, // optimistic, assumption is we have or will get the data
      'year': null
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      this.citoScoreData = _.get(await readPaginatedData(API_HOST + `/onderwijs/api/cito-score/?vestiging=${this.id}&jaar=2016`), '[0].cet_gem', null)
      const data = await getBbgaVariables(['OCITOSCH_GEM'], ['STAD'], -1)
      this.citoScoreGem = _.get(data, '[0].waarde', null)
      this.bbgaYear = _.get(data, '[0].jaar', null)

      this.hasData = !(this.citoScoreData === null || this.citoScoreGem === null)
      this.isBusy = false
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
