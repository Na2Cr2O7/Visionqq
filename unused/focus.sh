#!/bin/bash

# 仅将标题含 qq（不区分大小写）的窗口置于最前（激活）
wmctrl -l | grep -i 'qq' | while read -r line; do
    win_id=$(echo "$line" | awk '{print $1}')
    wmctrl -i -a "$win_id"
done