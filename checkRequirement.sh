#!/bin/bash

if [ ${#@} -ne 0 ] && [ "${@#"--help"}" = "" ]
then
    echo '...help...'
    echo '檢查 & 確認模組皆已安裝正確版本'
    exit 0
fi

cd `dirname $0`

echo -e "\033[30m\e[1;43mInstall Python3 Module......\e[0m"
/usr/bin/python3 -m pip install -r requirements.txt

echo "Check mtcnn version......"
mtcnn_version=$(/usr/bin/python3 -m pip show mtcnn | awk '/^Version: / {sub("^Version: ", ""); print}')
echo $mtcnn_version
echo "**********************************************************"
echo "$(tput setaf 0)$(tput setab 2) 已全部安裝完成 $(tput sgr 0)"
exit 0