<!-- Left column in original design, contains Vestiging specific data -->
<template>
  <div id="vestigingscijfers">
    <div class="row">
      <div class="col-md-12 col-lg-7">
        <div class="card std-height">
          <h5 class="card-header">Aantal leerlingen naar gewicht</h5>
          <div class="card-block">
            <leerlingen-naar-gewicht :id="id"></leerlingen-naar-gewicht>
          </div>
        </div>
      </div>
      <div class="col-md-12 col-lg-5">
        <div class="card std-height">
          <h5 class="card-header">TBD</h5>
          <div class="card-block text-center">
            TBD
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-sm-3">
      <div class="col-md-12 col-lg-7">
        <div class="card std-height">
          <h5 class="card-header">Schooladvies</h5>
          <div class="card-block">
            <school-advies :id="id"></school-advies>
          </div>
        </div>
      </div>
      <div class="col-md-12 col-lg-5">
        <div class="card std-height">
          <h5 class="card-header">SDQ (Strengths and Difficulties Questionnaire)</h5>
          <div class="card-block">
            <sdq :gebiedcode="gebiedscode"></sdq>
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-sm-3">
      <div class="col-md-12 col-lg-7">
        <div class="card std-height">
          <h5 class="card-header">Lopende subsidies</h5>
          <div class="card-block">
            <subsidie :id="id"></subsidie>
          </div>
        </div>
      </div>
      <div class="col-md-12 col-lg-5">
        <div class="card std-height">
          <h5 class="card-header">Cito score</h5>
          <div class="card-block">
            <cito-score :id="id"></cito-score>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import citoScore from './CitoScore'
import subsidie from './Subsidie'

import leerlingenNaarGewicht from './leerlingennaargewicht/VestigingscijferLeerlingenNaarGewicht.vue'
import schoolAdvies from './schooladviezen/VestigingscijferSchoolAdvies.vue'
import sdq from './sdq/SDQ.vue'

export default {
  props: [
    'id',
    'gebiedscode'
  ],
  components: {
    'leerlingen-naar-gewicht': leerlingenNaarGewicht,
    'school-advies': schoolAdvies,
    'cito-score': citoScore,
    'subsidie': subsidie,
    'sdq': sdq
  }
}
</script>

<style scoped>
  .std-height {
    height: 100%;
  }
</style>
