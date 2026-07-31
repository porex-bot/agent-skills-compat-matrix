import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { cpSync, existsSync, mkdirSync } from 'node:fs'
import { resolve } from 'node:path'

// taste-skill: Tailwind v4 via @tailwindcss/vite (NOT postcss tailwindcss plugin)
// gh-pages 子路径部署: base 从环境变量 VITE_BASE_URL 读, 默认 '/'
// 仓库为 <user>.github.io/agent-skills-compat-matrix 时需设 VITE_BASE_URL=/agent-skills-compat-matrix/
const base = process.env.VITE_BASE_URL || '/'

// build 后把根 site-data/*.json 复制进 dist/site-data, 供静态模式读取
function copySiteData() {
  return {
    name: 'copy-site-data',
    closeBundle() {
      const src = resolve(process.cwd(), '..', 'site-data')
      const dst = resolve(process.cwd(), 'dist', 'site-data')
      if (existsSync(src)) {
        mkdirSync(dst, { recursive: true })
        cpSync(src, dst, { recursive: true })
        console.log(`[copy-site-data] ${src} → ${dst}`)
      } else {
        console.warn(`[copy-site-data] ${src} 不存在, 跳过 (静态模式将无数据)`)
      }
    },
  }
}

export default defineConfig({
  base,
  plugins: [react(), tailwindcss(), copySiteData()],
  server: {
    port: 5173,
    // 开发期把 /api 代理到 FastAPI 后端 (8000)
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
