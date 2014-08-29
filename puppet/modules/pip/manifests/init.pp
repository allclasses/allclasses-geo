class pip {
  file { "/usr/local/wheels":
      ensure => "directory",
      owner  => "ubuntu",
      group  => "ubuntu",
      mode   => 750,
  }

  # Chain of commands to ensure pip is all up to date.
  exec { "easy_install pip":
    require=>File["/usr/local/wheels"],
    unless=>"which pip"
  }
  exec { "upgrade setuptools":
    command=>"pip install --upgrade setuptools",
    require=>Exec["easy_install pip"]
  }
  exec { "pip install wheel":
    require=>Exec["upgrade setuptools"]
  }
  exec { "install wheel":
    command=>"pip wheel -w /usr/local/wheels -f file:///usr/local/wheels/ virtualenv",
    require=>Exec["pip install wheel"]
  }
  exec { "install virtualenv":
    command=>"pip install -f file:///usr/local/wheels virtualenv",
    require=>Exec["install wheel"]
  }
}
