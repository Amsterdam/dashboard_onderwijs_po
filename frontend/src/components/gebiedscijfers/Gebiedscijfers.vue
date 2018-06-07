<!-- Right column in original design, contains Gebieds specific data -->
<template>
  <div>
    <div class="row mb-sm-3">
      <div class="col-sm-12 col-lg-7">
        <div class="card std-height">
          <h5 class="card-header">Opleiding</h5>
          <div class="card-block">
            <opleiding :gebiedcode="gebiedscode"></opleiding>
          </div>
        </div>
      </div>
      <div class="col-sm-12 col-lg-5">
        <div class="card std-height">
          <h5 class="card-header">Inkomen</h5>
          <div class="card-block">
            <inkomen :gebiedcode="gebiedscode"></inkomen>
          </div>
        </div>
      </div>
    </div>
    <div class="row mb-sm-3">
      <div class="col-sm-12 col-lg-7">
        <div class="card std-height">
          <h5 class="card-header">Migratieachtergrond</h5>
          <div class="card-block">
            <herkomst :gebiedcode="gebiedscode"></herkomst>
          </div>
        </div>
      </div>
      <div class="col-sm-12 col-lg-5">
        <div class="card std-height">
          <h5 class="card-header">Sociale problematiek</h5>
          <div class="card-block">
            <sociale-problematiek :gebiedcode="gebiedscode"></sociale-problematiek>
          </div>
        </div>
      </div>
    </div>
    <div class="row mb-sm-3">
      <div class="col-sm-12 col-lg-7">
        <div class="card">
          <h5 class="card-header">Veiligheidsindex</h5>
          <div class="card-block">
            <veiligheidsindex :gebiedcode="gebiedscode"></veiligheidsindex>
          </div>
        </div>
      </div>
      <div class="col-sm-12 col-lg-5">
        <div class="card">
          <h5 class="card-header">Criminaliteitsindex</h5>
          <div class="card-block">
            <criminaliteitsindex :gebiedcode="gebiedscode"></criminaliteitsindex>
          </div>
        </div>
      </div>
    </div>
    <div class="row mb-sm-3">
      <div class="col-sm-12 col-lg-7">
        <div class="card std-height">
          <h5 class="card-header">SDQ</h5>
          <div class="card-block">
            <sdq :gebiedcode="gebiedscode"></sdq>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// subcomponents that display the various variables
import gebiedscijfersHerkomst from './herkomst/GebiedscijfersHerkomst.vue'
import gebiedscijfersOpleiding from './opleiding/GebiedscijfersOpleiding.vue'
import gebiedscijfersInkomen from './inkomen/GebiedscijfersInkomen.vue'
import gebiedscijfersSocialeProblematiek from './socialeproblematiek/GebiedscijfersSocialeProblematiek.vue'
import gebiedscijfersVeiligheidsindex from './veiligheidsindex/GebiedscijfersVeiligheidsindex'
import gebiedscijfersCriminaliteitsindex from './criminaliteitsindex/GebiedscijfersCriminaliteitsindex.vue'
import sdq from './sdq/SDQ.vue'

export default {
  props: [
    'gebiedscode'
  ],
  components: {
    'herkomst': gebiedscijfersHerkomst,
    'opleiding': gebiedscijfersOpleiding,
    'inkomen': gebiedscijfersInkomen,
    'sociale-problematiek': gebiedscijfersSocialeProblematiek,
    'veiligheidsindex': gebiedscijfersVeiligheidsindex,
    'criminaliteitsindex': gebiedscijfersCriminaliteitsindex,
    'sdq': sdq
  }
}
</script>

<style scoped>
  .card {
    border-radius: 0 !important;
  }
</style>
