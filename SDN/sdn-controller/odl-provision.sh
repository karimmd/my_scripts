#!/bin/bash

wget https://nexus.opendaylight.org/content/groups/public/org/opendaylight/integration/distribution-karaf/0.6.2-Carbon/distribution-karaf-0.6.2-Carbon.tar.gz -O odl-controller.tar.gz
mkdir odl-controller
tar zxf odl-controller.tar.gz -C ./odl-controller --strip-components=1
rm odl-controller.tar.gz
echo "" >> ./odl-controller/etc/shell.init.script
echo "feature:install odl-restconf odl-l2switch-switch odl-openflowplugin-flow-services odl-openflowplugin-drop-test odl-dlux-core odl-dluxapps-nodes odl-dluxapps-topology odl-dluxapps-yangui odl-dluxapps-yangvisualizer odl-dluxapps-yangman ;" >> ./odl-controller/etc/shell.init.script
