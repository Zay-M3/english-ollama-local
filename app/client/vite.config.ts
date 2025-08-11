/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@chatcomponents': '/src/components/chat',
      '@chatutils': '/src/utils/chat',
      '@pages': '/src/pages',
      '@ui': '/src/components/ui',
      '@components' : 'src/components'
    }
  },
  test: {
    globals: true,
    environment: 'happy-dom',
  },
  server: {
    host: true,
    port: 5173,
    watch: {
      usePolling: true,
    }
  }
})
