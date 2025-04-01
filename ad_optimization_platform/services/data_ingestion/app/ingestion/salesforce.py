import pandas as pd
from simple_salesforce import Salesforce


class SalesforceClient:
    def __init__(self, username: str, password: str, security_token: str, domain: str = 'login'):
        """Initialize Salesforce client with credentials."""
        self.sf = Salesforce(
            username=username,
            password=password,
            security_token=security_token,
            domain=domain
        )

    def fetch_opportunities(self) -> pd.DataFrame:
        """
        Fetch closed-won opportunities from last 90 days and return as DataFrame.
        """
        query = """
            SELECT Id, AccountId, CloseDate, Amount 
            FROM Opportunity 
            WHERE StageName = 'Closed Won' AND CloseDate = LAST_90_DAYS
        """
        
        # Execute query and fetch records
        results = self.sf.query_all(query)
        records = results['records']
        
        # Convert to DataFrame
        df_salesforce = pd.DataFrame.from_records(
            [dict(record) for record in records]
        )
        
        # Clean up DataFrame by removing attributes column if it exists
        if 'attributes' in df_salesforce.columns:
            df_salesforce = df_salesforce.drop('attributes', axis=1)
            
        return df_salesforce

    def calculate_customer_metrics(self, df_salesforce: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate customer metrics from opportunities DataFrame.
        
        Returns DataFrame with frequency, average order value, and lifetime value per AccountId.
        """
        customer_metrics = df_salesforce.groupby('AccountId').agg(
            frequency=('Id', 'count'),
            avg_order_value=('Amount', 'mean'),
            lifetime_value=('Amount', 'sum'),
        ).reset_index()
        
        return customer_metrics