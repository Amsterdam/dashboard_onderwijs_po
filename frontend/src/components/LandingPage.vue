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
import Vestigingen from './Vestigingen.vue'

export default {
  components: {
    'vestigingen': Vestigingen
  }
}
</script>

<style scoped>
</style>
