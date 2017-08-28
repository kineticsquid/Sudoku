#!/bin/bash
echo "hello, $USER. testing now..."

wsk action invoke return_environment --blocking --result --param name Fred
echo ""

wsk action invoke return_environment --blocking --result
echo ""





