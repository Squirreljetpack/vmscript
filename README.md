vmscript is an accessibility layer for vfio setups.
It provides subcommands for attaching and detaching devices, and loading arbitrary xml modules into your vm definition, as well as for starting, stopping, and installing hooks into your VM.

The run subcommand adds conditional logic to robustly start, stop and log your VM activity, including filtering out non-existing devices from the VM definition (which would otherwise prevent startup).

For more, consult vmscript --help. (TODO)