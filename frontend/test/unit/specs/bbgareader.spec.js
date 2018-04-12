import { getBbgaVariables, annotate, orderFacets } from '@/services/bbgareader'

jest.mock('axios', () => ({
  get: jest.fn((url) => {
    const meta = {
      data: {
        _links: {
          next: {
            href: null
          }
        },
        count: 2,
        results: [
          {
            id: 1,
            jaar: 2017,
            variabele: 'FAKE',
            waarde: 3.1415,
            gebiedcode15: 'B'
          },
          {
            id: 2,
            jaar: 2018,
            variabele: 'FAKE',
            waarde: 2.7182818,
            gebiedcode15: 'B'
          }
        ]
      }
    }
    return Promise.resolve(meta)
  })
}))

describe('getBbgaVariables', () => {
  it('should access BBGA variables', async () => {
    expect(
      await getBbgaVariables(['FAKE'], ['B'], [2018])
    ).toEqual(
      [{
        id: 2,
        jaar: 2018,
        variabele: 'FAKE',
        waarde: 2.7182818,
        gebiedcode15: 'B'
      }]
    )
  })
})

describe('annotate', () => {
  const source = [
    {
      a: 1
    },
    {
      a: 2
    }
  ]
  const mapping = [
    [1, 'a'],
    [2, 'b']
  ]

  it('should annotate data', () => {
    expect(
      annotate(source, 'a', 'b', mapping)
    ).toEqual(
      [
        {a: 1, b: 'a'},
        {a: 2, b: 'b'}
      ]
    )
  })
})
