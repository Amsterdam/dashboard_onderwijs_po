from collections import defaultdict

from dataset.models import DataSummary
from dataset.models import Vestiging, CitoScores, LeerlingNaarGewicht
from dataset.models import SchoolAdvies, SchoolWisselaars, ToegewezenSubsidie

from dataset.models import LeerlingLeraarRatio


def create_summaries():
    """Create a summary for all vestigingen (what data is present)."""
    DataSummary.objects.all().delete()
    _create_with_brin6_data()
    _update_with_brin4_data()


def _create_with_brin6_data():
    summaries = defaultdict(dict)

    # assumption, these models have 'brin' and 'vestigingnummer' fields
    # and if they represent yearly measurements they have a 'jaar' field
    MODELS = [
        Vestiging,
        CitoScores,
        LeerlingNaarGewicht,
        SchoolAdvies,
        SchoolWisselaars,
        ToegewezenSubsidie
    ]

    for model in MODELS:
        is_yearly = hasattr(model, 'jaar')

        queryset = model.objects.all() \
            .filter(brin__isnull=False) \
            .filter(vestigingsnummer__isnull=False)

        objects = list(queryset)
        for obj in objects:
            _key = '{}{:02d}'.format(obj.brin, obj.vestigingsnummer)
            summary = summaries[_key][model.__name__] if model.__name__ in summaries[_key] else {}

            if is_yearly:
                entry = {obj.jaar: True}
            else:
                entry = {'present': True}
            summary.update(entry)

            summaries[_key][model.__name__] = summary

    instances = [DataSummary(row_key=k, columns=v) for k, v in summaries.items()]
    DataSummary.objects.bulk_create(instances)


def _update_with_brin4_data():
    # Some datasets are keyed by BRIN, not BRIN6 --- just repeat them as required.
    BRIN4_MODELS = [
        LeerlingLeraarRatio
    ]

    data_summaries = list(DataSummary.objects.all())
    for model in BRIN4_MODELS:
        is_yearly = hasattr(model, 'jaar')
        print('Our model, {}, is yearly {}'.format(
            model.__name__, is_yearly
        ))

        for data_summary in data_summaries:
            model_instances = list(
                model.objects.filter(brin__exact=data_summary.row_key[:4]))
            if not model_instances:
                continue

            s = data_summary.columns[model.__name__] \
                if model.__name__ in data_summary.columns \
                else {}

            for obj in model_instances:
                if is_yearly:
                    entry = {obj.jaar: True}
                else:
                    entry = {'present': True}
                s.update(entry)

            data_summary.columns[model.__name__] = s
            data_summary.save()
