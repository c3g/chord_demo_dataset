#!/usr/bin/env python3


def main():
    # Each phenopacket corresponds to one patient encounter.

    phenopackets = []

    with open("./samples.tsv", "r") as sf:
        samples = [s.split("\t") for s in sf.readlines()]

    for s in samples:
        phenopackets.append({
            "subject": {
                "id": s[0],
                "date_of_birth": "TODO",  # TODO
                "sex": s[1],
                "karyotypic_sex": "XX" if s[1] == "FEMALE" else "XY",  # TODO: Spice it up a bit
            },
            "phenotypic_features": [],
            "diseases": [],
            "meta_data": {
                "created_by": "David Lougheed",
                "submitted_by": "Ksenia Zaytseva",
                "resources": [],
                "updated": [],
                "external_references": []
            },
            "biosamples": [
                {
                    "id": s[0],  # TODO: Different biosample ID vs subject ID
                    "individual_id": s[0],
                    "description": f"Biosample for patient {s[0]}",
                    "sampled_tissue": {},  # TODO
                    "phenotypic_features": [],  # TODO
                    "individual_age_at_collection": "",  # TODO: Calculate from DOB
                    "histological_diagnosis": None,  # TODO
                    "tumor_progression": None,  # TODO
                    "diagnostic_markers": [],  # TODO
                    "procedure": None,  # TODO
                    "is_control_sample": False
                }
            ]
        })
