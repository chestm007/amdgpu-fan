# Fan controller for amdgpus [python3 only]

If you experience problems please create an issue.

## installation:
### pip
`sudo pip3 install amdgpu-fan`

### Arch linux
Available in the aur as `amdgpu-fan`

## usage:
`sudo amdgpu-fan`

## configuration:

.. code-block::

    # optional
    # cards:  # can be any card returned from
    #         # ls /sys/class/drm | grep "^card[[:digit:]]$"
    # - card0

    # optional
    # temp_drop: 5  # how much temperature should drop before fan speed is decreased
