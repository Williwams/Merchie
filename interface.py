from blizzardapi import BlizzardApi
from datetime import datetime, timedelta

locale="en_US"
region="us"
clientID=""
clientSecret=""
api_client = BlizzardApi(clientID, clientSecret)

def verify_item(itemID):
    if itemID not in itemDatabase:
        itemdata=api_client.wow.game_data.get_item(region, locale, itemID)
        itemDatabase.add(itemdata)


def submit_auction(auction):
    if auction["id"] in auctionDatabase(realmID):
        auctionDatabase.update(auction, last_modified)
    else:
        auctionDatabase.add(auction)

# These need to be put in to actual databases
auctionDatabase = []
itemDatabase = []

# Validate realms
realms = {}
realm_index=api_client.wow.game_data.get_connected_realms_index(region, locale)
datetime_format = "%a, %d %b %Y %H:%M:%S GMT"
for realm in realm_index['connected_realms']:
    # Strips the connected Realm ID which for some reason
    # is only provided within href
    realmID=realm['href'].split("/")[-1].split("?")[0]
    realm_info=api_client.wow.game_data.get_realm(region, locale, realmID)
    last_modified = datetime.strptime(realm_info['response_headers'], datetime_format)
    # Populate realm names under realmIDs. This only chooses a pre-identified "leader" for connected
    # realms and will require external data not available in the API for sister servers(it seems)
    if 'code' not in realm_info:
        realms[realmID] = {'name': realm_info["name"], 'slug': realm_info["slug"], 'Last-Modified': last_modified}

    # Verify that database is aware of all realms and RealmIDs
    # database_validate()
    if auctionDatabase[realmID]['last_modified']+timedelta(hours=1) < last_modified:
        # pull auction data per server
        auctiondata=api_client.wow.game_data.get_auctions(region, locale, realmID)
        for auction in auctiondata["auctions"]:
            # Make sure we have information on this item stored in the database
            verify_item(auction["item"]["id"])
            submit_auction(auction)