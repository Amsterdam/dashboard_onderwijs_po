import { readPaginatedData } from './datareader'

// BBGA API handling:
const API_URL = `https://api.data.amsterdam.nl/bbga/cijfers/`

export async function getBbgaVariable (variable, areaCode, year) {
  // grab BBGA data for one BBGA variable
  let url = API_URL + `?gebiedcode15=${areaCode}&variabele=${variable}`
  let results = await readPaginatedData(url)
  return results
}

export async function getBbgaVariables (variables, areaCodes, years) {
  // grab a number of BBGA variables for given areas and years
  let urls = []
  const yearsSet = new Set(years)

  for (let v of variables) {
    for (let gc of areaCodes) {
      let url = API_URL + `?gebiedcode15=${gc}&variabele=${v}`
      urls.push(url)
    }
  }

  let promisedResultsArrays = urls.map(url => readPaginatedData(url))
  let resultsArrays = await Promise.all(promisedResultsArrays)
  let out = [].concat.apply([], resultsArrays)

  out = out.filter(r => yearsSet.has(r.jaar))

  return out
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
