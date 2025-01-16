import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig(({ command }) => ({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src')
    }
  },
  build: {
    sourcemap: command === 'serve',
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          utils: ['date-fns', 'axios']
        }
      }
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => {
          // Rotas que precisam do prefixo /solar/
          const solarRoutes = ['/api/calendar', '/api/events', '/api/solar-times', '/api/convert'];
          for (const route of solarRoutes) {
            if (path.startsWith(route)) {
              return path.replace('/api', '/api/solar');
            }
          }
          // Mantém o caminho original para outras rotas
          return path;
        }
      }
    }
  }
}))
