<template>
  <div id="app">
    <div class="grid-container">
      <div class="content">
        <div class="grid-wrapper wrapper_12 contents-wrapper">
          <div class="grid-container container_12 main-view">
            <div class="grid-zone grid_12">
              <ams-header>Header</ams-header>
            </div>
          </div>
        </div>

        <div class="grid-wrapper wrapper_12 contents-wrapper">
          <div class="grid-container container_12 main-view">
            <div class="grid-zone grid_12">
                <div class="container-fluid">
                  <router-view></router-view>
                </div>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-wrapper">
        <div class="grid-container container_12 breakout-container">
          <div class="grid-zone grid_12 z-kolom1-4_1 breakout-zone hasbgcolor bgcolor_darkgrey footer">
            <ams-footer></ams-footer>
          </div>
        </div>
      </div>

      <loading-component></loading-component>
    </div>
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
<style scoped>
  .content {
    min-height: calc(100vh - 473px);
  }

  .footer {
    min-height: 412px;
  }
</style>
