#!/usr/bin/env python

from flask import Flask, render_template, flash, request
from wtforms import Form, validators, StringField, SubmitField, DecimalField
from wtforms.validators import NumberRange, ValidationError
import math
import os
import requests


class Explorer(object):
    uri = None
    sk = None
    address = None

    def __init__(self, uri, sk):
        self.uri = uri
        self.sk = sk
        self.address = self.get_address_by_secret_key(sk)

    def validate_address(self, address):
        res = requests.get(self.uri + '/address/' + address + '/validate')

        if res.status_code != 200:
            err = res.json()
            return False, err['detail']

        return True, ''

    def get_address_by_secret_key(self, sk):
        res = requests.get(self.uri + '/address/by/secret-key/' + sk)
        if res.status_code != 200:
            err = res.json()
            raise ValueError('Error getting faucet address: {}'.format(
                ' '.join([str(err['error']), err['reason'], err['detail']])))
        return res.json()


class AddressForm(Form):
    """Address Form."""
    address = StringField('Address', validators=[validators.required()])
    amount = DecimalField('Amount:', validators=[validators.required(), NumberRange(min=0, max=1, message='Too much!')])
    submit = SubmitField('Get Ergo!')

    def validate_address(form, field):
        ok, msg = explorer.validate_address(field.data)
        if not ok:
            raise ValidationError(msg)


app = Flask(__name__)
app.config.from_object(__name__)
for k in ['SECRET_KEY', 'SIGNER_URI', 'SK']:
    app.config[k] = os.environ.get(k, None)
    if not app.config[k]:
        raise ValueError('You must have "{}" variable'.format(k))

explorer = Explorer(app.config['SIGNER_URI'], app.config['SK'])


@app.route('/', methods=['GET', 'POST'])
def index():
    address_form = AddressForm(request.form)
    if request.method == 'POST':
        if address_form.validate():
            signer = app.config['SIGNER_URI']
            addresses_amounts = {address_form.address.data: math.floor(address_form.amount.data * 1000000000),}

            tx_response = requests.post(signer + '/transactions/create', json={
                'addresses_amounts': addresses_amounts,
                'sk': app.config['SK']
            })

            # print(tx_response)

            if tx_response.status_code != 200:
                flash('Error creating faucet transaction!')
                flash('Status code is: {}'.format(tx_response.status_code))
            else:
                tx = tx_response.json()
                url2send = 'https://api-testnet.ergoplatform.com/transactions'
                tx2node = requests.post(url2send, json=tx)
                if tx2node.status_code != 200:
                    flash('Error sending faucet transaction to Explorer at {}'.format('https://api-testnet.ergoplatform.com/transactions'))
                else:
                    flash('You will get some Ergo. Your tx_id={}'.format(tx['id']))
        else:
            for field, errors in address_form.errors.items():
                for error in errors:
                    flash("Error in the {} field - {}".format(getattr(address_form, field).label.text, error))

    return render_template('/index.html', form=address_form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=33333)
