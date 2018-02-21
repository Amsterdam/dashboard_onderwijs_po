<!-- Left column in original design, contains Vestiging specific data -->
<template>
  <div id="vestigingscijfers">
    <leerlingen-naar-gewicht :id="id"></leerlingen-naar-gewicht>
    <school-advies :id="id"></school-advies>
    <cito-score :id="id"></cito-score>
    <subsidie :id="id"></subsidie>
  </div>
</template>

<script>
import leerlingenNaarGewicht from './LeerlingenNaarGewicht'
import schoolAdvies from './SchoolAdvies'
import citoScore from './CitoScore'
import subsidie from './Subsidie'

export default {
  props: [
    'id'
  ],
  components: {
    'leerlingen-naar-gewicht': leerlingenNaarGewicht,
    'school-advies': schoolAdvies,
    'cito-score': citoScore,
    'subsidie': subsidie
  }
}
</script>

<style scoped>
</style>
