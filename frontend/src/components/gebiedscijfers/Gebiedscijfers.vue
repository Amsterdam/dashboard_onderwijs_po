<!-- Right column in original design, contains Gebieds specific data -->
<template>
  <div id="gebiedscijfers">
    <refactor :gebiedcode="gebiedscode"></refactor>
    <opleiding :gebiedcode="gebiedscode"></opleiding>
    <inkomen :gebiedcode="gebiedscode"></inkomen>
    <sociale-problematiek :gebiedcode="gebiedscode"></sociale-problematiek>
    <veiligheidsindex :gebiedcode="gebiedscode"></veiligheidsindex>
    <criminaliteitsindex :gebiedcode="gebiedscode"></criminaliteitsindex>
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

export default {
  props: [
    'gebiedscode'
  ],
  components: {
    'refactor': gebiedscijfersHerkomst,
    'opleiding': gebiedscijfersOpleiding,
    'inkomen': gebiedscijfersInkomen,
    'sociale-problematiek': gebiedscijfersSocialeProblematiek,
    'veiligheidsindex': gebiedscijfersVeiligheidsindex,
    'criminaliteitsindex': gebiedscijfersCriminaliteitsindex
  }
}
</script>

<style scoped>
</style>
