# ############################################     PARAMETERS    #######################################################
# Fill in variables below. Usernames, passwords, and enable passwords.
# Use text file switches.txt and paste in ip addresses of the devices. One per line.
# Alternatively, comment out lines 10-11 and use line 12 instead, if number of devices is relatively small.
# By default, only cisco platform is supported.
# ######################################################################################################################
user_list = ['admin', 'user']
password_list = ['password1', 'P@ssw0rd1']
enable_password_list = ['password1', 'P@ssw0rd1']
switchhosts = 'switches.txt'
with open(switchhosts) as f:
    switchhosts = f.read().splitlines()
# switchhosts = ['192.168.56.23', '192.168.56.40', '192.168.56.66']
# ######################################################################################################################
platform = 'cisco_ios'
errors = []
authentication_errors = []


def netmiko_find_username_password(usr, passw, en_passw, swh, plat):
    from netmiko import ConnectHandler
    from paramiko.ssh_exception import AuthenticationException
    print("##################################################" + "\n" + "SWITCHES IN THE HOST FILE: " + "\n" + str(swh)
          + "\n" + "##################################################")

    def inner_func():
        for u in usr:
            for p in passw:
                for ep in en_passw:
                    try:
                        net_connect = ConnectHandler(device_type=plat, ip=host, username=u, password=p, secret=ep)
                        net_connect.enable()
                        return print("Authentication Success!" + " - " + host + ": " + u + "/" + p + "/" + ep)
                    except:
                        if AuthenticationException:
                            authentication_errors.append("Authentication Failure" + " - " + host + ": " + u + "/" +
                                                         p + "/" + ep)
                        else:
                            errors.append(host)
    for host in swh:
        inner_func()
    print("##################################################")


def tellib_find_username_passwords(usr, passw, en_passw, swh):
    import telnetlib

    print("##################################################" + "\n" + "SWITCHES IN THE HOST FILE: " + "\n" + str(swh)
          + "\n" + "##################################################")

    def inner_func():
        try:
            for u in usr:
                for p in passw:
                    tn = telnetlib.Telnet(host, timeout=8)
                    tn.read_until(b"Username: ", timeout=1)
                    tn.write(u.encode('ascii') + b"\n")
                    if passw:
                        tn.read_until(b"Password: ")
                        tn.write(p.encode('ascii') + b"\n")
                        try:
                            response = tn.read_until(b">", timeout=1)
                        except EOFError as e:
                            print("Connection closed: %s" % e)
                        if b">" in response:
                            tn.write(b"enable\n")
                            for ep in en_passw:
                                tn.write(ep.encode('ascii') + b"\n")
                                try:
                                    response = tn.read_until(b"#", timeout=1)
                                except EOFError as e:
                                    print("Connection closed: %s" % e)
                                if b"#" in response:
                                    return print("Authentication Success!" + " - " + host + ": " + u + "/" + p + "/" +
                                                 ep)
        except:
            errors.append(host)

    for host in swh:
        inner_func()
    print("#####################################################")


netmiko_find_username_password(user_list, password_list, enable_password_list, switchhosts, platform)
tellib_find_username_passwords(user_list, password_list, enable_password_list, switchhosts)

for e in errors:
    print("##############################################")
    print("ERRORS WERE FOUND ON THIS HOST: " + e)
for a in authentication_errors:
    print("##############################################")
    print(a)
