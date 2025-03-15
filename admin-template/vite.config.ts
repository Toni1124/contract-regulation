import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import env from './env';

const proxy = {
  '^/permissions': {
    target: 'http://power.hpyyb.cn/',
    changeOrigin: true
  }
}
declare const process;

// https://vitejs.dev/config/
export default defineConfig(async () => ({
  plugins: [vue()],

  base: env.BASE_URL,

  define: {
    "process.env": process.env,
    'process.platform': JSON.stringify('win32'),
    'process.env.NODE_DEBUG': JSON.stringify(''),
  },

  resolve: {
    alias: {
      "@": "/src",
      "~": "",
    },
  },

  optimizeDeps: {
    include: ['monaco-editor/esm/vs/editor/editor.worker']
  },

  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          jsonWorker: ['monaco-editor/esm/vs/language/json/json.worker'],
          cssWorker: ['monaco-editor/esm/vs/language/css/css.worker'],
          htmlWorker: ['monaco-editor/esm/vs/language/html/html.worker'],
          tsWorker: ['monaco-editor/esm/vs/language/typescript/ts.worker'],
          editorWorker: ['monaco-editor/esm/vs/editor/editor.worker'],
        },
      },
    },
  },

  esbuild: {
    jsxFactory: 'h',
    jsxFragment: 'Fragment',
  },

  clearScreen: false,
  server: { proxy },
  preview: { proxy },
}));
