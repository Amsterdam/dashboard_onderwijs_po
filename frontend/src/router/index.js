import Vue from 'vue'
import Router from 'vue-router'
import Vestigingen from '@/components/Vestigingen'
import Vestiging from '@/components/Vestiging'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Vestigingen',
      component: Vestigingen
    },
    {
      path: '/vestiging/:id',
      name: 'Vestiging',
      component: Vestiging
    }
  ]
})
