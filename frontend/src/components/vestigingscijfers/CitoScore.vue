<template>
  <div></div>
</template>

<script>
import * as d3 from 'd3'
import util from '@/services/util'

const API_HOST = process.env.API_HOST

export default {
  props: [
    'id'
  ],
  data () {
    return {
      'citoScoreData': []
    }
  },
  async mounted () {
    this.setCitoScoreData()
  },
  methods: {
    async setCitoScoreData () {
      var url = API_HOST + `/onderwijs/api/cito-score/?vestiging=${this.id}&jaar=2016`
      let tmp = await util.readPaginatedData(url)
      this.citoScoreData = tmp
    },
    async draw () {
      // remove graph first, then redraw
      var target = d3.select(this.$el)
      target.selectAll('*').remove()

      target.append('div').append('h1')
        .style('text-align', 'center')
        .text(Math.round(this.citoScoreData[0].cet_gem))
      target.append('div')
        .style('text-align', 'right')
        .text('A\'dams gem = ' + Math.round(this.citoScoreData[0].cet_gem_avg))
    }
  },
  watch: {
    citoScoreData (to, from) {
      if (to.length) {
        this.draw()
      }
    }
  }
}
</script>

<style scoped>
</style>
