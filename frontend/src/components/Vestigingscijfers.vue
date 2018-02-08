<!-- Left column in original design, contains Vestiging specific data -->
<template>
  <div id="vestigingscijfers">
    <leerlingen-naar-gewicht :id="id"></leerlingen-naar-gewicht>
    <school-advies :id="id"></school-advies>
    <d3-example></d3-example>
  </div>
</template>

<script>
import leerlingenNaarGewicht from './LeerlingenNaarGewicht'
import schoolAdvies from './SchoolAdvies'
import d3Example from './D3Example'

export default {
  props: [
    'id'
  ],
  components: {
    'leerlingen-naar-gewicht': leerlingenNaarGewicht,
    'school-advies': schoolAdvies,
    'd3-example': d3Example
  }
}
</script>

<style scoped>
</style>
