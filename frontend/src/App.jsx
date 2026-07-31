import { Routes, Route, NavLink, Link } from 'react-router-dom'
import { useI18n } from './lib/lang.jsx'
import HomePage from './pages/HomePage.jsx'
import AgentsPage from './pages/AgentsPage.jsx'
import SkillDetailPage from './pages/SkillDetailPage.jsx'
import AgentDetailPage from './pages/AgentDetailPage.jsx'
import AdminPage from './pages/AdminPage.jsx'
import NotFoundPage from './pages/NotFoundPage.jsx'

export default function App() {
  const { t, lang, toggle } = useI18n();

  return (
    <div className="min-h-[100dvh] flex flex-col">
      <header className="sticky top-0 z-50 border-b border-[var(--color-rule)] bg-[rgba(16,14,12,0.92)] backdrop-blur">
        <div className="max-w-[1320px] mx-auto px-6 md:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5 text-[var(--color-text)] hover:no-underline">
            <span className="text-xl leading-none">🧩</span>
            <span className="font-[var(--font-serif)] font-semibold text-[19px] tracking-[-0.01em]">
              Compat <span className="italic font-black text-[var(--color-accent)]">Matrix</span>
            </span>
          </Link>
          <nav className="flex items-center gap-1">
            <NavItem to="/" label={t('navSkills')} end />
            <NavItem to="/agents" label={t('navAgents')} />
            <NavItem to="/admin" label={t('navAdmin')} />
            <button
              onClick={toggle}
              title={t('langToggleTitle')}
              className="ml-2 px-3 py-1.5 rounded font-[var(--font-mono)] text-xs font-medium uppercase tracking-wider border border-[var(--color-rule)] text-[var(--color-text-dim)] hover:text-[var(--color-accent)] hover:border-[var(--color-accent-2)] transition-colors"
            >
              <span className="text-[var(--color-text)]">{lang === 'en' ? 'EN' : '中'}</span>
              <span className="opacity-50 mx-1">/</span>
              <span>{lang === 'en' ? '中' : 'EN'}</span>
            </button>
            <a
              href="https://github.com/porex-bot/agent-skills-compat-matrix"
              target="_blank"
              rel="noreferrer"
              className="ml-1 px-3 py-1.5 font-[var(--font-mono)] text-xs font-medium uppercase tracking-wider text-[var(--color-text-dim)] hover:text-[var(--color-accent)]"
            >
              GitHub ↗
            </a>
          </nav>
        </div>
      </header>

      <main className="flex-1 max-w-[1320px] w-full mx-auto px-6 md:px-8 py-8 md:py-12">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/agents" element={<AgentsPage />} />
          <Route path="/skill/:id" element={<SkillDetailPage />} />
          <Route path="/agent/:id" element={<AgentDetailPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>

      <footer className="border-t border-[var(--color-border)] mt-16">
        <div className="max-w-[1320px] mx-auto px-6 md:px-8 py-8 text-xs text-[var(--color-text-faint)] font-[var(--font-mono)]">
          Agent Skills Compatibility Matrix — machine-validated, crawled + curated. MIT licensed.
        </div>
      </footer>
    </div>
  );
}

function NavItem({ to, label, end }) {
  return (
    <NavLink
      to={to}
      end={end}
      className={({ isActive }) =>
        `px-3 py-1.5 rounded font-[var(--font-mono)] text-xs font-medium uppercase tracking-wider transition-colors ${
          isActive
            ? 'text-[var(--color-accent)] bg-[var(--color-bg-elev)]'
            : 'text-[var(--color-text-dim)] hover:text-[var(--color-text)]'
        }`
      }
    >
      {label}
    </NavLink>
  );
}
