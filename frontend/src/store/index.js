import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    vestigingen: []
  },
  actions: {
    registerVestigingen (store, vestigingen) {
      store.commit('vestigingen', vestigingen)
    }
  },
  mutations: {
    vestigingen (state, vestigingen) {
      state.vestigingen = vestigingen
    }
  },
  getters: {
    vestigingen: state => {
      return state.vestigingen
    }
  }
})
