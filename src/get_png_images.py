from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

import argparse
import requests
import os, shutil, json


class MapbiomasAlertApi:

    URL_BASE = 'https://plataforma.alerta.mapbiomas.org/api/v1/graphql'

    def __init__(self, email, password) -> None:
        self.__email = email
        self.__password = password
        self.__token = self.auth()

    @property
    def email(self) -> str:  
        return self.__email

    @property
    def password(self) -> str:  
        return self.__password

    @property
    def token(self) -> dict:  
        return self.__token

    def auth(self):

        transport = AIOHTTPTransport(self.URL_BASE)
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql('''
            mutation sign_in($email: String!, $password: String!) {
                signIn(email:$email, password:$password){
                token
                }
            }''')
        
        params = {
            'email': self.email,
            'password': self.password
        }
        
        return client.execute(query, params)
        
    def get_png_by_alert_code(self, alert_code):
        
        transport = AIOHTTPTransport(self.URL_BASE, headers={'Authorization': self.token["signIn"]["token"]})
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("""
            query published_alert($alertCode: Int!){
                alertReport(alertCode: $alertCode){
                alertCode
                carCode
                source 
                images {
                    after {
                        satellite
                        url
                    }
                    before {
                        satellite
                        url
                    }
                }
                changes {
                    labels
                    overYears {
                        year
                        imageUrl
                    }
                }
                warnings
            }
        }""")

        result = client.execute(query, {
            'alertCode': alert_code
        })

        return result


def main(email, password, alert_code, save_path='.'):

    consume_api = MapbiomasAlertApi(email, password)

    alert_data = consume_api.get_png_by_alert_code(int(alert_code))
    alert_metadata = json.dumps(alert_data)

    # save metadata
    file_metadata = open('metadata_{}.json'.format(str(alert_code)), 'a')
    file_metadata.write(alert_metadata)
    file_metadata.close()

    t0_url_download = alert_data['alertReport']['images']['before']['url']
    t1_url_download = alert_data['alertReport']['images']['after']['url']

    r0 = requests.get(t0_url_download, stream=True)
    r1 = requests.get(t1_url_download, stream=True)

    if r1.status_code != 200:
        r1.raise_for_status()

    out_dir = os.path.abspath(save_path)

    filename_t0 = f"{out_dir}/{str(alert_code)}_t0.png"
    filename_t1 = f"{out_dir}/{str(alert_code)}_t1.png"

    with open(filename_t0, 'wb') as out_file:
        r0.raw.decode_content = True
        shutil.copyfileobj(r0.raw, out_file)

    with open(filename_t1, 'wb') as out_file:
        r1.raw.decode_content = True
        shutil.copyfileobj(r1.raw, out_file)

    print("Done: ", str(alert_code))
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--email', type=str,
                        help="this is the email registered to download Mapbiomas Alerta data. If you do not have one, please subscribe at the following link https://plataforma.alerta.mapbiomas.org/sign-up?callback_urlnull ")
    parser.add_argument('--password', type=str, help="")
    parser.add_argument('--alert_code', type=int, help="")
    parser.add_argument('--save_path', type=str, help="Path where the output will be saved", default=".")
    args = parser.parse_args()

    main(email=args.email, password=args.password, alert_code=args.alert_code, save_path=args.save_path)

