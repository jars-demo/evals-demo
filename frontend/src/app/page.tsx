import Link from 'next/link'

import { CopyButton } from '@/components/CopyButton'
import { CHAPTERS } from '@/lib/workshop'

// Real output of `uv run python -m triage run` against the offline baseline, trimmed.
const SCORECARD = [
  { mark: 'PASS', id: 'double-charge', answer: 'billing, normal' },
  { mark: 'FAIL', id: 'invoice-copy', answer: 'billing, normal' },
  { mark: 'FAIL', id: 'card-declined-blocked', answer: 'other, normal' },
  { mark: 'PASS', id: 'api-500', answer: 'bug, high' },
  { mark: 'PASS', id: 'forgot-password', answer: 'account, high' },
  { mark: 'FAIL', id: 'dark-mode', answer: 'feature_request, normal' },
]

const SCORES = [
  ['category', '69%'],
  ['urgency', '38%'],
  ['urgent_never_missed', '94%'],
  ['overall', '67%'],
]

const PARTS = [
  ['Cases', 'evals/data/cases.jsonl', 'Real inputs with the answer you expect.'],
  ['Feature', 'evals/triage/feature.py', 'The prompt and code under test.'],
  ['Graders', 'evals/triage/graders.py', 'Functions that score one answer from 0 to 1.'],
  ['Runner', 'evals/triage/run.py', 'Runs every case, averages, saves, compares.'],
]

const QUICKSTART = `git clone https://github.com/jars-demo/evals-demo.git
cd evals-demo/evals
uv sync
uv run python -m triage run`

export default function Home() {
  const minutes = CHAPTERS.reduce((sum, chapter) => sum + chapter.minutes, 0)

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-20 px-4 pt-16 pb-24 sm:pt-24">
      <section className="grid items-start gap-12 lg:grid-cols-[1.05fr_1fr]">
        <div className="flex min-w-0 flex-col gap-6">
          <p className="font-mono text-[12px] tracking-wider text-muted uppercase">
            AI engineering workshop · {CHAPTERS.length} chapters · {minutes} minutes
          </p>
          <h1 className="text-[2.75rem] leading-[1.05] font-semibold tracking-[-0.03em] text-balance sm:text-[3.5rem]">
            Evals, not vibes.
          </h1>
          <p className="max-w-xl text-[18px] leading-relaxed text-ink-2">
            You changed a prompt and the answers look better. Are they? Build a tiny eval harness
            for one LLM feature in plain Python, then compare prompts and models with numbers
            instead of opinions.
          </p>
          <ul className="flex flex-col gap-1.5 text-[15px] text-ink-2">
            <li>No dependencies: Python standard library only.</li>
            <li>No API key needed to start: an offline baseline runs right away.</li>
            <li>Any OpenAI-compatible model when you are ready: Groq, OpenAI or Ollama.</li>
            <li>A local Bring your provider page: check a provider and run the eval, no code.</li>
          </ul>
          <div className="flex flex-wrap gap-3 pt-2">
            <Link
              href="/workshop/01-why-evals"
              className="inline-flex h-11 items-center rounded-md bg-ink px-5 text-[15px] font-medium text-canvas hover:bg-ink-2"
            >
              Start the workshop
            </Link>
            <a
              href="https://github.com/jars-demo/evals-demo"
              className="inline-flex h-11 items-center rounded-md border border-line-strong px-5 text-[15px] font-medium hover:bg-surface"
            >
              View the code
            </a>
          </div>
        </div>

        <figure className="code min-w-0 overflow-hidden rounded-lg">
          <figcaption className="flex items-center justify-between border-b border-white/10 px-4 py-2.5 text-[12px] text-[#a3a3a0]">
            <span>uv run python -m triage run</span>
            <span>offline baseline</span>
          </figcaption>
          <div className="overflow-x-auto px-4 py-4 text-[12.5px] leading-[1.7]">
            {SCORECARD.map((row) => (
              <div key={row.id} className="whitespace-pre">
                <span className={row.mark === 'PASS' ? 'text-[#4ade80]' : 'text-[#f87171]'}>
                  {row.mark}
                </span>
                {'  '}
                {row.id.padEnd(24)}
                <span className="text-[#a3a3a0]">{row.answer}</span>
              </div>
            ))}
            <div className="text-[#a3a3a0]">...</div>
            <div className="mt-3 border-t border-white/10 pt-3">
              {SCORES.map(([name, value]) => (
                <div key={name} className="whitespace-pre">
                  {(name ?? '').padEnd(24)}
                  <span className={name === 'overall' ? 'font-medium text-white' : ''}>
                    {value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </figure>
      </section>

      <section aria-labelledby="anatomy" className="flex flex-col gap-6">
        <h2 id="anatomy" className="text-[1.6rem] font-semibold tracking-[-0.02em]">
          An eval has four parts
        </h2>
        <div className="grid border-t border-l border-line sm:grid-cols-2 lg:grid-cols-4">
          {PARTS.map(([name, file, about]) => (
            <div key={name} className="flex flex-col gap-2 border-r border-b border-line p-5">
              <span className="text-[15px] font-semibold">{name}</span>
              <code className="font-mono text-[12px] break-all text-accent">{file}</code>
              <span className="text-[14px] text-ink-2">{about}</span>
            </div>
          ))}
        </div>
      </section>

      <section aria-labelledby="chapters" className="grid gap-10 lg:grid-cols-[1fr_1.3fr]">
        <div className="flex flex-col gap-3">
          <h2 id="chapters" className="text-[1.6rem] font-semibold tracking-[-0.02em]">
            {CHAPTERS.length} short chapters
          </h2>
          <p className="text-[15px] leading-relaxed text-ink-2">
            Each one is a few minutes of reading, one thing to run, and an exercise. By the end you
            can put an eval in front of any AI feature you ship.
          </p>
        </div>
        <ol className="border-t border-line">
          {CHAPTERS.map((chapter) => (
            <li key={chapter.slug} className="border-b border-line">
              <Link
                href={`/workshop/${chapter.slug}`}
                className="flex items-baseline gap-4 py-3.5 hover:bg-surface"
              >
                <span className="w-7 shrink-0 font-mono text-[13px] text-muted">
                  {chapter.number}
                </span>
                <span className="min-w-0 flex-1 text-[15px] font-medium">{chapter.title}</span>
                <span className="shrink-0 font-mono text-[12px] text-muted">
                  {chapter.minutes} min
                </span>
              </Link>
            </li>
          ))}
        </ol>
      </section>

      <section aria-labelledby="start" className="flex flex-col gap-4">
        <h2 id="start" className="text-[1.6rem] font-semibold tracking-[-0.02em]">
          Run it in a minute
        </h2>
        <p className="text-[15px] text-ink-2">
          You need{' '}
          <a href="https://docs.astral.sh/uv/" className="text-accent underline underline-offset-4">
            uv
          </a>{' '}
          and git. uv installs Python for you.
        </p>
        <div className="code relative max-w-2xl overflow-x-auto rounded-lg px-4 pt-10 pb-4 text-[13px] leading-relaxed">
          <div className="absolute top-2 right-2">
            <CopyButton text={QUICKSTART} />
          </div>
          <pre>{QUICKSTART}</pre>
        </div>
      </section>
    </div>
  )
}
