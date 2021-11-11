import os
import json
import requests
import responses
from demo.src.r_aiven_service import DemoAivenStorage


class TestAivenServices():

    def test_aiven_creds_exist(self):
        """Test the presence of Aiven's creds."""
        assert os.environ["AIVEN_API_URL"] is not None
        assert os.environ["AIVEN_TOKEN"] is not None

    def test_aiven_user_permissions(self):
        """Test the Aiven's user permissions."""
        response = requests.get(f'{os.environ["AIVEN_API_URL"]}/v1/me',
                                headers={
                                    "Authorization": f'aivenv1 {os.environ["AIVEN_TOKEN"]}'
                                },
                                verify=True
                                )
        assert response.status_code == 200
        result = json.loads(response.text)
        assert "operator" in [
            value for key, value
            in result["user"]["project_membership"].items()
        ]

    @responses.activate
    def test_unauthed_calls(self):
        """Test unauthorized API calls to return a 401 status."""
        expected_response = {"errors": [{
            "message": "No valid client certificate presented",
            "status": 401
        }],
            "message": "No valid client certificate presented"}
        responses.add(
            responses.GET,
            f'{os.environ["AIVEN_API_URL"]}/v1/me',
            json=expected_response,
            status=401
        )
        resp = requests.get(f'{os.environ["AIVEN_API_URL"]}/v1/me')

        assert resp.status_code == 401
        assert resp.json() == expected_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == f'{os.environ["AIVEN_API_URL"]}/v1/me'
        assert responses.calls[0].response.json() == expected_response

    @responses.activate
    def test_projects_endpoint(self):
        """Test the Aiven call to Projects"""
        with open('demo/tests/mock_results.json', 'r') as result_file:
            data = result_file.read()
        expected_response = json.loads(data)["test_project_calls"]

        responses.add(
            responses.GET,
            f'{os.environ["AIVEN_API_URL"]}/v1/project',
            json=expected_response,
            status=200
        )
        resp = requests.get(f'{os.environ["AIVEN_API_URL"]}/v1/project')

        assert resp.status_code == 200
        assert resp.json() == expected_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == f'{os.environ["AIVEN_API_URL"]}/v1/project'
        assert "MY-PROJECT-NAME" in responses.calls[0].response.text
        assert responses.calls[0].response.json() == expected_response

    @responses.activate
    def test_services_endpoint(self):
        """Test the Aiven Project call to Services"""
        with open('demo/tests/mock_results.json', 'r') as result_file:
            data = result_file.read()
        expected_response = json.loads(data)["test_service_calls"]

        responses.add(
            responses.GET,
            f'{os.environ["AIVEN_API_URL"]}/v1/project/MY-PROJECT-NAME/service',
            json=expected_response,
            status=200
        )
        resp = requests.get(
            f'{os.environ["AIVEN_API_URL"]}/v1/project/MY-PROJECT-NAME/service')

        assert resp.status_code == 200
        assert resp.json() == expected_response
        assert len(responses.calls) == 1
        expected_url = f'{os.environ["AIVEN_API_URL"]}/v1/project/MY-PROJECT-NAME/service'
        assert responses.calls[0].request.url == expected_url
        assert "MY-SERVICE-NAME" in responses.calls[0].response.text
        assert responses.calls[0].response.json() == expected_response

    # def test_db_uri_params(self):
    # (todo) similar testing could be included for validating behavior

    def test_demo_project_call(self):
        """Test the API call's logic made to Aiven's Projects."""
        resp = DemoAivenStorage(os.environ["AIVEN_API_URL"],
                                os.environ["AIVEN_TOKEN"]).get_project_names()
        assert isinstance(resp, list)
        assert len(resp) == 1
        assert 'romainducarrouge-31f2' in resp

    def test_demo_service_call(self):
        """Test the API call's logic made to Aiven's Services."""
        project_name = 'romainducarrouge-31f2'
        resp = DemoAivenStorage(os.environ["AIVEN_API_URL"],
                                os.environ["AIVEN_TOKEN"]).get_services(project_name)
        assert isinstance(resp, list)
        assert len(resp) == 1
        assert 'pg-216f7124' in resp
