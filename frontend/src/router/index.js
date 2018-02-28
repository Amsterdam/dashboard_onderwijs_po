import Vue from 'vue'
import Router from 'vue-router'
import NewVestigingen from '@/components/NewVestigingen'
import Vestiging from '@/components/Vestiging'
import VindVestiging from '@/components/VindVestiging'

Vue.use(Router)

console.log('process.env.ROUTER_BASE', process.env.ROUTER_BASE)
console.log('process.env.NODE_ENV', process.env.NODE_ENV)
export default new Router({
  // mode: 'history', // we should use this, but more server settings are needed
  base: process.env.ROUTER_BASE,
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
