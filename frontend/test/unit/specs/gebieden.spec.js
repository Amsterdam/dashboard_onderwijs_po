import { getNameMapping } from '@/services/gebieden'

jest.mock('axios', () => ({
  get: jest.fn((url) => {
    let data = null
    
    // provide fake data:
    if (url.includes('buurt')) {
      data = [{
        _display: 'Aalsmeerwegbuurt Oost (K44d)',
        code: '44d'
      }]
    } else if (url.includes('gebied')) {
      data = [{
        code: 'DX21',
        naam: 'Bijlmer Oost'
      }]
    }

    const meta = {
      data: {
        _links: {
          next: {
            href: null
          }
        },
        count: 1,
        results: data
      }
    }

    return Promise.resolve(meta)
  })
}))

// await must be added 
describe('getAreaCodes', () => {
  it('should translate "STAD"', () => {
    getNameMapping().then(
      mapping => {
        return expect(mapping.get('STAD')).toEqual('Amsterdam')
      }
    )
  })

  it('should translate buurt codes', () => {
    getNameMapping().then(
      mapping => {
        return expect(mapping.get('DX21')).toEqual('Bijlmer Oost')
      }
    )
  })

  it('should translate GGW codes', () => {
    getNameMapping().then(
      mapping => {
        return expect(mapping.get('K44d')).toEqual('Aalsmeerwegbuurt Oost')
      }
    )
  })
})