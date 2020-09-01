import datetime
import pytz
from eth_hash.auto import keccak
import web3

a = keccak(b'Ethereum is a distributed database').hex()

year = int(input())
hash = input()

start = int(datetime.datetime(year, 9, 29, 23, 0, 0).replace(tzinfo=pytz.utc).timestamp())
end = int(datetime.datetime(year, 10, 1, 23, 0, 0).replace(tzinfo=pytz.utc).timestamp())

for day in range(start, end + 1, 86400):
    if hash == keccak(day.to_bytes(32, byteorder="big")).hex():
        print(datetime.datetime.utcfromtimestamp(day)).strftime("%d.%m")

