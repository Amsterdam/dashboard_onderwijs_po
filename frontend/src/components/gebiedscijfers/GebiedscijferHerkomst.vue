<template>
  <div id="gebiedscijfer-herkomst">
    <h3>Placeholder gebiedscijfers herkomst</h3>
  </div>
</template>

<script>

export default {
  props: [
    'gebiedscode',
    'herkomst'
  ],
  async mounted () {
    console.log('GebiedscijferHerkomst.vue ->', this.herkomst)
  }
}
</script>

<style scoped>

</style>
