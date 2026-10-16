"""Read-only checks for local Markdown links, report JSON and optional source hashes."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def anchors(text):
    result = set()
    seen = {}
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        slug = re.sub(r'[^\w\s-]', '', title.lower(), flags=re.UNICODE)
        slug = re.sub(r'\s', '-', slug)
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(slug + (f'-{count}' if count else ''))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-source-hashes', action='store_true',
                        help='Compare current hardware/production with the dated audit manifest.')
    args = parser.parse_args()
    problems = []
    count = 0
    for file in ROOT.rglob('*.md'):
        if '.git' in file.parts:
            continue
        body = file.read_text(encoding='utf-8-sig')
        for raw in re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', body):
            raw = raw.strip().strip('<>')
            url = urlsplit(raw)
            if url.scheme or url.netloc:
                continue
            count += 1
            target = (file.parent / unquote(url.path)).resolve() if url.path else file
            if not target.exists():
                problems.append(f'{file.relative_to(ROOT)}: missing {raw}')
            elif url.fragment and target.suffix == '.md':
                if unquote(url.fragment) not in anchors(target.read_text(encoding='utf-8-sig')):
                    problems.append(f'{file.relative_to(ROOT)}: missing anchor {raw}')
    reports = list((ROOT / 'docs/reports').rglob('*.json'))
    for report in reports:
        try:
            json.loads(report.read_text(encoding='utf-8'))
        except (ValueError, OSError) as exc:
            problems.append(f'{report.relative_to(ROOT)}: {exc}')
    if args.check_source_hashes:
        with (ROOT / 'docs/reports/source-manifest.csv').open(encoding='utf-8', newline='') as stream:
            for row in csv.DictReader(stream):
                file = ROOT / row['file']
                if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != row['sha256']:
                    problems.append(f"Dated source differs: {row['file']}")
    for problem in problems:
        print(problem)
    print(f'{count} local links, {len(reports)} JSON reports, {len(problems)} problems.')
    print('Documentation checks only; this does not validate electrical safety or operation.')
    return bool(problems)


if __name__ == '__main__':
    raise SystemExit(main())
