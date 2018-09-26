<!-- Right column in original design, contains Gebieds specific data -->
<template>
  <div>
    <div class="row mb-sm-3">
      <div class="col-sm-12 col-lg-7">
        <card-with-help title="Opleiding" :helpText="this.helpTexts.opleiding">
          <opleiding :gebiedcode="gebiedscode"></opleiding>
        </card-with-help>
      </div>
      <div class="col-sm-12 col-lg-5">
        <card-with-help title="Inkomen" :helpText="this.helpTexts.inkomen">
          <inkomen :gebiedcode="gebiedscode"></inkomen>
        </card-with-help>
      </div>
    </div>
    <div class="row mb-sm-3">
      <div class="col-sm-12 col-lg-7">
        <card-with-help title="Migratieachtergrond" :helpText="this.helpTexts.migratieAchtergrond">
          <herkomst :gebiedcode="gebiedscode"></herkomst>
        </card-with-help>
      </div>
      <div class="col-sm-12 col-lg-5">
        <card-with-help title="Sociale problematiek" :helpText="this.helpTexts.socialeProblematiek">
          <sociale-problematiek :gebiedcode="gebiedscode"></sociale-problematiek>
        </card-with-help>
      </div>
    </div>
    <div class="row mb-sm-3">
      <div class="col-sm-12 col-lg-7">
        <card-with-help title="Veiligheidsindex" :helpText="this.helpTexts.veiligheidsindex">
          <veiligheidsindex :gebiedcode="gebiedscode"></veiligheidsindex>
        </card-with-help>
      </div>
      <div class="col-sm-12 col-lg-5">
        <card-with-help title="Criminaliteitsindex" :helpText="this.helpTexts.criminaliteitsindex">
          <criminaliteitsindex :gebiedcode="gebiedscode"></criminaliteitsindex>
        </card-with-help>
      </div>
    </div>
    <div class="row mb-sm-3">
      <div class="col-sm-12 col-lg-7">
        <card-with-help title="SDQ" :helpText="this.helpTexts.sdq">
          <sdq :gebiedcode="gebiedscode"></sdq>
        </card-with-help>
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

import cardWithHelp from '../general/cardWithHelp.vue'
import helpTexts from '../../../static/help-texts'

export default {
  props: [
    'gebiedscode'
  ],
  components: {
    'card-with-help': cardWithHelp,
    'herkomst': gebiedscijfersHerkomst,
    'opleiding': gebiedscijfersOpleiding,
    'inkomen': gebiedscijfersInkomen,
    'sociale-problematiek': gebiedscijfersSocialeProblematiek,
    'veiligheidsindex': gebiedscijfersVeiligheidsindex,
    'criminaliteitsindex': gebiedscijfersCriminaliteitsindex,
    'sdq': sdq
  },
  data () {
    return {
      helpTexts
    }
  }
}
</script>

<style scoped>
  .card {
    border-radius: 0 !important;
  }
</style>
