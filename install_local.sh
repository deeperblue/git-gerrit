#!/bin/bash

cd "$(dirname $0)"

src_bin=bin
#src_completion=completion


#dst_completion=/etc/bash_completion.d/

#check env
if [[ "x$(uname -a | grep MINGW)" != "x" ]];then
	IS_MINGW="true"
	SUDO_CMD=
	dst_bin=${HOME}/bin/
else
	IS_MINGW="false"
	SUDO_CMD=sudo
	dst_bin=/usr/local/bin/
fi

# common functions.
die() {
    echo "${@}"
    exit 1
}

#Let mac user use homebrew to install.
#name=$(uname)
#if [ "Darwin" = "$name" ] ; then
#    dst_completion=/usr/local/etc/bash_completion.d/
#fi

# copy bin.
echo "installing git-gerrit to /usr/local/bin..."
if [ ! -d "$dst_bin" ];then
    mkdir "$dst_bin"
fi

if [ -w "$dst_bin" ]; then
    cp $src_bin/* "$dst_bin" -r
else
    echo "request sudo authorization to install git-gerrit to $dst_bin"
    ${SUDO_CMD} cp $src_bin/* "$dst_bin"
fi

${SUDO_CMD} chmod 775 "$dst_bin"
#if [ ! -d "$dst_completion" ] ; then
#    mkdir -p "$dst_completion"
#fi

# copy bash-completion.
#if [ -w "$dst_completion" ]; then
#    cp $src_completion/* "$dst_completion"
#else
#    echo "request sudo authorization to install git-gerrit to /usr/local/bin:"
#    sudo cp $src_completion/* "$dst_completion"
#fi

echo "git-gerrit install success."
