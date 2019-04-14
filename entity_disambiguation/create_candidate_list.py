# -*- coding: utf-8 -*-

import click
from wikipedia2vec.dump_db import DumpDB

from entity_disambiguation.ed_dataset import EntityDisambiguationDataset


@click.command()
@click.argument('dump_db_file', type=click.Path(exists=True))
@click.argument('out_file', type=click.File('w'))
@click.option('--data-dir', type=click.Path(exists=True), default='data/entity-disambiguation')
@click.option('--max-candidate-size', default=None, type=int)
def main(dump_db_file, out_file, data_dir, max_candidate_size):
    dump_db = DumpDB(dump_db_file)

    titles = set()
    valid_titles = frozenset(dump_db.titles())

    reader = EntityDisambiguationDataset(data_dir)
    for documents in reader.get_all_datasets():
        for document in documents:
            for mention in document.mentions:
                candidates = mention.candidates
                if max_candidate_size:
                    candidates = sorted(mention.candidates, key=lambda c: c.prior_prob,
                                        reverse=True)[:max_candidate_size]
                for candidate in candidates:
                    title = dump_db.resolve_redirect(candidate.title)
                    if title in valid_titles:
                        titles.add(title)

    for title in titles:
        out_file.write(title + '\n')


if __name__ == '__main__':
    main()