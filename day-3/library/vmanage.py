import os.path
import vagrant
from ansible.module_utils.basic import AnsibleModule
from pathlib import Path

def run_module():

    module_args = dict(
        path=dict(type='str', required=True),
        state=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

#   Checking Vagrantfile existence and state
    checkv = Path(module.params['path'] + 'Vagrantfile')

    if not checkv.is_file():
        module.fail_json(msg='There is no such Vagrantfile', **result)

    if not module.params:
        module.fail_json(msg='Please specify vm state', **result)

#   Defining vars
    vpath = module.params['path']
    vm = vagrant.Vagrant(vpath)
    currst = vm.status()[0][1]

    result = dict(
        state = '',
        ip_address = '',
        port = '',
        ssh_key = '',
        username = '',
        os_name = '',
        ram_size = ''
    )

#   Actions
    if module.params['state'] == 'started':
        vm = vagrant.Vagrant(vpath)
        currst = vm.status()[0][1]    
        if currst != 'running':
            vm.up()              
        result['state'] = vm.status()[0][1]
        result['ip_address'] = vm.user_hostname_port().split('@')[1].split(':')[0]
        result['port'] = vm.port()
        result['ssh_key'] = vm.keyfile()
        result['username'] = vm.user()
        result['os_name'] = vm.ssh(command='cat /etc/*-release').split()[0]
        result['ram_size'] = vm.ssh(command='free -h').split()[7]

    if module.params['state'] == 'stopped':
        if currst == 'running':
            vm.halt()              
        result['state'] = vm.status()[0][1]

    if module.params['state'] == 'destroyed':
        if currst != 'not_created':
            vm.halt()
            vm.destroy()              
        result['state'] = vm.status()[0][1]

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()


