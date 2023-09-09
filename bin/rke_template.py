#!/usr/bin/env python3

# This python3 script will template etc/rancher-config.yml.j2 file 
# using jinja2 and will output the final YML file to this folder

import jinja2
from jinja2 import Environment, FileSystemLoader, Template
import os, sys
import pathlib
import socket
import argparse
import textwrap


def getIP(k8s_hostname=None) -> str:
    final_ip = socket.gethostbyname(k8s_hostname)
    return final_ip


def getListOfHostnameIPs(hostnames=None) -> list:
    host_list = list()
    vmware_lst = list(hostnames.split(","))
    for nd in vmware_lst:
        ip = getIP(nd)
        host_list.append(dict({"name": nd, "ip": ip}))
    return host_list


def getListOfCertificates(path_loc=None) -> list:
    certs_files = pathlib.Path(path_loc)
    patterns = ("Root_*.cer") # Multiple internal certificates, incl. full chain
    files = [f for f in certs_files.iterdir() if any(f.match(p) for p in patterns)]
    return files


def createTMPCertFile(paths=None):
    outF = "etc/root-certs.txt"
    try:
        pathlib.Path(outF).unlink()
    except Exception:
        print("Temporary file (if any was created) has been removed.")

    with open(outF, "w") as outfile:
        for fname in paths:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

    r_file = open(outF, "r")
    all_of_it = r_file.read()
    intended_file = textwrap.indent(all_of_it, 10 * " ")

    w_file = open(outF, "w")
    w_file.write(intended_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-ho", "--hosts", help="VMware Host names, separated by comma.", required=True
    )
    parser.add_argument(
        "-cd",
        "--cluster_name",
        help="Cluster domain name to be created.",
        required=True,
    )
    parser.add_argument(
        "-v-rke", "--rke_k8s_version", help="Version of RKE Kubernetes.", required=True
    )
    parser.add_argument(
        "-s3-acc", "--s3_access_key", help="Access Key for S3", required=True
    )
    parser.add_argument(
        "-s3-sec", "--s3_secret_key", help="Secret Key for S3", required=True
    )
    parser.add_argument(
        "-reg",
        "--docker_registry",
        help="Docker Registry",
        required=True,
    )
    args = parser.parse_args()

    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit()

    # what will be templated
    data = dict(
        {
            "rke_cluster_config": "rancher-config.yml",
            "ansible_user": "rancher",
            "docker_registry": args.docker_registry,
            "cluster_name": args.cluster_name,
            "rke_k8s_version": args.rke_k8s_version,
            "s3_access_key": args.s3_access_key,
            "s3_secret_key": args.s3_secret_key,
        }
    )

    print(data)

    hostlist = getListOfHostnameIPs(args.hosts)
    certs_files = getListOfCertificates("folder/where/we/store/certs")
    createTMPCertFile(certs_files)

    ci_subpath = pathlib.Path(__file__).parent.parent
    print(ci_subpath)
    env = Environment(
        loader=FileSystemLoader([pathlib.Path(ci_subpath), pathlib.Path("etc/")])
    )
    template = env.get_template("etc/rancher-config.yml.j2")

    output = template.render(data=data, hostlist=hostlist)
    print(output)

    with open(pathlib.Path(ci_subpath, "rancher-config.yml"), "w") as f:
        f.write(output)
