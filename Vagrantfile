# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant configuration file, simplified from:
# https://github.com/pjan/the-ansibles/blob/master/contrib/vagrant/Vagrantfile

BOX_IMAGE = ENV['BOX_IMAGE'] || "ubuntu/trusty64"
BOX_VERSION = ENV['BOX_VERSION'] || "14.04"
BOX_IP_ZONE = ENV['BOX_IP_ZONE'] || "192.168.111"
BOX_FORWARDED_PORT = ENV['BOX_FORWARDED_PORT'] || 22

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Set up multiple servers for different services
  # NOTE: Make sure all IPs are on the same subnet, e.g. ip_end should always begin with 22

  # Insecure private key not working after vagrant upgrade
  # https://github.com/mitchellh/vagrant/issues/4967
  config.ssh.forward_agent = true
  config.ssh.insert_key = false

  config.vm.define "webserver" do |webserver|
    ip_end = "222"
    webserver.vm.box = BOX_IMAGE
    webserver.vm.network :private_network, ip: BOX_IP_ZONE + "." + ip_end
  end

  config.vm.define "elasticsearch" do |elastic|
    ip_end = "223"
    elastic.vm.box = BOX_IMAGE
    elastic.vm.box_version = BOX_VERSION
    elastic.vm.network :private_network, ip: BOX_IP_ZONE + "." + ip_end
  end

  config.vm.define "gitlab" do |gitlab|
    ip_end = "224"
    gitlab.vm.box = BOX_IMAGE
    gitlab.vm.box_version = BOX_VERSION
    gitlab.vm.network :private_network, ip: BOX_IP_ZONE + "." + ip_end

    gitlab.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "1024"]
    end
  end

  config.vm.define "osf-vagrant" do |osf|
    ip_end = "225"
    osf.vm.box = BOX_IMAGE
    osf.vm.box_version = BOX_VERSION
    osf.vm.network :private_network, ip: BOX_IP_ZONE + "." + ip_end

    osf.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "1024"]
    end
  end

  config.vm.define "waterbutler-01" do |waterbutler|
    ip_end = "111"
    waterbutler.vm.box = BOX_IMAGE
    waterbutler.vm.box_version = BOX_VERSION
    waterbutler.vm.network :private_network, ip: BOX_IP_ZONE + "." + ip_end

    waterbutler.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "1024"]
    end
  end

  config.vm.define "scrapi-01" do |scrapi|
    ip_end = "130"
    scrapi.vm.box = BOX_IMAGE
    scrapi.vm.box_version = BOX_VERSION
    scrapi.vm.network :private_network, ip: BOX_IP_ZONE + "." + ip_end

    scrapi.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "2048"]
    end
  end
end
