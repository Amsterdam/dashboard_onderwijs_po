// This module queries for known subsidies and for awarded subsidies
import { readPaginatedData } from './datareader'

const API_HOST = process.env.API_HOST

export async function getAvailableSubsidies (year) {
  return readPaginatedData(
    API_HOST + `/onderwijs/api/subdsidie/?jaar=${year}`
  )
}

export async function getAwardedSubsidies (year, brin6) {
  return readPaginatedData(
    API_HOST + `/onderwijs/api/toegewezen-subsidie/?jaar=${year}&vestiging=${brin6}`
  )
}

export async function getAllSubsidies (year, brin) {
  let beschikbareSubsidies = await getAvailableSubsidies(year)
  beschikbareSubsidies.sort(
    (a, b) => a.naam.toLocaleUpperCase().localeCompare(b.naam.toLocaleUpperCase())
  )
  let toegekendeSubsidies = await getAwardedSubsidies(year, brin)

  // Construct an array of arrays [['name', number], ...] with number as zero when not awarded
  return beschikbareSubsidies.map(
    function (subsidy) {
      let nAwarded = toegekendeSubsidies.find(
        d => subsidy.naam === d.subsidie
      )
      nAwarded = nAwarded || 0 // replace undefined with zero if not found
      return [subsidy.naam, nAwarded.aantal]
    }
  )
}
