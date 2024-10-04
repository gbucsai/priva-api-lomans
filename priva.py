import httpx
from dotenv import dotenv_values

# load config from .env file
config = dotenv_values(".env")


# define Priva API controller
class Priva:
    tenant_id = config["TENANT_ID"]
    client_id = config["CLIENT_ID"]
    client_secret = config["CLIENT_SECRET"]

    @classmethod
    def __get_token(self):
        form = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "priva.data-services",
        }
        r = httpx.post(
            url="https://auth.priva.com/connect/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=form,
        )
        response = r.json()
        return response["access_token"]

    @classmethod
    def get_assets(self):
        r = httpx.get(
            url=f"https://api.priva.com/data-insight-metadata/api/v1/tenants/{self.tenant_id}/assets",
            headers={"Authorization": f"Bearer {self.__get_token()}"},
        )
        return r.json()

    @classmethod
    def get_trendable_vars(self, asset_id: str):
        r = httpx.get(
            url=f"https://api.priva.com/data-insight-metadata/api/v1/tenants/{self.tenant_id}/assets/{asset_id}/variables/trendable",
            headers={"Authorization": f"Bearer {self.__get_token()}", "Accept": "*/*"},
        )
        return r.json()

    @classmethod
    def get_var_data(
        self,
        asset_id: str,
        start_time: str,
        end_time: str,
        deviceGroupId: str,
        deviceId: str,
        variableId: str,
    ):
        r = httpx.post(
            timeout=15,
            url=f"https://api.priva.com/data-insight-history/api/v4/data/{asset_id}",
            headers={"Authorization": f"Bearer {self.__get_token()}", "Accept": "*/*"},
            json={
                "startTime": f"{start_time}",
                "endTime": f"{end_time}",
                "variableReferenceList": [
                    {
                        "deviceGroupId": deviceGroupId,
                        "deviceId": deviceId,
                        "variableId": variableId,
                    }
                ],
            },
        )
        return r.json()


# instantiate client
priva_client = Priva()

# get site identifiers
sites = priva_client.get_assets()

# get trendable variable metadata
trendables = priva_client.get_trendable_vars(
    asset_id="86bcaa17-4432-4fb6-9be0-d4e99a4db88e"  # find all available asset IDs in get_assets() response
)

# get meter data for a specific variable
data = priva_client.get_var_data(
    asset_id="86bcaa17-4432-4fb6-9be0-d4e99a4db88e",  # find all available asset IDs in get_assets() response
    start_time="2024-10-02",  # "YYYY-MM-DD
    end_time="2024-10-03",  # "YYYY-MM-DD
    deviceGroupId="p79234",  # find all available device group IDs for an asset in get_trendable_vars() response
    deviceId="3bc478db-de65-4395-8022-88e904e8eb32",  # find all available device IDs for an asset in get_trendable_vars() response
    variableId="c5cb4bcd-c5ca-4360-8712-25dc74ba9b5d",  # find all available variable IDs for an asset in get_trendable_vars() response
)

# print (partial) results
print(sites)
print("------------------------------------")
print(trendables[0])
print("------------------------------------")
print(data["variables"][0]["samples"][0:5])
