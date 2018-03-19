<template>
  <div id="app" class="grid-container">
    <ams-header>Header</ams-header>

    <div class="grid-wrapper wrapper_12 contents-wrapper">
      <div class="grid-container container_12 main-view">
        <div class="grid-zone grid_12">
          <router-view></router-view>
        </div>
      </div>
    </div>

    <div class="contents-wrapper">
      <div class="grid-container container_12 breakout-container">
        <div class="grid-zone grid_12 z-kolom1-4_1 breakout-zone hasbgcolor bgcolor_darkgrey">
          <ams-footer>Footer</ams-footer>
        </div>
      </div>
    </div>

    <loading-component></loading-component>
  </div>
</template>

<script>
import amsHeader from '@/components/AMSHeader'
import amsFooter from '@/components/AMSFooter'
import loadingComponent from '@/components/LoadingComponent'

export default {
  name: 'App',
  components: {
    'ams-header': amsHeader,
    'ams-footer': amsFooter,
    'loading-component': loadingComponent
  }
}
</script>

<!-- Global styling -->
<style>
</style>
