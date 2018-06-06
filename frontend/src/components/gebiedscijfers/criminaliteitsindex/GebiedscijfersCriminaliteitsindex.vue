<template>
  <div>
    <h1 v-if="data" class="single-figure">{{data[0].waarde}}</h1>
    <div v-if="data && data.length" class="text-right small">Data uit {{data[0].jaar}}</div>
  </div>
</template>

<script>
import { getBbgaVariables } from '@/services/bbgareader'

export default {
  props: [
    'gebiedcode'
  ],
  data () {
    return {
      data: null
    }
  },
  async mounted () {
    this.getData()
  },
  methods: {
    async getData () {
      if (this.gebiedcode) {
        // LBETROKKEN_R Betrokkenheid met de buurt is geen percentage, kan niet in dezelfde plot!
        let variables = ['VCRIMIN_I']

        this.data = await getBbgaVariables(variables, [this.gebiedcode], -1)
      }
    }
  },
  watch: {
    gebiedcode (to, from) {
      this.getData()
    }
  }
}
</script>

<style scoped>
</style>
