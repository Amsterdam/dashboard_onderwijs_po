<template>
  <div id="schooladvies">
    Loading...
  </div>
</template>

<script>
import embed from 'vega-embed'
import util from '../services/util'

const vegaEmbedOptions = {
  'actions': {
    'export': false,
    'source': false,
    'editor': false},
  'renderer': 'svg'
}

const vegaSpec = {
  '$schema': 'https://vega.github.io/schema/vega-lite/v2.json',
  'description': 'Bar chart van schooladviezen',
  'data': {'values': []},
  'title': {
    'text': 'School adviezen',
    'offset': 12
  },
  'facet': {
    'column': {
      'field': 'advies',
      'type': 'ordinal'
    }
  },
  'spec': {
    'height': 60,
    'width': 100,
    'layer': [
      {
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
              'title': '',
              'labelAngle': 1e-10
            }
          },
          'color': {
            'field': 'jaar',
            'type': 'nominal',
            'legend': null,
            'scale': {
              'range': [
                '#3182bd',
                '#9ecae1',
                '#deebf7'
              ]
            }
          }
        }
      },
      {
        'mark': {
          'type': 'text',
          'baseline': 'bottom',
          'dy': -2
        },
        'encoding': {
          'x': {
            'field': 'jaar',
            'type': 'nominal'
          },
          'y': {
            'field': 'totaal',
            'type': 'quantitative'
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
    'view': {
      'stroke': 'transparent'
    },
    'axis': {
      'domainWidth': 1
    }
  }
}

export default {
  props: [
    'id'
  ],
  async created () {
    let url = `https://data.amsterdam.nl/onderwijs/api/aggregated-advies/?vestiging=${this.id}`
    try {
      vegaSpec.data.values = await util.readData(url)
      embed('#schooladvies', vegaSpec, vegaEmbedOptions)
    } catch (e) {
      console.error(`Error: Failed to load aggregated schooladviezen from url ${url}`)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
