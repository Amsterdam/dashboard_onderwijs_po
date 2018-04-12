import { readPaginatedData, readData, halNextAccessor, nextAccessor } from '@/services/datareader'

jest.mock('axios', () => ({
  get: jest.fn((url) => {
    const page1 = {
      data: {
        _links: {
          next: {
            href: '/test/?page=2'
          }
        },
        count: 2,
        results: [1]
      }
    }
    const page2 = {
      data: {
        _links: {
          next: {
            href: null
          }
        },
        count: 2,
        results: [2]
      }
    }

    let meta = null
    if (url.includes('page=1')) {
      meta = page1
    } else if (url.includes('page=2')){
      meta = page2
    }
    return Promise.resolve(meta)
  })
}))

describe('readPaginatedData', () => {
  it('reads paginated HAL-JSON endpoints', async () => {
    expect(await readPaginatedData('/test/')).toEqual([1, 2])
  })
})

describe('readData', () => {
  it('retrieves data from a REST endpoint', async () => {
    expect(await readData('/test/?page=2')).toEqual({
      _links: {
        next: {
          href: null
        }
      },
      count: 2,
      results: [2]
    })
  })
})

describe('halNextAccessor', () => {
  it('should retrieve next page url HAL-JSON style', () => {
    expect(halNextAccessor({
      data: {
        _links: {
          next: {
            href: 'NEXT'
          }
        }
      }
    })).toEqual(
      'NEXT'
    )
  })
})

describe('nextAccessor', () => {
  it('shoult retrieve next page url basic Django REST Framework style', () => {
    expect(nextAccessor(
      {
        data: {
          next: 'NEXT'
        }
      }
    )).toEqual(
      'NEXT'
    )
  })
})