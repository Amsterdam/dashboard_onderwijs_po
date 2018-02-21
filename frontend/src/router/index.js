import Vue from 'vue'
import Router from 'vue-router'
import Vestigingen from '@/components/Vestigingen'
import Vestiging from '@/components/Vestiging'
import VindVestiging from '@/components/VindVestiging'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: 'Vestigingen'
    },
    {
      path: '/vestigingen',
      name: 'Vestigingen',
      component: Vestigingen
    },
    {
      path: '/vestiging/:id',
      name: 'Vestiging',
      component: Vestiging
    },
    {
      path: '/vindvestiging',
      name: 'VindVestiging',
      component: VindVestiging
    }
  ]
})
