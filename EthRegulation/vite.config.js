export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://10.0.2.148:5000',
        changeOrigin: true
      }
    }
  }
}) 