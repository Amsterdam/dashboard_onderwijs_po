import { getDataUrl } from '@/services/jsondownload'

describe('getDataUrl', () => {
  it('should create a data url', () => {
    expect(
      getDataUrl([1, 2]
    )
    ).toEqual(
      'data:text/json;charset=utf-8,%5B1%2C2%5D'
    )
  })
})