from pya3 import *
from dotenv import load_dotenv
from datetime import datetime, timedelta



class AliceBlueDataScraper:
    ## Contructor to initialize the AliceBlueDataScraper with user credentials
    def __init__(self, user_id=None, api_key=None):
        load_dotenv()
        self.user_id = user_id or os.getenv("ALICE_USER_ID")
        self.api_key = api_key or os.getenv("ALICE_API_KEY")
        print("AliceBlueDataScraper initialized with user_id:", self.user_id)
        print("AliceBlueDataScraper initialized with api_key:", self.api_key)

        if not self.user_id or not self.api_key:
            raise ValueError("User ID and API KEY required. Set as arguments or in .env file.")
        
        self.Alice = Aliceblue(user_id=self.user_id, api_key=self.api_key)
        if not self.Alice.get_session_id():
            raise ValueError("Failed to get session ID. Check your credentials.")

    def Check_Login_info(self):
        profile = self.Alice.get_profile()
        print(f"--- AliceBlue Profile Information ---")
        print(f"Account Name   : {profile.get('accountName')}")
        print(f"Account ID     : {profile.get('accountId')}")
        print(f"Account Status : {profile.get('accountStatus')}")
        print(f"Broker Name    : {profile.get('sBrokerName')}")
        print(f"Products       : {', '.join(profile.get('product', []))}")
        print(f"Email          : {profile.get('emailAddr')}")
        print(f"Phone          : {profile.get('cellAddr')}")
        print(f"Demat Type     : {profile.get('dpType')}")
        print(f"POA Status     : {'Given' if profile.get('poaStatus')=='Y' else 'Not Given'}")


    def get_and_store_historical_data(self, symbol: str, timeframe_provided: str, from_date: datetime, to_date: datetime,file_path: str, exchange: str = "NSE", indices_require: bool = False):        
        print(
                f"Fetching historical data for symbol: '{symbol}'\n"
                f"  Timeframe : {timeframe_provided}\n"
                f"  From      : {from_date}\n"
                f"  To        : {to_date}\n"
                f"  Exchange  : {exchange}\n"
                f"  Indices   : {indices_require}\n"
                f"  Save to   : {file_path}\n"
            )

        instrument = self.Alice.get_instrument_by_symbol(exchange, symbol)
        from_datetime = from_date     # From last 7 days
        to_datetime = to_date                                # To now
        interval = timeframe_provided      # ["1", "D"]
        indices = indices_require      # For Getting index data
        data=self.Alice.get_historical(instrument, from_datetime, to_datetime, interval, indices)
        data.to_csv(file_path, index=False)
        print(f"Historical data for {symbol} from {from_datetime} to {to_datetime} saved to {file_path}.")
        return data