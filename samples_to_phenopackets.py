#!/usr/bin/env python3

import json
import random

from datetime import date
from faker import Faker

from divide_samples import datasets

fake = Faker()

fake.seed(108643)
random.seed(19618)

SECONDS_IN_YEAR = 60 * 60 * 24 * 365


def main():
    # Each phenopacket corresponds to one patient encounter.

    dataset_phenopackets = ([], [], [])

    with open("./samples.tsv", "r") as sf:
        sample_sexes = {s.split("\t")[0]: s.split("\t")[1].strip() for s in sf.readlines()}

    for dataset_samples, phenopackets in zip(datasets, dataset_phenopackets):
        for s in dataset_samples:
            individual_id = f"ind:{s}"
            individual_dob = fake.date_of_birth(minimum_age=20, maximum_age=100)
            individual_age = date.today() - individual_dob

            age_years = individual_age.total_seconds() // SECONDS_IN_YEAR  # Missing leap years; oh well
            age_string = f"P{int(age_years)}Y"

            ind_phenopacket = {
                "subject": {
                    "id": individual_id,
                    "date_of_birth": individual_dob.isoformat(),
                    "sex": sample_sexes[s],
                    "karyotypic_sex": "XX" if sample_sexes[s] == "FEMALE" else "XY",  # TODO: Spice it up a bit
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
                        },
                        {
                            "id": "uberon",
                            "name": "Uber-anatomy ontology",
                            "namespace_prefix": "UBERON",
                            "url": "http://purl.obolibrary.org/obo/uberon.owl",
                            "version": "2019-06-27",
                            "iri_prefix": "http://purl.obolibrary.org/obo/UBERON"
                        },
                        {
                            "id": "nci_thesaurus",
                            "name": "NCI Thesaurus",
                            "namespace_prefix": "NCIT",
                            "url": "https://ncit.nci.nih.gov",
                            "version": "2015-09-01",
                            "iri_prefix": "https://ncit.nci.nih.gov"
                        }
                    ],
                    "updates": [],
                    "external_references": []
                },
                "biosamples": [
                    {
                        "id": s,  # TODO: Different biosample ID vs subject ID
                        "individual_id": individual_id,  # TODO: Do we need to provide this?
                        "description": f"Biosample for patient {s}",
                        "sampled_tissue": {
                            "id": "UBERON_0000178",
                            "label": "blood"
                        },
                        "phenotypic_features": [],  # TODO
                        "individual_age_at_collection": {
                            "age": age_string
                        },  # TODO: Calculate from DOB
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

            if s == "NA19648":
                ind_phenopacket["diseases"] = [
                    {
                        "term": {
                            "id": "NCIT:C4872",
                            "label": "Breast Carcinoma"
                        },
                        "onset": {
                            "age": f"P{int(age_years - random.randrange(0, 5))}Y"
                        }
                    }
                ]
                phenotypic_feature = {
                    "type": {
                        "id": "HP:0012219",
                        "label": "Erythema nodosum"
                    },
                    "severity": {
                        "id": "HP: 0012825",
                        "label": "Mild"
                    },
                    "onset": {
                        "id": "HP:0003577",
                        "label": "Congenital onset"
                    },
                    "evidence": {
                        "reference": {
                            "id": "PMID:30962759",
                            "description": "Recurrent Erythema Nodosum in a Child with a SHOC2 Gene Mutation"
                        },
                        "evidence_code": {
                            "id": "ECO:0006017",
                            "label": "author statement from published clinical study used in manual assertion"
                        }
                    },
                    "negated": True,
                    "modifier": [
                        {
                            "id": "HP: 0012825 ",
                            "label": "Mild"
                        },
                        {
                            "id": "HP: 0012823 ",
                            "label": "Semi-mild"
                        }
                    ],
                }
                ind_phenopacket["biosamples"][0]["phenotypic_features"].append(phenotypic_feature)
                ind_phenopacket["genes"] = [
                    {
                        "id": "HGNC:2621",
                        "symbol": "CYP2C19"
                    }
                ]
                ind_phenopacket["variants"] = [
                    {
                        "id": 1,
                        "zygosity": {
                            "id": "GENO:0000135",
                            "label": "heterozygous"
                        },
                        "allele_type": "spdiAllele",
                        "allele": {
                            "id": "clinvar:13294",
                            "seq_id": "NC_000010.10",
                            "position": 123256214,
                            "deleted_sequence": "T",
                            "inserted_sequence": "G"
                        }
                    }
                ]
                ind_phenopacket["hts_files"] = [
                    {
                        "uri": "https://data.example/genomes/germline_wgs.vcf.gz",
                        "description": "Matched normal germline sample",
                        "hts_format": "VCF",
                        "genome_assembly": "GRCh38",
                        "individual_to_sample_identifiers": {
                            "patient:1": "NA12345"
                        }
                    },
                    {
                        "uri": "https://data.example/genomes/test2",
                        "description": "Matched normal germline sample",
                        "hts_format": "VCF",
                        "genome_assembly": "GRCh38",
                        "individual_to_sample_identifiers": {
                            "NA19648": "NA19648"
                        }
                    }
                ]

            phenopackets.append(ind_phenopacket)

    for di, p in enumerate(dataset_phenopackets):
        with open(f"dataset_{di}.json", "w") as output:
            json.dump(p, output, indent=4)


if __name__ == "__main__":
    main()
