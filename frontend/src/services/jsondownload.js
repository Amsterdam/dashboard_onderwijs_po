export function getDataUrl (data) {
  return 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(data))
}