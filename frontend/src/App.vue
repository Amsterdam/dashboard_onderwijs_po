<template>
  <div id="app">
    <div class="container app-container">
      <div class="container">
        <ams-header>Header</ams-header>
        <router-view></router-view>
      </div>
    </div>
    <div class="container-fluid">
      <div class="row bg-darkgrey footer">
        <ams-footer></ams-footer>
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
<style scoped>
  .app-container {
    min-height: calc(100vh - 412px);
    padding-bottom: 20px;
  }

  .footer {
    min-height: 412px;
  }
</style>
