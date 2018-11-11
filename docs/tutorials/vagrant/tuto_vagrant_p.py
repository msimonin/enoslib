from enoslib.api import generate_inventory
from enoslib.infra.enos_vagrant.provider import Enos_vagrant
from enoslib.infra.enos_vagrant.configuration import Configuration

import logging
import os

logging.basicConfig(level=logging.INFO)

conf = Configuration()\
       .add_machine(roles=["control"],
                    flavour="tiny",
                    number=1,
                    networks=["api"])\
       .add_machine(roles=["control", "compute"],
                    flavour="tiny",
                    number=1,
                    networks=["api"])\
       .finalize()

# claim the resources
provider = Enos_vagrant(conf)
roles, networks = provider.init()


# path to the inventory
inventory = os.path.join(os.getcwd(), "hosts")

# generate an inventory compatible with ansible
generate_inventory(roles, networks, inventory, check_networks=True)

# destroy the boxes
provider.destroy()
