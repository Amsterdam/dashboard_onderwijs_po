<template>
  <div id="leerlingengewicht">
    Loading...
  </div>
</template>

<script>
import embed from 'vega-embed'
import readPaginatedData from '../services/util'

const vegaEmbedOptions = {
  'actions': {
    'export': false,
    'source': false,
    'editor': false},
  'renderer': 'svg'
}

const vegaSpec = {
  '$schema': 'https://vega.github.io/schema/vega-lite/v2.json',
  'description': 'A simple bar chart with embedded data.',
  'data': {'values': []},
  'title': {
    'text': 'Leerlingen naar gewicht',
    'anchor': 'start',
    'offset': 12
  },
  'facet': {
    'column': {
      'field': 'gewicht',
      'type': 'ordinal'
    }
  },
  'spec': {
    'height': 80,
    'width': 100,
    'layer': [{
      'mark': 'bar',
      'encoding': {
        'y': {
          'field': 'totaal',
          'type': 'quantitative'
        },
        'x': {
          'field': 'jaar',
          'type': 'nominal',
          'axis': {
            'labelAngle': 1e-10, // 0 or 360 are not accepted here, bug in vega lite?
            'title': ''
          }
        },
        'color': {
          'field': 'jaar',
          'type': 'nominal',
          'legend': null,
          'scale': {
            'range': ['#3182bd', '#9ecae1', '#deebf7']
          }
        }
      }
    },
    {
      'mark': {
        'type': 'text',
        'baseline': 'bottom',
        'dy': -1
      },
      'encoding': {
        'y': {
          'field': 'totaal',
          'type': 'quantitative'
        },
        'x': {
          'field': 'jaar',
          'type': 'nominal'
        },
        'text': {
          'field': 'totaal',
          'type': 'quantitative'
        }
      }
    }
    ]
  },
  'config': {
    'view': {'stroke': 'transparent'},
    'axis': {'domainWidth': 1}
  }
}

export default {
  props: [
    'id'
  ],
  async created () {
    let url = `https://data.amsterdam.nl/onderwijs/api/leerling-naar-gewicht/?vestiging=${this.id}`
    try {
      let values = await readPaginatedData(url)
      vegaSpec.data.values = values
      embed('#leerlingengewicht', vegaSpec, vegaEmbedOptions)
    } catch (e) {
      console.error(`Error: Failed to load leerlingen naar gewicht data from url ${url}`)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
