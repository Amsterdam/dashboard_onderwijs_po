import { readPaginatedData } from './datareader'

const API_HOST = 'https://api.data.amsterdam.nl'
let code2NameCache = null

async function getAreaCodes () {
  let tmp = [['STAD', 'Amsterdam']]
  // handle buurten
  let buurtData = await readPaginatedData(API_HOST + '/gebieden/buurt/')
  let buurtMapping = buurtData.map(
    d => {
      let name = d._display.slice(0, d._display.search(/\s\(/))
      let areaCode = /\(\S*\)/.exec(d._display)[0].slice(1, -1)
      return [areaCode, name]
    }
  )

  // handle gebiedsgerichtwerken gebieden
  let ggwData = await readPaginatedData(API_HOST + '/gebieden/gebiedsgerichtwerken/')
  let ggwMapping = ggwData.map(
    d => [d.code, d.naam]
  )

  return new Map(buurtMapping.concat(ggwMapping).concat(tmp))
}

export async function getNameMapping () {
  if (!code2NameCache) {
    code2NameCache = getAreaCodes()
  }
  return code2NameCache
}
