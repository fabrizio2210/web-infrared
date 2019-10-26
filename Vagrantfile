# -*- mode: ruby -*-
# vi: set ft=ruby :

ENV['VAGRANT_DEFAULT_PROVIDER'] = 'libvirt'

# Check required plugins
REQUIRED_PLUGINS_LIBVIRT = %w(vagrant-libvirt)
exit unless REQUIRED_PLUGINS_LIBVIRT.all? do |plugin|
  Vagrant.has_plugin?(plugin) || (
    puts "The #{plugin} plugin is required. Please install it with:"
    puts "$ vagrant plugin install #{plugin}"
    false
  )
end

Vagrant.configure("2") do |config|

  # node to develop
  config.vm.define "web-develop" do |node1|
    node1.vm.hostname = "web-develop"
    node1.vm.box = "debian/stretch64"
    node1.vm.box_check_update = false
    node1.vm.synced_folder './src/', '/opt/web-infrared/'
    node1.vm.provider :libvirt do |domain|
      domain.memory = 1024
      domain.nested = true
      domain.storage :file, :size => '1G'
    end
  end
end
