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
import { readPaginatedData } from './services/datareader'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'leaflet/dist/leaflet.css'

import 'stijl/dist/css/ams-stijl.css'
import '../static/app.css'

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
      const url = API_HOST + '/onderwijs/api/vestiging/'
      let vestigingen = this.$store.state.vestigingen
      if (!vestigingen.length) {
        vestigingen = await readPaginatedData(url)
        this.registerVestigingen(vestigingen)
      }
    }
  }
})

vueApp.init()
