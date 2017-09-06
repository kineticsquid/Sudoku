#!/bin/bash
echo "hello, $USER. testing now..."

bx wsk action invoke return_environment --blocking --result --param name Fred
echo ""

bx wsk action invoke return_environment --blocking --result
echo ""





