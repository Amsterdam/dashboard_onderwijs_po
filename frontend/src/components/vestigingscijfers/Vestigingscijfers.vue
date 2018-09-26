<!-- Left column in original design, contains Vestiging specific data -->
<template>
  <div id="vestigingscijfers">
    <!--<h3>De vestiging</h3>-->
    <div class="row mb-sm-3">
      <div class="col-md-12 col-lg-7">
        <card-with-help title="Aantal leerlingen naar gewicht" :helpText="this.helpTexts.leerlingenNaarGewicht">
          <leerlingen-naar-gewicht :id="id"></leerlingen-naar-gewicht>
        </card-with-help>
      </div>
      <div class="col-md-12 col-lg-5">
        <card-with-help title="">
        </card-with-help>
      </div>
    </div>

    <div class="row mb-sm-3">
      <div class="col-md-12 col-lg-7">
        <card-with-help title="Schooladvies" :helpText="this.helpTexts.schoolAdvies">
          <school-advies :id="id"></school-advies>
        </card-with-help>
      </div>
      <div class="col-md-12 col-lg-5">
        <card-with-help title="Cito score" :helpText="this.helpTexts.citoScore">
          <cito-score :id="id"></cito-score>
        </card-with-help>
      </div>
    </div>

    <div class="row mb-sm-3">
      <div class="col-md-12 col-lg-7">
        <card-with-help title="Lopende subsidies" :helpText="this.helpTexts.lopendeSubsidies">
          <subsidie :id="id"></subsidie>
        </card-with-help>
      </div>
    </div>

  </div>
</template>

<script>
import citoScore from './CitoScore'
import subsidie from './Subsidie'

import leerlingenNaarGewicht from './leerlingennaargewicht/VestigingscijferLeerlingenNaarGewicht.vue'
import schoolAdvies from './schooladviezen/VestigingscijferSchoolAdvies.vue'

import cardWithHelp from '../general/cardWithHelp.vue'
import helpTexts from '../../../static/help-texts'

export default {
  props: [
    'id',
    'gebiedscode'
  ],
  components: {
    'card-with-help': cardWithHelp,
    'leerlingen-naar-gewicht': leerlingenNaarGewicht,
    'school-advies': schoolAdvies,
    'cito-score': citoScore,
    'subsidie': subsidie
  },
  data () {
    return {
      helpTexts
    }
  }
}
</script>

<style lang="scss" scoped>

  .parent {
  }

  .child {
    /*padding: 25% 5px;*/
  }
</style>
