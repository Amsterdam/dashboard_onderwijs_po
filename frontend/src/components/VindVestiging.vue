<!-- Type ahead find + data handling -->
<template>
    <div class="tt-dropdown-menu">
    <input type="text" class="typeahead form-control" placeholder="Zoek hier naar een vestiging">
  </div>
</template>

<script>
// see also: https://vuejsdevelopers.com/2017/05/20/vue-js-safely-jquery-plugin/
// see also: https://twitter.github.io/typeahead.js/examples/
import jQuery from 'jquery'
import 'corejs-typeahead/dist/typeahead.jquery.js' // this is the maintained version of Twitter typeahead.js
import 'typeahead.js-bootstrap4-css/typeaheadjs.css' // this fixes the CSS for Bootstrap 4

import { mapGetters } from 'vuex'

function Matcher () {
  let map = null // should be an es6 map (long names to ids)
  let strings = []

  function match (query, callback) {
    // match query against known strings, show results dropdown
    let substrRegex = new RegExp(query, 'i')
    callback(strings.filter(str => substrRegex.test(str)))
  }

  match.map = function (value) {
    if (arguments.length) {
      map = value
      strings = Array.from(map.keys())
      return match
    } else {
      return map
    }
  }

  match.findMatchId = function (str) {
    console.log()
    return map.get(str)
  }

  return match
}

export default {
  created () {
    this.vars = {
      matcher: Matcher()
    }
  },
  mounted () {
    // initialize typeahead text input without data (added later asynchronously)
    jQuery(this.$el).find('.typeahead')
      .typeahead(null, {
        name: 'states',
        source: this.vars.matcher,
        templates: {
          header: '<strong>Scholen die overeenkomen</strong>'
        }
      }).bind('typeahead:select', this.wasSelected)

    if (this.vestigingen.length) { this.setTypeaheadData(this.vestigingen) }
  },
  methods: {
    wasSelected (event, suggestion) {
      let key = this.vars.matcher.findMatchId(suggestion)
      this.$router.push({name: 'Vestiging', params: {id: key}})
    },
    setTypeaheadData (vestigingen) {
      let map = new Map(vestigingen.map(d => [d.naam, d.brin6]))
      this.vars.matcher.map(map)
    }
  },
  computed: {
    ...mapGetters([
      'vestigingen'
    ])
  },
  watch: {
    vestigingen (to, from) {
      if (to) {
        this.setTypeaheadData(to)
      }
    }
  }
}
</script>

<style scoped>
</style>
