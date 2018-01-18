// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'

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
    async init () {
      this.vestigingen = this.$store.state.vestigingen

      if (!this.vestigingen.length) {
        let next = 'https://data.amsterdam.nl/onderwijs/api/vestigingen/'

        while (next) {
          try {
            let response = await Vue.axios.get(next)
            next = response.data.next
            response.data.results.forEach(result => {
              this.vestigingen.push(result)
            })
          } catch (e) {
            next = null
          }
        }

        this.$store.commit('vestigingen', this.vestigingen)
      }
    }
  }
})

main.init()
