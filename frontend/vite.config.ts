import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
        port: 5173,
        open: true,
        fs: {
            strict: false
        },
        historyApiFallback: true
    },

    build: {
      outDir: 'dist',
    },
    define: {
      'process.env': env,
    }
  };
});
