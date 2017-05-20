#!/usr/bin/env python

import os
from os import path
from subprocess import check_call
import project_root
from helpers import parse_arguments, apply_patch


def main():
    args = parse_arguments('receiver_first')

    cc_repo = path.join(project_root.DIR, 'third_party', 'sprout')
    model = path.join(cc_repo, 'src', 'examples', 'sprout.model')
    src = path.join(cc_repo, 'src', 'examples', 'sproutbt2')

    if args.option == 'deps':
        print ('libboost-math-dev libssl-dev libprotobuf-dev '
               'protobuf-compiler libncurses5-dev')

    if args.option == 'run_first':
        print 'receiver'

    if args.option == 'setup':
        # apply patch to reduce MTU size
        apply_patch('sprout_mtu.patch', cc_repo)

        sh_cmd = './autogen.sh && ./configure --enable-examples && make -j2'
        check_call(sh_cmd, shell=True, cwd=cc_repo)

    if args.option == 'receiver':
        os.environ['SPROUT_MODEL_IN'] = model

        # Sprout will print the port to listen on in a format required by tests
        check_call([src])

    if args.option == 'sender':
        os.environ['SPROUT_MODEL_IN'] = model

        cmd = [src, args.ip, args.port]
        check_call(cmd)


if __name__ == '__main__':
    main()
