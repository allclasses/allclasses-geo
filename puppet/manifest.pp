Exec {
  path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/", "/usr/local/bin/" ]
}

# disable on the iptables service block doesn't seem to work,
# so execute the command manually
exec {"disable firewall":
  command => "ufw disable"
}

exec { "apt-get update": } ->
package {
  "curl": ensure => installed;
  "git": ensure => installed;
  "vim": ensure => installed;
  "python-dev": ensure => installed;
  "python-setuptools": ensure => installed;
  "libssl-dev": ensure => installed;
  "libpq-dev": ensure => installed;
  "htop": ensure => installed;
}

node default {
  include pip
  include nginx
  include supervisor
}
