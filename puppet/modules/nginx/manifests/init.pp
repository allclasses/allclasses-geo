class nginx {
  File {
    require => Package[nginx]
  }
  package {
    "nginx": ensure => installed;
  }
  file { "/etc/nginx/nginx.conf":
    content => template("nginx/nginx.conf"),
    notify => Service[nginx]
  }
  file { "/etc/nginx/conf.d/geo.conf":
    content => template("nginx/geo.conf"),
    notify => Service[nginx]
  }
  file {
    "/etc/nginx/conf.d/default.conf": ensure => absent;
    "/etc/nginx/conf.d/ssl.conf": ensure => absent;
    "/etc/nginx/conf.d/virtual.conf": ensure => absent;
  }
  service { "nginx":
    ensure => running,
    require => File["/etc/nginx/conf.d/geo.conf",
                    "/etc/nginx/conf.d/default.conf",
                    "/etc/nginx/conf.d/ssl.conf",
                    "/etc/nginx/conf.d/virtual.conf"]
  }
}
