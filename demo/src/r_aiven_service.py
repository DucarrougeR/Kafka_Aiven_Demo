import os
import requests
import json
import psycopg2

from loguru import logger
from typing import List, Dict


class DemoAivenStorage():
    """Validates our Aiven infrastructure.

    Attributes:
      api_url: The base URL for Aiven's API.
      token: The authentication token for API calls.
    """
    # Auth format: aivenv1 <TOKEN>

    def __init__(self, api_url: str, token: str) -> None:
        self.api_url = api_url
        self.token = token

    def get_project_names(self) -> List[str]:
        """Return the list of all Aiven Project names.

        Returns:
          List of all project_names from API reponse.
        """
        api_route = f"{self.api_url}/v1/project"
        response = requests.get(api_route,
                                headers={
                                    "Authorization": f"aivenv1 {self.token}"
                                },
                                verify=True
                                )
        if response.status_code == 200:
            all_projects = json.loads(response.text)

            logger.info("Retrieved the list of Aiven Projects.")
            return [all_projects["projects"][i]["project_name"]
                    for i in range(0, len(all_projects["projects"]))
                    ]

        logger.error(f"Error with request, yielding {response.status_code}")

    def get_services(self, project_name: str) -> List[str]:
        """Return the list of Aiven Service names for the project.

        Args:
          project_name: Aiven Project name to search.

        Returns:
          List of all service_names from API reponse.
        """
        api_route = f"{self.api_url}/v1/project/{project_name}/service"

        response = requests.get(api_route,
                                headers={
                                    "Authorization": f"aivenv1 {self.token}"
                                },
                                verify=True
                                )
        if response.status_code == 200:
            all_services = json.loads(response.text)
            logger.info(
                f"Retrieved the list of Services for Project {project_name}.")

            return [all_services["services"][i]["service_name"]
                    for i in range(0, len(all_services["services"]))
                    ]

        logger.error(f"Error with request, yielding {response.status_code}")

    def get_db_uri_params(self, service_name
                          ) -> Dict[str, str]:
        """Return the parameters for the destination database.

        Args:
          service_name: Aiven Service name to process.
        """
        project = "romainducarrouge-31f2"  # hardcoded for demo
        api_route = f"{self.api_url}/v1/project/{project}/service/{service_name}"

        response = requests.get(api_route,
                                headers={
                                    "Authorization": f"aivenv1 {self.token}"
                                },
                                verify=True
                                )
        if response.status_code == 200:
            db_details = json.loads(response.text)
            logger.info(
                f"Retrieved the list of PosgreSQL Services for the demo.")
            # could also use the entire URI string availble at:
            # db_details["service"]["service_uri_params"]["pg"]
            uriParams = {
                "host": db_details["service"]["service_uri_params"]["host"],
                "dbname": db_details["service"]["service_uri_params"]["dbname"],
                "password": db_details["service"]["service_uri_params"]["password"],
                "port": db_details["service"]["service_uri_params"]["port"],
                "ssl": db_details["service"]["service_uri_params"]["sslmode"],
                "user": db_details["service"]["service_uri_params"]["user"]
            }
            return uriParams

        logger.error(f"Error with request, yielding {response.status_code}")
