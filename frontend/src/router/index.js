import Vue from 'vue'
import Router from 'vue-router'
import NewVestigingen from '@/components/NewVestigingen'
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
      component: NewVestigingen
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
