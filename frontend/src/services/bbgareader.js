import { readPaginatedData } from './datareader'
import _ from 'lodash'

// BBGA API handling:
const API_URL = `https://api.data.amsterdam.nl/bbga/cijfers/`

export async function getBbgaVariableOld (variable, areaCode, year) {
  // grab BBGA data for one BBGA variable
  return readPaginatedData(API_URL + `?gebiedcode15=${areaCode}&variabele=${variable}`)
}

export async function getBbgaVariables (variables, areaCodes, years) {
  // grab a number of BBGA variables for given areas and years
  let unflattened = variables.map(v => areaCodes.map(ac => readPaginatedData(
    API_URL + `?gebiedcode15=${ac}&variabele=${v}`
  )))
  let awaited = await Promise.all(_.flattenDeep(unflattened))

  const yearsSet = new Set(years)
  let out = _.flatten(awaited)
  return out.filter(r => yearsSet.has(r.jaar))
}

export function annotate (data, sourceVar, injectedVar, valueMapping) {
  // use for labeling and facet order (i.e. inject extra property for Vega)
  // valueMapping like: [[sourceValue, targetValue], ...]
  let m = new Map(valueMapping)
  return data.map(
    function (d) {
      d[injectedVar] = m.get(d[sourceVar])
      return d
    }
  )
}

export function orderFacets (data, sourceVar, values) {
  let valueMapping = values.map((d, i) => [d, i])
  return annotate(data, sourceVar, '_facetorder', valueMapping)
}
