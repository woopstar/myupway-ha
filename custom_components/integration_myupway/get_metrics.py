import json
import os
import re
import argparse
import sys

import requests





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--system_id", type=int, help="The system/heat pump ID")
    args = parser.parse_args()

    system_id = args.system_id
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    session = requests.session()
    auth_response = session.post("https://myupway.com/LogIn", {
        "returnUrl": f"/System/{system_id}/Status/Overview",
        "Email": email,
        "Password": password
    })

    # The login endpoint doesn't use HTTP 4XX status codes, so we check that it
    # redirects to the "returnUrl" we requested
    redirect = auth_response.history.pop()
    if redirect.headers.get("Location") != f"/System/{system_id}/Status/Overview":
        raise Exception("Authentication failed")

    # Start fetching values, one "group" at a time
    for definition_group_name in definition_groups.keys():
        definition_group = definition_groups[definition_group_name]

        values_response = session.post("https://myupway.com/PrivateAPI/Values", {
            "hpid": system_id,
            "variables": get_definition_variables(definition_group)
        })

        values = values_response.json()

        # Augment the definition groups with the values received
        augmented_definition_group = augment_definition_values(definition_group, values)
        definition_groups[definition_group_name] = augmented_definition_group

    metrics = {
        "system_id": system_id,
        "metrics": definition_groups
    }
