<template>
  <div></div>
</template>

<script>
import * as d3 from 'd3'
import { readPaginatedData, nextAccessor } from '@/services/datareader'

const API_HOST = process.env.API_HOST

export default {
  props: [
    'id'
  ],
  data () {
    return {
      'subsidieData': []
    }
  },
  async mounted () {
    this.setSubsidieData()
  },
  methods: {
    async setSubsidieData () {
      var url = API_HOST + `/onderwijs/api/toegewezen-subsidie/?vestiging=${this.id}&subsidie__jaar=2017`
      this.subsidieData = await readPaginatedData(url, nextAccessor)
    },
    async drawSubsidieTabel () {
      if (this.subsidieData) {
        var target = d3.select(this.$el)

        target.selectAll('div')
          .data(this.subsidieData).enter()
          .append('div')
          .style('font-size', '12px')
          .text(function (d, i) { return d.subsidie + ' ' + d.aantal })
      }
    }
  },
  watch: {
    subsidieData (to, from) {
      this.drawSubsidieTabel()
    }
  }
}
</script>

<style>
</style>
