# hass-asterisk
Home Assistant platform for Asterisk integration


##### Example configuration

```
asterisk_ami:
  host: localhost
  username: admin
  password: correcthorsebatterystaple
  monitor:
  - 100
  - 101
  - 102
  mailboxes:
  - 100@default
```

The platform requires a matching entry in Asterisk's manager.conf or similar. For example:

```
[admin]
secret = correcthorsebatterystaple
deny=0.0.0.0/0.0.0.0
permit=127.0.0.1/255.255.255.0
read = system,call,log,verbose,command,agent,user,config,command,dtmf,reporting,cdr,dialplan,originate,message
writetimeout = 5000
```

TODO: Confirm which permissions are actually needed
