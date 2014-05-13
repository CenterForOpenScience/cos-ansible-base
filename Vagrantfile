# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant configuration file, simplified from:
# https://github.com/pjan/the-ansibles/blob/master/contrib/vagrant/Vagrantfile

# --- Configuration

PROJECT_NAME  = ENV['PROJECT_NAME']  || "ANSIBLES"

BOX_IMAGE     = ENV['BOX_IMAGE']     || "ubuntu/trusty64"
BOX_NAME      = ENV['BOX_NAME']      || "testbox"
BOX_ADMIN     = ENV['BOX_ADMIN']     || "vagrant"
BOX_IP_ZONE   = ENV['BOX_IP_ZONE']   || "192.168.111"
BOX_IP_END    = ENV['BOX_IP_END']    || "111"
BOX_MEMORY    = ENV['BOX_MEMORY']    || "1024"
BOX_CPUS      = ENV['BOX_CPUS']      || "1"
BOX_DOCKER    = ENV['BOX_DOCKER']    || false


# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # CONFIGURATION

  config.vm.box = BOX_IMAGE
  config.vm.network :private_network, ip: BOX_IP_ZONE + "." + BOX_IP_END
  config.vm.network :forwarded_port, guest: 22, host: ("9" + BOX_IP_END).to_i

  config.vm.provider :virtualbox do |vb|
    # vb.gui = true
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
    vb.customize ["modifyvm", :id, "--memory", BOX_MEMORY]
    vb.customize ["modifyvm", :id, "--cpus", BOX_CPUS]
  end

  # config.vm.provision :shell, :inline => $docker_cmd

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "base.yml"
    ansible.inventory_path = "vagrant"
    ansible.sudo = true
    ansible.limit = BOX_NAME
  end

end
