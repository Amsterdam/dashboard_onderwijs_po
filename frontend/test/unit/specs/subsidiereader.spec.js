import { getAvailableSubsidies, getAwardedSubsidies, getAllSubsidies } from '@/services/subsidiereader'

jest.mock('axios', () => ({
  get: jest.fn((url) => {

    const availableSubsidies = {
      data: {
        _links: {
          next: {
            href: null
          }
        },
        count: 1,
        results: [
          {
            jaar: 2017,
            naam: 'TESTSUBSIDIE'
          }
        ]
      }
    }

    const noSubsidies = {
      '_links': {
        'self': {
          "href":"http://127.0.0.1:8000/onderwijs/api/subsidie/?jaar=1900&format=json"
        },
        'next': {
          'href': null
        },
        'previous': {
          "href": null
        }
      },
      'count': 0,
      'results': []
    }

    const awardedSubsidies = {
      data: {
        _links: {
          next: {
            href: null
          }
        },
        count: 1,
        results: [
          {
            subsidie: 'TESTSUBSIDIE',
            brin: '00AA',
            vestigingsnummer: 0,
            aantal: 1,
            vestiging: '00AA00'
          }    
        ]
      }
    }

    let data = null
    if (url.includes('/subsidie/')) {
      if (url.includes('1900')) {
        data = noSubsidies
      } else {
        data = availableSubsidies
      }
    } else if (url.includes('toegewezen')) {
      if (url.includes('1900')) {
        data = noSubsidies
      } else {
        data = awardedSubsidies
      }
    }

    return Promise.resolve(data)
  })
}))

describe('getAvailableSubsidies', async () => {
  it('should retrieve a JSON array of available subsidies', async () => {
    expect(
      await getAvailableSubsidies(2017)
    ).toEqual([{
      jaar: 2017,
      naam: 'TESTSUBSIDIE'
    }])
  })

  it('should retrieve a JSON array of available subsidies', async () => {
    expect(
      await getAvailableSubsidies('2017')
    ).toEqual([{
      jaar: 2017,
      naam: 'TESTSUBSIDIE'
    }])
  })

})

describe('getAvailableSubsidies', async () => {
  it('should retrieve a JSON array of available subsidies', async () => {
    expect(await getAvailableSubsidies(1900)).toEqual([])
  })
})

describe('getAwardedSubsidies', async () => {
  it('should retrieve a JSON array of awarded subsidies', async () => {
    expect(
      await getAwardedSubsidies(2017, '00AA00')
    ).toEqual([{
      subsidie: 'TESTSUBSIDIE',
      brin: '00AA',
      vestigingsnummer: 0,
      aantal: 1,
      vestiging: '00AA00'
    }])
  })
})

describe('getAwardedSubsidies', async () => {
  it('should retrieve a JSON array of awarded subsidies', async () => {
    expect(await getAvailableSubsidies(1900, '00AA00')).toEqual([])
  })
})