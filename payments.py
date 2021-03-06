import requests
import json

def AddCreditCard(name, email, creditcard, expmonth, expyear, address, city, state, cvv, zipcode):
    add = requests.post('http://107.170.240.130:3000/addcreditcard', data={"user_name": name, "email":email, "cc_number":creditcard, "cvv":cvv, "expiration_month":expmonth, "expiration_year":expyear, "address1":address, "city":city, "state":state, "country":"US", "zip":zipcode})
    return add

def AuthorizeCreditCard(credit_card_id):
    authorize = requests.post('http://107.170.240.130:3000/authorizecredit', data={"credit_id":credit_card_id})
    return authorize

def Charge(acct_token,account_id, credit_card_id, amount, desc):
    charge = requests.post('http://107.170.240.130:3000/charge', data={"acct_token":acct_token,"credit_card_id": credit_card_id, "account_id": account_id, "amount": amount, "desc": desc})
    return charge

def CreateExpertAccount(account_token, account_name):
    create = requests.post('http://107.170.240.130:3000/create', data={"account_token":account_token, "account_name": account_name})
    return create.json()