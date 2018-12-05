# Fan controller for amdgpus

If you experience problems please create an issue.

## installation:
### pip
`sudo pip3 install .`

### Arch linux
Available in the aur as `amdgpu-fan`

## usage:  
`sudo amdgpu-fan`  

## configuration:
```
# /etc/amdgpu-fan.yml
# format is:
# -[temp(*C), speed(0-100%)]
# eg:

- [0, 0]
- [40, 30]
- [60, 50]
- [80, 100]
```


