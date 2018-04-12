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
      data = availableSubsidies
    } else if (url.includes('toegewezen')) {
      data = awardedSubsidies
    }

    return Promise.resolve(data)
  })
}))

describe('getAvailableSubsidies', () => {
  it('should retrieve a JSON array of available subsidies', async () => {
    expect(
      await getAvailableSubsidies(2017)
    ).toEqual([{
      jaar: 2017,
      naam: 'TESTSUBSIDIE'
    }])
  })
})

describe('getAwardedSubsidies', () => {
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

