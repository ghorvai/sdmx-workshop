"""
Dataflow Module

This module provides the Dataflow class for extracting and managing information from an SDMX (Statistical Data and Metadata eXchange) dataflow.

The Dataflow class is implemented as a dataclass, providing a clean and efficient way to handle SDMX data structures. It fetches data from a given URL and parses the JSON response to extract relevant information about the dataflow.

Key Features:
- Fetches and parses SDMX dataflow information from a provided URL
- Extracts and organizes dimension names, codes, and their human-readable labels
- Handles time range constraints in the data
- Provides methods to populate all variables with a single call

Class Overview:
Dataflow:
    Attributes:
        url (str): The URL of the SDMX dataflow
        df_details_json (dict): Raw JSON data of the dataflow
        df_name (str): Name of the dataflow
        df_description (str): Description of the dataflow
        df_dimension_names (dict[str, str]): Mapping of dimension IDs to their names
        df_code_names (dict[str, dict[str, str]]): Nested dictionary of dimension codes and their labels

    Methods:
        populate_variables(): Fetches data and populates all class variables
        _get_df_details_json(): Fetches the raw JSON data from the URL
        _extract_dataflow_info(): Extracts basic dataflow information (name and description)
        _extract_dimension_names(): Extracts names of dimensions from the dataflow
        _extract_constrained_codes_and_names(): Extracts codes and their labels for each dimension
        _get_code_list_urns(): Retrieves URNs (Uniform Resource Names) for code lists
        _get_code_list_id_urns(): Retrieves ID URNs for code lists
        _parse_content_constraints(): Parses content constraints from the dataflow
        _get_year_range(): Extracts year range from a time period object

Usage:
    1. Create a Dataflow instance with the SDMX dataflow URL
    2. Call populate_variables() to fetch and process the data
    3. Access the extracted information through the instance attributes

Example:
    ```python
    dataflow = Dataflow("https://example.com/sdmx-dataflow")
    dataflow.populate_variables()
    print(dataflow.df_name)
    print(dataflow.df_dimension_names)
    ```

Dependencies:
    - requests: For making HTTP requests
    - dataclasses: For the @dataclass decorator
    - datetime: For parsing date information

Note:
    This implementation uses modern Python type hints and requires Python 3.7 or later for proper type checking.
    The use of the | operator for union types in type hints requires Python 3.10+ for runtime support,
    but will type-check correctly in Python 3.7+ with 'from __future__ import annotations'.

Author: Gergely HORVAI
Version: 1.0.0
Date: 2024-sep-29
"""

#from __future__ import annotations  # This allows us to use | for union types in Python 3.7+
from dataclasses import dataclass, field
from datetime import datetime
import requests

@dataclass
class Dataflow:
    """
    A dataclass to extract and manage information from an SDMX dataflow.
    """
    url: str
    df_details_json: dict = field(default_factory=dict)
    df_name: str = ""
    df_description: str = ""
    df_dimension_names: dict[str, str] = field(default_factory=dict)
    df_code_names: dict[str, dict[str, str]] = field(default_factory=dict)

    ACCEPT_HEADER = {'Accept': 'application/vnd.sdmx.structure+json;version=1.0;urn=true'}

    def populate_variables(self) -> None:
        """Populate all variables with data from the dataflow."""
        self._get_df_details_json()
        self._extract_dataflow_info()
        self._extract_dimension_names()
        self._extract_constrained_codes_and_names()

    def _get_df_details_json(self) -> None:
        """Fetch the dataflow details JSON from the URL."""
        response = requests.get(self.url, headers=self.ACCEPT_HEADER)
        response.raise_for_status()
        self.df_details_json = response.json()['data']

    def _extract_dataflow_info(self) -> None:
        """Extract basic dataflow information."""
        dataflow = self.df_details_json['dataflows'][0]
        self.df_name = dataflow['name']
        self.df_description = dataflow['description']

    def _extract_dimension_names(self) -> None:
        """Extract dimension names from the dataflow."""
        concepts = self.df_details_json['conceptSchemes'][0]['concepts']
        self.df_dimension_names = {item['id']: item['name'] for item in concepts}

    def _extract_constrained_codes_and_names(self) -> None:
        """Extract constrained codes and names from the dataflow."""
        code_list_urns = self._get_code_list_urns()
        code_list_id_urns = self._get_code_list_id_urns()
        attributes = self._parse_content_constraints()

        for dimension_code, codes in attributes.items():
            try:
                all_codes_and_names = dict(code_list_id_urns[code_list_urns[dimension_code]])
            except KeyError:
                all_codes_and_names = {code: 'No codelist found' for code in codes}
                print(f'No codelist found for {dimension_code}')
            
            self.df_code_names[dimension_code] = {
                code: all_codes_and_names.get(code, 'Unknown code')
                for code in codes
            }

    def _get_code_list_urns(self) -> dict[str, str]:
        """Get code list URNs from the dataflow."""
        dimensions = self.df_details_json['dataStructures'][0]['dataStructureComponents']['dimensionList']['dimensions']
        return {
            dim['id']: dim['localRepresentation']['enumeration']
            for dim in dimensions
        }

    def _get_code_list_id_urns(self) -> dict[str, list[tuple[str, str]]]:
        """Get code list ID URNs from the dataflow."""
        return {
            codelist['links'][0]['urn']: [(code['id'], code['name']) for code in codelist['codes']]
            for codelist in self.df_details_json['codelists']
        }

    def _parse_content_constraints(self) -> dict[str, list[str] | list[int]]:
        """Parse content constraints from the dataflow."""
        attributes = {}
        for item in self.df_details_json['contentConstraints'][0]['cubeRegions'][0]['keyValues']:
            attr_id = item['id']
            value_type = next(key for key in item.keys() if key not in ['id', 'type'])
            
            if value_type == 'values':
                attributes[attr_id] = item[value_type]
            elif value_type == 'timeRange':
                attributes[attr_id] = self._get_year_range(item[value_type])
            else:
                raise ValueError(f'Unknown value type: {value_type}')
        return attributes

    @staticmethod
    def _get_year_range(time_period_obj: dict[str, dict[str, str]]) -> list[int]:
        """Extract year range from a time period object."""
        start_year = datetime.fromisoformat(time_period_obj['startPeriod']['period']).year
        end_year = datetime.fromisoformat(time_period_obj['endPeriod']['period']).year
        return [start_year, end_year]