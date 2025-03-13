const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: "/basic/frontend/" // ✅ 重要：修正静态资源路径
})
