import { readPaginatedData } from './datareader'
import { getNameMapping } from './gebieden'

import _ from 'lodash'

// BBGA API handling:
const API_URL = `https://api.data.amsterdam.nl/bbga/cijfers/`

export async function getBbgaVariables (variables, areaCodes, year) {
  // grab a number of BBGA variables for given areas and years
  let unflattened = variables.map(v => areaCodes.map(ac => readPaginatedData(
    API_URL + `?gebiedcode15=${ac}&variabele=${v}&jaar=${year}`
  )))
  let awaited = await Promise.all(_.flattenDeep(unflattened))

  return _.flatten(awaited)
}

export function annotate (data, sourceVar, injectedVar, valueMapping) {
  // use for labeling and ordering (i.e. inject extra properties for Vega)
  // valueMapping like: [[sourceValue, targetValue], ...]
  let m = new Map(valueMapping)
  return data.map(
    function (d) {
      d[injectedVar] = m.get(d[sourceVar])
      return d
    }
  )
}

export function order (data, sourceVar, values) {
  let valueMapping = values.map((d, i) => [d, i])
  return annotate(data, sourceVar, '_order', valueMapping)
}

export async function translateAreaCodes (data) {
  let nameMapping = await getNameMapping()
  return data.map(d => {
    d.gebiedcode15 = nameMapping.get(d.gebiedcode15)
    return d
  })
}
