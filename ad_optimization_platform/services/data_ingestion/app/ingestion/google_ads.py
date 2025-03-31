from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.protobuf.message import Message
import logging
from typing import List, Dict, Any, Optional, Union

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

    def execute_query(self, customer_id: str, query: str,
                      return_total_results_count: bool = True) -> List[Dict[str, Any]]:
        """
        Executes a Google Ads Query Language (GAQL) query.

        Args:
            customer_id (str): Google Ads Customer ID.
            query (str): GAQL query string.

        Returns:
            List[Dict[str, Any]]: A list of results from the query.
        """
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            request = self.client.get_type("SearchGoogleAdsRequest")
            request.customer_id = customer_id
            request.search_settings.return_total_results_count = return_total_results_count
            request.query = query
            stream = ga_service.search_stream(request=request)

            results = []
            for batch in stream:
                for row in batch.results:
                    results.append(self._parse_proto_message(row))

            return results
        except GoogleAdsException as ex:
            self._handle_google_ads_exception(ex, query=query)

    def perform_operation(self, customer_id: str, entity_type: str, operation_type: str,
                          operations: List[Dict[str, Any]]) -> List[str]:
        """
        Performs a generic operation (create, update, delete) on a Google Ads entity.

        Args:
            customer_id (str): Google Ads Customer ID.
            entity_type (str): The entity type (e.g., 'campaign', 'ad_group').
            operation_type (str): The operation type ('create', 'update', 'delete').
            operations (List[Dict[str, Any]]): List of operations containing entity data.

        Returns:
            List[str]: A list of resource names affected by the operation.
        """
        try:
            service_name = f"{entity_type.capitalize()}Service"
            service = self.client.get_service(service_name)
            mutate_method_name = f"mutate_{entity_type}s"
            mutate_method = getattr(service, mutate_method_name)

            if operation_type == "delete":
                operations = [{"remove": op} for op in operations]

            response = mutate_method(customer_id=customer_id, operations=operations)
            return [result.resource_name for result in response.results]
        except GoogleAdsException as ex:
            self._handle_google_ads_exception(ex, operation_type=operation_type, entity_type=entity_type)

    def get_metadata(self, entity_name: str, customer_id: Optional[str] = "1234567890") -> Dict[str, Any]:
        """
        Retrieves metadata about a specific entity type.

        Args:
            entity_name (str): The entity name (e.g., 'campaign', 'ad_group').
            customer_id (Optional[str]): Google Ads Customer ID for metadata lookup.

        Returns:
            Dict[str, Any]: Metadata about the entity.
        """
        query = f"SELECT name, category, selectable, filterable, sortable FROM google_ads_field WHERE name = '{entity_name}'"
        return self.execute_query(customer_id, query)

    def get_available_fields(self, entity_name: str, customer_id: Optional[str] = "1234567890") -> List[str]:
        """
        Retrieves available fields for an entity.

        Args:
            entity_name (str): The entity name (e.g., 'campaign', 'ad_group').
            customer_id (Optional[str]): Google Ads Customer ID for field lookup.

        Returns:
            List[str]: A list of field names available in the entity.
        """
        query = f"SELECT name FROM google_ads_field WHERE category = 'RESOURCE' AND name LIKE '{entity_name}_%'"
        fields = self.execute_query(customer_id, query)
        return [field["name"] for field in fields]

    def _parse_proto_message(self, message: Message) -> Dict[str, Any]:
        """
        Converts a protobuf message to a dictionary.

        Args:
            message (Message): A protobuf message.

        Returns:
            Dict[str, Any]: A dictionary representation of the message.
        """
        return {field.name: getattr(message, field.name) for field in message.DESCRIPTOR.fields}

    def _handle_google_ads_exception(self, ex: GoogleAdsException, **context):
        """
        Handles Google Ads API exceptions.

        Args:
            ex (GoogleAdsException): The exception instance.
            context (dict): Additional context about the operation.
        """
        self.logger.error(
            f"Request ID: {ex.request_id} failed with status {ex.error.code().name} and errors: {ex.failure.errors}"
        )
        for error in ex.failure.errors:
            self.logger.error(f"\tError: {error.message} (Code: {error.error_code.name})")
        if context:
            self.logger.error(f"Context: {context}")
        raise ex