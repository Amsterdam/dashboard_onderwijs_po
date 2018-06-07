<!--
leaflet map
also make algemene informatie de default tab
-->
<template>
  <div>
    <div class="row mb-sm-3">
      <div class="col-md-12 col-lg-7">
        <div class="card std-height">
          <h5 class="card-header">
            Informatie uit schoolwijzer
          </h5>
          <div class="card-block p-3">
            Aantal leerlingen: {{ vestiging.leerlingen }}<br>
            <a :href="vestiging.schoolwijzer_url">Schoolwijzer pagina</a>
          </div>
        </div>
      </div>

      <div class="col-md-12 col-lg-5">
        <div class="card std-height">
          <h5 class="card-header">Adres</h5>
          <div class="card-block p-3">
            <address>
              {{ vestiging.adres.adres }}<br>
              {{ vestiging.adres.postcode }}<br>
              {{ vestiging.adres.plaats }}<br><br>
              Telefoon: {{ vestiging.adres.telefoon }}<br>
              Email: {{ vestiging.adres.email }}<br>
              Website: <a :href="vestiging.adres.website">{{ vestiging.adres.website }}</a><br>
            </address>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  props: [
    'vestiging'
  ],
  mounted () {
    console.log(this.vestiging)
  }
}
</script>

<style>

</style>
