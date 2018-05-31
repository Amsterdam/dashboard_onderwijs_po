import Vue from 'vue'
import Router from 'vue-router'
import landingPage from '@/components/LandingPage'
import Vestiging from '@/components/Vestiging'
import DataSummary from '@/components/DataSummary'

Vue.use(Router)

console.log('process.env.ROUTER_BASE', process.env.ROUTER_BASE)
console.log('process.env.NODE_ENV', process.env.NODE_ENV)
console.log('process.env.API_HOST', process.env.API_HOST)
export default new Router({
  // mode: 'history', // we should use this, but more server settings are needed
  base: process.env.ROUTER_BASE,
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  },
  routes: [
    {
      path: '/',
      redirect: 'Vestigingen'
    },
    // These components need grid wrapper:
    {
      path: '/vestigingen',
      name: 'Vestigingen',
      component: landingPage
    },
    {
      path: '/vestiging/:id',
      name: 'Vestiging',
      component: Vestiging
    },
    // This component should not get all the grid wrapper stuff:
    {
      path: '/summary/',
      name: 'DataSummary',
      component: DataSummary
    }
  ]
})
