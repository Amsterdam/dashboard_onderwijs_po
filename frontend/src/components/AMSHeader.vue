<template>
  <div class="ams-header">
    <header>
      <img class="ams-header__logo" src="../../static/logo-short.svg" height="45px">
    </header>
    <span class="header-title"><b>TITEL</b></span>
  </div>
</template>

<script>

export default {
  name: 'AMSHeader',
  components: {
  }
}

</script>

<style lang="scss" scoped>
.ams-header {
  width: 100%;
  display: flex;
  flex-direction: row;
  padding: .5rem;

  .header-title {
    margin-left: 1rem;
    display: flex;
    align-items: center;
    font-size: 1.7rem;
  }
}
</style>
