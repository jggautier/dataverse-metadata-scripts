# Replace dataset metadata in given datasets
import csv
from csv import DictReader
import requests

server = 'https://demo.dataverse.org'  # Enter name of server url, which is home page URL of the Dataverse installation, e.g. https://demo.dataverse.org
apikey = ''  # Enter API token of Dataverse account that has edit privileges on the datasets

# metadatafile = ''  # Path to JSON file that contains the replacement metadata
datasetPIDs = ''  # Path to CSV file with list of dataset PIDs

reader = csv.reader(open(datasetPIDs))
total = len(list(reader)) - 1

count = 0
with open(datasetPIDs, mode='r', encoding='utf-8') as f:
    csv_dict_reader = DictReader(f, delimiter=',')
    for row in csv_dict_reader:
        title = 'Executives Agreements Database, %s' % (row['title'].rstrip())
        description = '%s\n\ncover memo' % (row['dsDescriptionValue'].rstrip())
        metadataValues = {
            "fields": [
                {
                    "typeName": "title",
                    "value": title
                },
                {
                    "typeName": "author",
                    "value": [
                        {
                            "authorName": {
                                "typeName": "authorName",
                                "value": "Oona A. Hathaway"
                            },
                            "authorAffiliation": {
                                "typeName": "authorAffiliation",
                                "value": "Yale Law School"
                            }
                        },
                        {
                            "authorName": {
                                "typeName": "authorName",
                                "value": "Curtis A. Bradley"
                            },
                            "authorAffiliation": {
                                "typeName": "authorAffiliation",
                                "value": "Duke Law School"
                            }
                        },
                        {
                            "authorName": {
                                "typeName": "authorName",
                                "value": "Jack Goldsmith"
                            },
                            "authorAffiliation": {
                                "typeName": "authorAffiliation",
                                "value": "Harvard Law School"
                            }
                        },
                    ]
                },
                {
                    "typeName": "dsDescription",
                    "value": [
                        {
                            "dsDescriptionValue": {
                                "typeName": "dsDescriptionValue",
                                "value": description
                            }
                        }

                    ]
                }
            ]
        }

        datasetPID = row['persistent_id'].rstrip()
        url = '%s/api/datasets/:persistentId/editMetadata' % (server)
        params = {'persistentId': datasetPID, 'replace': 'true'}
        r = requests.put(
            url,
            # data=open(metadatafile, 'rb'),
            json=metadataValues,
            params=params,
            headers={
                'X-Dataverse-key': apikey,
                'content-type': 'application/json'
            })
        count += 1

        if r.status_code == 200:
            print('Success! %s - %s of %s' % (datasetPID, count, total))
        else:
            print('Failed (%s): %s! %s of %s' % (r.status_code, datasetPID, count, total))
