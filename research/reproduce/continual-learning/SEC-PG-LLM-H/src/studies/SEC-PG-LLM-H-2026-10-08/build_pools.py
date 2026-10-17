"""Builds pools.json, the candidate pools of unseen books for SEC-PG-LLM-H, from Project Gutenberg's metadata catalog only (pg_catalog.csv:
ebook number, type, title, language, authors, subjects, LoCC). No book text is read. Run once before the freeze:
  python3 build_pools.py <path to pg_catalog.csv>
Rule (fixed before any book was fetched):
  EN (domain A, old task): Type 'Text', Language exactly 'en', a LoCC class starting PR or PS, 'fiction' in Subjects (case-insensitive);
  FR (domain B, new task): Type 'Text', Language exactly 'fr', a LoCC class starting PQ, 'fiction' in Subjects;
  DE (domain B, new task): Type 'Text', Language exactly 'de', a LoCC class starting PT, 'fiction' in Subjects;
  in all three: no ebook already in DATA/SEEN.md, and no work by an author of a book in DATA/SEEN.md's Gutenberg rows
  (Austen, Melville, Hugo, Goethe, Darwin, Joyce, Dante, Mary Shelley, Conan Doyle, Dickens), which removes other editions,
  translations and excerpts of the seen texts."""
import csv, json, sys, hashlib, re, pathlib, os, datetime
HERE = pathlib.Path(__file__).resolve().parent; SEEN = HERE.parents[1] / 'DATA' / 'SEEN.md'
SEEN_AUTHORS = ['Austen, Jane', 'Melville, Herman', 'Hugo, Victor', 'Goethe, Johann Wolfgang von', 'Darwin, Charles', 'Joyce, James', 'Dante Alighieri', 'Shelley, Mary Wollstonecraft', 'Doyle, Arthur Conan', 'Dickens, Charles']
RULES = {'EN': ('en', ('PR', 'PS')), 'FR': ('fr', ('PQ',)), 'DE': ('de', ('PT',))}
def main(path):
    raw = open(path, 'rb').read(); rows = list(csv.DictReader(open(path, encoding='utf-8')))
    seen_ids = sorted({int(m) for m in re.findall(r'gutenberg/pg(\d+)\.txt', SEEN.read_text())})
    pools = {}
    for name, (lang, locc_pre) in RULES.items():
        ids = []
        for r in rows:
            if r['Type'] != 'Text' or r['Language'] != lang: continue
            locc = [x.strip() for x in r['LoCC'].split(';')]
            if not any(l.startswith(p) for l in locc for p in locc_pre): continue
            if 'fiction' not in r['Subjects'].lower(): continue
            if int(r['Text#']) in seen_ids or any(a in r['Authors'] for a in SEEN_AUTHORS): continue
            ids.append(int(r['Text#']))
        pools[name] = sorted(ids)
    meta = {r['Text#']: dict(title=r['Title'].replace('\n', ' ')[:120], authors=r['Authors'][:120], language=r['Language'], locc=r['LoCC']) for r in rows if int(r['Text#']) in {i for v in pools.values() for i in v}}
    out = dict(catalog_url='https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv', catalog_sha256=hashlib.sha256(raw).hexdigest(), catalog_rows=len(rows), catalog_fetched_utc=datetime.datetime.fromtimestamp(os.path.getmtime(path), datetime.timezone.utc).isoformat(timespec='seconds') + ' (modification time of the downloaded file)',
               rule=__doc__.split('Rule (fixed before any book was fetched):')[1].strip(), seen_ids_excluded=seen_ids, seen_authors_excluded=SEEN_AUTHORS,
               sizes={k: len(v) for k, v in pools.items()}, pools=pools, catalog_metadata=meta)
    json.dump(out, open(HERE / 'pools.json', 'w'), separators=(',', ':'), ensure_ascii=False); print(json.dumps(out['sizes']), out['catalog_sha256'])
if __name__ == '__main__': main(sys.argv[1])
