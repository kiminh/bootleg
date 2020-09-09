from collections import defaultdict
import numpy as np

from bootleg.symbols.constants import BASE_SLICE, FINAL_LOSS
from bootleg.utils import train_utils

# returns dictionary from alias index to the max number of candidates; we'll use this for padding later
def get_max_cands_per_alias(add_null_cand, aliases, entity_symbols):
    res = {}
    for idx in range(len(aliases)):
        alias = aliases[idx]
        res[str(idx)] = len(entity_symbols.get_qid_cands(alias)) + int(add_null_cand)
    return res

# Returns an index set into the candidates for an alias but does not include null candidates (equivalent to a filter that does
# not filter away any candidates). This is used for base head filters (i.e. a slice of everything)
def get_all_cands_filter_values(add_null_cand, aliases, entity_symbols):
    res = {}
    for idx in range(len(aliases)):
        alias = aliases[idx]
        no_filter = [i for i in range(len(entity_symbols.get_qid_cands(alias)) + int(add_null_cand))]
        res[str(idx)] = no_filter
    return res

def get_slice_values(slice_names, line):
    slices = {}
    if 'slices' in line:
        assert type(line['slices']) is dict
        aliases = line["aliases"]
        slices = line["slices"]
        # remove slices that we don't need
        for slice_name in list(slices.keys()):
            if slice_name not in slice_names:
                del slices[slice_name]
            else:
                assert len(slices[slice_name]) == len(aliases), 'Must have a prob label for each mention'
        # FINAL_LOSS and BASE_SLICE are in slice_names but are generated by us so we do not want them to be in slices
        assert FINAL_LOSS not in slices and BASE_SLICE not in slices, f"You can't have {BASE_SLICE} or {FINAL_LOSS} be slice names. You have {slices.keys()}. These are internally generated."
        for slice_name in slice_names:
            if slice_name in [FINAL_LOSS, BASE_SLICE]:
                continue
            if slice_name not in slices:
                slices[slice_name] = {str(i): 0.0 for i in range(len(aliases))}
    return slices