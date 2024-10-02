import argparse
import pandas as pd
import shutil
from collections import defaultdict
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description='Make 5 fold datasets for ultralytics')
    parser.add_argument('data_dirpath', type=Path, help='data directory')
    parser.add_argument('fold_info_filepath', type=Path, help='data directory')
    parser.add_argument('output_dirpath', type=Path, help='output directory')
    parser.add_argument('--keep_augs', action='store_true', help='if True, keep augmented images, else only keep original images')
    return parser.parse_args()


def replace_ith_part(path, i, new_part):
    return Path().joinpath(*path.parts[:i]) / new_part / Path().joinpath(*path.parts[i+1:])


def copy_to_fold(filepath, root_dirpath, output_dirpath, fold_index, split):
    relative_filepath = filepath.relative_to(root_dirpath)
    relative_filepath = replace_ith_part(relative_filepath, -2, split)
    new_filepath = output_dirpath / f'fold_{fold_index}' / relative_filepath
    new_filepath.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(filepath, new_filepath)


def read_metadata(data_dirpath):
    metadata = []
    for filepath in data_dirpath.glob('**/images/**/*.*'):
        split = filepath.parent.name
        id_ = filepath.stem
        label_filepath = replace_ith_part(filepath, -3, 'labels').with_suffix('.txt')
        if id_[-1] in {'v', 'd', 'h'}:
            id_ = id_[:-1]

        label_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        label_filepath = (filepath.parents[2] / 'labels' / split / filepath.stem).with_suffix('.txt')
        if label_filepath.exists():
            labels = pd.read_csv(label_filepath, sep=' ', header=None, names=['class', 'x', 'y', 'w', 'h'])
            label_counts = label_counts | labels['class'].value_counts().to_dict()

        metadata.append(
            {
                'image_filepath': filepath,
                'label_filepath': label_filepath,
                'name': filepath.stem,
                'id': id_,
                'split': split,
            } | label_counts
        )
    df = pd.DataFrame(metadata)
    return df


def main(args):
    # Read fold info
    df_fold_info = pd.read_csv(args.fold_info_filepath)

    # Read filepaths
    df_metadata = read_metadata(args.data_dirpath)
    df_metadata = df_metadata[df_metadata['split'].isin({'train', 'val'})]  # No labels for test, so skip it
    assert len(df_metadata) == 1600

    if not args.keep_augs:
        df_metadata = df_metadata[df_metadata['name'] == df_metadata['id']]
        assert len(df_metadata) == 400

    # Save data for each fold
    for fold_index in range(5):
        # Get train and val data
        df_train = df_fold_info[df_fold_info['fold'] != fold_index]
        df_val = df_fold_info[df_fold_info['fold'] == fold_index]
        assert len(df_train) == df_train['id'].nunique()
        assert len(df_val) == df_val['id'].nunique()

        # Save train and val data
        for _, row in df_metadata[df_metadata['id'].isin(df_train['id'])].iterrows():
            copy_to_fold(row['image_filepath'], args.data_dirpath, args.output_dirpath, fold_index, split='train')
            copy_to_fold(row['label_filepath'], args.data_dirpath, args.output_dirpath, fold_index, split='train')
        for _, row in df_metadata[df_metadata['id'].isin(df_val['id'])].iterrows():
            copy_to_fold(row['image_filepath'], args.data_dirpath, args.output_dirpath, fold_index, split='val')
            copy_to_fold(row['label_filepath'], args.data_dirpath, args.output_dirpath, fold_index, split='val')

    # Check integrity
    # - sum number of images and labels in each fold split is expected
    # - ids of train and val do not overlap
    # - ids of vals for different folds do not overlap and sum up to all ids
    val_ids = dict()
    for fold_index in range(5):
        n_images, n_labels = 0, 0
        image_names, image_ids = defaultdict(list), defaultdict(list)
        label_names, label_ids = defaultdict(list), defaultdict(list)
        for split in ['train', 'val']:
            for filepath in args.output_dirpath.glob(f'fold_{fold_index}/images/{split}/*.*'):
                assert filepath.exists(), filepath
                n_images += 1
                name = filepath.stem
                id_ = name
                if id_[-1] in {'v', 'd', 'h'}:
                    id_ = id_
                image_names[split].append(name)
                image_ids[split].append(id_)
            for filepath in args.output_dirpath.glob(f'fold_{fold_index}/labels/{split}/*.*'):
                assert filepath.exists(), filepath
                n_labels += 1
                name = filepath.stem
                id_ = name
                if id_[-1] in {'v', 'd', 'h'}:
                    id_ = id_
                label_names[split].append(name)
                label_ids[split].append(id_)

        assert sorted(list(set(image_names['train']))) == sorted(list(set(label_names['train'])))
        assert sorted(list(set(image_names['val']))) == sorted(list(set(label_names['val'])))
        assert len(set(image_ids['train']).intersection(set(image_ids['val']))) == 0
        assert len(set(label_ids['train']).intersection(set(label_ids['val']))) == 0

        val_ids[fold_index] = image_ids['val']

        assert n_images == n_labels == len(df_metadata)
    
    for i in range(5):
        for j in range(5):
            if i == j:
                continue
            assert len(set(val_ids[i]).intersection(set(val_ids[j]))) == 0

    # Print stats
    for fold_index in range(5):
        df_metadata = read_metadata(args.output_dirpath / f'fold_{fold_index}')
        print(f'Fold {fold_index}')
        print(f'\tNumber of images: {len(df_metadata)}, train: {len(df_metadata[df_metadata["split"] == "train"])}, val: {len(df_metadata[df_metadata["split"] == "val"])}')
        print(f'\tTrain classes counts: {df_metadata[df_metadata["split"] == "train"][[0, 1, 2, 3, 4]].sum().to_dict()}')
        print(f'\tVal classes counts{df_metadata[df_metadata["split"] == "val"][[0, 1, 2, 3, 4]].sum().to_dict()}')
        

if __name__ == '__main__':
    args = parse_args()
    main(args)
