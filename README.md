vmscript is an accessibility wrapper for vfio setups.
It provides subcommands for attaching and detaching devices, and loading arbitrary xml modules into your vm definition, as well as for starting, stopping, and installing hooks into your VM.

The run subcommand adds conditional logic to robustly start, stop and log your VM activity, including filtering out non-existing devices from the VM definition (which would otherwise prevent startup).

```
> vmscript --help

vmscript - An accessibility wrapper for vfio setups.
      
      Usage: vmscript [options] <subcommand> [VM_MACHINE] [subcommand_options]
      
      Options:
        --xml-dir <path>            Sets VM_XML_DIR, determining to the path to the directory containing XML definitions. Defaults to '../xmls' relative to the script.
        --wait <seconds>            Sets VM_WAIT, determining seconds to wait between status checks (e.g., for VM running). Defaults to 5.
        --clean                     Sets VM_CLEAN to true, causing 'prepare' subcommand to remove all disk devices. Defaults to 'false'.
        --command-timeout <seconds> Sets VM_COMMAND_TIMEOUT, determining seconds to wait for virsh commands. Defaults to 30.
        --shutdown-tries <count>    Sets VM_SHUTDOWN_TRIES, determining number of shutdown attempts before offering to force off. Defaults to 2.
        --no-run-with-sudo          Sets VM_RUN_WITH_SUDO to false, causing 'run' and 'shutdown' subcommands to not use sudo when invoking virsh. Defaults to 'true'.
        --no-looking-glass false    Sets VM_LOOKING_GLASS to false, causing 'run' to start the client. Defaults to 'true' when conditions are met.
        --help, -h                  Show this help message.
      
      Additional environment variables:
        VM_MACHINE           Name of the VM to operate on (can also be passed as an argument).
        DEBUG                Defaults to 'false'.
      
      Subcommands:
        prepare [VM_MACHINE]
          Prepares the VM's XML configuration from a base xml at $VM_XML_DIR/$VM_MACHINE/$VM_MACHINE.xml
          (see dump subcommand) as follows:
          - filters out USB devices and block disk devices that are not currently
          connected or available on the host system.
          - If VM_CLEAN is true, all disks are removed.
          - merges additional XML definitions found in $VM_XML_DIR/$VM_MACHINE/*.xml
            - files featuring device definitions are included only when all devices referred to are present
            - The XML definitions can either be fully defined (see vmscript _mergexml --help for more details)
              or the kind of device fragments accepted by virsh attach-device
      
        attach [VM_MACHINE]
          Interactively lists available USB devices on the host and allows you to select
          one to attach to the specified VM. Works whether the VM is running or shut down.
      
        detach [VM_MACHINE]
          Interactively lists USB devices currently defined for (or attached to) the VM
          and allows you to select one to detach. This will remove the device definition
          from the VM's configuration if it's shut down, or live-detach if running.
      
        info [VM_MACHINE]
          Displays information about the VM, including paths to log files, configuration files,
          hook directories and connected USB devices
      
        dump [VM_MACHINE]
          Dumps the current live XML configuration of the VM to its base XML file.
          The prepare subcommand can then logically modify this file with other xml modules.
      
        run [VM_MACHINE]
          Starts the VM:
          - Logs to systemctl (as well as stdout)
          - Invokes the prepare subcommand
          - unmounts any disks defined in the XML from the host system.
          - Based on the value of VM_LOOKING_GLASS, starts a display client
          - invokes shutdown subcommand on script exit.
      
        shutdown [VM_MACHINE]
          Shuts down the VM gracefully.
          In an interactive terminal:
          - if the VM doesn't shut down after VM_SHUTDOWN_TRIES, it will prompt to force off (virsh destroy).
          - restarts gvfs-udisks2-volume-monitor.
      
        install [VM_MACHINE]
          Presents a menu interface for installing various collections of files, such as from a collection
          of QEMU hooks to the VM.
```