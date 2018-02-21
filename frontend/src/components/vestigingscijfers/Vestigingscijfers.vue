<!-- Left column in original design, contains Vestiging specific data -->
<template>
  <div id="vestigingscijfers">
    <leerlingen-naar-gewicht :id="id"></leerlingen-naar-gewicht>
    <school-advies :id="id"></school-advies>
  </div>
</template>

<script>
import leerlingenNaarGewicht from './LeerlingenNaarGewicht'
import schoolAdvies from './SchoolAdvies'

export default {
  props: [
    'id'
  ],
  components: {
    'leerlingen-naar-gewicht': leerlingenNaarGewicht,
    'school-advies': schoolAdvies
  }
}
</script>

<style scoped>
</style>
