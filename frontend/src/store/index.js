import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    vestigingen: []
  },
  mutations: {
    vestigingen (state, vestigingen) {
      state.vestigingen = vestigingen
    }
  }
})
