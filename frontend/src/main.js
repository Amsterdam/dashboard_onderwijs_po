// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import BootstrapVue from 'bootstrap-vue'
import { mapActions } from 'vuex'

import store from './store'
import util from './services/util'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'leaflet/dist/leaflet.css'

Vue.use(VueAxios, axios)

Vue.use(BootstrapVue)

Vue.config.productionTip = false

let API_HOST = process.env.API_HOST

/* eslint-disable no-new */
let vueApp = new Vue({
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
      const url = API_HOST + '/onderwijs/api/vestigingen/'
      let vestigingen = this.$store.state.vestigingen
      if (!vestigingen.length) {
        vestigingen = await util.readPaginatedData(url)
        this.registerVestigingen(vestigingen)
      }
    }
  }
})

vueApp.init()
