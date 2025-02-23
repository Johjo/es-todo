import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  build: {
    outDir: '../../../target/classes/static',
  },
  root: 'src/main/webapp',
  server: {
    host: '0.0.0.0',
    hmr: { overlay: false },
    allowedHosts: ['todolist-ytreza-front.osc-fr1.scalingo.io'],
    proxy: {
      '/style': {
        ws: true,
        changeOrigin: true,
        rewrite: path => path.replace('/style', ''),
        target: 'http://localhost:9005',
      },
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },
  define: {
    'process.env': {},
  },
});
