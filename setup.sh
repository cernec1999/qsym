#!/bin/bash

# check ptrace_scope for PIN
if ! grep -qF "0" /proc/sys/kernel/yama/ptrace_scope; then
  echo "Please run 'echo 0|sudo tee /proc/sys/kernel/yama/ptrace_scope'"
  exit -1
fi

git submodule init
git submodule update

# install system deps
sudo apt-get update
sudo apt-get install -y libc6 libstdc++6 linux-libc-dev gcc-4.8-multilib \
  llvm-4.0-dev g++-4.8 g++-4.8-multilib python python-pip \
  lsb-release

# install z3
pushd third_party/z3
rm -rf build
CC=gcc-4.8 CXX=g++-4.8 ./configure --prefix=/usr/local/qsym
pushd build
make -j$(nproc)
sudo make install
popd

# build test directories
pushd tests
python build.py
popd

cat <<EOM
Please install qsym by using (or check README.md):

  $ virtualenv venv
  $ source venv/bin/activate
  $ pip install .
EOM
