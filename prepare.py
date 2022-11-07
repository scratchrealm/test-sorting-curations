import spikeforest as sf
import spikeinterface as si
import sortingview.views as vv
from helpers.create_units_table import create_units_table
import os


def main():
    prepare_sorting(study_name='paired_boyden32c', recording_name='1103_1_1', sorter_name='SpykingCircus')

def prepare_sorting(*, study_name: str, recording_name: str, sorter_name: str):
    aa = f'{study_name}/{recording_name}/{sorter_name}'
    print(aa)
    print('Loading recording')
    R = sf.load_spikeforest_recording(study_name=study_name, recording_name=recording_name)
    recording = R.get_recording_extractor()
    print('Loading sorting')
    S = sf.load_spikeforest_sorting_output(study_name=study_name, recording_name=recording_name, sorter_name=sorter_name)
    sorting = S.get_sorting_extractor()
    print('Preparing figurl')
    dirname = f'spikeforest/{aa}'
    os.makedirs(dirname, exist_ok=True)
    curation_fname = f'{dirname}/curation.json'
    if not os.path.exists(curation_fname):
        with open(curation_fname, 'w') as f:
            f.write('{}') # empty curation
    curation_uri = f'gh://scratchrealm/test-sorting-curations/main/{dirname}/curation.json'
    url = prepare_figurl(recording=recording, sorting=sorting, label=aa, curation_uri=curation_uri)

    readme_text = f'''
# {aa}

[View]({url})

This file was automatically generated.
'''
    with open(f'{dirname}/README.md', 'w') as f:
        f.write(readme_text)

def prepare_figurl(*, recording: si.BaseRecording, sorting: si.BaseSorting, label: str, curation_uri: str):
    v = example_sorting_curation(sorting=sorting)
    return v.url(label=label, state={'sortingCuration': curation_uri})

def example_sorting_curation(*, sorting: si.BaseSorting):
    view_sc = vv.SortingCuration2()

    view_ut = create_units_table(sorting=sorting)

    view_ml = vv.MountainLayout(
        items=[
            vv.MountainLayoutItem(
                label='Units',
                view=view_ut
            ),
            vv.MountainLayoutItem(
                label='Curation',
                view=view_sc,
                is_control=True,
                control_height=600
            )
        ]
    )
    return view_ml

if __name__ == '__main__':
    main()