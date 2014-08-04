# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant configuration file, simplified from:
# https://github.com/pjan/the-ansibles/blob/master/contrib/vagrant/Vagrantfile

# --- Configuration

PROJECT_NAME  = ENV['PROJECT_NAME']  || "ANSIBLES"

BOX_IMAGE     = ENV['BOX_IMAGE']     || "ubuntu/trusty64"
BOX_NAME      = ENV['BOX_NAME']      || "vagrantbox"
BOX_ADMIN     = ENV['BOX_ADMIN']     || "vagrant"
BOX_IP_ZONE   = ENV['BOX_IP_ZONE']   || "192.168.111"
BOX_IP_END    = ENV['BOX_IP_END']    || 111
BOX_MEMORY    = ENV['BOX_MEMORY']    || "800"
BOX_CPUS      = ENV['BOX_CPUS']      || "1"
BOX_DOCKER    = ENV['BOX_DOCKER']    || false
NODE_NUMBER   = ENV['NODE_NUMBER']   || 3


# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # CONFIGURATION
  NODES = Hash[NODE_NUMBER.times.map { |n| ['Node%d' % n, '%s.%d' % [BOX_IP_ZONE, (BOX_IP_END + n)]] }]

  NODES.each do |nodenumber, node_ip|
    config.vm.define nodenumber do |node_config|

      node_config.vm.box = BOX_IMAGE
      node_config.vm.network :private_network, ip: node_ip
      node_config.vm.hostname = 'cos-ansible-%s' % nodenumber

      node_config.ssh.forward_agent = true

      node_config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--ioapic", "on"]
        vb.customize ["modifyvm", :id, "--memory", BOX_MEMORY]
        vb.customize ["modifyvm", :id, "--cpus", BOX_CPUS]
      end
    end
  end
end
