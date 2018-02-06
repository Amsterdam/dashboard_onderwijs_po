import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // Register all state data in the state object
    vestigingen: []
  },
  actions: {
    // Actions are available to manipulate the state
    // A component has access to these actions data by using mapActions, e.g.:
    //   methods: {
    //     ...mapActions({
    //       setText: 'setText'
    //     })
    //  }
    // See also main.js
    registerVestigingen (store, vestigingen) {
      store.commit('vestigingen', vestigingen)
    }
  },
  mutations: {
    // The real manipulation of the state is by means of a mutation
    // Mutations are triggered by commits, this is normally done in an action
    vestigingen (state, vestigingen) {
      state.vestigingen = vestigingen
    }
  },
  getters: {
    vestigingen: state => {
      // Provide access to state data, or part of the state data
      // A component has access to the state data by using mapGetters, e.g.:
      //   computed: {
      //     ...mapGetters([
      //       'vestigingen'
      //     ])
      //   }
      // See also HelloWorld.vue
      return state.vestigingen
    }
  }
})
