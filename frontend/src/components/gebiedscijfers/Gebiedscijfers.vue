<!-- Right column in original design, contains Gebieds specific data -->
<template>
  <div id="gebiedscijfers">
    <gebiedscijfer-opleiding v-if="gebiedscode" :gebiedscode="gebiedscode"></gebiedscijfer-opleiding>
    <gebiedscijfer-herkomst v-if="herkomst" :herkomst="herkomst" :gebiedscode="gebiedscode"></gebiedscijfer-herkomst>
  </div>
</template>

<script>
// Add subcomponent imports that display the various variables.
import gebiedscijferOpleiding from './GebiedscijferOpleiding'
import gebiedscijferHerkomst from './GebiedscijferHerkomst'
import util from '@/services/util'

const bbgaCijferUrl = 'https://api.data.amsterdam.nl/bbga/cijfers/'
const jaren = [2016, 2017]

export default {
  data: function () {
    return {
      opleiding: null,
      herkomst: null,
      veiligheidsindex: null,
      inkomen: null,
      socialeProblematiek: null,
      cirminaliteitsIndex: null
    }
  },
  props: [
    'gebiedscode'
  ],
  components: {
    'gebiedscijfer-opleiding': gebiedscijferOpleiding,
    'gebiedscijfer-herkomst': gebiedscijferHerkomst
  },
  methods: {
    async getBbgaData (variables, mappings, years) {
      console.log('Running getBbgaData')
      // goal: [{jaar, label, waarde}, ...]
      let out = []

      for (let variable of variables) {
        let queryString = `?gebiedcode15=${this.gebiedscode}&variabele=${variable}`
        let url = bbgaCijferUrl + queryString
        let data = await util.readPaginatedHalJsonData(url)
        // console.log(data)

        // here we error out
        for (let datum of data) {
          // console.log('Datum', datum)
          let label = mappings[datum.variabele]
          out.push({
            label,
            jaar: datum.jaar,
            waarde: datum.waarde
          })
        }
      }
      return out
    },
    async setHerkomst () {
      // console.log('Running setHerkomst')
      let variables = ['BEVSUR_P', 'BEVANTIL_P', 'BEVTURK_P', 'BEVMAROK_P', 'BEVOVNW_P', 'BEVWEST_P', 'BEVAUTOCH_P']
      let mappings = {
        BEVSUR_P: 'Surinaams',
        BEVANTIL_P: 'Antilliaans',
        BEVTURK_P: 'Turks',
        BEVMAROK_P: 'Marrokaans',
        BEVOVNW_P: 'Overig niet-westers',
        BEVWEST_P: 'Westers',
        BEVAUTOCH_P: 'Autochtoon'
      }
      this.herkomst = await this.getBbgaData(variables, mappings, jaren)
      // console.log('Herkomst', this.herkomst)
    }
  },
  created () {
    // console.log('ik besta')
  },
  mounted () {
    this.setHerkomst()
  }
}

</script>

<style scoped>
</style>
