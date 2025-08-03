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
    }
  },
  server: {
    host: true,
    port: 5173,
    watch: {
      usePolling: true,
    }
  }
})
