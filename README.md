# jabber-pic-server

Simple Jabber Pic server for Active Directory

# TODO / In Progress

* LDAP_SSL - for secure connection (need to support local certfile etc)
* Move logging to file instead of stdout
* Web based configuration instead of .env file?

# Configuration

Create a .env file in either the local directory or ```/srv/jabber-pic-server```.  You can specify an alternate folder using the ```-c / --config``` parameter.

```
LDAP_SERVER=hostnameorIP
LDAP_PORT=389
LDAP_SSL=False
LDAP_USER=binduser@domain.tld
LDAP_PASS=userpassword
LDAP_BASE="dc=domain,dc=tld"
LDAP_LOOKUP=sAMAccountName
LDAP_ATTRIBUTE=thumnailPhoto
```

## LDAP_SERVER

Hostname/IP Address of LDAP server.

## LDAP_PORT

LDAP Port to connect to - defaults to 389.

## LDAP_SSL

Not implemented yet.

## LDAP_USER

Username to bind with.

## LDAP_PASS

Password for ```LDAP_USER``` binding.

## LDAP_BASE

Match this to the base for LDAP user lookups.

## LDAP_LOOKUP

Match this to the field you use in your jabber config file for photo lookups.

```xml
<Directory>
 <PhotoURISubstitutionEnabled>True</PhotoURISubstitutionEnabled>
 <PhotoURISubstitutionToken>sAMAccountName</PhotoURISubstitutionToken>
 <PhotoURIWithToken>http://<server>/pics/sAMAccountName.jpg</PhotoURIWithToken>

 <BDIPhotoURISubstitutionEnabled>True</BDIPhotoURISubstitutionEnabled>
 <BDIPhotoURISubstitutionToken>sAMAccountName</BDIPhotoURISubstitutionToken>
 <BDIPhotoURIWithToken>http://<server>/pics/sAMAccountName.jpg</BDIPhotoURIWithToken>
</Directory>
```

## LDAP_ATTRIBUTE

Match this field to the attribute you use in LDAP for the photo.

#### Directory Attribute - thumbnailPhoto
```xml
<Directory>
 <PhotoSource>thumbnailPhoto</PhotoSource>

 <BDIPhotoSource>thumbnailPhoto</BDIPhotoSource>
</Directory>
```

#### Directory Attribute - jpegPhoto
```xml
<Directory>
 <PhotoSource>jpegPhoto</PhotoSource>

 <BDIPhotoSource>jpegPhoto</BDIPhotoSource>
</Directory>
```

#### Directory Attribute - photoUri
```xml
<Directory>
 <PhotoSource>photoUri</PhotoSource>

 <BDIPhotoSource>photoUri</BDIPhotoSource>
</Directory>
```

# Running

Finish this.
