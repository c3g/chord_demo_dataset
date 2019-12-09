#!/usr/bin/env python3

from datetime import date
from faker import Faker
import random
import json

fake = Faker()


SECONDS_IN_YEAR = 60 * 60 * 24 * 365


def main():
    # Each phenopacket corresponds to one patient encounter.

    phenopackets = []

    with open("./samples.tsv", "r") as sf:
        samples = [s.split("\t") for s in sf.readlines()]

    for s in samples:
        individual_id = f"ind:{s[0]}"
        individual_dob = fake.date_of_birth(minimum_age=20, maximum_age=100)
        individual_age = date.today() - individual_dob

        age_years = individual_age.total_seconds() // SECONDS_IN_YEAR  # Missing leap years; oh well
        age_string = f"P{int(age_years)}Y"

        ind_phenopacket = {
            "subject": {
                "id": individual_id,
                "date_of_birth": individual_dob.isoformat(),
                "sex": s[1],
                "karyotypic_sex": "XX" if s[1] == "FEMALE" else "XY",  # TODO: Spice it up a bit
                "taxonomy": {
                    "id": "NCBITaxon:9606",
                    "label": "Homo sapiens",
                },
            },
            "phenotypic_features": [],
            "diseases": [],
            "meta_data": {
                "created_by": "David Lougheed",
                "submitted_by": "Ksenia Zaytseva",
                "resources": [
                    {
                        "id": "ncbi_taxonomy",
                        "name": "NCBI Taxonomy OBO Edition",
                        "namespace_prefix": "NCBITaxon",
                        "url": "http://purl.obolibrary.org/obo/ncbitaxon.owl",
                        "version": "2018-07-27",
                        "iri_prefix": "http://purl.obolibrary.org/obo/NCBITaxon_"
                    }
                ],
                "updated": [],
                "external_references": []
            },
            "biosamples": [
                {
                    "id": s[0],  # TODO: Different biosample ID vs subject ID
                    "individual_id": individual_id,  # TODO: Do we need to provide this?
                    "description": f"Biosample for patient {s[0]}",
                    "sampled_tissue": {
                        "id": "UBERON_0000178",
                        "label": "blood"
                    },
                    "phenotypic_features": [],  # TODO
                    "individual_age_at_collection": age_string,  # TODO: Calculate from DOB
                    "histological_diagnosis": None,  # TODO
                    "tumor_progression": None,  # TODO
                    "diagnostic_markers": [],  # TODO
                    "procedure": {
                        "code": {
                            "id": "NCIT_C15189",
                            "label": "Biopsy"
                        }
                    },
                    "is_control_sample": False
                }
            ]
        }
        if individual_id.split(':')[1] in ['NA19648', 'NA19658', 'NA20509']:
            ind_phenopacket["diseases"] = {
                    "term": {
                        "id": "NCIT:C4872",
                        "label": "Breast Carcinoma"
                    },
                    "onset": {
                        "age": f"P{int(age_years - random.randrange(0, 5))}Y"
                    }
                }
        phenopackets.append(ind_phenopacket)
    with open('data.json', 'w') as output:
        json.dump(phenopackets, output, indent=4)
    print(json.dumps(phenopackets, indent=2))


if __name__ == "__main__":
    main()
