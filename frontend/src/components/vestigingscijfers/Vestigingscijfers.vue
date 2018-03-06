<!-- Left column in original design, contains Vestiging specific data -->
<template>
  <div id="vestigingscijfers">
    
    
    


    <h3>De vestiging</h3>
    <div class="row mb-sm-3">
      <div class="col-md-12 col-lg-7">
        <div class="card">
          <h5 class="card-header">Aantal leerlingen naar gewicht</h5>
          <div class="card-block">
            <leerlingen-naar-gewicht :id="id"></leerlingen-naar-gewicht>
          </div>
        </div>
      </div>
      <div class="col-md-12 col-lg-5">
        <div class="card">
          <h5 class="card-header"></h5>
          <div class="card-block">
            tbd
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-sm-3">
      <div class="col-md-12 col-lg-7">
        <div class="card">
          <h5 class="card-header">Schooladvies</h5>
          <div class="card-block">
            <school-advies :id="id"></school-advies>
          </div>
        </div>
      </div>
      <div class="col-md-12 col-lg-5">
        <div class="card">
          <h5 class="card-header"></h5>
          <div class="card-block">
            tbd
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-sm-3">
      <div class="col-md-12 col-lg-7">
        <div class="card">
          <h5 class="card-header">Lopende subsidies</h5>
          <div class="card-block">
            <subsidie :id="id"></subsidie>
          </div>
        </div>
      </div>
      <div class="col-md-12 col-lg-5">
        <div class="card">
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
