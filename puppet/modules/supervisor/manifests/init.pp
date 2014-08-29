class supervisor {
  exec { "pip install supervisor":
    creates => "/usr/bin/supervisord",
    require => Exec["easy_install pip"]
  }
  file { "/var/log/supervisor":
    ensure => directory,
    owner => "ubuntu"
  }
  file { "/etc/supervisord.conf":
    content => template("supervisor/supervisord.conf"),
    owner => "ubuntu",
    require => Exec["pip install supervisor"],
    notify => Service[supervisord]
  }
  file { "/etc/init.d/supervisord":
    source => "puppet:///modules/supervisor/supervisord",
    owner => "ubuntu",
    mode => "0755"
  }
  service { "supervisord":
    ensure => running,
    require => [Exec["pip install supervisor"],
                File["/etc/init.d/supervisord"]]
  }
}
