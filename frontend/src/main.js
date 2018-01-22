// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'

import { mapActions } from 'vuex'
import readPaginatedData from './services/util'

Vue.use(VueAxios, axios)

Vue.config.productionTip = false

/* eslint-disable no-new */
let main = new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
  methods: {
    ...mapActions({
      registerVestigingen: 'registerVestigingen'
    }),

    async init () {
      const url = 'https://data.amsterdam.nl/onderwijs/api/vestigingen/'
      let vestigingen = this.$store.state.vestigingen
      if (!vestigingen.length) {
        vestigingen = await readPaginatedData(url)
        this.registerVestigingen(vestigingen)
      }
    }
  }
})

main.init()
