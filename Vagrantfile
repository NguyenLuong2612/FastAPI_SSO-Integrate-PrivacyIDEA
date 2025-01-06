Vagrant.configure("2") do |config|
  # Define the base box to use

  config.vm.provision "file", source: "C:/Users/lomki/.ssh/id_ed25519.pub", destination: "$HOME/id_ed25519.pub"
  config.vm.provision "file", source: "./cert.pem", destination: "$HOME/cert.pem"
  config.vm.provision "file", source: "./key.pem", destination: "$HOME/key.pem"
  config.vm.provision "shell", path: "./bootstrap.sh"
  config.vm.box = "gusztavvargadr/ubuntu-server-2404-lts"
  config.vm.box_version = "2404.0.2409"

  config.vm.define "backend" do |backend|
    backend.vm.hostname = "backend"
    backend.vm.provision "file", source: "./backend", destination: "$HOME/backend"
    backend.vm.provision "shell", path: "./backend/backend.sh"
    backend.vm.provider "vmware_workstation" do |v|
      v.vmx["memsize"] = "2048"
      v.vmx["numvcpus"] = "2"
    end
    backend.vm.network "private_network", ip: "10.128.0.20"
  end

  config.vm.define "frontend" do |frontend|
    frontend.vm.hostname = "frontend"
    frontend.vm.provision "file", source: "./frontend", destination: "$HOME/frontend"
    frontend.vm.provision "shell", path: "./frontend/frontend.sh"
    frontend.vm.provider "vmware_workstation" do |v|
      v.vmx["memsize"] = "2048"
      v.vmx["numvcpus"] = "2"
    end
    frontend.vm.network "private_network", ip: "10.128.0.21"
  end

  config.vm.define "db" do |db|
    db.vm.hostname = "db"
    db.vm.provision "file", source: "./database", destination: "$HOME/database"
    db.vm.provision "shell", path: "./database/db.sh"
    db.vm.provider "vmware_workstation" do |v|
      v.vmx["memsize"] = "2048"
      v.vmx["numvcpus"] = "2"
    end
    db.vm.network "private_network", ip: "10.128.0.19"
  end

  config.vm.define "pi" do |pi|
    pi.vm.hostname = "pi"
    pi.vm.provision "shell", path: "./pi.sh"
    pi.vm.provider "vmware_workstation" do |v|
      v.vmx["memsize"] = "2048"
      v.vmx["numvcpus"] = "2"
    end
    pi.vm.network "private_network", ip: "10.128.0.23"
  end  
end
