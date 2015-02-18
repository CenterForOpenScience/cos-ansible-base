#!/bin/sh -e

### BEGIN INIT INFO
# Provides:          csf-started
# Required-Start:    $csf
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: send upstart signal after starting csf
# Description:       csf needs to run before some upstart services can run
### END INIT INFO

. /lib/lsb/init-functions

case "$1" in
    start)
        log_daemon_msg "Signaling csf started..." "csf-started"
        initctl emit csf-started --no-wait
    ;;

    *)
        log_action_msg "Usage: /etc/init.d/csf-started start"
        exit 1
    ;;
esac

exit 0
