import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import { LanguageProvider } from './lib/lang.jsx'

// basename 跟 vite.config.js 的 base 保持一致:
// - 本地开发: '/'
// - GitHub Pages 子路径部署: '/agent-skills-compat-matrix/'
// 不配 basename 时, BrowserRouter 默认按 '/' 解析 pathname,
// 在子路径部署下所有路由都匹配失败, 落到 * 兜底显示 404。
const basename = import.meta.env.BASE_URL

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter basename={basename}>
      <LanguageProvider>
        <App />
      </LanguageProvider>
    </BrowserRouter>
  </StrictMode>,
)
