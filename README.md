# Generate Accounts

This is simple and probably flawed script intended to generate some YAML that can be fed into the [torrancew/accounts](https://forge.puppet.com/torrancew/account) puppet module.

It was written to gather a load of user data from an Ubuntu box that was being ported into Puppet. With some minor adjustments it could be used elsewhere.

## Notes and Limitations

* Assumes UIDs start at 1000
* Assumes you're using feature/multiple_ssh_keys or a compatible fork
* Requires sudo to collect keys and password hashes
