# A email client in termail

## Introduction

emcli is inspired by mutt, enable you send email in terminal handy.

## Installation

To install emcli, simply:

    pip install emcli

Or install emcli from source code:

    git clone https://github.com/lalor/emcli
    cd emcli
    sudo python setup.py install

## Usage

save emcli settings in `~/.emcli.cnf`:

    $ cat ~/.emcli.cnf
    [DEFAULT]
    smtp_server = smtp.qq.com
    smtp_port = 25
    username = 403720692@qq.com
    password = abc123

send email to multiple recipents:

    echo "This email come from terminal" | emcli -s "This is subject" -r joy_lmx@163.com me@mingxinglai.com

send email with attaches:

    emcli -s "This is subject" -a *.py -r joy_lmx@163.com < /etc/passwd
