# Fan controller for amdgpus

If you experience problems please create an issue.

<a href="https://aur.archlinux.org/packages/amdgpu-fan/"><img src="https://raw.githubusercontent.com/CorvetteCole/amdgpu-fan/master/download_aur.png" height="54"></a>

## Installation:

### Arch Linux, Manjaro and derivatives
Install from the [AUR](https://aur.archlinux.org/packages/amdgpu-fan/) using your favorite helper, or build manually as shown below:

.. code-block::

    $ git clone https://github.com/chestm007/amdgpu-fan.git
    $ cd amdgpu-fan
    $ makepkg -si

## Usage:
`$ sudo amdgpu-fan`  
Start the daemon with `$ sudo systemctl start amdgpu-fan`  
Make it with run at startup with `$ sudo systemctl enable amdgpu-fan`


## Configuration:
Edit `/etc/amdgpu-fan.yml` to create the desired fan curve

.. code-block::

    # /etc/amdgpu-fan.yml
    # eg:

    # optional
    # cards:  # can be any card returned from
    #         # ls /sys/class/drm | grep "^card[[:digit:]]$"
    # - card0

    # optional
    # temp_drop: 5  # how much temperature should drop before fan speed is decreased
