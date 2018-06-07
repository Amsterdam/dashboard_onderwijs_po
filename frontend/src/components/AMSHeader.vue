<template>
  <div class="container" style="padding:0em">
    <div class="ams-header">
      <header>
        <router-link :to="{ name: 'Vestigingen' }">
          <img class="ams-header__logo" src="../../static/logo-short.svg" height="45px">
        </router-link>
      </header>
      <span class="header-title"><b>Dashboard primair onderwijs</b></span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AMSHeader',
  components: {
  }
}
</script>

<style scoped>
.ams-header {
  width: 100%;
  display: flex;
  flex-direction: row;
  padding: .5rem;
  margin-left: -25px;
}

.ams-header .header-title {
  margin-left: 1rem;
  display: flex;
  align-items: center;
  font-size: 1.7rem;
}
</style>
