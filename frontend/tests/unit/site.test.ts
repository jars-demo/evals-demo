import fs from 'node:fs'
import path from 'node:path'

import { describe, expect, it } from 'vitest'

import { CHAPTERS, findChapter } from '@/lib/workshop'

const ROOT = path.join(process.cwd(), '..')

describe('chapters', () => {
  it('has seven chapters numbered in order', () => {
    expect(CHAPTERS.map((chapter) => chapter.number)).toEqual([
      '01',
      '02',
      '03',
      '04',
      '05',
      '06',
      '07',
    ])
  })

  it.each(CHAPTERS.map((chapter) => [chapter.slug, chapter] as const))(
    '%s has a summary, a time and the standard sections',
    (_slug, chapter) => {
      expect(chapter.summary.length).toBeGreaterThan(10)
      expect(chapter.minutes).toBeGreaterThan(0)
      expect(chapter.body).toMatch(/^## Goal$/m)
      expect(chapter.body).toMatch(/^## Check it works$/m)
      expect(chapter.body).toMatch(/^## Exercise$/m)
    },
  )

  it('only mentions files that exist', () => {
    const mentioned = new Set(
      CHAPTERS.flatMap((chapter) =>
        [...chapter.body.matchAll(/`((?:evals|\.github)\/[\w./-]+\.\w+)`/g)].map((m) => m[1] ?? ''),
      ),
    )
    expect(mentioned.size).toBeGreaterThan(4)
    for (const file of mentioned) {
      expect(fs.existsSync(path.join(ROOT, file)), `${file} is missing`).toBe(true)
    }
  })

  it('quotes the prompt exactly as it is in the code', () => {
    const feature = fs.readFileSync(path.join(ROOT, 'evals/triage/feature.py'), 'utf8')
    const prompt = /PROMPT = f"""[\s\S]*?"""/.exec(feature)?.[0]

    expect(prompt).toBeDefined()
    expect(findChapter('05-real-model')?.body).toContain(prompt)
  })
})
