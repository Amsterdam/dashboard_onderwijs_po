<!-- This page is intended to give an overview of present / missing data -->
<template>
  <div>
    <h1>Data beschikbaarheid per vestiging</h1>
    <table class="table table-sm table-responsive">
      <thead>
        <tr>
          <th>BRIN6</th>
          <template v-for="item in ordered">
            <th :colspan="item.entries.length" v-bind:key="item.variable">{{ item.variable }}</th>
          </template>
        </tr>
        <tr>
          <th></th>
          <template v-for="item in ordered">
            <template v-for="value in item.entries">
              <th :key="item.variable+value">{{ value }}</th>
            </template>
          </template>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.row_key">
          <td><router-link :to="{path: '/vestiging/' + row.row_key}">{{ row.row_key }}</router-link></td>
          <template v-for="item in ordered">
            <template v-for="value in item.entries">
              <td v-if="row.columns[item.variable] && row.columns[item.variable][value]" :key="row.row_key+item.variable+value">ok</td>
              <td v-else :key="row.row_key+item.variable+value" class="text-danger">leeg</td>
            </template>
          </template>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { readPaginatedData } from '@/services/datareader'
import _ from 'lodash'

const URL = process.env.API_HOST + '/onderwijs/api/data-summary/'
const nYears = 4

function getFullHeader (rows) {
  let fullHeader = rows.reduce((header, currentRow, idx) => {
    // console.log('voor _.merge', header)
    let h = _.merge(header, currentRow.columns)
    // console.log('na _.merge', h)
    return h
  }, {})
  return fullHeader
}

export default {
  data () {
    return {
      'rows': null,
      'header': null,
      'years': null,
      'ordered': null
    }
  },
  mounted () {
    this.setData()
    this.setYears()
  },
  methods: {
    setYears () {
      const currentYear = (new Date()).getFullYear()
      this.years = _.range(nYears).map((d) => currentYear - d)
    },
    setHeader () {
      if (this.rows && this.rows.length) {
        this.header = getFullHeader(this.rows)
      }
    },
    setVariableOrder () {
      if (this.header) {
        // sort the variables (aka. available datasets) alphabetically
        // then sort the entries per variabel numerically (in case of years) and convert to array
        // make sure the array does not contain the true values
        let ordered = Object.entries(this.header)
          .sort((a, b) => a[0] > b[0])
          .map(d => ({
            variable: d[0],
            entries: Object.entries(d[1])
              .sort((a, b) => a[0] > b[0])
              .map(d => d[0])
          }))
        this.ordered = ordered
      }
    },
    async setData () {
      this.rows = await readPaginatedData(URL)
    }
  },
  watch: {
    rows (to) {
      this.setHeader(to)
    },
    header (to) {
      if (to) {
        console.log('HEADER', to)
        this.setVariableOrder(to)
      }
    }
  }
}
</script>

<style>

</style>
