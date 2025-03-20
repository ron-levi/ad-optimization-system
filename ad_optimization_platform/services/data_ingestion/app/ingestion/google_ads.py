from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import logging
from typing import List, Dict, Any, Optional

class GoogleAdsClientWrapper:
    def __init__(self, config_path: Optional[str] = None):
        """
        Initializes the Google Ads Client.

        Args:
            config_path (Optional[str]): Path to the Google Ads YAML credentials file.
        """
        service_root = Path(__file__).parent
        yaml_path = config_path or (service_root / "google-ads.yaml")
        self.client = GoogleAdsClient.load_from_storage(str(yaml_path))
        self.logger = logging.getLogger(__name__)

    def execute_query(self, customer_id: str, query: str) -> List[Dict[str, Any]]:
        """
        Executes a Google Ads Query Language (GAQL) query.

        Args:
            customer_id (str): Google Ads Customer ID.
            query (str): GAQL query string.

        Returns:
            List[Dict[str, Any]]: A list of results from the query.
        """
        try:
            service = self.client.get_service("GoogleAdsService")
            response = service.search(customer_id=customer_id, query=query)

            results = []
            for row in response:
                results.append(self._parse_proto_message(row))

            return results
        except GoogleAdsException as ex:
            self._handle_google_ads_exception(ex)

    def create_entity(self, customer_id: str, entity_type: str, operations: List[Dict[str, Any]]) -> List[str]:
        """
        Creates a new entity in Google Ads.

        Args:
            customer_id (str): Google Ads Customer ID.
            entity_type (str): The entity type (e.g., 'campaign', 'ad_group').
            operations (List[Dict[str, Any]]): List of operations containing entity data.

        Returns:
            List[str]: A list of created resource names.
        """
        try:
            service = self.client.get_service(f"{entity_type.capitalize()}Service")
            mutate_method = getattr(service, "mutate_" + entity_type + "s")

            response = mutate_method(customer_id=customer_id, operations=operations)

            return [result.resource_name for result in response.results]
        except GoogleAdsException as ex:
            self._handle_google_ads_exception(ex)

    def update_entity(self, customer_id: str, entity_type: str, operations: List[Dict[str, Any]]) -> List[str]:
        """
        Updates an existing entity in Google Ads.

        Args:
            customer_id (str): Google Ads Customer ID.
            entity_type (str): The entity type (e.g., 'campaign', 'ad_group').
            operations (List[Dict[str, Any]]): List of update operations.

        Returns:
            List[str]: A list of updated resource names.
        """
        return self.create_entity(customer_id, entity_type, operations)

    def delete_entity(self, customer_id: str, entity_type: str, resource_names: List[str]) -> List[str]:
        """
        Deletes an entity from Google Ads.

        Args:
            customer_id (str): Google Ads Customer ID.
            entity_type (str): The entity type (e.g., 'campaign', 'ad_group').
            resource_names (List[str]): List of entity resource names to delete.

        Returns:
            List[str]: A list of deleted resource names.
        """
        operations = [{"remove": name} for name in resource_names]
        return self.create_entity(customer_id, entity_type, operations)

    def get_metadata(self, entity_name: str) -> Dict[str, Any]:
        """
        Retrieves metadata about a specific entity type.

        Args:
            entity_name (str): The entity name (e.g., 'campaign', 'ad_group').

        Returns:
            Dict[str, Any]: Metadata about the entity.
        """
        try:
            service = self.client.get_service("GoogleAdsFieldService")
            query = f"SELECT name, category, selectable, filterable, sortable FROM google_ads_field WHERE name = '{entity_name}'"
            return self.execute_query("1234567890", query)  # Dummy customer ID for metadata lookup
        except GoogleAdsException as ex:
            self._handle_google_ads_exception(ex)

    def get_available_fields(self, entity_name: str) -> List[str]:
        """
        Retrieves available fields for an entity.

        Args:
            entity_name (str): The entity name (e.g., 'campaign', 'ad_group').

        Returns:
            List[str]: A list of field names available in the entity.
        """
        try:
            query = f"SELECT name FROM google_ads_field WHERE category = 'RESOURCE' AND name LIKE '{entity_name}_%'"
            fields = self.execute_query("1234567890", query)  # Dummy customer ID
            return [field["name"] for field in fields]
        except GoogleAdsException as ex:
            self._handle_google_ads_exception(ex)

    def _parse_proto_message(self, message):
        """
        Converts a protobuf message to a dictionary.

        Args:
            message: A protobuf message.

        Returns:
            Dict[str, Any]: A dictionary representation of the message.
        """
        return {field.name: getattr(message, field.name) for field in message.DESCRIPTOR.fields}

    def _handle_google_ads_exception(self, ex: GoogleAdsException):
        """
        Handles Google Ads API exceptions.

        Args:
            ex (GoogleAdsException): The exception instance.
        """
        self.logger.error(
            f"Request ID: {ex.request_id} failed with status {ex.error.code().name} and errors: {ex.failure.errors}"
        )
        for error in ex.failure.errors:
            self.logger.error(f"\tError: {error.message} (Code: {error.error_code.name})")
        raise ex