<template>
  <div id="app">
    <div class="container">
      <ams-header>Header</ams-header>
      <router-view></router-view>
    </div>

    <loading-component></loading-component>
    <div class="container-fluid">
      <div class="row bg-darkgrey footer">
        <ams-footer></ams-footer>
      </div>
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
