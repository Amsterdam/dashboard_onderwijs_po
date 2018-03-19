<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col">
        <vestigingen></vestigingen>
      </div>
    </div>
  </div>
</template>

<script>
import VindVestiging from './VindVestiging.vue'
import Vestigingen from './Vestigingen.vue'

export default {
  components: {
    'vind-vestiging': VindVestiging,
    'vestigingen': Vestigingen
  }
}
</script>

<style scoped>
</style>
