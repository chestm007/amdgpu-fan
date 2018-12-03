# fan controller for amdgpus

if you experience problems please create an issue.

usage:  
`sudo amdgpu-fan`  

configuration:
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


