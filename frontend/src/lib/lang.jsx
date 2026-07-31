// 语言上下文 — 中英双语切换, 持久化到 localStorage
import { createContext, useContext, useState, useCallback, useMemo } from 'react'
import { translate, caveat } from './i18n.js'

const LanguageContext = createContext(null);

const STORAGE_KEY = 'asm-lang';

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(() => {
    if (typeof window === 'undefined') return 'en';
    return localStorage.getItem(STORAGE_KEY) || 'en';
  });

  const setLanguage = useCallback((next) => {
    setLang(next);
    try { localStorage.setItem(STORAGE_KEY, next); } catch {}
  }, []);

  const toggle = useCallback(() => {
    setLanguage(lang === 'en' ? 'zh' : 'en');
  }, [lang, setLanguage]);

  // t(key, params) — 翻译; tc(enText, zhOverride) — caveat 本地化
  const value = useMemo(() => ({
    lang,
    setLanguage,
    toggle,
    t: (key, params) => translate(lang, key, params),
    tc: (enText, zhOverride) => caveat(lang, enText, zhOverride),
  }), [lang, setLanguage, toggle]);

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useI18n() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error('useI18n must be used within LanguageProvider');
  return ctx;
}
