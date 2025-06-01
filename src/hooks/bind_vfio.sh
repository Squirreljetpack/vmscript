#!/bin/bash

## Load the config file
source "/etc/libvirt/hooks/kvm.conf"

rmmod nvidia_uvm
rmmod nvidia_modeset
rmmod nvidia
sleep 2

## Load vfio
modprobe vfio
modprobe vfio_iommu_type1
modprobe vfio_pci


# For each DEV (id from lspci), maps 0000:01:00.0 to pci_0000_01_00_0, and detaches all pci in iommu group
if [ ! -z "$(ls -A /sys/class/iommu)" ]; then
    for DEV in $DEVS; do
        for IOMMUDEV in $(ls /sys/bus/pci/devices/$DEV/iommu_group/devices) ; do
        	formatted_dev=${IOMMUDEV//[:.]/_}
        	formatted_dev="pci_$formatted_dev"
            virsh nodedev-detach $formatted_dev
        done
    done
fi
