set -x

echo Sample of CLI functionality
python3 main.py
python3 main.py client
python3 main.py engagement
python3 main.py event
python3 main.py engagement compose -h
python3 main.py event receive-email -h

echo
echo Clear the database
python3 main.py environment reset

echo
echo Engage a client via inbound email
python3 main.py client engage -n 'Sissi Wang' -a sissi@brokrly.com -b in -e "I would like to buy a house"
python3 main.py engagement list
python3 main.py event list -eid 1

echo
echo Response dry run
python3 main.py engagement compose -id 1 --dry-run
python3 main.py engagement compose -id 1

echo
echo Follow up
python3 main.py event timeout -t 2
python3 main.py engagement compose -id 1

echo
echo Update seller and receive email from them
python3 main.py engagement counterparty -id 1 -n 'Joe Seller' -e joe@seller.com -a '123 San Francisco'
python3 main.py event receive-email -eid 1 -s counterparty -e 'I have a competing offer of $1.1M. Would you like to bid?'
python3 main.py event list -eid 1

echo
echo Inform client of seller email
python3 main.py engagement compose -id 1
