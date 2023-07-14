from keystoneauth1 import loading
from keystoneauth1 import session as session
from keystoneclient.v3 import client as client
from keystoneauth1.identity import v3
import json
#cinder
# Setting up KeyStone Client
auth = v3.Password(
    auth_url = "https://infra.mail.ru:35357/v3",
    username = "",
    password = "",
    user_domain_name = "default",
    project_name = "service",
    project_domain_name = "default"
)
sess = session.Session(auth=auth)
keystone = client.Client(session=sess)

# Getting list of projects
keystone.users.get(user="glance")