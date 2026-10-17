import Link from 'next/link'

import { BackToTop } from './BackToTop'

export const REPO_URL = 'https://github.com/jars-demo/evals-demo'

export function Mark({ size = 22 }: { size?: number }) {
  // A tick inside a frame: a passing case.
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" aria-hidden="true">
      <rect x="1" y="1" width="22" height="22" rx="4" fill="#111111" />
      <path
        d="m7 12.5 3.2 3.2L17 9"
        fill="none"
        stroke="#4ade80"
        strokeWidth="2.4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <>
      <header className="border-b border-line">
        <nav
          aria-label="Main"
          className="mx-auto flex h-14 max-w-5xl items-center justify-between gap-4 px-4"
        >
          <Link href="/" className="inline-flex items-center gap-2.5 text-[15px] font-semibold">
            <Mark />
            Evals, not vibes
          </Link>
          <ul className="flex items-center gap-5 text-[14px] text-ink-2">
            <li>
              <Link href="/workshop" className="hover:text-ink">
                Workshop
              </Link>
            </li>
            <li>
              <a href={REPO_URL} className="hover:text-ink">
                GitHub
              </a>
            </li>
          </ul>
        </nav>
      </header>
      <main id="main" className="flex-1">
        {children}
      </main>
      <footer className="border-t border-line">
        <div className="mx-auto flex max-w-5xl flex-col gap-2 px-4 py-6 text-[13px] text-muted sm:flex-row sm:justify-between">
          <span>Evals, not vibes · MIT licensed</span>
          <a href={REPO_URL} className="hover:text-ink">
            GitHub
          </a>
        </div>
      </footer>
      <BackToTop />
    </>
  )
}
