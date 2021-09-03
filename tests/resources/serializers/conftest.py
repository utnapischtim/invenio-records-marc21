# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""


import pytest


@pytest.fixture(scope="function")
def marc21_metadata():
    """Record UI metadata."""
    return {
        "json": {
            "leader": {
                "undefined": 0,
                "record_length": 0,
                "record_status": "new",
                "encoding_level": "not_applicable",
                "type_of_record": "language_material",
                "indicator_count": 2,
                "bibliographic_level": "monograph_item",
                "subfield_code_count": 2,
                "base_address_of_data": 0,
                "character_coding_scheme": "ucs_unicode",
                "descriptive_cataloging_form": "isbd_punctuation_omitteed",
                "multipart_resource_record_level": "set",
                "length_of_the_length_of_field_portion": 4,
                "length_of_the_implementation_defined_portion": 0,
                "length_of_the_starting_character_position_portion": 5,
            },
            "summary": [
                {
                    "summary": "A wonderful serenity has taken possession of my entire soul, like these sweet mornings of spring which I enjoy with my whole heart. I am alone, and feel the charm of existence in this spot, which was created for the bliss of souls like mine. I am so happy, my dear friend, so absorbed in the exquisite sense of mere tranquil existence, that I neglect my talents. I should be incapable of drawing a single stroke at the present moment; and yet I feel that I never was a greater artist than now. When, while the lovely valley teems with vapour around me, and the meridian sun strikes the upper surface of the impenetrable foliage of my trees, and but a few stray gleams steal into the inner sanctuary, I throw myself down among the tall grass by the trickling stream; and, as I lie close to the earth, a thousand unknown plants are noticed by me: when I hear the buzz of the little world among the stalks, and grow familiar with the countless indescribable forms of the insects and flies, then I feel the presence of the Almighty, who formed us in his own image, and the breath ",
                    "__order__": ["summary", "display_constant_controller"],
                    "display_constant_controller": "Summary",
                }
            ],
            "__order__": [
                "leader",
                "title_statement",
                "subject_added_entry_topical_term",
                "subject_added_entry_topical_term",
                "subject_added_entry_topical_term",
                "subject_added_entry_topical_term",
                "summary",
                "production_publication_distribution_manufacture_and_copyright_notice",
                "main_entry_personal_name",
            ],
            "title_statement": {
                "title": "Proceedings of the 3rd International Brain-Computer Interface Workshop and Training Course",
                "__order__": [
                    "title",
                    "remainder_of_title",
                    "statement_of_responsibility",
                    "title_added_entry",
                    "nonfiling_characters",
                ],
                "title_added_entry": "No added entry",
                "remainder_of_title": "Subtitle field.",
                "nonfiling_characters": "0",
                "statement_of_responsibility": "hrsg. von Josef Frank",
            },
            "main_entry_personal_name": {
                "__order__": ["affiliation", "type_of_personal_name_entry_element"],
                "affiliation": "Institute of Solid State Physics (5130)",
                "type_of_personal_name_entry_element": "Surname",
            },
            "subject_added_entry_topical_term": [
                {
                    "__order__": [
                        "miscellaneous_information",
                        "level_of_subject",
                        "thesaurus",
                    ],
                    "thesaurus": "Source not specified",
                    "level_of_subject": "No information provided",
                    "miscellaneous_information": ["Test"],
                },
                {
                    "__order__": [
                        "miscellaneous_information",
                        "level_of_subject",
                        "thesaurus",
                    ],
                    "thesaurus": "Source not specified",
                    "level_of_subject": "No information provided",
                    "miscellaneous_information": ["Invenio"],
                },
                {
                    "__order__": [
                        "miscellaneous_information",
                        "level_of_subject",
                        "thesaurus",
                    ],
                    "thesaurus": "Source not specified",
                    "level_of_subject": "No information provided",
                    "miscellaneous_information": ["TUGraz"],
                },
                {
                    "__order__": [
                        "topical_term_or_geographic_name_entry_element",
                        "level_of_subject",
                        "thesaurus",
                    ],
                    "thesaurus": "Source not specified",
                    "level_of_subject": "No information provided",
                    "topical_term_or_geographic_name_entry_element": "Marc21",
                },
            ],
            "production_publication_distribution_manufacture_and_copyright_notice": [
                {
                    "__order__": [
                        "place_of_production_publication_distribution_manufacture",
                        "name_of_producer_publisher_distributor_manufacturer",
                        "name_of_producer_publisher_distributor_manufacturer",
                        "name_of_producer_publisher_distributor_manufacturer",
                        "name_of_producer_publisher_distributor_manufacturer",
                        "date_of_production_publication_distribution_manufacture_or_copyright_notice",
                        "sequence_of_statements",
                    ],
                    "sequence_of_statements": "Not applicable/No information provided/Earliest",
                    "name_of_producer_publisher_distributor_manufacturer": [
                        "Hulk",
                        "Thor",
                        "Captain",
                        "Black Widow",
                    ],
                    "place_of_production_publication_distribution_manufacture": [
                        "Tu Graz"
                    ],
                    "date_of_production_publication_distribution_manufacture_or_copyright_notice": [
                        "2004"
                    ],
                }
            ],
        }
    }


@pytest.fixture(scope="function")
def full_record(marc21_record, marc21_metadata):
    """Full record as is expected by the UI serializer."""
    marc21_record
    marc21_record["id"] = "9jkx5-hx115"
    marc21_record["pid"] = {
        "pk": 58,
        "status": "R",
        "obj_type": "rec",
        "pid_type": "marcid",
    }

    marc21_record["files"] = {"enabled": True}
    marc21_record["access"] = {
        "files": "restricted",
        "embargo": {"until": None, "active": False, "reason": None},
        "metadata": "restricted",
        "status": "restricted",
    }
    marc21_record["metadata"] = marc21_metadata

    return marc21_record


@pytest.fixture(scope="function")
def list_records(full_record):
    """Fixture list of records."""
    list_records = {
        "hits": {"hits": [full_record, full_record]},
    }
    return list_records
