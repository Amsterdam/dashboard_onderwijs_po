'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

// ROUTER_BASE must be a regular expression
module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  ROUTER_BASE: '"/"'
})
